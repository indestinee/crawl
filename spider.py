import re, requests, os
from config import cfg
from utils import Cache

def http(url):
    return 'http://' + url if url.find('://') == -1 else url

def is_prefix(name, prefix):
    return name[:len(prefix)] == prefix

def add_suffix(name, suffix):
    return (name + suffix) if name[-len(suffix):] != suffix else name

class Spider(object):
    # def __init__(self):{{{
    def __init__(self, *, timeout=None, encoding=None, cookies=None,\
            headers=cfg.default_headers, headers_path=None, keys=None,\
            cache_path=cfg.defaut_html_path, extra_header={},\
            from_cache=False, save_cache=False, path_recursive=False):
        ''' 
        Args:
            timeout: float. timeout of requests
                default: None, no timeout
            
            headers: dict. headers of requests
                default: config.py/cfg.default_headers
                * if headers_path != None this argument won't count.

            headers_path: str. file-path of the headers.
                default: None

            keys: list/set. select keys from headers
                default: None, means all keys

            cache_path: str. path to store html
                default: config.py/cfg.defaut_html_path

            extra_header: dict. extra_header need to be added
                default: None
                * usually to add cookies, so can share the same session with chrome

            from_cache: bool. whether get response from local cache
                default: False
                * saved in cache_path/

            save_cache: bool. whether save response to local cache
                default: False
                * saved in cache_path/

            path_recursive: bool. whether save response as the url path
                default: False
                * website.com/1/2/3/4.html -> website.com/1-_-||/2-_-||/3-_-||/4.html if False
                    else website.com/1/2/3/4.html

        Return:
            class of Spider
        '''

        self.sess = requests.Session()
        self.timeout=timeout
        self.headers = self.make_headers(headers_path, keys) \
            if isinstance(headers_path, str) else headers

        self.headers.update(extra_header)
        self.cache = Cache(cache_path)
        self.encoding = encoding
        self.request_from_cache, self.request_save_cache=\
                from_cache, save_cache
        self.request_path_recursive = path_recursive

        self._request_prefix = 'request_'
        self._request_list = [name for name in self.__dict__.keys()\
                if is_prefix(name, self._request_prefix)]
    # }}}
    def add_log(self, log):# {{{
        print(log)
    # }}}
    def make_headers(self, headers_path, keys):# {{{
        assert isinstance(keys, (list, set, None))
        headers = {}
        keys = set(keys) if keys else keys
        with open(headers_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                x = line.find(':')
                if x != -1 and (not keys or line[:x] in keys):
                    headers[line[:x]] = line[x+1:-1]
        return headers
    # }}}
    def get_final_target(self, url, *args, **kwargs):# {{{
        print('[ERR] not complete yet')
        return None
        while True:
            response = self.get(url)

        return response
    # }}}
    def get(self, url, *args, **kwargs):# {{{
        self.add_log('[LOG] request a get from {}'.format(url))
        if 'headers' not in kwargs:
            kwargs['headers'] = self.headers
        if 'timeout' not in kwargs and self.timeout:
            kwargs['timeout'] = self.timeout

        rkwargs = {key: value for key, value in kwargs.items()\
                if not is_prefix(key, self._request_prefix)}

        for key in self._request_list:
            if key not in kwargs:
                kwargs[key] = self.__dict__[key]
        
        path = self.url2path(url, kwargs['request_path_recursive'])
        if kwargs['request_from_cache']:
            response = self.cache.load(add_suffix(path, '.pkl'))
            if response:
                return response

        try:
            response = self.sess.get(http(url), *args, **rkwargs)
            self.add_log('[SUC] get response')
        except:
            self.add_log('[ERR] no response')
            return None

        if self.encoding:
            response.encoding = self.encoding
        if kwargs['request_save_cache']:
            self.cache.bin_save(response.content, path)
            self.cache.save(response, add_suffix(path, '.pkl'))
        return response
    # }}}
    def post(self, url, *args, **kwargs):# {{{
        self.add_log('[LOG] send a post to {}'.format(url))
        if 'headers' not in kwargs:
            kwargs['headers'] = self.headers
        if 'timeout' not in kwargs and self.timeout:
            kwargs['timeout'] = self.timeout

        rkwargs = {key: value for key, value in kwargs.items()\
                if not is_prefix(key, self._request_prefix)}

        for key in self._request_list:
            if key not in kwargs:
                kwargs[key] = self.__dict__[key]
        
        path = self.url2path(url, kwargs['request_path_recursive'])
        if kwargs['request_from_cache']:
            response = self.cache.load(add_suffix(path, '.pkl'))
            if response:
                return response

        try:
            response = self.sess.post(http(url), *args, **rkwargs)
            self.add_log('[SUC] get response')
        except:
            self.add_log('[ERR] no response')
            return None

        if self.encoding:
            response.encoding = self.encoding
        if kwargs['request_save_cache']:
            self.cache.bin_save(response.content, path)
            self.cache.save(response, add_suffix(path, '.pkl'))
        return response
    # }}}
    def bin_save(self, response, name):# {{{
        self.cache.bin_save(response.content, name)
    # }}}
    def download(self, name, *args, **kwargs):# {{{
        response = self.get(*args, **kwargs)
        if not response:
            return False
        self.bin_save(response, name)
        return True
    # }}}
    def split(self, url):# {{{
        url = url[8:] if url[:8] == 'https://' else (\
                url[7:] if url[:7] == 'http://' else url)
        
        x = url.find('/')
        if x == -1:
            url += '/index.html'
            x = url.find('/')
        if x == len(url) - 1:
            url += 'index.html'

        host = url[:x]
        path = url[x+1:]
        name = url.split('/')[-1]
        return host, path, name
    # }}}
    def host(self, url):# {{{
        return self.split(url)[0]
    # }}}
    def url2path(self, url, recursive=False):# {{{
        host, path, name = self.split(url)
        if not recursive:
            return os.path.join(host, path.replace('/', '-_-||'))
        else:
            return os.path.join(host, *(path.split('/')))
    # }}}
    def ignore(self, text, ss='\n\t\r'):# {{{
        for s in ss:
            text = text.replace(s, ' ')
        l = len(text)
        while True:
            text = text.replace('  ', ' ')
            r = len(text)
            if l == r:
                break
            l = r
        return text
    # }}}
    def divide(self, text, key='div', *, st=0):# {{{
        start = '<' + key
        end = '</' + key + '>'

        result = []
        titles = []
        depth = 0

        while True:
            x = text[st:].find(start) + st
            y = text[st:].find(end) + st

            if x >= st and (x < y or y < st):
                z, subresult, subtitles = \
                        self.divide(text, key=key, st=x+1)
                finish = z
                t = text[x:].find('>') + x
                result.append({'content': text[x:finish], 'sub': subresult,
                    'title': text[x: t+1]})
                titles.append({'titles': text[x: t+1], 'sub': subtitles})
                st = finish
                depth = 1
            elif y >= st and (y < x or x < st):
                return y + len(end), result, titles
            else:
                break
        return st, result, titles
    # }}}
