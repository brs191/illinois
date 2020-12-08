#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 15:35:19 2020

@author: bollam
https://gist.github.com/mmisono/8972731

"""

#%matplotlib inline
import networkx as nx
import matplotlib.pyplot as plt
import math
import numpy as np
from random import random
from numpy import arange

W = 1    # Width of the frame
L = 1    # Length of the frame
area = W*L

# Attractive force calculation
def f_a(d,k):
    # your code here
    return (d*d)/k

#np.testing.assert_allclose(f_a(4,3), 5.33, atol=0.01,rtol=0)
#np.testing.assert_allclose(f_a(3,3.4), 2.65, atol=0.01,rtol=0)
#np.testing.assert_allclose(f_a(4,3.4), 4.71, atol=0.01,rtol=0)
    
# Repulsive force calculation
def f_r(d,k):
    # your code here
    return (k*k)/d

### Please DO NOT hard-code the answers as we will also be using hidden test cases when grading your submission.

np.testing.assert_allclose(f_r(4,3), 2.25, atol=0.01,rtol=0)
np.testing.assert_allclose(f_r(3,3.4), 3.85, atol=0.01,rtol=0)
np.testing.assert_allclose(f_r(3,4), 5.33, atol=0.01,rtol=0)

# If you need to modify this function for debugging purposes, you can simply copy and paste this function into a new cell.
def fruchterman_reingold(G,iteration):
   
    area = W*L
    k = math.sqrt(area/nx.number_of_nodes(G))
    
    t = W/2
    dt = t/(iteration+1)

    for i in range(iteration):
        #print(i, " of ", iteration)
        
        # ALREADY COMPLETED. SEE CODE CELL BELOW.
        G = calculate_repulsive_forces(G, k)
       
        # COMPLETE THIS FUNCTION LATER
        G = calculate_attractive_forces(G, k)
        
        # Limit the maximum displacement to the temperature t
        # and then prevent from being displaced outside frame
        for v in G.nodes():
            dx = G.nodes[v]['dx']
            dy = G.nodes[v]['dy']
            disp = math.sqrt(dx*dx+dy*dy)
            if disp != 0:
                d = min(disp,t)/disp
                x = G.nodes[v]['x'] + dx*d
                y = G.nodes[v]['y'] + dy*d
                x =  min(W,max(0,x)) - W/2
                y =  min(L,max(0,y)) - L/2
                G.nodes[v]['x'] = min(math.sqrt(W*W/4-y*y),max(-math.sqrt(W*W/4-y*y),x)) + W/2
                G.nodes[v]['y'] = min(math.sqrt(L*L/4-x*x),max(-math.sqrt(L*L/4-x*x),y)) + L/2

        # Cooling
        t -= dt

    pos = {}
    for v in G.nodes():
        pos[v] = [G.nodes[v]['x'],G.nodes[v]['y']]
        
    plt.close()
    plt.ylim([-0.1,1.1])
    plt.xlim([-0.1,1.1])
    plt.axis('off')
        
    return pos

def calculate_repulsive_forces(G, k):       
    for v in G.nodes():
        G.nodes[v]['dx'] = 0
        G.nodes[v]['dy'] = 0
        for u in G.nodes():
            if v != u:
                dx = G.nodes[v]['x'] - G.nodes[u]['x']
                dy = G.nodes[v]['y'] - G.nodes[u]['y']
                delta = math.sqrt(dx*dx+dy*dy)
                if delta != 0:
                    d = f_r(delta,k)/delta
                    G.nodes[v]['dx'] += dx*d
                    G.nodes[v]['dy'] += dy*d
    return G

def calculate_attractive_forces(G, k):       
    # your code here
    for v,u in G.edges():
        dxx = G.nodes[v]['x'] - G.nodes[u]['x']
        dyy = G.nodes[v]['y'] - G.nodes[u]['y']
        delta = math.sqrt(dxx*dxx+dyy*dyy)
        if delta != 0:
            ddx = (dxx/delta)*f_a(delta,k)
            ddy = (dyy/delta)*f_a(delta,k)

            G.nodes[v]['dx'] -= ddx
            G.nodes[v]['dy'] -= ddy

            G.nodes[u]['dx'] += ddx
            G.nodes[u]['dy'] += ddy
    return G

### Please DO NOT hard-code the answers as we will also be using hidden test cases when grading your submission.
N = 5
G = nx.cycle_graph(N)

G.nodes[0]['x'] = 0.8168184889480099
G.nodes[0]['y'] = 0.5311428534216505
G.nodes[1]['x'] = 0.6654594641114429
G.nodes[1]['y'] = 0.7842081286602168
G.nodes[2]['x'] = 0.9229503471222402
G.nodes[2]['y'] = 0.21495774524514744
G.nodes[3]['x'] = 0.1353894225040374
G.nodes[3]['y'] = 0.9657448268419787
G.nodes[4]['x'] = 0.037138912320340944
G.nodes[4]['y'] = 0.578448424341083

for v in G.nodes():
    G.nodes[v]['dx'] = 0
    G.nodes[v]['dy'] = 0

k = math.sqrt(area/nx.number_of_nodes(G))

G_a = calculate_attractive_forces(G, k)

np.testing.assert_allclose(G_a.nodes[0]['dx'], -1.46, atol=0.01,rtol=0)
np.testing.assert_allclose(G_a.nodes[0]['dy'], 0.25, atol=0.01,rtol=0)
np.testing.assert_allclose(G_a.nodes[1]['dx'], 0.46, atol=0.01,rtol=0)
np.testing.assert_allclose(G_a.nodes[1]['dy'], -0.96, atol=0.01,rtol=0)
np.testing.assert_allclose(G_a.nodes[2]['dx'], -2.28, atol=0.01,rtol=0)
np.testing.assert_allclose(G_a.nodes[2]['dy'], 2.62, atol=0.01,rtol=0)