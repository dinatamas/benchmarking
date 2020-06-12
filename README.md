Benchmarking
============

A simple, one-file, decorator-based benchmarking utility.<br>
Offers the same accuracy and low overhead as `time.timeit`.

`time.timeit` doesn't return the return value of the function.<br>
However, this benchmarking tool is capable of doing that.<br>
`time.timeit` is implemented in Python, so there's nothing stopping
us from reimplementing it (and simplifying a bit):
https://github.com/python/cpython/blob/master/Lib/timeit.py

`timeit.repeat` => `Benchmarker.timeit`<br>
`timeit.timeit` => `Benchmarker.timeit.wrapper`<br>
`timeit.inner`  => `Benchmarker._timeit`

The configuration of this tools is similar to the conventions of the `logging` module.

Todos
-----

* Make this module thread safe!
* Support passing global scope vars to func.
* Support custom timers.