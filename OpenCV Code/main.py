import chess
import chess.uci
import find_corners
import find_squares
import cv2
import numpy as np
import imutils
import string
import grid_generate as gg
import game



def play(board,engine):
    if gg.move_made:
        ret = game.game_play(board,gg.player_move,engine)
        if ret:
            gg.move_made=False
            gg.player_move=''
            print board
        else:
            gg.move_made=False
            gg.player_move=''
        

if __name__=='__main__':
    board = chess.Board()
    engine = chess.uci.popen_engine('stockfish 7 x64.exe')
    engine.uci()
    image=cv2.imread("C:/Users/Ebin/Pictures/chessboard.jpg")
    image = imutils.resize(image,640,480)
    squares=find_squares.get_squares(image)
    corners=find_corners.get_corners(image)
    corners=gg.compare_corners(squares,corners)
    gg.mark_corners(image,corners)
    all_squares = gg.generate_points(corners)
    gg.mark_corners(image,all_squares)
    b_rank,b_file = gg.rank_file_generate(all_squares)
    
    window='mouse_input'
    cv2.namedWindow(window)
    
    gg.get_mouse_input(window,b_rank,b_file)
    print "game started"
    print board
    while True:
        cv2.imshow(window,image)
        play(board,engine)
        if cv2.waitKey(1)&0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    engine.quit()
    
        
