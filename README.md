# renren-blog-spider
A spider to get your renren blog articles down from its mobile site. 从人人网爬自己的日志内容

## Preparation

Please make sure that `Python 3` has been setup in your system. Then install the following modules:

```
pip install beautifulsoup4
pip install requests
```
PS: You may need use `pip3` instead of `pip` in some cases.

## Update Config

Clone this project to your local folder. `cd` to this folder for the `config.json`:

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

```
http://3g.renren.com/
```
After successful login, please navigate to your profile page (个人主页）。You would need paste the following information to the `config.json`:

- Paste the full URL for your profile page (个人主页） to `"profileLink"`;

- Paste renren's cookie information (including cookie keys) to the `"cookies"`. If your are on Chrome, your may right click at the web page, select Inspect (检查) , and at the Application tab, find "Cookies" from side menu under "Storage".

For other configurations, your may leave them as they are or edit at your discretion:

- `"startPage"`: Renren has pagination of 10 articles per page. You may start from any page. Note that this page number is in the human way, and the first page is `1`.

- `"endPage"`: If you leave it as `0`, it will proceed until the last page (your very first blog article). Otherwise, it would end at the page your specified here.

- `"outputFileName"`: The script would generate a `txt` file in the same folder of the script. This is to specify the filename. (If a file with the same filename already exists, it would not replace that file. Instead, it would append number behind the file name).

## Run the script

`cd` to the folder containing the script, then:

```
python ./spider.py
```

## Limitations

1. If any error occurs, e.g. a network error, this script would stop (you may find where it stops from the console output);

2. For the article contents, images would remain as the `img` tag. This script would NOT download the images.
