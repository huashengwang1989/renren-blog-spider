# renren-blog-spider

## UPDATE

This script seems just survived for a few days. Now Renren will redirect to http://dnactivity.renren.com/, and the 3g.renren.com used no longer works.

万年不变的人人网变了。现在 3g.renren.com 会自动跳转了。目前人人网日志处于看不到的状态（桌面版 404 中）。该脚本没活过一周。

-----------------------------------

A spider to get your renren blog articles down from its mobile site.

从人人网爬自己的日志内容

This is based on the current layout of 3g.renren.com. If Renren has any other subsequent update, this script may not work.

该脚本基于目前人人网移动站 3g.renren.com。如果人人网对此有任何更新，该脚本可能会无法工作。

## Preparation 准备

Please make sure that `Python 3` has been setup in your system. Then install the following modules:

请确保已安装 `Python 3`。然后安装如下模组：

```
pip install beautifulsoup4
pip install requests
```
PS: You may need use `pip3` instead of `pip` in some cases.

注：你可能需要将`pip`替换为`pip3`。

## Update Config 更改 Config 文件

Clone this project to your local folder. `cd` to this folder for the `config.json`:

将该项目克隆至你本地。`cd`去本地文件夹，然后更改`config.json`的信息：

```json
{
    "cookies": {
        "Hm_lvt_xxxxxxxx": "0123456789",
        "Hm_lpvt_xxxxxxxxxxxxxx": "0123456789",
        "alxn": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "mt": "xxxxxxxxxxxx"
    },
    "profileLink": "http://3g.renren.com/profile.do?id=1234567890&sid=_123abc123abc&123abc&htf=2",
    "startPage": 1,
    "endPage": 0,
    "outputFileName": "renren_articles"
}
```

You would need update with your information here. Please login your Renren page via your browser at its `3g.renren.com` mobile site. Do not use the desktop version.

更改前请先登录人人网。记得从它的移动站登录。

```
http://3g.renren.com/
```

After successful login, please navigate to your profile page (个人主页）。You would need paste the following information to the `config.json`:

- Paste the full URL for your profile page (个人主页） to `"profileLink"`;

- Paste renren's cookie information (including cookie keys) to the `"cookies"`. If your are on Chrome, your may right click at the web page, select Inspect (检查) , and at the Application tab, find "Cookies" from side menu under "Storage".

登录成功后前往个人主页。复制个人主页的网址，黏贴至`"profileLink"`。 然后找到人人网相关的 cookies，也黏贴过去。注意 Cookie 的键名也需要修改。

For other configurations, your may leave them as they are or edit at your discretion:

其他选项可按需修改。

- `"startPage"`: Renren has pagination of 10 articles per page. You may start from any page. Note that this page number is in the human way, and the first page is `1`.

人人网日志每 10 篇一页。你可以从任意页开始。注意这里的页码第一页为`1`。

- `"endPage"`: If you leave it as `0`, it will proceed until the last page (your very first blog article). Otherwise, it would end at the page your specified here.

如果为`0`，那将从开始页一直抓取到最末页。否则将抓取到你设的页数。

- `"outputFileName"`: The script would generate a `txt` file in the same folder of the script. This is to specify the filename. (If a file with the same filename already exists, it would not replace that file. Instead, it would append number behind the file name).

程序会自动在同一个文件夹生成该文件名的 txt 文件。（如果已存在相同文件不会被覆盖，新生成的文件会自动重命名。）

## Run the script 跑起来

`cd` to the folder containing the script, then:

```
python ./spider.py
```

## Limitations 限制

1. If any error occurs, e.g. a network error, this script would stop (you may find where it stops from the console output);

如果脚本跑的时候碰到任何错误，它会停止（你可以从终端的日志中知道它在什么时候停止了。）

2. For the article contents, images would remain as the `img` tag. This script would NOT download the images.

该脚本仅下载文章的文本内容。其不会下载文章中的图片。

## Questions 问题

### Why need I fill in cookies instead of the login credentials? 为何需要填写 Cookie 而非直接填写用户名和密码？

Login credentials would also work initially, but it would soon trigger Renren's robot detection and need fill in verification code. This is difficult to bypass.

用户名和密码一开始也可以工作，但不久就会触发人人网验证机制。这个很难绕过。
