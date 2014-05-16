'''
Some utility functions, for use in my code
'''

try:
    import cPickle as pickle
except ImportError:
    import pickle

import os
import functools

def cache(stub, directory='.', verbose=False):
    '''Caches the output of a function.

    Output goes to the filename .`stub`.cpickle, stored
    as protocol "2" i.e. in binary form'''
    name = os.path.join(directory, '.{0}.cpickle'.format(stub))
    def decorator(fn):
        @functools.wraps(fn)
        def __inner(*args, **kwargs):
            if os.path.isfile(name):
                if verbose:
                    print "Extractng from cache"
                with open(name) as infile:
                    return pickle.load(infile)
            else:
                if verbose:
                    print "Building cache"
                results = fn(*args, **kwargs)
                with open(name, 'w') as outfile:
                    pickle.dump(results, outfile, protocol=2)
                return results
        return __inner
    return decorator
