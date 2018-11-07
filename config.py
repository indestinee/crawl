class Config:
    headers_path='crawl/headers.txt'
    html_path='html_cache'
    download_path = 'downloads'

    default_url_protocol='http'
    default_html_replace_suffix = set([
        'html', 'htm', 'php', 'xml', 'jsp',
    ])
    default_ignores = '\n\t\r'

cfg = Config()
