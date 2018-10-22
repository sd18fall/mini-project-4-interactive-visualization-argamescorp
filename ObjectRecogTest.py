import cv2
cv2.__version__
import numpy as np
from time import sleep

# Defining a range of the color green
lowerBound=np.array([33,80,40])
upperBound=np.array([102,255,255])

# Make a VideoCapture object (camera)
cam= cv2.VideoCapture(0)

# Making kernel to delete noise (open = erosion followed by dilation, close is reversed)
# MORPH_OPEN deletes noise outside of the object, MORPH_CLOSE inside of the object)
kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))

# Main loop
running = True
while running:
    # Get the video data
    ret, orImg=cam.read()
    # Resize the frame, to have not too many pixels
    orImg=cv2.resize(orImg,(1280,720))
    img = cv2.flip(orImg, 1)
    # convert BGR to HSV
    imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    # create the Mask, look for the object in this color range
    mask=cv2.inRange(imgHSV,lowerBound,upperBound)
    # Delete all the noise in the image
    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

    maskFinal=maskClose # This is our final image with object in black-white (object is white)
    im2, conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    coords = []
    radius = []
    centerCoords = []
    #cv2.drawContours(img,conts,-1,(255,0,0),3)
    for i in range(len(conts)):
        #x,y,w,h=cv2.boundingRect(conts[i])
        #cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255), 2)
        (x,y),rad = cv2.minEnclosingCircle(conts[i])
        center = (int(x),int(y))
        coords.append(center)
        radius.append(int(rad))
        i = 0
    if len(radius) > 0:
        while i < 2:
            center = coords[radius.index(max(radius))]
            centerCoords.append(center)
            coords.remove(center)
            rad = max(radius)
            radius.remove(max(radius))
            cv2.circle(img,center,rad,(0,22,0),2)
            if i == len(radius):
                break
            i +=1
    print(centerCoords)


    cv2.imshow("cam",img)
    cv2.waitKey(10)
