#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 19:45:40 2020

@author: hanisha nunna, raja shekar bollam
"""

class Painter:
    def __init__(self):
        print("Initialize Painter class")
    
    def paint(self): #, srcImg, R):
        print("Implement Paint function")
#        function paint(sourceImage,R1 ... Rn) {
#            canvas := a new constant color image
#            
#            // paint the canvasfor each brush radius Ri, from largest to smallest 
#            do {
#               // apply Gaussian blur
#               referenceImage = sourceImage * G(fσRi)
#               // paint a layer
#               paintLayer(canvas, referenceImage, Ri)
#            }
#            return canvas
#        }
        
    def paintLayer(self): #, canvas, refImg, R)
        print("Implement paintLayer function")
#        procedure paintLayer(canvas,referenceImage, R)
#        {
#            S := a new set of strokes, initially empty
#            
#            // create a pointwise difference image
#            D := difference(canvas,referenceImage)
#            
#            grid := f g R
#            
#            for x=0 to imageWidth stepsize grid do
#                for y=0 to imageHeight stepsize grid do
#                {
#                    // sum the error near (x,y)
#                    M := the region (x-grid/2..x+grid/2, y-grid/2..y+grid/2)
#                    
#                    areaError := ∑ i , j ∈ M D i,j / grid 2
#                    
#                    if (areaError > T) then
#                    {
#                    // find the largest error point
#                        (x 1 ,y 1 ) := arg max i , j ∈ M D i,j
#                        s :=makeStroke(R,x 1 ,y 1 ,referenceImage)
#                        add s to S
#                    }
#                }
#            paint all strokes in S on the canvas, in random order
#        }        
        
    def makeSplineStroke(self): #, x0, y0, refImage):
        print("Implement makeSplineStroke function")
#        function makeSplineStroke(x 0 ,y 0 ,R,refImage)
#        {
#            strokeColor = refImage.color(x 0 ,y 0 )
#            K = a new stroke with radius R and color strokeColor
#            add point (x 0 ,y 0 ) to K
#            (x,y) := (x 0 ,y 0 )
#            (lastDx,lastDy) := (0,0)
#        
#            for i=1 to maxStrokeLength do
#            {
#                if (i > minStrokeLength and
#                    |refImage.color(x,y)-canvas.color(x,y)|<
#                    |refImage.color(x,y)-strokeColor|) then
#                    return K
#                
#                // detect vanishing gradient
#                if (refImage.gradientMag(x,y) == 0) then
#                    return K
#                
#                // get unit vector of gradient
#                (gx,gy) := refImage.gradientDirection(x,y)
#                // compute a normal direction
#                (dx,dy) := (-gy, gx)
#                
#                // if necessary, reverse direction
#                if (lastDx * dx + lastDy * dy < 0) then
#                    (dx,dy) := (-dx, -dy)
#                    
#                // filter the stroke direction
#                (dx,dy) :=f c *(dx,dy)+(1-f c )*(lastDx,lastDy)
#                (dx,dy) := (dx,dy)/(dx 2 + dy 2 ) 1/2
#                (x,y) := (x+R*dx, y+R*dy)
#                (lastDx,lastDy) := (dx,dy)
#                
#                add the point (x,y) to K
#            }
#            return K
#        }


def main():
    painter = Painter()
    painter.paint()
    painter.paintLayer()
    painter.makeSplineStroke()
    print("Program ended")
    
if __name__ == "__main__":
    main()
