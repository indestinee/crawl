class Config:
    default_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8', 
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Connection': 'keep-alive'
    }
    default_html_cache_path='html_cache'
    default_url_prefix='http://'
    default_html_replace_suffix = [
        '.html', '.htm', '.php', '.xml', '.jsp',
    ]
    default_downloads_path = 'downloads'
    default_ignores = '\n\t\r'

cfg = Config()
