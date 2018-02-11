import cv2
import numpy as np
import imutils

def get_squares(image):
    print "detecting all the chessboard squares..."
    image=imutils.resize(image,640,480)
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    corners=cv2.goodFeaturesToTrack(gray,100,0.01,12) 
    corners=np.int0(corners)
    mark_squares(image,corners)
    return corners

def mark_squares(image,corners):
    cv2.namedWindow("detected squares")
    for i in corners:
        x,y=i.ravel()
        cv2.circle(image,(x,y),3,(255,0,0),-1)
    cv2.imshow("detected squares",image)
    cv2.waitKey(0)
    cv2.destroyWindow("detected squares")

if __name__ == "__main__":

    image = cv2.imread("C:/Users/Ebin/Pictures/chessboard.jpg")
    get_squares(image)
