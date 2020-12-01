#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 12:55:21 2020

@author: raja
https://github.com/mpastell/SciPy-CookBook/blob/master/originals/LineIntegralConvolution_attachments/lic_internal.pyx
https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjctP7utZ3tAhUafd4KHek2B9oQFjAAegQIARAC&url=https%3A%2F%2Fscipy-cookbook.readthedocs.io%2F_downloads%2Fb323b5a79a98fecba57e28185e383c64%2Flic_demo.py&usg=AOvVaw355H3vrH-ib7aFx9ldgWTH
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
    


#    - x and y indicate the coordinates of the pixel we're currently on.
#    - ux and uy indicate the x and y components of the vector at the current pixel
#    -  dicate the current subpixel position (treating the current pixel
#      as a unit square where (0,0) represents the top-left of the pixel, while (1,1) 
#      represents the bottom-right of the pixel).
#    - nx and ny indicate the total number of pixels along the x and y axes 
#      within the domain of the entire vector field.
def advance(ux, uy, x, y, fx, fy, nx, ny):

    if (ux < 0):
        tx = -fx/ux
    else:
        tx = (1-fx)/ux
        
    if (uy < 0):
        ty = -fy/uy
    else:
        ty = (1-fy)/uy
            
    if tx < ty:
        if ux >= 0:
            x += 1
            fx = 0
        else:
            x -= 1
            fx = 1
        fy += tx*uy
    else:
        if uy >= 0:
            y += 1
            fy = 0
        else:
            y -= 1
            fy = 1
        fx += ty*ux
        
# Boundaries round-off
    if x < 0:
        x = 0
    if y < 0:
        y = 0
        
    if x >= nx:
        x = nx-1
    if y >= ny:
        y = ny-1
        
#    print(x,y,fx,fy)
    
    return (x,y,fx,fy)

x_1, y_1, fx_1, fy_1 = advance(-19.09, 14.25, 0, 0, 0.5, 0.5, 10, 10)

#np.testing.assert_allclose(x_1, 0, atol=0.01,rtol=0)

print(x_1, y_1, fx_1, fy_1)

### Please DO NOT hard-code the answers as we will also be using hidden test cases when grading your submission.
size_test = 100

# Generate 100x100 random noise texture
np.random.seed(123)
texture = np.random.rand(size_test, size_test).astype(np.float64)

# Regenerate vector field with new dimensions
xs = np.linspace(-1,1,size_test).astype(np.float64)[None,:]
ys = np.linspace(-1,1,size_test).astype(np.float64)[:,None]

vx = np.zeros((size_test,size_test),dtype=np.float64)
vy = np.zeros((size_test,size_test),dtype=np.float64)
for (x,y) in vortices:
    rsq = (xs-x)**2+(ys-y)**2
    vx +=  (ys-y)/rsq
    vy += -(xs-x)/rsq
    
# Generate sinusoidal kernel function
L = 5 #Radius of the kernel
kernel = np.sin(np.arange(2*L+1)*np.pi/(2*L+1)).astype(np.float64)

# vx, vy, texture = (100, 100)
def compute_streamline(vx, vy, texture, px, py, kernel):
    # YOUR CODE HERE
    h = vx.shape[0]
    w = vx.shape[1]
    
    klen = kernel.shape[0]
    res = np.zeros((h,w))    
   
    for i in range(h):
        for j in range(w):
            x = j;
            y = i;
            # step 1
            fx = 0.5
            fy = 0.5
            
            k = klen//2
            res[i,j] += kernel[k]*texture[x,y]
            while k < klen-1: #forward direction
                (x, y, fx, fy) = advance(vx[i,j], vy[i,j], x, y, fx, fy, w, h)
                k += 1
                res[i,j] += kernel[k]*texture[x,y]
#                print("+ ", k, " res ", res[i,j])
                
#            k = klen//2
            x = j;
            y = i;
            fx = 0.5
            fy = 0.5
            while k > 0: #backward direction
                (x, y, fx, fy) = advance(-vx[i,j], -vy[i,j], x, y, fx, fy, w, h)
#                print("-", k)
                k -= 1
                res[i,j] += kernel[k]*texture[x,y]
                
               
#    k = klen//2
#    res = kernel[k]*texture[px, py] #kw*dw
#    while k>0:
#        (x[k], y[k], fx[k], fy[k]) = advance(0,0,0,0,0,0,0,0)
#        k-=1
#        print("k is ", k)
#        
#    k = klen//2
#    while k<klen-1:
#        (x, y, fx, fy) = advance(0,0,0,0,0,0,0,0)
#        k+=1

    print(res)
    return res
    
#compute_streamline(vx, vy, texture, 9, 9, kernel)
#np.testing.assert_allclose(compute_streamline(vx, vy, texture, 9, 9, kernel), 3.622, atol=0.01,rtol=0)
#np.testing.assert_allclose(compute_streamline(vx, vy, texture, 30, 82, kernel), 5.417, atol=0.01,rtol=0)
#np.testing.assert_allclose(compute_streamline(vx, vy, texture, 99, 99, kernel), 4.573, atol=0.01,rtol=0)


def lic(vx, vy, texture, kernel):
    # YOUR CODE HERE
    h = vx.shape[0]
    w = vx.shape[1]
    
    res = np.zeros((h,w))
    
    for i in range(h):
        for j in range(w):
            px = j
            py = i;
            res = compute_streamline(vx, vy, texture, px, py, kernel)
#            res[j,i] = res/sum(kernel)
    
    return res

    
### Please DO NOT hard-code the answers as we will also be using hidden test cases when grading your submission.
size_test = 100

# Generate 100x100 random noise texture
np.random.seed(123)
texture = np.random.rand(size_test, size_test).astype(np.float64)

# Regenerate vector field with new dimensions
xs = np.linspace(-1,1,size_test).astype(np.float64)[None,:]
ys = np.linspace(-1,1,size_test).astype(np.float64)[:,None]

vx = np.zeros((size_test,size_test),dtype=np.float64)
vy = np.zeros((size_test,size_test),dtype=np.float64)
for (x,y) in vortices:
    rsq = (xs-x)**2+(ys-y)**2
    vx +=  (ys-y)/rsq
    vy += -(xs-x)/rsq
    
# Generate sinusoidal kernel function
L = 5 #Radius of the kernel
kernel = np.sin(np.arange(2*L+1)*np.pi/(2*L+1)).astype(np.float64) 

result = lic(vx, vy, texture, kernel)

np.testing.assert_allclose(result[50][50], 0.566, atol=0.01,rtol=0)
np.testing.assert_allclose(result[99][99], 0.657, atol=0.01,rtol=0)
np.testing.assert_allclose(result[28][36], 0.405, atol=0.01,rtol=0)