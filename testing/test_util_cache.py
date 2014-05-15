import cPickle
from srw.util import cache
import os
import unittest

class TestCache(unittest.TestCase):

    cache_stub = 'cachestub'
    cache_name = '.{}.cpickle'.format(cache_stub)

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

        assert cPickle.load(open(self.cache_name)) == 10

