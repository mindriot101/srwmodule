import time
import matplotlib.pyplot as plt
import logging
from contextlib import contextmanager
logging.basicConfig(level=logging.DEBUG)

class Plotter(object):
    def __init__(self, ax, autoscale=True):
        self.ax = ax
        self.line = None
        self.autoscale = autoscale

    def update(self, x, y, *args, **kwargs):
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
                self.logger.debug("Sleeping for {} seconds".format(self.sleep_time))
                time.sleep(self.sleep_time)
        else:
            self.logger.debug("Not repeating")
            fn(*args, **kwargs)
            plt.show()

@contextmanager
def auto_updater(*args, **kwargs):
    au = AutoUpdater(*args, **kwargs)
    yield au
