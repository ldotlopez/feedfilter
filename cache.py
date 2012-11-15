import os

class Cache():
    def __init__(self, cache_dir = 'cache', debug = True):
        self._debug = debug
        self._cache_dir = cache_dir

    def debug(self, msg):
        if self._debug:
            print msg

    def _get_cachename(self, name):
        return os.path.join(self._cache_dir, digest.hashlib.md5(name).hexdigest())

    def fetch_url(self, url):
        fname = self._get_cachename(url)
        if os.path.exists(fname):
            self.debug("Found url in cache")
            return (''.join(open(fname).read()), True)
        else:
            self.debug("Cache fault")
            buff = ''.join(urllib.urlopen(url).read())
            fh = open(fname, 'w+')
            fh.write(buff)
            fh.close()
            return (buff, False)

    def delete(self, url):
        os.unlink(self._get_cachename(url))

