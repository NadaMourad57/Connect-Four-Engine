Here’s a **README** file for your Connect 4 project:

---

# Connect 4 Game with Minimax Algorithm

## Overview

This is a console-based implementation of the **Connect 4** game where a human player competes against an AI. The AI uses the **Minimax algorithm** to evaluate potential moves and select the best one, ensuring a challenging gameplay experience.

## Features

- **Console-based gameplay**: The game is played entirely in the terminal.
- **Human vs AI**: The human player competes against an AI player.
- **Minimax Algorithm**:
  - AI uses the Minimax algorithm to evaluate and choose optimal moves.
  - Configurable depth for decision-making.
  - Includes `MAXIMIZE` and `MINIMIZE` functions.
- **Scoring System**:
  - Tracks the number of "connected fours" for both players.
- **Dynamic Board Display**: The game board updates after every turn.

## How to Play

1. **Run the Game**:
   - Ensure you have Python installed.
   - Run the game script:
     ```bash
     python connect4.py
     ```

2. **Human's Turn**:
   - Enter the column number (0-6) where you want to drop your disc.
   - The game validates the move. If the column is full or invalid, you'll be prompted to try again.

3. **AI's Turn**:
   - The AI "thinks" and chooses the best column to play using the Minimax algorithm.
   - The chosen move is displayed on the board.

4. **Game End**:
   - The game ends when the board is full, and the winner is determined based on the number of "connected fours" each player has.

## Rules

- Players take turns dropping discs into the columns.
- The disc falls to the lowest available space in the selected column.
- The goal is to form a horizontal, vertical, or diagonal line of **four discs** (a "connect four").
- The game ends when the board is full, and the winner is the player with the highest score of "connected fours."

## Code Overview

### Main Classes and Functions

- **`Connect4` Class**:
  - Manages the game state, board initialization, valid moves, and scoring system.
  - Includes methods like `play`, `is_valid_move`, and `generate_children`.

- **Minimax Algorithm**:
  - `maximize`: The AI evaluates moves to maximize its utility.
  - `minimize`: The AI simulates the human's moves to minimize its utility.
  - `decision`: Entry point for the AI to choose the best move.

- **Helper Functions**:
  - `eval_state`: Evaluates the utility of a game state based on scores.
  - `count_connected_fours`: Counts the number of "connected fours" for a given player.
  - `terminal_test`: Checks if the game is in a terminal state.

### Key Concepts

1. **Minimax with Depth Limit**:
   - The algorithm explores a game tree up to a specified depth to balance performance and decision quality.

2. **Child Boards**:
   - All possible moves for a player are generated as "children" of the current board state.

3. **Scoring**:
   - The heuristic (`eval_state`) calculates utility as the difference between the AI's and human's "connected fours."

## Example Gameplay

### Starting Board:

```
Current Board:
[[0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0]]
```

### Human's Turn:
```
Your turn! Choose a column (0-6): 3
```

### Updated Board:
```
Current Board:
[[0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0]
 [0 0 0 1 0 0 0]]
```

### AI's Turn:
```
AI is thinking...
AI chooses column 4

Current Board:
[[0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0]
 [0 0 0 1 2 0 0]]
```

## Requirements

- **Python**: Ensure Python 3.x is installed on your system.
- **Numpy**: The game uses `numpy` for managing the game board. Install it with:
  ```bash
  pip install numpy
  ```

## How to Customize

1. **Change Board Size**:
   - Modify the `rows` and `cols` parameters when initializing the `Connect4` class.

2. **Adjust AI Depth**:
   - Modify the `depth` parameter in the `decision` function to control the complexity of the AI's decision-making:
     ```python
     col = decision(game.board, depth=4)  # Higher depth = smarter AI, slower performance
     ```

3. **Heuristic Function**:
   - Update the `eval_state` function to improve AI performance based on additional heuristics.

## Known Limitations

- The AI's performance depends on the `depth` parameter. Higher depths may increase computation time significantly.
- The heuristic function (`eval_state`) can be further refined for better decision-making.

## Future Enhancements

- Add an option to play **human vs. human**.
- Implement **alpha-beta pruning** to optimize the Minimax algorithm.
- Add a GUI using `Tkinter` or another framework for better user experience.
- Allow saving and loading game states.



