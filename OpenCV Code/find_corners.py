import cv2
import numpy as np
import imutils

#empty list to store corner points
corners=[]
corners_selected=False

# mouse callback fn to mark the corner points of the chess board
def add_points(event,x,y,flags,param):
    #stores conrner points
    global corners,corners_selected

    if len(corners)>=4:
        return
    #check for a left click
    if event==cv2.EVENT_LBUTTONDOWN:
        # highlight the selected point and add to list
        mark_point((x,y),param)
        corners.append((x,y))
        print "point %d selected" %len(corners)
        if len(corners)==4:
            mark_point(corners[0],param)
            corners_selected=True
            print "4 corners succesfully taken:"
            print corners

#fn to highliight selected points on the chessboard
def mark_point((x,y),image):
    global corners

    #for first corner only mark a circle
    if len(corners)==0:
        cv2.circle(image,(x,y),10,(0,255,0),-1)

    #for other corners, mark with a circle and draw a line from the last corner
    elif len(corners)==4:
        cv2.line(image,corners[-1],(x,y),(255,0,0),5)

    #if the 4 corners are marked, join first and last with a line    
    else:
        cv2.circle(image,(x,y),10,(0,255,0),-1)
        cv2.line(image,corners[-1],(x,y),(255,0,0),5)

def get_corners(image):
    global corners
    image=imutils.resize(image,640,480)
    cv2.namedWindow("image")
    cv2.setMouseCallback("image",add_points,image)
    while 1:
        cv2.imshow("image",image)
        if cv2.waitKey(1)== 27:
            break
        elif corners_selected:
            cv2.imshow("image",image)
            break
        else:
            pass
        
    print "click anywhere on the image to continue"
    cv2.waitKey(0)
    cv2.destroyWindow("image")
    return corners
    
    

if __name__ == "__main__":
    image=cv2.imread("C:/Users/Ebin/Pictures/chessboard.jpg")
    get_corners(image)


    cv2.destroyAllWindows()
        
