
import requests
from bs4 import BeautifulSoup
from bs4 import Tag
import json
import re
import os

# default headers

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
}

# get configs from config.json

with open('config.json') as json_config:
    configs = json.load(json_config)
cookies = configs['cookies']
profileLink = configs["profileLink"]
startPage = configs['startPage'] if configs['startPage'] else 1
endPage = configs['endPage'] if configs['endPage'] else 0
outputFilename = configs['outputFileName'] if configs['outputFileName'] else 'renren_articles'

# init and open output file

originalOutputFilename = outputFilename
fileNameCount = 0
while os.path.isfile(outputFilename + '.txt'):
    fileNameCount = fileNameCount + 1
    outputFilename = originalOutputFilename + str(fileNameCount)
f = open(outputFilename + '.txt', 'w+')
print('\n输出文件为：' + '\x1b[7;37;44m'+ outputFilename + '.txt\x1b[0m')

# init session

session = requests.Session()

# Blog link

class LinkWithCount:
    'Contains a link, its name, as well as the count. This is currently for link to blogs.'
    def __init__(self, name, link, count, tag):
        self.name = name
        self.link = link
        self.count = count
        self.tag = tag

def getBlogPageLink(response):
    bsObj = BeautifulSoup(response.text, 'html.parser')
    aTags = bsObj.find_all('a')

    targetLink = None

    for aTag in aTags:
        aHref = aTag.get('href')
        aText = aTag.text
        if aText == '日志':
            countSibling = aTag.next_sibling
            while (countSibling and not isinstance(countSibling, Tag)):
                countSibling = countSibling.next_sibling
            blogCount = 0
            if isinstance(countSibling, Tag) and countSibling.text:
                countStr = re.sub(r'[^0-9]', '', countSibling.text)
                blogCount = int(countStr)
            targetLink = LinkWithCount(aText, aHref, blogCount, aTag)
    
    return targetLink

# GET your profile page first, and then get the link to the blogs, as well as total number of blogs.

print('获取主页中...')
responseProfile = session.get(profileLink, headers = headers, cookies = cookies)
print('获取主页成功。')

# Normalise link for blogs, by adding / modifying the curpage route query.

blogLinkInfo = getBlogPageLink(responseProfile)
blogLink = blogLinkInfo.link

if 'curpage=' in blogLink:
    blogLink = re.sub(r'curpage\=[0-9]+\&', 'curpage=' + str(startPage - 1) + '&', blogLink)
else:
    blogLink = re.sub(r'wmyblog\.do\?', 'wmyblog.do?curpage=' + str(startPage - 1) + '&', blogLink)

articleBackwardCountFrom = blogLinkInfo.count - (10 * (startPage - 1))

print('获取日志页中...\n共 ' + str(blogLinkInfo.count) + ' 篇。\n将从第 ' + str(startPage) + ' 页、第 ' + str(articleBackwardCountFrom) + ' 篇开始（最末页最早的日志为第一篇）。')

if endPage > 0:
    print('将至第 ' + str(endPage) + ' 页为止。')

# Get the first / start page of 10 articles.

responseBlog = session.get(blogLink, headers = headers, cookies = cookies)

print('获取日志页成功。')
print('获取日志链接中...')

class Article:
    'Contain article title, link and stringified date as well as content'
    def __init__(self, title, link, datetime):
        self.title = title
        self.link = link
        self.datetime = datetime
    
    def addContent(self, content):
        self.content = content

# Get the article full content and add to corresponding article instance.

def getAndAddArticleContent(article):
    aLink = article.link
    articlePageResponse = session.get(aLink, headers = headers, cookies = cookies)
    articleBsObj = BeautifulSoup(articlePageResponse.text, 'html.parser')
    articleContentDiv = articleBsObj.find('div', 'con')
    ATag = articleContentDiv.find('a')

    if ((not (ATag is None)) and (ATag.text.strip() == '阅读全文')):
        fullTextLink = ATag.get('href').strip()
        articlePageResponse = session.get(fullTextLink, headers = headers, cookies = cookies)
        articleBsObj = BeautifulSoup(articlePageResponse.text, 'html.parser')
        articleContentDiv = articleBsObj.find('div', 'con')
        article.link = fullTextLink
    print('articleContentDiv', articleContentDiv.name)
    articleContentDiv.name = 'article'
    del articleContentDiv['class']

    for br in articleContentDiv.find_all('br'):
            br.replace_with('\n')
        
    for x in articleContentDiv.find_all():
        if len(x.get_text(strip=True)) == 0:
            x.extract()

    article.addContent(articleContentDiv)
    return article

# main recursive function

def getBlogDetails(response, divClassName, backwardCountFrom, countPageFrom):
    count = backwardCountFrom
    currentPage = countPageFrom
    bsObj = BeautifulSoup(response.text, 'html.parser')
    listItemDivsWrapper = bsObj.find('div', divClassName)
    listItemDivs = listItemDivsWrapper.find_all('div', class_=False)
    
    resList = []

    for listItemDiv in listItemDivs:
        articleDatetimePTag = listItemDiv.find('p', 'time')
        articleTitleATag = listItemDiv.find('a')
        link = articleTitleATag.get('href').strip()
        title = articleTitleATag.text.strip()
        time = articleDatetimePTag.contents[0].strip()
        article = Article(title, link, time)
        article = getAndAddArticleContent(article)
        resList.append(article)
        
        print('\n' + '\x1b[6;30;42m' + '[' + str(count) + '] ' + title + '\x1b[0m')
        print('🔗 ' + '\33[34m' + article.link[:68] + '...' + '\x1b[0m')
        print('\33[92m' + time + '\x1b[0m' + '\n')
        
        stripedContent = article.content.text.strip()
        stripedContentSplits = stripedContent.splitlines()
        length = len(stripedContentSplits)
        if (length > 8):
            stripedContent = '\n'.join(stripedContentSplits[0:5]) + '\n... ...'
        print('\33[90m' + stripedContent + '\x1b[0m')
        print('\n-----------------------------\n')

        f.write('>>>> ARTICLE %s\n' % str(count))
        f.write('%s\n' % title)
        f.write('%s\n\n' % time)
        f.write('%s\n\n' % article.link)
        f.write('%s\n' % article.content)
        f.write('\n-----------------------------\n\n')
        
        count = count - 1

    lastDiv = listItemDivsWrapper.find('div', class_='l')
    nextPageATag = lastDiv.find('a', title='下一页')

    # When there is still next page link:

    if (not (nextPageATag is None) and (endPage == 0 or currentPage < endPage)):
        currentPage = currentPage + 1
        print('\n>> 转至下一页 (%s)\n' % str(currentPage))
        nextPageLink = nextPageATag.get('href')
        responseBlogNextPage = session.get(nextPageLink, headers = headers, cookies = cookies)
        nextPageList = getBlogDetails(responseBlogNextPage, 'list', count, currentPage)
        for nextPageListItem in nextPageList:
            resList.append(nextPageListItem)
    return resList

blogs = getBlogDetails(responseBlog, 'list', articleBackwardCountFrom, startPage)

f.close()

print('全部完成。' )