'''
Helper classes for matplotlib animations
'''


import time
import matplotlib.pyplot as plt
import logging
from contextlib import contextmanager
logging.basicConfig(level=logging.DEBUG)

class Plotter(object):
    '''Handles auto updating a plot, currently with a single line on it.

    Example usage:

    >>> ax = fig.add_subplot(111)
    >>> pax = Plotter(ax)
    >>>
    >>> while True:
    >>>     pax.update(xdata, ydata, 'r.')
    >>>     time.sleep(10)
    '''
    def __init__(self, ax, autoscale=True):
        self.ax = ax
        self.line = None
        self.autoscale = autoscale

    def update(self, x, y, *args, **kwargs):
        ''' Update the data on the attached axis instance.

        If a line is not present, create one '''
        if self.line:
            self.update_line(x, y, *args, **kwargs)
        else:
            self.new_line(x, y, *args, **kwargs)

    def update_line(self, x, y, *args, **kwargs):
        self.line.set_xdata(x)
        self.line.set_ydata(y)

        if self.autoscale:
            self.ax.set_xlim(min(x), max(x))
            self.ax.set_ylim(min(y), max(y))

    def new_line(self, x, y, *args, **kwargs):
        self.line = self.ax.plot(x, y, *args, **kwargs)[0]

class AutoUpdater(object):
    '''
    Class to make a long running plot easier.

    Construct an object before making any matplotlib figures etc., then supply
    an update function to call on each tick. This function should perform any
    data analysis required to update the plot.

    Example usage:

    >>> au = AutoUpdater(sleep_time=10)
    >>> fig, ax = plt.subplots(1, 1)
    >>> pax = Plotter(ax)
    >>>
    >>> def update_plot(ax):
    >>>     pax.update(xdata, ydata)
    >>>
    >>> # Start the rendering loop
    >>> au.run(update_plot, pax)

    The class takes these parameters:

    * `sleep_time`: time to sleep before each tick. Inverse frame rate
    * `repeat`:     whether to repeat or not. Set to false to just plot once
                    and return to normal matplotlib behaviour
    '''
    def __init__(self, sleep_time, repeat=True):
        self.sleep_time = sleep_time
        self.repeat = repeat
        self.logger = logging.getLogger(self.__class__.__name__)

        if self.repeat:
            plt.ion()

    def run(self, fn, *args, **kwargs):
        if self.repeat:
            while True:
                self.logger.debug("Performing analysis")
                fn(*args, **kwargs)
                self.logger.debug("Drawing screen")
                plt.draw()
                self.logger.debug("Sleeping for {0} seconds".format(self.sleep_time))
                time.sleep(self.sleep_time)
        else:
            self.logger.debug("Not repeating")
            fn(*args, **kwargs)
            plt.show()

@contextmanager
def auto_updater(*args, **kwargs):
    ''' Create an AutoUpdater instance with a context '''
    au = AutoUpdater(*args, **kwargs)
    yield au
