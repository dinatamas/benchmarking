timeit doesn't return the return value of the function.
However, this benchmarking tool is capable of doing that.
timeit is implemented in Python, so there's nothing stopping
us from reimplementing it (and simplifying a bit):
https://github.com/python/cpython/blob/master/Lib/timeit.py

timeit.repeat => Benchmarker.timeit
timeit.timeit => Benchmarker.timeit.wrapper
timeit.inner  => Benchmarker._timeit

The benchmarking system should really resemble the logging module's
functionality. In logging, you import the module, call basicConfig()
once, and then call logging.info, etc. This requires a RootLogger.