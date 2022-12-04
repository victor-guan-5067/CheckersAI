from random import randint
from BoardClasses import Move
from BoardClasses import Board
# The following part should be completed by students.
# Students can modify anything except the class name and existing functions and variables.

from datetime import datetime, timedelta
import copy, math


class StudentAI():
    def __init__(self, col, row, p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col, row, p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1: 2, 2: 1}
        self.color = 2

    # makes a random move
    def make_sim_move(self, board, color):
        """
        Simulates a random move. Used in StudentAI.simulate().
        @board : Board object, where move is made
        @color : Current color that makes move
        """
        moves = board.get_all_possible_moves(color)
        if len(moves) > 0:
            index = randint(0, len(moves) - 1)
            inner_index = randint(0, len(moves[index]) - 1)
            move = moves[index][inner_index]
            board.make_move(move, color)
        return board

    def simulate(self, board, color, allottedtime):
        """
        Simulates a game based on provided board state and how much time it can run at maximum
        @return : True if win, False if not
        """

        turns_to_tie = 0
        simulatestarttime = datetime.now()

        while datetime.now() - simulatestarttime < allottedtime:
            board = self.make_sim_move(board, color)

            # returns True if self won, False if opponent won
            if 0 != board.is_win(color):
                return self.color == board.is_win(color)
            # will win if
            if turns_to_tie >= self.board.tie_max:
                return True

            # change color/turn
            if color == self.color:
                color = self.opponent[self.color]
            else:
                color = self.color
            turns_to_tie += 1
        return False

    def get_move(self, move):
        starttime = datetime.now()
        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1

        tree = self.board.get_all_possible_moves(self.color)
        currentmove = tree[0][0]  # the first selects the first possible move available
        chosen = currentmove  # the default move to return is the first possible move available
        resultdict = {}  # holds known moves and their associated win ratios
        resultdict[currentmove] = [0, 0]  # instantiates resultdict with values for first move
        moveboard = copy.deepcopy(
            self.board)  # copy of the board, used to simulate games without altering actual board state
        result = False  # records latest simulation result (win or not)
        parenttotal = 0

        state = 2
        # state is used to segment aspects of the mcts algorithm into smaller parts, so the while loop condition can be checked more often and the risk of exceeding the allotted time limit is mitigated
        """state key
        0 := select next node to test
        1 := expand selected node & choose
        2 := simulate game off of move
        3 := backpropagate results
        """
        explored = False

        while not explored:
            if state == 0:
                maxknown = -1
                for childpiece in tree:
                    for childmove in childpiece:
                        if childmove not in resultdict or resultdict[childmove][1] <= 0:
                            currentmove = childmove
                            resultdict[currentmove] = [0, 0]
                            break
                        else:
                            uct = resultdict[childmove][0] / resultdict[childmove][1] + math.sqrt(
                                2 * math.log(parenttotal) / resultdict[childmove][1])
                            # uct = nodewins/nodetotal + sqrt(2*ln(parenttotal)/nodetotal)
                            if uct > maxknown:
                                currentmove = childmove
                                maxknown = uct
                state = 1
            elif state == 1:
                moveboard = copy.deepcopy(self.board)  # copy of the board
                moveboard.make_move(currentmove, self.color)  # update simulation board with chosen move
                if self.color == moveboard.is_win(self.color):
                    self.board.make_move(currentmove, self.color)
                    return currentmove
                state = 2
            elif state == 2:
                result = self.simulate(moveboard, self.opponent[self.color],
                                       timedelta(seconds=9, milliseconds=900) - (datetime.now() - starttime))  # simulate game off of focus move
                state = 3
            elif state == 3:
                if result:
                    resultdict[currentmove][0] += 1
                resultdict[currentmove][1] += 1
                parenttotal += 1
                # If a move has 95% win rate, just make it
                if (resultdict[currentmove][1] >= 50 and ((resultdict[currentmove][0]/resultdict[currentmove][1]) > 0.95)):
                    explored = True
                    
                # If every node's been explored around 100 times, just make the move
                if (parenttotal/len(tree) >= 200):
                    explored = True
                state = 0
            else:
                state = 0
        bestodds = 0
        for piece in tree:
            for move in piece:
                if resultdict[move][0] / resultdict[move][1] > bestodds:
                    chosen = move
                    bestodds = resultdict[move][0] / resultdict[move][1]
        self.board.make_move(chosen, self.color)
        return chosen

    # first run
    # selection is start state of board when running get_move()
    # expansion is get_all_possible_moves from state
    # simulation tests one of the possible moves
    # backpropagate result, adds to total games regardless and win count if win
    # consecutive runs
    # selection chooses next untouched move
    # expansion same
    # simulation same
    # backpropagate same
    # ...
    # once all base level moves checked, move down to moves branching off of main possible moves
    # run against RandomAI with "python3 AI_Runner.py 8 8 3 l /home/agee4/CheckersAI/src/checkers-python/main.py /home/agee4/CheckersAI/src/checkers-python/Tools/Sample_AIs/Random_AI/main.py"
