#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 09:29:36 2020

@author: bollam
"""

import numpy as np
import matplotlib.pyplot as plt
import numpy.linalg as la

import matplotlib.image as mpimg

mario = mpimg.imread("mario_big.png")

#plt.imshow(mario)
#print(mario.shape)
#        print(mario[i,j])
print(mario[5,100])
t = mario[5,100]
print(t[0])
print(t[1])
print(t[2])
print(t[3])
#if (t[0] == 1.0 and t[1] == 0.03529412 and t[2] == 0.039215688 and t[3] == 1.0):
#if (t[0] == 1.0):
#    print("red it is")      
#
#if (t[1] <= 0.04):
#    print("red it is")  
#    
#if (t[2] <= 0.04):
#    print("red it is")  
  
luigi = mario
for i in range(mario.shape[0]):
    for j in range(mario.shape[1]):
        t = mario[i,j]
        if (t[0] == 1. and t[1] <= 0.04 and t[2] <= 0.04):
            luigi[i,j] = [0, 1, 0, 1]
            
      
plt.imshow(mario)