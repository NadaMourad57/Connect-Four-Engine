import numpy as np


class Connect4:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = None
        self.scores = {1: 0, 2: 0}  # 1: human, 2: AI

    def initialize_board(self):
        self.board = np.zeros((self.rows, self.cols), dtype=int)

    def play(self, col, player):
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = player
                self.update_scores(player, row, col)
                return True
        return False

    def is_valid_move(self, col):
        # column is in the range of the board and column is not full
        return 0 <= col < self.cols and self.board[0][col] == 0

    def get_valid_moves(self):
        # returns a list of columns that are  available according to if the column is full or not
        # the function that checks for the condition is the is valid move function
        return [col for col in range(self.cols) if self.is_valid_move(col)]

    def get_children(self, player):
        children = []
        # generate the children the states are generated by inserting a disc for the human in each valid column
        for col in self.get_valid_moves():
            child_board = self.board.copy()

            # moves on rows from down to top and inserts the disc where the cell is empty  and then
            #  adds the child to the children and the corresponding column
            for row in range(self.rows - 1, -1, -1):
                if child_board[row][col] == 0:
                    child_board[row][col] = player
                    break
            children.append((child_board, col))
        return children

    def is_full(self):
        return np.all(self.board != 0)

    def update_scores(self, player, row, col):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            for sign in [-1, 1]:
                r, c = row, col
                while 0 <= r + dr * sign < self.rows and 0 <= c + dc * sign < self.cols:
                    r, c = r + dr * sign, c + dc * sign
                    if self.board[r][c] == player:
                        count += 1
                        if count == 4:
                            self.scores[player] += 1
                            break
                    else:
                        break

    def print_board(self):
        print("\nCurrent Board:")
        print(self.board)
        print("\n")




def generate_positional_scores(rows, cols):
    scores = np.zeros((rows, cols))
    mid_row, mid_col = rows // 2, cols // 2
    for row in range(rows):
        for col in range(cols):
            scores[row][col] = rows + cols - (abs(row - mid_row) + abs(col - mid_col))
    return scores


def calculate_positional_advantage(board, player):
    rows,cols=board.shape
    position_scores=generate_positional_scores(rows,cols)
    score=0

    for i in range(rows):
        for j in range(cols):
            if board[i][j]==player:
                score+=position_scores[i][j]
    return score


def search_direction(board, length, direction, row, col, player):
    rows, cols = board.shape
    change_x, change_y = direction
    for k in range(length):
        new_row = row + k * change_x
        new_col = col + k * change_y
        if new_row < 0 or new_row >= rows or new_col < 0 or new_col >= cols:
            return 0
        if board[new_row][new_col] != player:
            return 0

    return 1
def count_connected_N(board, player, length):
    count = 0
    directions = {
        "vertical": (0, 1),
        "horizontal": (1, 0),
        "positivediagonal": (1, 1),
        "negativediagonal": (1, -1)
    }
    rows, cols = board.shape
    
    for row in range(rows):
        for col in range(cols):
            for direction in directions.values():
                # Count the fully connected sequences (length 4)
                if length == 4:
                    count += search_direction(board, length, direction, row, col, player)
                # Count the potential sequences (length 2 or 3 with one empty space)
                elif length == 2 or length == 3:
                    count += check_potential_sequence(board, player, row, col, length, direction)
    
    return count

def check_potential_sequence(board, player, row, col, length, direction):
    count = 0
    directions = direction
    empty_spots = 0
    

    for sign in [-1, 1]:
        r, c = row, col
        sequence = []


        for i in range(length + 1): 
            r, c = r + sign * directions[0], c + sign * directions[1]
            if 0 <= r < board.shape[0] and 0 <= c < board.shape[1]:
                if board[r][c] == player:
                    sequence.append(1) 
                elif board[r][c] == 0:
                    sequence.append(0) 
                    empty_spots += 1 
                else:
                    break
            else:
                break
        if len(sequence) == length + 1 and empty_spots == 1:
            count += 1

    return count


def adjust_weights(board):
    filled_cells = np.count_nonzero(board)
    total_cells = board.size
    fill_percentage = filled_cells / total_cells

    if fill_percentage < 0.33:  # Early game
        return {"fours": 50, "threes": 20, "twos": 10, "position": 30}
    elif fill_percentage < 0.66:  # Mid-game
        return {"fours": 100, "threes": 50, "twos": 10, "position": 10}
    else:  # Late game
        return {"fours": 1000, "threes": 200, "twos": 0, "position": 5}


