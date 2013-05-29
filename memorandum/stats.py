"""
memorandum.stats
~~~~~~~~~~~~~~~~
"""
import numpy
from numpy.ma import masked, nomask

from memorandum.utils import filter_for_values


def find_highest_outliers(data, prob=[.9]):
    """
    Given a dict of data find the high outliers in this data
    """
    all_values = filter_for_values(data)
    quantile = mquantiles(sorted(all_values), prob=prob)[-1]
    return [
        (date, val) for date, val in data["daily_views"].iteritems() 
        if val > quantile
    ], quantile
    

def mquantiles(a, 
               prob=list([.25, .5, .75]), 
               alphap=.4, 
               betap=.4, 
               axis=None,
               limit=()):
    """
    Computes empirical quantiles for a data array. Taken from scipy so we dont
    have to depend on scipy
    """
    def _quantiles1D(data, m, p):
        x = numpy.sort(data.compressed())
        n = len(x)
        if n == 0:
            return numpy.ma.array(numpy.empty(len(p), dtype=float), mask=True)
        elif n == 1:
            return numpy.ma.array(numpy.resize(x, p.shape), mask=nomask)
        aleph = (n * p + m)
        k = numpy.floor(aleph.clip(1, n - 1)).astype(int)
        gamma = (aleph - k).clip(0, 1)
        return (1. - gamma) * x[(k - 1).tolist()] + gamma * x[k.tolist()]

    # Initialization & checks ---------
    data = numpy.ma.array(a, copy=False)
    if data.ndim > 2:
        raise TypeError("Array should be 2D at most !")
    #
    if limit:
        condition = (limit[0] < data) & (data < limit[1])
        data[~condition.filled(True)] = masked
    #
    p = numpy.array(prob, copy=False, ndmin=1)
    m = alphap + p * (1. - alphap - betap)
    # Computes quantiles along axis (or globally)
    if (axis is None):
        return _quantiles1D(data, m, p)
    return numpy.ma.apply_along_axis(_quantiles1D, axis, data, m, p)
