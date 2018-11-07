import re
# from config import *
from .utils import *
from lxml import etree
from urllib.parse import urljoin, quote, unquote
from urllib.request import Request
from html import unescape



def remove_3(url):# {{{
    '''
        remove # from url
    '''
    ph = url[::-1].find('/')
    if ph == -1:
        return url
    
    sharp = url[-ph:].find('#')
    if sharp == -1:
        return url

    url = url[:len(url) - ph + sharp]
    return url
# }}}
def make_headers(headers_path):# {{{
    '''
        @params:
            headers_path (str)
        
        @return:
            headers (dict)

    '''
    headers = {}
    with open(headers_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            x = line.find(':')
            if x != -1:
                headers[line[:x]] = line[x+2:-1]
    return headers
# }}}
_spliturl_re_ = re.compile('(.*?)://(.*?)/(.*)\?(.*)')
def split_url(url):# {{{
    '''
        (.*?)://(.*?)/(.*)\?(.*)'
        protocol, host, path, params
    '''
    url = remove_3(url)
    if url.find('://') == -1:
        url = '://' + url

    if url[url.find('://')+3:].find('/') == -1:
        url = url + '/'

    if url.find('?') == -1:
        url = url + '?'

    match = _spliturl_re_.match(url)
    if match:
        return match.groups()
    return '', '', '', ''
# }}}
def get_host(url):# {{{
    return split_url(url)[1]
# }}}
def fix_path(path, params=None, path_replace='/'):
    path = path.replace('/', path_replace)
    if path == '' or path[-1] == '/':
        path = path + 'index.html'
    if params:
        suffix = path.split('.')[-1]
        if suffix.find('/') != -1:
            path = path + '?' + params
        else:
            path = path + '?' + params + '.' + suffix
    return path

def remove_tag(html, tag):
    _tag_re_ = re.compile('<{}[^<>]*?>.*?</{}>'.format(tag, tag), re.S)
    return _tag_re_.sub('\n', html)


_tag_re_ = re.compile('<[^<>]*?>', re.S)
def remove_tags(html):
    '''
        return list
    '''
    for tag in ['script', 'style']:
        html = remove_tag(html, tag)
    res = []
    for each in _tag_re_.sub('\n', html).split('\n'):
        row = each.strip()
        if row == '':
            continue
        res.append(unescape(row))
    return res
    

def toxml(data):
    if not isinstance(data, str):
        data = data.text
    return etree.HTML(data)

def fix_url(text, protocol, host):
    text = text.replace('\/', '/')
    text = text.replace('\\"', '"')
    text = text.replace('\\\'', '\'')
    for quote in '\'\"':
        for t in ['src', 'href']:
            text = re.sub('{} *= *{}//'.format(t, quote),\
                    '{}={}{}://'.format(t, quote, protocol), text)
            text = re.sub('{} *= *{}/'.format(t, quote),\
                    '{}={}{}://{}/'.format(t, quote, protocol, host), text)
    return text

def add_prefix(text, url):
    for quote in '\'\"':
        for t in ['href']:
            text = re.sub('{} *= *{}http'.format(t, quote),\
                    '{}={}{}http'.format(t, quote, url), text)
    return text
