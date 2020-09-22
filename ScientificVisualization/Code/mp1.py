#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

def getContourCase(top,left,thres,cells):
    row = len(cells)
    col = len(cells[0])
    if (top+1 >= col or left+1 >= row):
        return 0
    
    a = 0
    if (cells[left, top] > thres):
        a = 1
    
    if (cells[left, top+1] > thres):
        a = ((a << 1) | 1)
    else:
        a = (a << 1)
        
    if (cells[left+1, top+1] > thres):
        a = ((a << 1) | 1)
    else:
        a = (a << 1)

    if (cells[left+1, top] > thres):
        a = ((a << 1) | 1)
    else:
        a = (a << 1)
    
    return a 

def interpolate(v1,v2,t):
    return (t-v1)/(v2-v1)
    
def disambiguateSaddle(top,left,thres,cells):
    if ((cells[left, top] + cells[left+1, top+1] + cells[left, top+1] + cells[left+1, top])/4 >= thres):
        return True
    else:
        return False
    
def getCellSegments(top,left,thres,cells):
    key = getContourCase(top,left,thres,cells)
#    print("key is ", bin(key))
    
    lines=list([])

    if (key&8 == 8 and key&4 == 0): #10xx v1 == 1, v2 == 0
        v1 = cells[left, top]
        v0 = cells[left, top+1]
        t = interpolate(v0, v1, thres)
        lines.append((left, top+(1-t)))
    elif (key&8 == 0 and key&4 == 4): #01xx v1 == 1, v2 == 0 DONE
        v0 = cells[left, top]
        v1 = cells[left, top+1]
        t = interpolate(v0, v1, thres)
        lines.append((left, top+t))
        
    if (key&4 == 4 and key&2 == 0): #x10x v1 == 1, v2 == 0 DONE
        v1 = cells[left, top+1]
        v0 = cells[left+1, top+1]
        t = interpolate(v0, v1, thres)
        lines.append((left+(1-t), top+1))
    elif (key&4 == 0 and key&2 == 2): #x01x
        v0 = cells[left, top+1]
        v1 = cells[left+1, top+1]
        t = interpolate(v0, v1, thres)
        lines.append((left+t, top+1))
    
    if (key&2 == 2 and key&1 == 0): #xx10 v1 == 1, v2 == 0
        v1 = cells[left+1, top+1]
        v0 = cells[left+1, top]
        t = interpolate(v0, v1, thres)
        lines.append((left+1, top+t))
    elif (key&2 == 0 and key&1 == 1): #xx01 v1 == 1, v2 == 0 DONE
        v0 = cells[left+1, top+1]
        v1 = cells[left+1, top]
        t = interpolate(v0, v1, thres)
        lines.append((left+1, top+(1-t)))
            
    if (key&1 == 0 and key&8 == 8): #1xx0 v1 == 1, v2 == 0 
        v1 = cells[left, top]
        v0 = cells[left+1, top]
        t = interpolate(v0, v1, thres)
        lines.append((left+(1-t), top))
    elif (key&1 == 1 and key&8 == 0): #0xx1 v1 == 1, v2 == 0 DONE
        v0 = cells[left, top]
        v1 = cells[left+1, top]
        t = interpolate(v0, v1, thres)
        lines.append((left+t, top))

        
    if len(lines) == 0:
        return lines
    else:
        segments = list()
        segments.append(lines)
        return segments
            
def getContourSegments(thres,cells):
    row = len(cells)
    col = len(cells[0])
    contour = list()
    
    for left in range(row):
        for top in range(col):
            contour.extend(getCellSegments(left, top, thres, cells))
            
    return contour

#
#test_cases_1 = np.array([[0.5,0.6,0.6,0.5],[0.5,0.7,0.7,0.4],[0.5,0.7,0.7,0.4],[0.5,0.7,0.7,0.4]])
#assert getCellSegments(3,3,0.9,test_cases_1) == []
#
#test_cases_2 = np.array([[0.07339991, 0.38311005, 0.38311005, 0.07339991],[0.38311005, 0.99744795, 0.99744795, 0.38311005],[0.38311005, 0.99744795, 0.99744795, 0.38311005],[0.07339991, 0.38311005, 0.38311005, 0.07339991]])
#result = getCellSegments(0,0,0.2,test_cases_2)
#result[0].sort()
#assert result == [[(0, 0.40876959985875827), (0.40876959985875827, 0)]]
#
#test_cases_3 = np.array([[0.05,0.4,0.4,0.05],[0.4,0.9,0.9,0.4],[0.4,0.9,0.9,0.4],[0.05,0.4,0.4,0.05]])
#result = getCellSegments(2,2,0.2,test_cases_3)
#result[0].sort()
#assert result == [[(2.571428571428571, 3), (3, 2.571428571428571)]]

test_cases = np.array([[0.07339991, 0.38311005, 0.38311005, 0.07339991],[0.38311005, 0.99744795, 0.99744795, 0.38311005],[0.38311005, 0.99744795, 0.99744795, 0.38311005],[0.07339991, 0.38311005, 0.38311005, 0.07339991]])
result = getContourSegments(0.9,test_cases)
result.sort()
for item in result:
    item.sort()
    
print(result)
assert result == [[(0.8413772778791607, 1), (0.8413772778791607, 2)], [(0.8413772778791607, 1), (1, 0.8413772778791607)], [(0.8413772778791607, 2), (1, 2.1586227221208394)], [(1, 0.8413772778791607), (2, 0.8413772778791607)], [(1, 2.1586227221208394), (2, 2.1586227221208394)], [(2, 0.8413772778791607), (2.1586227221208394, 1)], [(2.1586227221208394, 1), (2.1586227221208394, 2)], [(2, 2.1586227221208394), (2.1586227221208394, 2)]]

