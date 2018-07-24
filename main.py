from spider import Spider
from html_lib import *
from IPython import embed

tries = 5
class Url_list(list):
    def __init__(self):
        super().__init__()
        self.l, self.r = 0, 0
        self.vis = set()
    
    def front(self):
        return self[self.l] if self.l < self.r else None

    def move_front(self):
        if self.l < self.r:
            data = self[self.l]
            self.l += 1
            return data
        return None

    def append(self, x):
        if x in self.vis:
            return 0

        super().append(x)
        self.r += 1
        self.vis.add(x)
        return 1

target = 'https://www.qidian.com/'

proxies = {
  'http': 'http://172.18.101.221:3182',
  'https': 'http://172.18.101.221:1080',
}

host_list = set([
    'www.qidian.com',
    'read.qidian.com',
    'book.qidian.com',
    'qidian.com',
])

__url_re__ = re.compile('href *= *[\'|"](.*?)["|\']', re.S)

def bfs(target):
    url, [_protocol, _host, _] = url_analysis(target)
    spider = Spider(encoding='utf-8', path_replace=None,\
            save_cache=True, from_cache=True, fix_url=True)
    url_list = Url_list()
    url_list.append(target)
    while True:
        cur = url_list.move_front()
        if not cur:
            break
        
        for times in range(tries):
            response = spider.get(cur)
            if response:
                break

        urls = __url_re__.findall(response.text)
        cnt = 0
        for url in urls:
            if url[:4] == 'http':
                pass
            elif url[:1] == '#':
                continue
            elif has_prefix(url, 'javascript') or url == '':
                continue
            else:
                print(url)

            host = url_analysis(url)[1][1]
            if host in host_list:
                cnt += url_list.append(url)

        print('[LOG] #%d done: %s'%(url_list.l, cur))
        print('[LOG] +%d total=%d'%(cnt, url_list.r))
    
    return url_list

url_list = bfs(target)

