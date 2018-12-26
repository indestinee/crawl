import re, requests, os
from .config import cfg
from .utils import *
from .html_lib import *

class Spider(requests.Session):
    def __init__(self,# {{{
            headers=None, headers_path=cfg.headers_path, extra_header={},\
            download_path=cfg.download_path, html_path=cfg.html_path,\
            from_cache=False, save_cache=False, path_replace=None,\
            fix_url=False, encoding=None, **kwargs):
        ''' 
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
        '''
        super().__init__()

        self.headers = headers if headers else make_headers(headers_path)
        self.headers.update(extra_header)

        self.download_cache = Cache(download_path)
        self.cache = Cache(html_path)
        self.from_cache, self.save_cache = from_cache, save_cache

        self.path_replace = path_replace
        self.fix_url = fix_url
        self.encoding = encoding
        self.default_params = kwargs
        self.default_params.setdefault('headers', self.headers)
    # }}}
    def get(self, url, *args, **kwargs):# {{{
        '''
        Same params to requests.get

        @extra params:
            from_cache (bool): wether to load cache
            save_cache (bool): wether to save cache
        '''
        cp.log(
            'request (#b)GET(#) from (#y){}(#)'.format(url)
        )
        return self._request('GET', url, *args, **kwargs)
    # }}}
    def post(self, url, *args, **kwargs):# {{{
        '''
        Same params to requests.post

        @extra params:
            from_cache (bool): wether to load cache
            save_cache (bool): wether to save cache
        '''
        cp.log(
            'send (#b)POST(#) to (#y){}(#)'.format(url)
        )
        return self._request('POST', url, *args, **kwargs)
    # }}}
    def _request(self, method, url, from_cache=None, save_cache=None,# {{{
            *args, **_kwargs):

        kwargs = self.default_params.copy()
        kwargs.update(_kwargs)
    
        protocol, host, path, params = split_url(url)
        if protocol == '':
            protocol = 'http'
            url = '{}://{}'.format(protocol, url)

        html_path = os.path.join(host, *fix_path(path, params).split('/'))
        pkl_path = touch_suffix(html_path, '.pkl')

        if from_cache is None:
            from_cache = self.from_cache
        
        if save_cache is None:
            save_cache = self.save_cache

        if from_cache:
            response = self.cache.load(pkl_path)
            if response:
                cp.suc(
                    'load response from (#y){}(#)'.format(os.path.join(self.cache.path, html_path))
                )
                return response

        # response = super().request(method, url, *args, **kwargs)
        try:
            response = super().request(method, url, *args, **kwargs)
            cp.suc(
                'get response'
            )
        except requests.exceptions.ConnectTimeout:
            cp.err(
                'no response: (#r){}(#)'.format(
                    'ConnectTimeout'
                )
            )
            return None
        except requests.exceptions.ConnectionError:
            cp.err(
                'no response: (#r){}(#)'.format(
                    'ConnectionError'
                )
            )
            return None
        except requests.exceptions.ReadTimeout:
            cp.err(
                'no response: (#r){}(#)'.format(
                    'ReadTimeout'
                )
            )
            return None
        except:
            cp.err(
                'no response: (#r){}(#)'.format(
                    'not sure'
                )
            )
            return None

        if self.encoding:
            response.encoding = self.encoding

        if save_cache:
            text = fix_url(response.text, protocol, host)
            self.cache.dump(response, pkl_path, force=True)
            self.cache.dump(text, html_path, file_type='str', force=True)
            cp.log(
                '(#b){}(##) saved in (#y){}(##)'.format(url, os.path.join(self.cache.path, html_path))
            )
        return response
    # }}}
    def download(self, url, name=None, **kwargs):# {{{
        if name is None: name = url.split('/')[-1].split('?')[0]
        if 'save_cache' not in kwargs:
            kwargs['save_cache'] = False
        response = self.get(url, **kwargs)
        if response is None:
            return False
        self.download_cache.dump(response.content, name, file_type='bin', force=True)
        cp.log(
            '(#b){}(##) saved in (#y){}(##)'.format(url, os.path.join(self.download_cache.path, name))
        )
        return True
    # }}}
