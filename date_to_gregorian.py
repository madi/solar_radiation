# coding: utf-8

__author__ = "Margherita Di Leo"
__license__ = "GPL v.3"
__version__ = "0.1"
__email__ = "dileomargherita@gmail.com"

import os
import datetime



def date2greg(day, month, year):
    """
    Converts day of the year, given in dd, mm, yyyy into gregorian date.
    Month can be alternatively given as 'Jan', 'Feb', etc.
    """
    monthDict={'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, \
               'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
    if month in monthDict:
        m = monthDict[month]
    else:
        m = month
    dayofyear = str(day) + "." + str(m) + "." + str(year)
    dt = datetime.datetime.strptime(dayofyear,'%d.%m.%Y')
    tt = dt.timetuple()
    greg = tt.tm_yday
    return greg
    

