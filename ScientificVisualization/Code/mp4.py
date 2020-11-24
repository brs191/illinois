#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 12:55:21 2020

@author: raja
"""

import numpy as np
import pylab as plt

size = 300

vortex_spacing = 0.5
extra_factor = 2.

a = np.array([1,0])*vortex_spacing
b = np.array([np.cos(np.pi/3),np.sin(np.pi/3)])*vortex_spacing
rnv = int(2*extra_factor/vortex_spacing)
vortices = [n*a+m*b for n in range(-rnv,rnv) for m in range(-rnv,rnv)]
vortices = [(x,y) for (x,y) in vortices if -extra_factor<x<extra_factor and -extra_factor<y<extra_factor]


xs = np.linspace(-1,1,size).astype(np.float64)[None,:]
ys = np.linspace(-1,1,size).astype(np.float64)[:,None]

vx = np.zeros((size,size),dtype=np.float64)
vy = np.zeros((size,size),dtype=np.float64)
for (x,y) in vortices:
    rsq = (xs-x)**2+(ys-y)**2
    vx +=  (ys-y)/rsq
    vy += -(xs-x)/rsq
    
def advance(ux, uy, x, y, fx, fy, nx, ny):
    # YOUR CODE HERE
    for (x,y) in vortices:
        print(x, y)
        # for each x,y calculate tx and ty
    
    return (0,0,0,0)

x_1, y_1, fx_1, fy_1 = advance(-19.09, 14.25, 0, 0, 0.5, 0.5, 10, 10)

print(x_1, y_1, fx_1, fy_1)