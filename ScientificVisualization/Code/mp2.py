#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 18:58:38 2020

@author: bollam
"""

#%matplotlib inline
from pyvista import set_plot_theme
set_plot_theme('document')

import pyvista as pv
import math
import numpy as np
#import pylab as plt
from pyvista import examples

dem = examples.download_crater_topo()
subset = dem.extract_subset((572, 828, 472, 728, 0, 0), (1,1,1))
pv.plot_itk(subset)
terrain = subset.warp_by_scalar() #Warp into a 3D surface mesh (without volume)
#terrain.plot()


xnew = terrain.x[::2, ::2, ::2]
ynew = terrain.y[::2, ::2, ::2]
znew = terrain.z[::2, ::2, ::2]
coarse = pv.StructuredGrid(xnew, ynew, znew)
#coarse.plot()

#NOTE: You do not need to round any values within your results.
def bilin(x, y, points):
    x1, y1, v1 = points[0]
    x2, y2, v2 = points[1]
    x3, y3, v3 = points[3]
    x4, y4, v4 = points[2]
    
    tx = (x-x1)/(x2-x1)
    print(tx)
    vx = (1-tx)*v1 + tx*v2
    print(vx)
    
    vy = (1-tx)*v4 + tx*v3
    print(vy)
    
    y5 = y1
    y6 = y4
    t = (y-y5)/(y6-y5)
    print(t)
    v = (1-t)*vx + t*vy
    print(v)
    return v


errz   = []                    #Create a new empty list for holding absolute error values
intz   = np.zeros_like(terrain.z) #Create a new array for holding bilinearly interpolated values from coarse mesh

xlen   = coarse.z.shape[0]-1   #Number of cells (points-1) on the x-axis of the coarse mesh
ylen   = coarse.z.shape[1]-1   #Number of cells (points-1) on the y-axis of the coarse mesh
print((xlen)*2)
print(len(terrain.z))
scale = (terrain.z.shape[0]-1)/(coarse.z.shape[0]-1) #Reduction factor between original and coarse; should equal 2

# YOUR CODE HERE
#intmesh = coarse
#print(coarse.z[1,1,0])\
print(xnew)
#for x in range(xlen):
#    for y in range(ylen):
#        intz[x][y][0] = bilin(x, y)