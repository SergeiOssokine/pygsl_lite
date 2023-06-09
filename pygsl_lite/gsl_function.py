#!/usr/bin/env python
# Author : Pierre Schnizer
"""
Collection of Callbacks systems for  pygsl_lite. They follow the GSL definitions as
close as possible. Instead os a struct python classes are used.

All solvers accept a C void pointer, which is passed to the callback. In Pygsl
this is an abitrary python object.  See the doc strings of the various classes
for further detail.

"""
from . import _callback


class _gsl_function:
    initfunc = None
    freefunc = None
    def __init__(self, func, args):
        """
        input : func, args
            func ... a callable Python object accepting a double
                     and args
            args ... additional arguments. Supply None if not needed.
        """
        self._ptr = None
        assert(self.initfunc != None)
        assert(self.freefunc != None)
        self._ptr = self.initfunc((func, args))

    def __del__(self,):
        if hasattr(self, '_ptr'):
            if self._ptr != None:
                self.freefunc(self._ptr)

    def get_ptr(self):
        return self._ptr

class _gsl_function_fdf(_gsl_function):
    def __init__(self, func, deriv, fdf, args):
        self._ptr = None
        assert(self.initfunc != None)
        assert(self.freefunc != None)
        self._ptr = self.initfunc((func, deriv, fdf, args))

class gsl_function(_gsl_function):
    """
    This class defines the callbacks known as gsl_function to
    gsl.

    e.g to supply the function f:

    def f(x, params):
        a = params[0]
        b = parmas[1]
        c = params[3]
        return a * x ** 2 + b * x + c

    to some solver, use

    function = gsl_function(f, params)
    """

    initfunc =  _callback.gsl_function_init
    freefunc =  _callback.gsl_function_free

class gsl_function_fdf(_gsl_function_fdf):
    """
    This class defines the callbacks known as gsl_function_fdf to
    gsl.

    e.g to supply the function f:

    def f(x, None):
        return exp(2 * x)

    def df(x, None):
        return 2 * exp(2 * x)

    def fdf(x, None):
        myf  =  f(x, None)
        mydf = df(x, None)
        return myf, mydf


    to some solver, accepting gsl_function_fdf, use

    function = gsl_function_fdf(f, df, fdf, params)
    """
    initfunc =  _callback.gsl_function_init_fdf
    freefunc =  _callback.gsl_function_free_fdf



class gsl_multiroot_function(_gsl_function):
    """
    This class defines the callbacks for gsl_multiroot_function.

    To supply the function rosenbrock define the function:

    def rosenbrock_f(x, params):
        a = params[0]
        b = params[1]
        y = copy.copy(x)
        y[0] = a * (1 - x[0])
        y[1] = b * (x[1] - x[0] * x[0])
        return y

    sys = multiroots.gsl_multiroot_function(rosenbrock_f, params, 2)
    """
    initfunc =  _callback.gsl_multiroot_function_init
    freefunc =  _callback.gsl_multiroot_function_free

    def __init__(self, func, args, size):
        self._ptr = None
        assert(self.initfunc != None)
        assert(self.freefunc != None)
        self._ptr = self.initfunc((func, args, size))



class gsl_multiroot_function_fdf(_gsl_function_fdf):
    """
    This class defines the callbacks for gsl_multiroot_function.

    To supply the function rosenbrock define the functions:

    def rosenbrock_f(x, params):
        a = params[0]
        b = params[1]
        y = copy.copy(x)
        y[0] = a * (1 - x[0])
        y[1] = b * (x[1] - x[0] * x[0])
        return y

    def rosenbrock_df(x, params):
        a = params[0]
        b = params[1]
        df = Numeric.zeros((x.shape[0], x.shape[0]), Numeric.Float)
        df[0,0] = -a
        df[0,1] = 0
        df[1,0] = -2 * b * x[0]
        df[1,1] = b
        return df

    def rosenbrock_fdf(x, params):
        f = rosenbrock_f(x, params)
        df = rosenbrock_df(x, params)
        return f, df

    # dimension of x
    size = 2
    sys = multiroots.gsl_multiroot_function(rosenbrock_f, rosenbrock_df,
                                            rosenbrock_fdf, params, size)
    """
    initfunc =  _callback.gsl_multiroot_function_init_fdf
    freefunc =  _callback.gsl_multiroot_function_free_fdf

    def __init__(self, f, df, fdf, args, size):
        self._ptr = None
        assert(self.initfunc != None)
        assert(self.freefunc != None)
        self._ptr = self.initfunc((f, df, fdf, args, size))
