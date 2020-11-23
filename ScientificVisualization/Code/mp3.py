#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 23:37:31 2020

@author: raja
"""

#%matplotlib inline
from pyvista import set_plot_theme
set_plot_theme('document')

import numpy as np
import pyvista as pv
from itkwidgets import view, compare, cm
import itkwidgets
from pyvista import examples

# Volume rendering is not supported with Panel yet
pv.rcParams["use_panel"] = False
#
#vol = examples.download_knee_full()
#vol
#
#cpos = [(-381.74, -46.02, 216.54), (74.8305, 89.2905, 100.0), (0.23, 0.072, 0.97)]
#
##viewer = view(vol, cmap=cm.bone, camera=cpos, shadow=False) # No shading
##viewer

vol_frog = examples.download_frog()

#print(vol_frog.x.shape)
#print(vol_frog.y.shape)
#print(vol_frog.z.shape)
print(vol_frog.dimensions)
print(len(vol_frog.x))
print(len(vol_frog.points))
#print("scalar is ", vol_frog.point_arrays["scalars"])
print(vol_frog.active_scalars[6])

#dims = (vol_frog.x.shape[0], vol_frog.y.shape[0], vol_frog.z.shape[0])
dims = (vol_frog.dimensions[0], vol_frog.dimensions[1], vol_frog.dimensions[2])
origin = vol_frog.origin #0,0,0
spacing = (1, 1, 3)
print(dims , spacing)

grid = pv.UniformGrid(dims, spacing)
grid.spacing = (1, 1, 3)

print(grid.dimensions)
