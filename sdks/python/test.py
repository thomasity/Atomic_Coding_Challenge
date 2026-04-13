import unittest
import copy
from ai import (
  get_flipped, apply_move, get_valid_moves,
  evaluate_board, minimax, get_move, get_depth,
  DEPTH_THRESHOLDS
)
from client import prepare_response

# Standard starting board: player 1 at [3,3],[4,4] — player 2 at [3,4],[4,3]
STARTING_BOARD = [
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 1, 2, 0, 0, 0],
  [0, 0, 0, 2, 1, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
]

# Board where player 1 can immediately take a corner at [0,0]
CORNER_AVAILABLE_BOARD = [
  [0, 2, 1, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
]

# Board where no moves are available for player 1
NO_MOVES_BOARD = [
  [1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 0],
]


class TestGetFlipped(unittest.TestCase):
  def test_valid_move_returns_correct_tiles(self):
    # Placing at [5,3] as player 1 flips the opponent at [4,3]
    flipped = get_flipped(5, 3, 1, STARTING_BOARD)
    self.assertEqual(flipped, [(4, 3)])

  def test_invalid_move_returns_empty(self):
    # [0,0] has no opponent tiles to flank
    flipped = get_flipped(0, 0, 1, STARTING_BOARD)
    self.assertEqual(flipped, [])

  def test_occupied_cell_returns_empty(self):
    # [3,3] is already occupied — placing there flanks nothing
    flipped = get_flipped(3, 3, 2, STARTING_BOARD)
    self.assertEqual(flipped, [])

  def test_player_two_valid_move(self):
    # Placing at [5,4] as player 2 flips the opponent at [4,4]
    flipped = get_flipped(5, 4, 2, STARTING_BOARD)
    self.assertEqual(flipped, [(4, 4)])

  def test_multi_direction_flip(self):
    # Board where a single move flips tiles in two directions
    board = [
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 1, 0, 0, 0, 0],
      [0, 0, 0, 2, 0, 0, 0, 0],
      [0, 1, 2, 0, 2, 1, 0, 0],
      [0, 0, 0, 2, 0, 0, 0, 0],
      [0, 0, 0, 1, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
    ]
    # Placing at [3,3] as player 1 should flip [3,2] (left) and [3,4] (right) and [2,3] (up) and [4,3] (down)
    flipped = get_flipped(3, 3, 1, board)
    self.assertIn((3, 2), flipped)
    self.assertIn((3, 4), flipped)
    self.assertIn((2, 3), flipped)
    self.assertIn((4, 3), flipped)


class TestApplyMove(unittest.TestCase):
  def test_valid_move_returns_new_board(self):
    new_board = apply_move(5, 3, 1, STARTING_BOARD)
    self.assertIsNotNone(new_board)
    self.assertEqual(new_board[5][3], 1)
    self.assertEqual(new_board[4][3], 1)  # flipped

  def test_invalid_move_returns_none(self):
    self.assertIsNone(apply_move(0, 0, 1, STARTING_BOARD))

  def test_does_not_mutate_original_board(self):
    original = copy.deepcopy(STARTING_BOARD)
    apply_move(5, 3, 1, STARTING_BOARD)
    self.assertEqual(STARTING_BOARD, original)


class TestGetValidMoves(unittest.TestCase):
  def test_starting_board_player_one_has_four_moves(self):
    moves = get_valid_moves(1, STARTING_BOARD)
    self.assertEqual(len(moves), 4)

  def test_starting_board_player_two_has_four_moves(self):
    moves = get_valid_moves(2, STARTING_BOARD)
    self.assertEqual(len(moves), 4)

  def test_no_moves_returns_empty(self):
    moves = get_valid_moves(1, NO_MOVES_BOARD)
    self.assertEqual(moves, [])

  def test_all_moves_are_on_empty_cells(self):
    moves = get_valid_moves(1, STARTING_BOARD)
    for row, col in moves:
      self.assertEqual(STARTING_BOARD[row][col], 0)


class TestEvaluateBoard(unittest.TestCase):
  def test_starting_board_is_symmetric(self):
    # Both players have equal tiles, positions, and mobility — score should be 0
    self.assertEqual(evaluate_board(1, STARTING_BOARD), 0)

  def test_player_with_corner_scores_higher(self):
    board = copy.deepcopy(STARTING_BOARD)
    board[0][0] = 1
    self.assertGreater(evaluate_board(1, board), evaluate_board(2, board))

  def test_opponent_perspective_is_inverse(self):
    # evaluate_board(1) and evaluate_board(2) should be opposites on a symmetric board
    score_p1 = evaluate_board(1, STARTING_BOARD)
    score_p2 = evaluate_board(2, STARTING_BOARD)
    self.assertEqual(score_p1, -score_p2)


class TestGetDepth(unittest.TestCase):
  def test_returns_highest_depth_for_max_time(self):
    depth = get_depth(15000)
    self.assertEqual(depth, DEPTH_THRESHOLDS[0][1])

  def test_returns_lower_depth_for_short_time(self):
    depth_long = get_depth(15000)
    depth_short = get_depth(500)
    self.assertGreater(depth_long, depth_short)

  def test_minimum_depth_for_zero_time(self):
    self.assertEqual(get_depth(0), DEPTH_THRESHOLDS[-1][1])


class TestGetMove(unittest.TestCase):
  def test_returns_a_list(self):
    move = get_move(1, STARTING_BOARD, 15000)
    self.assertIsInstance(move, list)
    self.assertEqual(len(move), 2)

  def test_move_is_on_empty_cell(self):
    move = get_move(1, STARTING_BOARD, 15000)
    self.assertEqual(STARTING_BOARD[move[0]][move[1]], 0)

  def test_returns_none_when_no_valid_moves(self):
    self.assertIsNone(get_move(1, NO_MOVES_BOARD, 15000))

  def test_takes_corner_when_available(self):
    # [0,0] is the only valid move and it's a corner — bot must take it
    move = get_move(1, CORNER_AVAILABLE_BOARD, 15000)
    self.assertEqual(move, [0, 0])


class TestPrepareResponse(unittest.TestCase):
  def test_returns_correct_bytes(self):
    self.assertEqual(prepare_response([2, 3]), b'[2, 3]\n')

  def test_response_ends_with_newline(self):
    self.assertTrue(prepare_response([0, 0]).endswith(b'\n'))


if __name__ == '__main__':
  unittest.main()
