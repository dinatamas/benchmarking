"""Tool for measuring the execution time of functions and methods.

This module builds on many of the techniques seen in the Python standard
library module `timeit`. The performance and accuracy of `timeit` should be
comparable and close to this module's.

Usage
=====

Simply `import benchmarking` and use the `@benchmarking.timeit` decorator to
measure the execution time of any function or method.
The measurement results will be stored in the `timings` and `time` attributes
of the originally decorated function. The latter is the minimum value of the
former for convenient access.
Usually, when measuring performance, only the lowest time is of interest, as it
is very unlikely that Python's performance would show any variance, it's more
probable that the differences are caused by scheduling, and needn't be regarded.

The default benchmarker performs 1 measurement with 1 call for simplicity. To
overwrite these default values, use the `basic_config` function or modify the
class variables of `Benchmarker` (a.k.a. `root`).

For more advanced use, subclass `Benchmarker`. This way it's easier to handle
multiple benchmarking profiles (one for each subclass).

Classes
=======

Benchmarker

Functions
=========

basic_config : int?, int?, bool? -> None
enable       : _ -> None
disable      : _ -> None

"""


# TODO: Make this module thread safe!
# TODO: Support passing global scope vars to func.
# TODO: Support custom timers.


import functools
import gc
import itertools
import time


#####################
# BENCHMARKER CLASS #
#####################


class Benchmarker:
    """Benchmarking timer utility.
    
    Attributes
    ==========

    disabled : `bool`
        Whether or not timing measurements should be performed.
        If false, a lot of overhead can be avoided.
    num_timings : `int`
        How many timing measurements to perform.
    num_calls : `int`
        How many times to call the function in a timing measurement.
    disable_gc : `bool`
        Whether or not to disable the garbage collector for the duration of a
        timing measurement. Shows more accurately how much CPU time the
        function actually consumes, but in a realistic scenario the garbage
        collector would be running.
    
    Methods
    =======

    disable : _ -> None
    enable  : _ -> None
    timeit  : function -> function
    _timeit : itertools.repeat, function, *args, **kwargs -> int

    """

    disabled    = False
    num_timings = 1
    num_calls   = 1
    disable_gc  = False

    @classmethod
    def disable(cls):
        """Disables all benchmarking."""
        cls.disabled = True
    
    @classmethod
    def enable(cls):
        """Enables all benchmarking."""
        cls.disabled = False

    @staticmethod
    def _timeit(it, func, *args, **kwargs):
        """Performs one timing measurement.
        
        Arguments
        =========

        it : `itertools.repeat`
            Corresponds to the `num_calls` class variable.
        func : `function`
            The decorated function to benchmark.
        
        Returns
        =======

        `int` : The time it took to perform the calls.
        
        """
        t0 = time.perf_counter()
        for _ in it:
            func(*args, **kwargs)
        t1 = time.perf_counter()
        return t1-t0

    @classmethod
    def timeit(cls, func):
        """Decorator method for `wrapper`."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """Performs a set of timing measurements."""
            if cls.disabled:
                return func(*args, **kwargs)
            timings = []
            if cls.disable_gc:
                gcold = gc.isenabled()
                gc.disable()
            try:
                for _ in range(cls.num_timings):
                    it = itertools.repeat(None, cls.num_calls)
                    t = cls._timeit(it, func, *args, **kwargs)
                    timings.append(t)
            finally:
                if cls.disable_gc and gcold:
                    gc.enable()
            setattr(wrapper, 'timings', timings)
            setattr(wrapper, 'time', min(timings))
            return func(*args, **kwargs)
        return wrapper


#################################
# MODULE-LEVEL ROOT BENCHMARKER #
#################################


root = Benchmarker


########################
# SIMPLE CONFIGURATION #
########################


def basic_config(
        num_timings=root.num_timings,
        num_calls=root.num_calls,
        disable_gc=root.disable_gc
    ):
    """Configure the root benchmarker."""
    root.disabled    = False
    root.num_timings = num_timings
    root.num_calls   = num_calls
    root.disable_gc  = disable_gc


def disable():
    """Disable benchmarking on the root benchmarker."""
    root.disable()


def enable():
    """Enable benchmarking on the root benchmarker."""
    root.enable()


##########################
# MODULE-LEVEL DECORATOR #
##########################


timeit = root.timeit