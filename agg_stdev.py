# stdev aggregator to 3 deviations
from visidata import *
import functools

__author__ = 'Geekscrapy'
__version__ = '1.0'

import statistics

def within_x_stdev(N, w):

  try:
    abs(N[0])# Values must be a number (int/float etc.
  except TypeError:     # Values must be a number (int/float etc.)
    return float('NAN')
  except IndexError:    # Value must have at least 1 entry
    return None

  if len(set(N)) == 1:  # All values are the same
    return None
  elif len(N) <= 2:     # Number of values are less than or equal to 2, so can't calc stdev
    return -1

  N_mean = statistics.mean(N)
  N_stdev = statistics.stdev(N)
  lower_bound = N_mean - ( N_stdev * w )
  upper_bound = N_mean + ( N_stdev * w )

  outliers = list(filter(lambda n: not(bool(lower_bound < n < upper_bound)), N))

  return outliers or None

@functools.lru_cache(100)
def _stdev(within, helpstr=''):
  return aggregators._defaggr(f'{within}_stdev', vlen, lambda col,rows,within=within: within_x_stdev(sorted(col.getValues(rows)), within), helpstr)

def stdev(stdd, helpstr):
  return [_stdev(within, helpstr) for within in range(1,stdd+1) ]

vd.aggregators['stdev_mine'] = stdev(3, '3 standard deviations')
