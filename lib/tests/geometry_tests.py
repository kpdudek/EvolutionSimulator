#!/usr/bin/env python3

import os,sys, time
import numpy as np
from matplotlib import pyplot as plt

path = os.getcwd()
sys.path.insert(1,os.path.dirname(path))
import Geometry as geom

# Test map values
print(geom.map_val(5,0,10,10,0))
print(geom.map_val(5,0,10,-10,0))
print(geom.map_val(5,0,10,0,-10))
