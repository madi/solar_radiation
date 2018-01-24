
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
LOC = "prova_gmted"
MAPSET = "PERMANENT"

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

def rastImport(IN_PATH, raster, grassname):
    rasterpath = os.path.join(IN_PATH, raster)
    grass.read_command('r.external', input = rasterpath, 
                       output = grassname,
                       overwrite = True)
    
#-----------------------------------------------------------------------

def rastExport(OUT_PATH, grassname, filename):
    rasterpath = os.path.join(OUT_PATH, filename + '.tif')
    grass.run_command('r.out.gdal', input = grassname,
                      output = rasterpath,
                      format = 'GTiff')

#-----------------------------------------------------------------------

def rastCleanup(pattern):
    patt = pattern + '*'
    grass.run_command('g.remove', type = 'raster',
                      pattern = patt, 
                      flags = 'f')

#-----------------------------------------------------------------------

def CalcSolarRad(IN_PATH, OUT_PATH, elevation):
    """
    Calculates daily sum of solar radiation for each month. Default value 
    is adopted for albedo.
    """
    # Import tile of elevation map
    r_elevation = elevation.split('.')[0]
    rastImport(IN_PATH, elevation, r_elevation)
    
    # Set computational region to fit to elevation map
    grass.read_command('g.region', flags = 'p', raster = r_elevation)
    
    # calculate horizon angles (to speed up the subsequent r.sun calculation)
    # step=30 produces 12 maps
    # in lat-lon coordinate system, bufferzone is expressed in degree unit
    r_horizon = r_elevation + '_horangle' 
    grass.run_command('r.horizon', elevation = r_elevation, 
                      step = 30, 
                      bufferzone = 1, 
                      output = r_horizon, 
                      maxdistance = 5000)

    # slope + aspect
    r_aspect = r_elevation + '_aspect'
    r_slope = r_elevation + '_slope'
    grass.run_command('r.slope.aspect', elevation = r_elevation,
                      aspect = r_aspect, 
                      slope = r_slope,
                      overwrite = True)
                      
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
    # result: output global (total) irradiance/irradiation [W.m-2] for 
    # given day/time
    
    for day in days:
        r_glob_rad = r_elevation + '_glob_rad_' + str(day)
        grass.run_command('r.sun', elevation = r_elevation, 
                          horizon_basename = r_horizon, 
                          horizon_step = 30, 
                          aspect = r_aspect, 
                          slope = r_slope, 
                          glob_rad = r_glob_rad, 
                          day = day, 
                          time = 14,
                          overwrite = True)
        # Export
        rastExport(OUT_PATH, r_glob_rad, r_glob_rad)
    
    # Cleanup
    rastCleanup(r_elevation)
    
#-----------------------------------------------------------------------
    
if __name__ == "__main__":
    pass



