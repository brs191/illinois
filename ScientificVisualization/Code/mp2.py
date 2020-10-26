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
dem

subset = dem.extract_subset((572, 828, 472, 728, 0, 0), (1,1,1))
subset

pv.plot_itk(subset)

terrain = subset.warp_by_scalar() #Warp into a 3D surface mesh (without volume)
print(terrain.dimensions)
print(terrain)

print(terrain.bounds)
xmin = terrain.bounds[0]
xmax = terrain.bounds[1]
ymin = terrain.bounds[2]
ymax = terrain.bounds[3]
zmin = terrain.bounds[4]
zmax = terrain.bounds[5]

print(xmin)
print(zmax)


terrain.slice()


#xnew = np.linspace(xmin, xmax, 126)
#ynew = np.linspace(ymin, ymax, 126)
#znew = np.linspace(zmin, zmax, 1)
#print(len(ynew))
#
#x,y,z = np.meshgrid(xnew, ynew, znew)
#
#print(y.shape)
coarse = pv.StructuredGrid()
coarse.x = terrain.x[0:256:2, 0:256:2, 0:256:2]
coarse.y = terrain.y[0:256:2, 0:256:2, 0:256:2]
coarse.z = terrain.z[0:256:2, 0:256:2, 0:256:2]

#print(coarse.dimensions)

#terrain.plot()

#print(terrain.y[0,:,0])
#print(terrain.x)
#print(terrain.y)

#print(terrain.z[:2,:2,:2])
#print(len(terrain.z[:2,:2,:2]))



#xrng = np.linspace(X_bounds_min, X_bounds_max, total points), 
#yrng = np.linspace(Y_bounds_min, Y_bounds_max, total points)