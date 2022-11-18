from random import randint
from BoardClasses import Move
from BoardClasses import Board
#The following part should be completed by students.
#Students can modify anything except the class name and existing functions and variables.

#from datetime import datetime, timedelta

class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2
    def get_move(self,move):
        starttime = datetime.now()
        tree = self.board.get_all_possible_moves(self.color)
        chosen = tree[0][0]
        currentpiece,currentmove = 0,0
        while (datetime.now() - starttime < timedelta(minutes=11,seconds=59)):
        #    currentmax = 0
        #     result = simulate(child)
        #     if result == win
        #         wincount++
        #     uct = wincount/nodetotal + sqrt(2*ln(parenttotal)/nodetotal)
        #     if uct > currentmax
        #         chosen = child
        #         currentmax = uct
        #     if len(tree[currentpieceindex])
        self.board.make_move(chosen,self.color)
        return chosen

    #first run ~ selection is start state of board when running get_move()
    # expansion is get_all_possible_moves from state
    # simulation tests one of the possible moves
    # result is backpropped, adds to total games regardless and win count if win
    # selection chooses next untouched move
    # expansion same
    # backprop same
    # ...
    # once all base level moves checked, move down to moves branching off of main possible moves

            ### below is default for get_move
        #if len(move) != 0:
        #    self.board.make_move(move,self.opponent[self.color])
        #else:
        #    self.color = 1
        #moves = self.board.get_all_possible_moves(self.color)
        #index = randint(0,len(moves)-1)
        #inner_index =  randint(0,len(moves[index])-1)
        #move = moves[index][inner_index]
        #self.board.make_move(move,self.color)
        #return move
