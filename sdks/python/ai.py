import copy
from typing import Optional


##############################################################
# Constants for the game. Modify if rules of the game change
##############################################################

# Number of rows and columns on the board.
# If changed, POSITION_WEIGHTS must also be updated to match the new board size.
BOARD_SIZE = 8

# The two player identifiers the server can assign us — update here if the server changes them
PLAYERS = (1, 2)

# All 8 directions a tile can be approached from (vertical, horizontal, diagonal)
DIRECTIONS = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]

##############################################################
# Search parameters:
# Can be tuned to adjust the behavior of the AI.
##############################################################

# MOBILITY WEIGHT:
# Weight to give to mobility (number of valid moves) in the
# evaluation function.
# Higher means AI prioritizes player's number of movement options more,
# lower means AI prioritizes tile count and position more.
# Briefly experimented with tuning this;
# found 5 to work just fine, but could change with more testing/trials.
MOBILITY_WEIGHT = 5

# POSITION WEIGHTS:
# Based on short research that corners are very good,
# squares adjacent to corners are very bad,
# and edges are good.
# See reference/inspiration:
# https://medium.com/@jackychoi26/how-to-write-an-othello-ai-with-alpha-beta-search-58131ffe67eb
POSITION_WEIGHTS = [
  [100, -20,  10,   5,   5,  10, -20, 100],
  [-20, -50,   0,   0,   0,   0, -50, -20],
  [ 10,   0,   0,   0,   0,   0,   0,  10],
  [  5,   0,   0,   5,   5,   0,   0,   5],
  [  5,   0,   0,   5,   5,   0,   0,   5],
  [ 10,   0,   0,   0,   0,   0,   0,  10],
  [-20, -50,  0,    0,   0,   0, -50, -20],
  [100, -20,  10,   5,   5,  10, -20, 100],
]

# Maps minimum turn time (ms) to search depth.
# Lowers depth in case server changes max turn time, to avoid timeouts.
DEPTH_THRESHOLDS = [
  (12000, 4),
  (3000,  3),
  (1000,  2),
  (0,     1),
]

def get_depth(max_turn_time: int) -> int:
  """Returns the search depth to use based on the server's max turn time."""
  for threshold, depth in DEPTH_THRESHOLDS:
    if max_turn_time >= threshold:
      return depth
  return 1  # Default to depth 1 if no thresholds match, though this should not happen


def get_flipped(row: int, col: int, player: int, board: list) -> list:
  """Returns a list of (row, col) tiles that would be flipped if player places at (row, col)."""
  opponent = PLAYERS[1] if player == PLAYERS[0] else PLAYERS[0]
  all_flipped = []

  for dr, dc in DIRECTIONS:
    r, c = row + dr, col + dc
    candidates = []
    while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == opponent:
      candidates.append((r, c))
      r += dr
      c += dc
    if candidates and 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
      all_flipped.extend(candidates)

  return all_flipped


def apply_move(row: int, col: int, player: int, board: list) -> list:
  """Applies a move for player at (row, col) and returns the resulting board. Returns None if the move is invalid."""
  flipped = get_flipped(row, col, player, board)
  if not flipped:
    return None
  new_board = copy.deepcopy(board)
  new_board[row][col] = player
  for r, c in flipped:
    new_board[r][c] = player
  return new_board


def get_valid_moves(player: int, board: list) -> list:
  """Returns all legal moves for player as a list of (row, col) tuples."""
  moves = []
  for row in range(BOARD_SIZE):
    for col in range(BOARD_SIZE):
      if board[row][col] == 0 and get_flipped(row, col, player, board):
        moves.append((row, col))
  return moves


def evaluate_board(player: int, board: list) -> int:
  """Scores the board for player using tile count, positional weights, and mobility.
  Positive means player is winning."""
  opponent = PLAYERS[1] if player == PLAYERS[0] else PLAYERS[0]
  tile_score = 0
  position_score = 0
  for r in range(BOARD_SIZE):
    for c in range(BOARD_SIZE):
      if board[r][c] == player:
        tile_score += 1
        position_score += POSITION_WEIGHTS[r][c]
      elif board[r][c] == opponent:
        tile_score -= 1
        position_score -= POSITION_WEIGHTS[r][c]

  mobility_score = (len(get_valid_moves(player, board)) - len(get_valid_moves(opponent, board))) * MOBILITY_WEIGHT

  return position_score + tile_score + mobility_score


def minimax(board: list, player: int, depth: int, current_player: int) -> int:
  """Recursively searches ahead by depth turns. Maximizes score on our turns,
  minimizes on opponent's turns, assuming the opponent plays optimally."""
  opponent = PLAYERS[1] if player == PLAYERS[0] else PLAYERS[0]
  next_player = opponent if current_player == player else player

  # Base case: evaluate board if depth is 0
  if depth == 0:
    return evaluate_board(player, board)

  valid_moves = get_valid_moves(current_player, board)
  # If no valid moves, skip turn. If opponent also has no moves, evaluate board.
  if not valid_moves:
    if not get_valid_moves(next_player, board):
      return evaluate_board(player, board)
    return minimax(board, player, depth - 1, next_player)

  # Maximizing if it's our turn, minimizing if it's opponent's turn (assuming opponent also plays optimally)
  if current_player == player:
    best = float('-inf')
    for row, col in valid_moves:
      new_board = apply_move(row, col, current_player, board)
      score = minimax(new_board, player, depth - 1, next_player)
      best = max(best, score)
    return best
  best = float('inf')
  for row, col in valid_moves:
    new_board = apply_move(row, col, current_player, board)
    score = minimax(new_board, player, depth - 1, next_player)
    best = min(best, score)
  return best


def get_move(player: int, board: list, max_turn_time: int) -> Optional[list]:
  """Returns the best move for player as [row, col] using minimax search, or None if no moves are available."""
  opponent = PLAYERS[1] if player == PLAYERS[0] else PLAYERS[0]
  depth = get_depth(max_turn_time)

  valid_moves = get_valid_moves(player, board)
  if not valid_moves:
    return None

  best_score = float('-inf')
  best_move = None

  for row, col in valid_moves:
    new_board = apply_move(row, col, player, board)
    score = minimax(new_board, player, depth - 1, opponent)
    if score > best_score:
      best_score = score
      best_move = [row, col]

  # print(f"Best move for player {player}: {best_move} with score {best_score} at depth {depth}")
  return best_move
