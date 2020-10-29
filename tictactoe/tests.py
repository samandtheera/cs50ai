from tictactoe import board_columns

columns = []

for i in range(3):
    print(i)

def max_value(board):

    if terminal(board):
        return None

    if player(board) == X:
        v = -math.inf
        if terminal(board):
            return utility(board)
        for action in actions(board):
            # assign a minimum value 'a'
            a = min_value(result(board, action))
        return v


def min_value(board):

    if terminal(board):
        return None

    if player(board) == O:
        v = math.inf
        if terminal(board):
            return utility(board)
        for action in actions(board):
            v = min(v, max_value(result(board, action)))
        return v
