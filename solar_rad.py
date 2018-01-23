
__author__ = "Margherita Di Leo"
__license__ = "GPL v.3"
__version__ = "0.1"
__email__ = "dileomargherita@gmail.com"

import os
import sys
from date_to_gregorian import *

# Setting up GRASS GIS env
GISBASE = "/usr/local/grass-7.5.svn"
GISDB = os.path.join(os.path.expanduser("~"), "grassdata")
LOC = "WGS84"
MAPSET = "tmp"

os.environ['GISDBASE'] = GISDB
os.environ['GISBASE'] = GISBASE
GPYDIR = os.path.join(GISBASE, "etc", "python")
sys.path.append(GPYDIR)
import grass.script as grass
import grass.script.setup as gsetup
gsetup.init(GISBASE, GISDB, LOC, MAPSET)


"""
From: https://grass.osgeo.org/grass75/manuals/r.sun.html
r.sun works in two modes: In the first mode it calculates for the set 
local time a solar incidence angle [degrees] and solar irradiance values 
[W.m-2]. In the second mode daily sums of solar radiation [Wh.m-2.day-1] 
are computed within a set day. 
"""

#-----------------------------------------------------------------------

def CalcSolarRad(IN_PATH, OUT_PATH, elevation):
    """
    Calculates daily sum of solar radiation for each month. Default value 
    is adopted for albedo.
    """
    
    # Set computational region to fit to elevation map
    grass.read_command('g.region', flags = 'p', raster = elevation)
    
    # calculate horizon angles (to speed up the subsequent r.sun calculation)
    # step=30 produces 12 maps
    grass.run_command('r.horizon', elevation = elevation, 
                      step = 30, 
                      bufferzone = 200, 
                      output = 'horangle', 
                      maxdistance = 5000)

    # slope + aspect
    grass.run_command('r.slope.aspect', elevation = elevation,
                      aspect = 'aspect.dem', 
                      slope = 'slope.dem')
                      
    # List of days for which we want to calculate global irradiation
    # The year is only indicated to tell whether it is a leap year,
    # which would change the gregorian date. However, for the sake
    # of this exercise, we assume the year is NOT a leap year                 
    days = [date2greg(15,'Jan',2017), date2greg(15,'Feb',2017), \
            date2greg(15,'Mar',2017), date2greg(15,'Apr',2017), \
            date2greg(15,'May',2017), date2greg(15,'Jun',2017), \
            date2greg(15,'Jul',2017), date2greg(15,'Aug',2017), \
            date2greg(15,'Sep',2017), date2greg(15,'Oct',2017), \
            date2greg(15,'Nov',2017), date2greg(15,'Dec',2017),]

    # calculate global radiation for 12 days within 12 months at 2p.m.
    # result: output global (total) irradiance/irradiation [W.m-2] for given day/time
    for day in days:
        grass.run_command('r.sun', elevation = elevation, 
                          horizon_basename = 'horangle', 
                          horizon_step = 12, 
                          aspect = 'aspect.dem', 
                          slope = 'slope.dem', 
                          glob_rad = 'global_rad', 
                          day = day, 
                          time = 14)
        
        
         
    #r.univar global_rad
    
    
    
#-----------------------------------------------------------------------
    
if __name__ == "__main__":
    pass



