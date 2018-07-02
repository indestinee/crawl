import re
from config import *
from utils import *
from lxml import etree

def toxml(data):
    if not isinstance(data, str):
        data = data.text
    return etree.HTML(data)

__url_re__ = re.compile('(.*?)://(.*?)/(.*)')
def url_analysis(url):
    '''
    @params:
        url (str): url
    
    @returns:
        url, [protocol, host, path]
    '''
    x = url.find('://')
    if x == -1:
        url = cfg.default_url_prefix + url
        x = url.find('://')

    if url[x+3:].find('/') == -1:
        url += '/'

    results = re.findall(__url_re__, url)
    return url, results[0]

def url_path(url, path_replace):
    '''
    @params:
        url (str): url
        path_replace (str): str to replace /

    @returns
        url, path
    '''
    url, [protocol, host, path] = url_analysis(url)
    if path.split('/')[-1].find('.') == -1:
        path += 'html' if path != '' else 'index.html'

    low_url = url.lower()
    for suffix in cfg.default_html_replace_suffix:
        if has_suffix(low_url, suffix):
            path = path[:-len(suffix)] + '.html'

    path = path.replace('/', path_replace)
    return url, host + '/' + path

def ignore(text, ignores=cfg.default_ignores):
    re_pattern = '(' +  '|'.join(ignores) + ')'
    text = re.sub(re_pattern, '', text)
    l = len(text)
    while True:
        text = text.replace('  ', ' ')
        r = len(text)
        if l == r:
            break
        l = r
    return text
