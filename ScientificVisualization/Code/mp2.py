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
## Q11 = (x1, y1), Q12=(x1, y2), Q21 = (x2, y1) Q22 = (x2, y2)
def bilin(x, y, points):
    x1, y1, v1 = points[0]
    x2, y1, v2 = points[1]
    x1, y2, v3 = points[2]
    x2, y2, v4 = points[3]
    
    fxy1 = ((x2-x)/(x2-x1))*v1 + ((x-x1)/(x2-x1))*v2
    fxy2 = ((x2-x)/(x2-x1))*v3 + ((x-x1)/(x2-x1))*v4
   
    fxy = ((y2-y)/(y2-y1))*fxy1 + ((y-y1)/(y2-y1))*fxy2
    print(fxy)
    
    return fxy

#testing_points = [(1,1,3), (3,1,6), (1,3,7), (3,3,9)]
#result = bilin(2,2,testing_points)
#np.testing.assert_allclose(result,6.25, rtol=1e-2)
#result = bilin(2.5,2.5,testing_points)
#np.testing.assert_allclose(result,7.6875, rtol=1e-3)
#result = bilin(1.1,1.1,testing_points)
#np.testing.assert_allclose(result,3.3475, rtol=1e-3)

errz   = []                    #Create a new empty list for holding absolute error values
intz   = np.zeros_like(terrain.z) #Create a new array for holding bilinearly interpolated values from coarse mesh

xlen   = coarse.z.shape[0]-1   #Number of cells (points-1) on the x-axis of the coarse mesh 129
ylen   = coarse.z.shape[1]-1   #Number of cells (points-1) on the y-axis of the coarse mesh 129
print((xlen)*2)
print(len(terrain.z))
scale = (terrain.z.shape[0]-1)/(coarse.z.shape[0]-1) #Reduction factor between original and coarse; should equal 2

for i in range(xlen):
    for j in range(ylen):
        intz[i*2][j*2][0] = coarse.z[i,j,0]

zxlen = intz.shape[0] - 1
zylen = intz.shape[1] - 1

for i in range(zxlen):
    for j in range(zylen):
        if (i%2 == 1 and j%2 == 1): #both odd indices
            # Q11(x1,y1) Q21(x1,y2) Q12(x2,y1) Q22(x2,y2)
            points = [(i-1, j-1, intz[i-1, j-1, 0]), 
                     (i+1, j-1, intz[i+1, j-1, 0]), 
                     (i-1, j+1, intz[i-1, j+1, 0]), 
                     (i+1, j+1, intz[i+1, j+1, 0])]
            intz[i,j,0] = bilin(i, j, points)
        else:
            if (j%2 == 1): #col is odd
                intz[i,j,0] = (intz[i,j-1,0] + intz[i,j+1,0])/2
            if(i%2 == 1): #row is odd
                intz[i,j,0] = (intz[i-1,j,0] + intz[i+1,j,0])/2

errz = np.zeros(terrain.z.shape[0]*terrain.z.shape[1])
k = 0
for i in range(terrain.z.shape[0]):
    for j in range(terrain.z.shape[1]):
        if (k == 89):
            print("i, j is ", i, j)
            print("89 is ", terrain.z[i,j,0], intz[i,j,0])

        if (k == 66039):
            print("t3 i, j is ", i, j)
            print("-10 is ", terrain.z[i,j,0], intz[i,j,0])
        errz[k] = abs(terrain.z[i,j,0] - intz[i,j,0])
        k = k + 1
    
print("terrainz shape is ", terrain.z.shape)
print("intz size is ", intz.shape)        
print("intz ", intz[100,100,0])
print("terrain ", terrain.z[100,100,0])
print("coarse ", coarse.z[50,50,0])
print("test ", intz[130][130][0])
print("test2 ", intz[247][13][0])

print("errz t1 ", errz[89])
print("errz t2 ", errz[30678])
print("-10 is ", len(errz) - 10)
print("errz t3 ", errz[-10])
