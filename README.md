# Crawl

## requirement
1. python3.x enviroment
2. python3.x packages:
```shell
pip3 install re lxml urllib html requests pickle json
```
    

## how to start a project
```bash
PROJECT_PATH='my_project'   # path of your own project
mkdir $PROJECT_PATH         # create the directory
cd $PROJECT_PATH            # change directory
git init                    # inititialize your git project
git submodule add 'https://github.com/indestinee/crawl' # add crawl as submodule
git submodule update --init --recursive # init all submodules
# remove line #4 in submodule: ./utils.__init__.py 'from .database import DataBase' if you don't need database
```

## example
```python
from crawl.spider import Spider
spider = Spider(headers_path='./crawl/headers.txt', from_cache=True, save_cache=True)
response = spider.get('https://baidu.com/')
response = spider.get('https://github.com/indestinee/crawl')
jpg = spider.download('http://tp.yiaedu.com/showimg.php?url=http://uploads.xuexila.com/allimg/1703/867-1F330164643.jpg')
```
<img src='https://raw.githubusercontent.com/indestinee/crawl/master/present/1.png'>

## components

### class Spider
```python3
@params:
    headers (dict): headers
        default: None
        priority: higher than headers_path

    headers_path (str): path of the headers (copy from browser)
        default: headers.txt

    extra_header (dict): extra_header need to be added
        default: None
        priority: higher than headers # replace keys existing

    downloads_path (str): path to save downloading files

    html_path (str): path to store html cache

    from_cache (bool): whether get response from html_path
        default: False

    save_cache (bool): whether save response to html_path
        default: False

    path_replace (str): string to replace '/'
        default: None

    encoding (str): default encoding of response
        default: None

    **kwargs (any): default params for requests

@returns:
    instance of class
```
### submodules
utils: <a href='https://github.com/indestinee/utils'>link</a>
