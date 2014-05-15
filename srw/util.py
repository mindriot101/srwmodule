import cPickle
import os
import functools

def cache(stub, verbose=False):
    '''
    Caches the output of a function
    '''
    name = '.{}.cpickle'.format(stub)
    def decorator(fn):
        @functools.wraps(fn)
        def __inner(*args, **kwargs):
            if os.path.isfile(name):
                if verbose:
                    print "Extractng from cache"
                with open(name) as infile:
                    return cPickle.load(infile)
            else:
                if verbose:
                    print "Building cache"
                results = fn(*args, **kwargs)
                with open(name, 'w') as outfile:
                    cPickle.dump(results, outfile, protocol=2)
                return results
        return __inner
    return decorator
