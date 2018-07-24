import re
from config import *
from utils import *
from lxml import etree

def make_headers(headers_path):
    headers = {}
    with open(headers_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            x = line.find(':')
            if x != -1:
                headers[line[:x]] = line[x+2:-1]
    return headers

def url_analysis(url):
    '''
    @params:
        url (str): url
    
    @returns:
        url, [protocol, host, path]
        protocol default: http
    '''
    x1 = url.find('://')
    if x1 == -1:
        url = '://'.join([cfg.default_url_protocol, url])
        x1 = url.find('://')
    
    x2 = url[x1+3:].find('/')
    if x2 == -1:
        url += '/'
        x2 += len(url)
    else:
        x2 += x1 + 3

    return url, [url[:x1], url[x1+3:x2], url[x2+1:]]

def fix_path(path, replace=None):
    '''
    @params:
        path (str)
        path_replace (str): str to replace /

    @returns
        path
    '''
    if path == '' or path[:-1] == '/':
        path += 'index__.html'
    
    filename = path.split('/')[-1]
    if filename.find('.') == -1:
        path += '__.html'
    
    suffix = path.split('.')[-1].lower()
    if suffix in cfg.default_html_replace_suffix:
        path = path[:-len(suffix)] + 'html'

    if replace:
        path = path.replace('/', replace)
    return path

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

def toxml(data):
    if not isinstance(data, str):
        data = data.text
    return etree.HTML(data)

def fix_url(text, protocol, host):
    for quote in '\'\"':
        for t in ['src', 'href']:
            text = re.sub('{} *= *{}//'.format(t, quote),\
                    '{}={}{}://'.format(t, quote, protocol), text)
            text = re.sub('{} *= *{}/'.format(t, quote),\
                    '{}={}{}://{}/'.format(t, quote, protocol, host), text)
    return text
