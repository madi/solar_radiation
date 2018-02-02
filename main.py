# coding: utf-8

__author__ = "Margherita Di Leo"
__license__ = "GPL v.3"
__version__ = "0.1"
__email__ = "dileomargherita@gmail.com"

import os
import argparse
from solar_rad import CalcSolarRad



parser = argparse.ArgumentParser(description = "Performs calculation of \
                                 solar radiation over tiles in a folder. ")
parser.add_argument("--inPath", dest = "inPath",
                                 help = "Path to tiles to be processed")
parser.add_argument("--outPath", dest = "outPath",
                                 help = "Path to output folder")                                 


args = parser.parse_args()

IN_PATH = args.inPath
OUT_PATH  = args.outPath

tileList = []

#-----------------------------------------------------------------------

def CreateTileList(IN_PATH):
    for tile in os.listdir(str(IN_PATH)):
        tileList.append(tile)
        tileList.sort()
    return tileList

#-----------------------------------------------------------------------

if __name__ == "__main__":
        
    tileList = CreateTileList(IN_PATH)
    
    for tile in tileList:
        CalcSolarRad(IN_PATH, OUT_PATH, tile)



