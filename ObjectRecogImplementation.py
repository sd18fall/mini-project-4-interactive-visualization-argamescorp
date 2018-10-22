import cv2
cv2.__version__
import numpy as np

def setUp(resolution):
    # Defining a range of the color green
    global lowerBound
    lowerBound=np.array([33,80,40])
    global upperBound
    upperBound=np.array([102,255,255])

    # Defining screen resolution
    global horRes
    horRes = resolution[0]
    global vertRes
    vertRes = resolution[1]

def getCoords():
    # Make a VideoCapture object (camera)
    cam= cv2.VideoCapture(0)

    # Making kernel to delete noise (open = erosion followed by dilation, close is reversed)
    # MORPH_OPEN deletes noise outside of the object, MORPH_CLOSE inside of the object)
    kernelOpen=np.ones((5,5))
    kernelClose=np.ones((20,20))

    # Main loop

    # Get the video data
    ret, orImg=cam.read()

    # Resize the frame, to have not too many pixels and flip the image.
    orImg=cv2.resize(orImg,(horRes,vertRes))
    global img
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
    widthList = []
    centerCoords = [(-1,-1),(-1,-1)]
    #cv2.drawContours(img,conts,-1,(255,0,0),3)
    for i in range(len(conts)):
        x,y,w,h=cv2.boundingRect(conts[i])
        #cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255), 2)
        #(x,y),rad = cv2.minEnclosingCircle(conts[i])
        center = (int(x),int(y))
        coords.append(center)
        #radius.append(int(rad))
        widthList.append(w)
        i = 0
    if len(widthList) > 0:
        while i < 2:
            center = coords[widthList.index(max(widthList))]
            if center[0] < horRes/2:
                centerCoords[0] = center
            else:
                centerCoords[1] = center
            coords.remove(center)
            width = max(widthList)
            widthList.remove(max(widthList))
            #cv2.circle(img,center,rad,(0,22,0),2)
            if i == len(widthList):
                break
            i +=1
    print (centerCoords)

def main():
    setUp([1280,720])
    while True:
        print('test')
        getCoords()
        cv2.imshow("cam",img)
        cv2.waitKey(10)
        
if __name__ == '__main__':
    main()
