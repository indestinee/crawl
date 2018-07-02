import re, requests, os
from config import cfg
from utils import *
from html_lib import *

class Spider(object):
    def __init__(self, *, timeout=None, encoding=None,\
            headers=cfg.default_headers, headers_path=None,\
            extra_header={}, cookies=None, keys=None,\
            cache_path=cfg.default_html_cache_path,
            from_cache=False, save_cache=False, path_replace='|',\
            downloads_path=cfg.default_downloads_path):
        ''' 
        @params:
            timeout (float): timeout of requests
                default: None, no timeout

            encoding (str): default encoding of response
                default: None

            cookies (str): cookies for session (copy from browser)
            
            headers (dict): headers of requests
                default: config.py/cfg.default_headers
                *note: if headers_path != None, this param won't count

            headers_path (str): path of the headers (copy from browser)
                default: None
                instance:
                    DNT: 1
                    Host: github.com
                    Upgrade-Insecure-Requests: 1

            keys (list/set): select keys from headers
                default: None, means all keys

            cache_path (str): path to store html
                default: config.py/cfg.defaut_html_path

            extra_header (dict): extra_header need to be added
                default: None

            from_cache (bool): whether get response from local cache
                default: False

            save_cache (bool): whether save response to local cache
                default: False

            path_replace (str): what to replace '/'
                default: |

            downloads_path (str): path to save downloads

        @returns:
            instance of class
        '''

        self.sess = requests.Session()
        self.timeout=timeout
        self.encoding = encoding

        self.headers = self.make_headers(headers_path) \
            if isinstance(headers_path, str) else headers
        self.headers.update(extra_header)
        if cookies:
            self.headers['cookies'] = cookies

        if keys:
            tmp_keys = list(self.headers.keys())
            for key in tmp_keys:
                if key not in keys:
                    self.headers.pop(key)

        self.cache = Cache(cache_path)
        self.from_cache, self.save_cache=from_cache, save_cache

        self.path_replace = path_replace
        self.downloads = Cache(downloads_path)

        self.default_options_keys = [
            'headers', 'timeout',
        ]

    def add_log(self, log):
        print(log)

    def make_headers(self, headers_path):
        headers = {}
        with open(headers_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                x = line.find(':')
                if x != -1:
                    headers[line[:x]] = line[x+1:-1]
        return headers

    def get(self, url, *args, **kwargs):
        '''
        Same params to requests.get

        @extra params:
            from_cache (bool): wether to load cache
            to_cache (bool): wether to save cache
        '''
        self.add_log('[LOG] request GET from {}'.format(url))
        return self.request(self.sess.get, url, *args, **kwargs)

    def post(self, url, *args, **kwargs):
        '''
        Same params to requests.post

        @extra params:
            from_cache (bool): wether to load cache
            to_cache (bool): wether to save cache
        '''
        self.add_log('[LOG] send POST to {}'.format(url))
        return self.request(self.sess.post, url, *args, **kwargs)

    def request(self, method, url, from_cache=False, save_cache=False,\
            *args, **kwargs):
        for opt in self.default_options_keys:
            if opt not in kwargs:
                kwargs[opt] = self.__dict__[opt]

        url, html_path = url_path(url, self.path_replace)
        pkl_path = touch_suffix(html_path, '.pkl')

        if from_cache:
            response = self.cache.load(pkl_path)
            if response:
                return response

        try:
            response = method(url, *args, **kwargs)
            self.add_log('[SUC] get response')
        except:
            self.add_log('[ERR] no response')
            return None

        if self.encoding:
            response.encoding = self.encoding

        if save_cache:
            self.cache.dump(response, pkl_path)
            self.cache.dump(response.content, html_path, 'bin')
        return response
    
    def download(self, name, *args, **kwargs):
        response = self.get(*args, **kwargs)
        if not response:
            return False
        self.downloads.dump(response.content, name, 'bin')
        return True

