try:
    import cPickle as pickle
except ImportError:
    import pickle

from srw.util import cache
import os
import unittest

class TestCache(unittest.TestCase):

    cache_stub = 'cachestub'
    cache_name = '.{0}.cpickle'.format(cache_stub)

    def setUp(self):
        if os.path.isfile(self.cache_name):
            os.remove(self.cache_name)

    @classmethod
    def setUpClass(cls):
        @cache(cls.cache_stub)
        def cached_function(cls):
            return 10

        cls.cached_function = cached_function

    def test_that_a_value_without_a_cache_creates_one(self):
        self.cached_function()
        assert os.path.isfile(self.cache_name)

    def test_cache_contents(self):
        self.cached_function()
        self.cached_function()

        assert pickle.load(open(self.cache_name)) == 10

def test_custom_cache_directory():
    cache_stub = 'test'
    cache_path = '/tmp/.{0}.cpickle'.format(cache_stub)

    @cache(cache_stub, directory=os.path.dirname(cache_path))
    def do_test():
        return 5

    if os.path.isfile(cache_path):
        os.remove(cache_path)

    assert do_test() == 5

    assert os.path.isfile(cache_path)

