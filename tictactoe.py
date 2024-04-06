"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    
    # When the game is over, return any player. In this case, return X.
    # count the number of times each player has played
    numX, numO = 0, 0
    for row in board:
        for col in row:
            if col == X:
                numX += 1
            elif col == O:
                numO += 1
    
    # determine player's move based on num of X and O
    if numX == numO:
        return X
    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    
    # Given the state of the board, what are all the possible moves the player can make?

    moves = set()
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                moves.add((i, j))

    # print(moves)
    return moves

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    # While not modifying the original board.
    # Deepcopy: creating an entirely new board completely independent from the original
    # shallow copy: creating a copy of the board that is linked to the original - changing 
    #                 the value within any of the boards also changes the other board
    
    all_actions = actions(board)
    new_board = copy.deepcopy(board)
    symbol = player(board)
    
    if action in all_actions:
        new_board[action[0]][action[1]] = symbol
    else:       # raise exception
        raise KeyError
    
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    winX = [X,X,X]
    winO = [O,O,O]
    
    win_states = [board[0], board[1], board[2],
                  [board[0][0], board[1][0], board[2][0]],  # col 0
                  [board[0][1], board[1][1], board[2][1]],  # col 1
                  [board[0][2], board[1][2], board[2][2]],  # col 2
                  [board[0][0], board[1][1], board[2][2]],  # diag 0
                  [board[0][2], board[1][1], board[2][0]]   # diag 1
                  ]
    
    for state in win_states:
        if state == winX:
            return X
        if state == winO:
            return O
        
    return None     # no winners yet

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    
    # A game is over if a player wins, or if all the squares are filled
    if winner(board) is not None:
        return True
    
    # no one has won, check if board is full
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False

    # board is full. game ended with a tie
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    
    # Assumes game has already ended
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0


# the 2 functions call each other recursively until the terminal state is reached
# Max player picks action A in Actions(S) that produces highest value of min-val(result(S,A))
# Pruning: alpha - the best score the max player can guarantee so far
# beta - the best score the min player can guarantee so far

def max_valued_action(board, alpha, beta):
    """
    Returns the max value together with the best action that gave the max value
    """
    if terminal(board):
        return [utility(board), None]
    v = -math.inf
    best_action = None
    for action in actions(board):
        
        # determine the best value the min player can get from their perspective
        new_v = min_valued_action(result(board, action), alpha, beta)[0]
        if new_v > v:
            best_action = action
            v = new_v
        
        # min player ignores any path with v more than beta
        if v >= beta:  
            break
        
        # update the best score guaranteed by the max player
        alpha = max(alpha, v)
    return [v, best_action]


# Min player picks action A in Actions(S) that produces lowest value of max-val(result(S,A))
def min_valued_action(board, alpha, beta):
    """
    Returns the min value together with the best action that gave the min value
    """
    if terminal(board):
        return [utility(board), None]
    v = math.inf
    best_action = None
    for action in actions(board):
        
        # determine the best value the max player can get from their perspective
        new_v = max_valued_action(result(board, action), alpha, beta)[0]
        if new_v < v:
            best_action = action
            v = new_v
        
        # max player ignores any path with v less than alpha
        if v <= alpha:  
            break
        
        # update the best score guaranteed by the min player
        beta = min(beta, v)     
    return [v, best_action]


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    # X attempts to maximise the score, while O attempts to minimise the score.
    
    if player(board) == X:
        return max_valued_action(board, -math.inf, math.inf)[1]
    return min_valued_action(board, -math.inf, math.inf)[1]


# def max_valued_action(board):
#     """
#     Returns the max value together with the best action that gave the max value
#     """
#     if terminal(board):
#         return [utility(board), None]
#     v = -math.inf
#     prev_v = v
#     for action in actions(board):
#         v = max(v, min_valued_action(result(board, action))[0])
#         if v != prev_v:
#             best_action = action
#             prev_v = v
#     return [v, best_action]


# # Min player picks action A in Actions(S) that produces lowest value of max-val(result(S,A))
# def min_valued_action(board):
#     """
#     Returns the min value together with the best action that gave the min value
#     """
#     if terminal(board):
#         return [utility(board), None]
#     v = math.inf
#     prev_v = v
#     for action in actions(board):
#         v = min(v, max_valued_action(result(board, action))[0])
#         if v != prev_v:
#             best_action = action
#             prev_v = v
#     return [v, best_action]


# def minimax(board):
#     """
#     Returns the optimal action for the current player on the board.
#     """
    
#     # X attempts to maximise the score, while O attempts to minimise the score.
    
#     if player(board) == X:
#         return max_valued_action(board)[1]
#     return min_valued_action(board)[1]
