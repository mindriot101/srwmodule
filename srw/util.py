'''
Some utility functions, for use in my code
'''

try:
    import cPickle as pickle
except ImportError:
    import pickle

import os
import functools
import logging
logging.basicConfig(level=logging.INFO)

def cache(stub, directory='.', verbose=False):
    '''Caches the output of a function.

    Output goes to the filename .`stub`.cpickle, stored
    as protocol "2" i.e. in binary form'''
    name = os.path.join(directory, '.{0}.cpickle'.format(stub))

    logger = logging.getLogger(__name__)
    if verbose:
        logger.setLevel(logging.DEBUG)

    def decorator(fn):
        @functools.wraps(fn)
        def __inner(*args, **kwargs):
            if os.path.isfile(name):
                logger.debug("Extracting from cache")
                with open(name) as infile:
                    return pickle.load(infile)
            else:
                logger.debug("Building cache")
                results = fn(*args, **kwargs)
                with open(name, 'w') as outfile:
                    pickle.dump(results, outfile, protocol=2)
                return results
        return __inner
    return decorator
