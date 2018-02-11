import chess
import chess.uci

#path=

def input_move(board, move):
    move=chess.Move.from_uci(str(move))
    if move in board.legal_moves:
        board.push_uci(str(move))
        print "player move:"+str(move)
        return True
    else:
        return False

def output_move(board,engine):
    engine.position(board)
    move,__ = engine.go(movetime=2000)
    board.push_uci(str(move))
    print "computer move:"+str(move)

def game_play(board,move,engine):
    if board.turn:
        if move is None:
            move=get_move()
        ret=input_move(board,move)
        if ret:
            pass
        else:
            print "invalid move! Try again"
            return False
        output_move(board,engine)
        return True

    else:
        output_move(board,engine)
        return True
        #print board

def get_move():
    print board
    move=raw_input("Enter the next move:")
    return move

if __name__=="__main__":
    board = chess.Board()
    engine = chess.uci.popen_engine('stockfish 7 x64.exe')
    engine.uci()
    while True:
        game_play(board,None,engine)
        r=raw_input("enter x to quit, anything else to continue")
        if r=='x':
            break
        else:
            pass

    engine.quit()


            
    
    