def eval_state(board):
    # Heuristic function to evaluate the state of the board
    
    # Calculate the AI's connected fours, threes, and twos
    ai_connected_four = count_connected_N(board, 2, 4)
    ai_connected_three = count_connected_N(board, 2, 3)
    ai_connected_two = count_connected_N(board, 2, 2)
    
    # Calculate the human's connected fours, threes, and twos
    human_connected_four = count_connected_N(board, 1, 4)
    human_connected_three = count_connected_N(board, 1, 3)
    human_connected_two = count_connected_N(board, 1, 2)
    
    # Calculate AI's positional advantage
    ai_positional_advantage = calculate_positional_advantage(board, 2)
    
    # Get the weights based on the board state
    weights = adjust_weights(board)
    
    # Calculate the AI's score
    ai_score = (
        weights["fours"] * ai_connected_four +
        weights["threes"] * ai_connected_three +
        weights["twos"] * ai_connected_two +
        weights["position"] * ai_positional_advantage
    )
    
    # Calculate the human's score
    human_score = (
        weights["fours"] * human_connected_four +
        weights["threes"] * human_connected_three +
        weights["twos"] * human_connected_two +
        weights["position"] * calculate_positional_advantage(board, 1)  # human has player 1
    )

    # Return the difference between AI's and human's scores
    return ai_score - human_score



def search_direction(board, length, direction, row, col, player):
    rows, cols = board.shape
    change_x, change_y = direction
    for k in range(length):
        new_row = row + k * change_x
        new_col = col + k * change_y
        if new_row < 0 or new_row >= rows or new_col < 0 or new_col >= cols:
            return 0
        if board[new_row][new_col] != player:
            return 0

    return 1


def count_connected_N(board, player, length):
    count=0
    directions={
        "vertical":(0,1),
        "horizontal":(1,0),
        "positivediagonal":(1,1),
        "negativediagonal":(-1,-1)
    }
    rows, cols = board.shape
    for row in range(rows):
        for col in range(cols):
           for direction in directions.values():
            count+=search_direction(board,length,direction,row,col,player)

    return count


def terminal_test(board):
    return np.all(board != 0)


class game_algorithms:

    def __init__(self):
        self.Is_pruning = False

    def minimize(self, board, depth, alpha=float('-inf'), beta=float('inf')):
        # recursive calss till it reachses the depth , each call we decrease depth by 1
        if terminal_test(board) or depth == 0:
            return None, eval_state(board)
        min_child = None
        min_utility = float('inf')
        temp_game = Connect4()
        temp_game.board = board
        for child_board, col in temp_game.get_children(1):
            _, utility = self.maximize(child_board, depth - 1, alpha, beta)
            if utility < min_utility:
                min_child = col
                min_utility = utility
            if self.Is_pruning:
                if min_utility <= alpha:
                    break
                beta=min(min_utility,beta)

        return min_child, min_utility

    def maximize(self, board, depth, alpha=float('-inf'), beta=float('inf')):
        if terminal_test(board) or depth == 0:
            return None, eval_state(board)
        max_child = None
        max_utility = -float('inf')
        temp_game = Connect4()
        temp_game.board = board
        for child_board, col in temp_game.get_children(2):
            _, utility = self.minimize(child_board, depth - 1, alpha, beta)
            if utility > max_utility:
                max_child = col
                max_utility = utility
            if self.Is_pruning:
                if max_utility >= beta:
                    break
                alpha=max(max_utility,alpha)
        return max_child, max_utility

    def decision(self,board, depth=4):
        # starts as a maximize state for the AI
        col, _ = self.maximize(board, depth)
        return col


def play_game():
    game = Connect4()
    game.initialize_board()
    game.print_board()
    game_algo = game_algorithms()

    # Choose algorithm
    choice = int(input("Choose Algorithm:\n1 - Minimax\n2 - Minimax with Pruning\nYour Choice: "))
    if choice == 1:
        game_algo.Is_pruning = False
        print("Minimax without pruning selected.")
    elif choice == 2:
        game_algo.Is_pruning = True
        print("Minimax with pruning selected.")
    else:
        print("Invalid choice. Defaulting to Minimax without pruning.")
        game_algo.Is_pruning = False

    while not game.is_full():
        # Human Turn
        valid = False
        while not valid:
            try:
                col = int(input("Your turn! Choose a column (0-6): "))
                if game.is_valid_move(col):
                    valid = True
                    game.play(col, 1)
                else:
                    print("Invalid move! Try again.")
            except ValueError:
                print("Please enter a valid column number.")
        game.print_board()

        if game.is_full():
            break

        # AI Turn
        print("AI is thinking...")
        col = game_algo.decision(game.board,depth=4)
        game.play(col, 2)
        print(f"AI chooses column {col}")
        game.print_board()

        # End game
    print("Game Over!")
    ai_score = game.scores[2]
    human_score = game.scores[1]
    print(f"Final Scores - AI: {ai_score}, Human: {human_score}")
    if ai_score > human_score:
        print("AI wins!")
    elif human_score > ai_score:
        print("You win!")
    else:
        print("It's a tie!")

if __name__ == "__main__":
     play_game()



