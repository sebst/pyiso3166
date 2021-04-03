import os 
DIR = os.path.dirname(os.path.abspath(__file__))
import json
import hashlib
from urllib.parse import urlparse
import urllib.request

__all__ = ['Iso3166Data']

class Iso3166Data():
    # SRC_URL = 'https://raw.githubusercontent.com/esosedi/3166/master/data/iso3166-2.json'
    SRC_URL = 'https://raw.githubusercontent.com/sebst/pyiso3166/master/data/iso3166-2.json'
    EXPECTED_HASH = "e56de6051b8e80f5aa1cd93a8d1ea3af142b34c5b54720405ce2c3a0e9816790"
    CACHE_FILE_NAME = "%s/iso3166-2.json"%(DIR)

    _data = {}
    _keys = []
    _pos = 0
    _len = 0

    def __init__(self,
                 use_cache_file=True):
        self.use_cache_file = use_cache_file
        content = self._load()
        retrieved_hash = hashlib.sha256(content).hexdigest()
        assert retrieved_hash == self.EXPECTED_HASH
        self._data = json.loads(content)
        self._keys = sorted(self._data.keys())
        self._pos = 0
        self._len = len(self._keys)

    def _load(self):
        if self.use_cache_file:
            try:
                with open(self.CACHE_FILE_NAME, 'rb') as f:
                    return f.read()
            except FileNotFoundError:
                content = self._load_from_src()
                with open(self.CACHE_FILE_NAME, 'wb') as f:
                    f.write(content)
                return content
        else:
            return self._load_from_src()
    
    def _load_from_src(self):
        o = urlparse(self.SRC_URL)
        if o.scheme in ['http', 'https']:
            return self._load_from_src_web(self.SRC_URL)
        if o.scheme in ['file']:
            return self._load_from_src_file(self.SRC_URL)
        raise NotImplementedError("Scheme `%s` is not supported."%(o.scheme))
    
    def _load_from_src_web(self, url):
        with urllib.request.urlopen(url) as f:
            return f.read()
    
    def _load_from_src_file(self, loc):
        raise NotImplementedError("Loading from files is currently not supported.")
    
    def remove_cache_file(self):
        if os.path.exists(self.CACHE_FILE_NAME):
            os.remove(self.CACHE_FILE_NAME)
    
    def __iter__(self):
        self._pos = 0
        return self
    
    def __next__(self):
        if self._pos < self._len:
            key = self._keys[self._pos]
            value = self._data[key]
            self._pos += 1
            return key, value
        else:
            raise StopIteration
    
    def get(self, cc_code):
        return self._data[cc_code.upper()]


if __name__ == "__main__":
    from pprint import pprint
    iso = Iso3166Data()
    pprint(iso.get("us"))
    # for country_code, data in iso:
        # print(country_code, data)