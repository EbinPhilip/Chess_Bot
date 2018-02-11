
import find_corners
import find_squares
import cv2
import numpy as np
import imutils
import string

player_move=''
move_made=False

# this fn compares the manually identified corners with all points
# in the squares array to determine the actual corner points
def compare_corners(squares,corners):
    final_corners=[]
    x_cords=squares[:,:,0]
    y_cords=squares[:,:,1]

    for i in corners:
        # compute distnace between i-th corner and all points on the square
        # the result is stored in an array of same length as squares
        x_squares=np.square(x_cords-i[0])
        y_squares=np.square(y_cords-i[1])
        result=np.sqrt(x_squares+y_squares)

        # find the array element with minimum distance 
        min_val=np.amin(result)
        if min_val>15:
            final_corners.append(i)
            continue
        
        # find the positition of that element
        val_position = np.argwhere(result==min_val)

        # add the element at that position from squares to the final corners list
        x,y = squares[val_position.ravel()[0],:,:].ravel()
        final_corners.append((x,y))
    print "corners matched successfully"   
    return final_corners

# fn to mark the points detected
def mark_corners(image,corners):
    image= imutils.resize(image,640,480)
    for i in corners:
        if type(i) is tuple:
            cv2.circle(image,i,5,(0,0,255),-1)
        # if corners is a multidimensional np array
        else:
            for j in i:
                x,y = j.ravel()
                cv2.circle(image,(x,y),5,(0,0,255),-1)

    cv2.imshow("corners identified",image)
    cv2.waitKey(0)
    cv2.destroyWindow("corners identified")

# fn to assign coordinates for rank and file
def rank_file_generate(all_squares):
    b_rank=dict()
    b_file=dict()
    for i in range(1,9):
        b_rank[string.ascii_lowercase[i-1]] = all_squares[:,i,0]
        b_file[9-i] = all_squares[i,:,1]
    return b_rank,b_file

def interpret_cords((x,y),b_rank,b_file):
        
    rank_keys=b_rank.keys()
    rank_keys.sort()

    file_keys=b_file.keys()
    file_keys.sort(reverse=True)
    
    for key in rank_keys:
        if np.amax(b_rank[key])> x:
            print x,np.amax(b_rank[key])
            r=key
            break
        r=None
        
    for key in file_keys:
        if np.amax(b_file[key])> y:
            print y,np.amax(b_file[key])
            f=key
            break
        f=None

    if r!=None and f!=None:
        print "square:"+str(r)+str(f)
        return str(r)+str(f)

    else:
        print "out of bounds"
  


def get_cords(event,x,y,flags,params):
    global move_made,player_move
    if event==cv2.EVENT_LBUTTONDOWN:
        x_cords=x
        y_cords=y
        move=interpret_cords((x_cords,y_cords),b_rank,b_file)
        if not move_made:
            player_move = player_move+move
            if len(player_move)==4:
                move_made=True
                
        

def get_mouse_input(window,rank_input,file_input):
    
    global b_rank,b_file
    b_rank=rank_input
    b_file=file_input

    
    cv2.setMouseCallback(window,get_cords)

        

# fn to generate all chessboard squares from the identified corners
def generate_points(corners):
    # first generate the coordinates of 9 points of the board which lie along the line joining the 1st and 4th corner(1st edge of the chessboard)
    #x coords
    array1=np.linspace(corners[0][0],corners[3][0],num=9,endpoint=True,retstep=False,dtype=np.int0).reshape((9,1))
    #y coords
    array2=np.linspace(corners[0][1],corners[3][1],num=9,endpoint=True,retstep=False,dtype=np.int0).reshape((9,1))
    # make an array to combine both th x and y set of coordinanates
    edge_1=np.ones((9,1,2),dtype=np.int0)
    # store them into the array
    edge_1[:,:,0]=array1
    edge_1[:,:,1]=array2


    # generate coordinates of 9 points along the second edge similarly
    array1=np.linspace(corners[1][0],corners[2][0],num=9,endpoint=True,retstep=False,dtype=np.int0).reshape((9,1))
    array2=np.linspace(corners[1][1],corners[2][1],num=9,endpoint=True,retstep=False,dtype=np.int0).reshape((9,1))

    edge_2=np.ones((9,1,2),dtype=np.int0)
    
    edge_2[:,:,0]=array1
    edge_2[:,:,1]=array2

    #make a final array to store all the chess square coords
    # use linspace on both edges to generate the coordinate of corners of all chessboard squares
    final_array = np.zeros((9,9,2),dtype=np.int0)  
    # the for loop picks the first coord from both edges and generates the 9 points in between 
    for i in range(0,9):
        ix,iy = edge_1[i,:].ravel()
        jx,jy = edge_2[i,:].ravel()
        
        final_array[i,:,0] = np.linspace(ix,jx,num=9,endpoint=True,retstep=False,dtype=np.int0)
        final_array[i,:,1] = np.linspace(iy,jy,num=9,endpoint=True,retstep=False,dtype=np.int0)
        
    print "squares ends succesfully identified"
    # return all the chessoard corners
    return final_array

        
if __name__=='__main__':
    image=cv2.imread("C:/Users/Ebin/Pictures/chessboard.jpg")
    squares=find_squares.get_squares(image)
    corners=find_corners.get_corners(image)
    corners=compare_corners(squares,corners)
    mark_corners(image,corners)
    all_squares = generate_points(corners)
    mark_corners(image,all_squares)
    b_rank,b_file = rank_file_generate(all_squares)
    print "rank"
    print b_rank
    print "file"
    print b_file
    get_mouse_input(image,b_rank,b_file,)
