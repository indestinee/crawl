import re, requests, os
from config import cfg
from utils import *
from html_lib import *

class Spider(requests.Session):
    def __init__(self,\
            headers, extra_header={}, cookies=None,\
            download_path=cfg.download_path, cache_path=cfg.html_path,\
            from_cache=False, save_cache=False, path_replace=None,\
            fix_url=False, encoding=None, **kwargs):
        ''' 
        @params:
            headers_path (str): path of the headers (copy from browser)
                default: headers.txt

            extra_header (dict): extra_header need to be added
                default: None

            cookies (str): cookies for session (copy from browser)

            downloads_path (str): path to save downloads

            cache_path (str): path to store html

            from_cache (bool): whether get response from local cache
                default: False

            save_cache (bool): whether save response to local cache
                default: False

            path_replace (str): what to replace '/'
                default: None

            encoding (str): default encoding of response
                default: None

        @returns:
            instance of class
        '''
        super().__init__()

        self.encoding = encoding

        self.headers = headers
        self.headers.update(extra_header)
        if cookies:
            self.headers.setdefault('cookies', cookies)


        self.download_path = Cache(download_path)
        self.cache = Cache(cache_path)
        self.from_cache, self.save_cache=from_cache, save_cache

        self.path_replace = path_replace
        self.fix_url = fix_url

        self.default_params = kwargs
        self.default_params.setdefault('headers', self.headers)

    def add_log(self, log):
        print(log)

    def get(self, url, *args, **kwargs):
        '''
        Same params to requests.get

        @extra params:
            from_cache (bool): wether to load cache
            save_cache (bool): wether to save cache
        '''
        self.add_log('[LOG] request GET from {}'.format(url))
        return self._request('GET', url, *args, **kwargs)

    def post(self, url, *args, **kwargs):
        '''
        Same params to requests.post

        @extra params:
            from_cache (bool): wether to load cache
            save_cache (bool): wether to save cache
        '''
        self.add_log('[LOG] send POST to {}'.format(url))
        return self._request('POST', url, *args, **kwargs)

    def _request(self, method, url, from_cache=None, save_cache=None,\
            *args, **_kwargs):

        kwargs = self.default_params.copy()
        kwargs.update(_kwargs)
    
        url, [protocol, host, path] = url_analysis(url)
        html_path = fix_path(path)
        pkl_path = touch_suffix(html_path, '.pkl')

        if not from_cache:
            from_cache = self.from_cache
        if not save_cache:
            save_cache = self.save_cache

        if from_cache:
            response = self.cache.load(pkl_path)
            if response:
                return response

        try:
            response = super().request(method, url, *args, **kwargs)
            self.add_log('[SUC] get response')
        except:
            self.add_log('[ERR] no response')
            return None

        if self.encoding:
            response.encoding = self.encoding

        if save_cache:
            self.cache.dump(response, pkl_path)
            text = fix_url(response.text, protocol, host)
            self.cache.dump(text, html_path, 'str')
        return response
    
    def download(self, name, *args, **kwargs):
        response = self.get(*args, **kwargs)
        if not response:
            return False
        self.downloads.dump(response.content, name, 'bin')
        return True

