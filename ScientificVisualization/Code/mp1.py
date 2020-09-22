#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 11:04:11 2020

@author: bollam
"""
import numpy as np

def getContourCase(top,left,thres,cells):
    row = len(cells)
    col = len(cells[0])

    a = 0
    if (cells[left, top] > thres): #msb
        a = 1 #msb
    
    if (top+1 < col and cells[left, top+1] > thres):
        a = (a << 1) ^ 1
    else:
        a = (a << 1) ^ 0

    if (top+1 < col and left+1 < row and cells[left+1, top+1] > thres):
        a = (a << 1) ^ 1
    else:
        a = (a << 1) ^ 0
        
    if (left+1 < col and cells[left+1, top] > thres): #lsb
        a = (a << 1) ^ 1
    else:
        a = (a << 1) ^ 0
     
    return a 

def interpolate(v1,v2,t):
    return abs((t-v1)/(v2-v1))

def getCellSegments(top,left,thres,cells):
    row = len(cells)
    col = len(cells[0])
    key = getContourCase(top,left,thres,cells)

    lines=list([])
    if (key&8 == 8 and key&4 == 4) == 0:
        if (top+1 < col):
            lines.append((left, top+interpolate(cells[left, top], cells[left, top+1], thres)))

    if (key&4 == 4 and key&2 == 2) == 0:
        if (top+1 < col and left+1 < row):
            lines.append((left+interpolate(cells[left, top+1], cells[left+1, top+1], thres),top+1))

    if (key&2 == 2 and key&1 == 1) == 0:
        if (top+1 < col and left+1 < row):
            lines.append((left+1, top+(1-interpolate(cells[left+1, top+1], cells[left+1, top], thres))))
        
    if (key&1 == 1 and key&8 == 8) == 0:
        if (left+1 < row):
            lines.append((left+(1-interpolate(cells[left+1, top], cells[left, top], thres)), top))
        
    if len(lines) == 0:
        return lines
    else:
        segments = list()
        segments.append(lines)
        print(segments)
        return segments

def getContourSegments(thres,cells):
    row = len(cells)
    col = len(cells[0])
    
    segments = list()
    
    for left in range(row):
        for top in range(col):
            segments.extend(getCellSegments(top, left, thres, cells))

    return segments
            
    
test_cases = np.array([[0.5,0.6,0.6,0.5],[0.5,0.7,0.7,0.4],[0.5,0.7,0.7,0.4],[0.5,0.7,0.7,0.4]])
print(getContourCase(0,2,0.4,test_cases))
print(getContourCase(3,3,0.4,test_cases))

test_cases_1 = np.array([[0.5,0.6,0.6,0.5],[0.5,0.7,0.7,0.4],[0.5,0.7,0.7,0.4],[0.5,0.7,0.7,0.4]])
assert getCellSegments(3,3,0.9,test_cases_1) == []
test_cases_2 = np.array([[0.07339991, 0.38311005, 0.38311005, 0.07339991],[0.38311005, 0.99744795, 0.99744795, 0.38311005],[0.38311005, 0.99744795, 0.99744795, 0.38311005],[0.07339991, 0.38311005, 0.38311005, 0.07339991]])
result = getCellSegments(0,0,0.2,test_cases_2)
result[0].sort()
assert result == [[(0, 0.40876959985875827), (0.40876959985875827, 0)]]
test_cases_3 = np.array([[0.05,0.4,0.4,0.05],[0.4,0.9,0.9,0.4],[0.4,0.9,0.9,0.4],[0.05,0.4,0.4,0.05]])
result = getCellSegments(2,2,0.2,test_cases_3)
result[0].sort()
assert result == [[(2.571428571428571, 3), (3, 2.571428571428571)]]

test_cases = np.array([[0.07339991, 0.38311005, 0.38311005, 0.07339991],[0.38311005, 0.99744795, 0.99744795, 0.38311005],[0.38311005, 0.99744795, 0.99744795, 0.38311005],[0.07339991, 0.38311005, 0.38311005, 0.07339991]])
result = getContourSegments(0.9,test_cases)
print(result)