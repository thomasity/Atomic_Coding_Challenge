import unittest
import client

# Standard starting board
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

class TestGetScoreFromTile(unittest.TestCase):
  def test_valid_move_flips_one_piece(self):
    # Placing at [5,3] as player 1 flips the opponent at [3,3]
    score = client.get_score_from_tile(5, 3, 1, STARTING_BOARD)
    self.assertEqual(score, 1)

  def test_invalid_move_scores_zero(self):
    # Placing at [0,0] flips nothing
    score = client.get_score_from_tile(0, 0, 1, STARTING_BOARD)
    self.assertEqual(score, 0)

  def test_occupied_cell_scores_zero(self):
    # [3,3] is already occupied by player 1
    score = client.get_score_from_tile(3, 3, 2, STARTING_BOARD)
    self.assertEqual(score, 0)

  def test_player_two_valid_move(self):
    # Placing at [5,4] as player 2 flips the opponent at [3,4]
    score = client.get_score_from_tile(5, 4, 2, STARTING_BOARD)
    self.assertEqual(score, 1)

class TestGetMove(unittest.TestCase):
  def test_returns_a_valid_move(self):
    board = [
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 1, 0, 0, 0],
      [0, 0, 0, 1, 1, 0, 0, 0],
      [0, 0, 0, 2, 1, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
    ]
    self.assertTrue((client.get_move(1, board) == [4, 2]) or (client.get_move(1, board) == [5, 2]))

  def test_returns_none_when_no_valid_moves(self):
    # Board where player 1 has no valid moves (all cells filled except one with no flanking)
    board = [
      [1, 1, 1, 1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1, 1, 1, 0],
    ]
    self.assertIsNone(client.get_move(1, board))

  def test_returns_a_list(self):
    move = client.get_move(1, STARTING_BOARD)
    self.assertIsInstance(move, list)
    self.assertEqual(len(move), 2)

  def test_move_is_on_empty_cell(self):
    move = client.get_move(1, STARTING_BOARD)
    self.assertEqual(STARTING_BOARD[move[0]][move[1]], 0)

class TestPrepareResponse(unittest.TestCase):
  def test_prepare_response_returns_a_valid_response(self):
    self.assertEqual(client.prepare_response([2, 3]), b'[2, 3]\n')

  def test_response_ends_with_newline(self):
    response = client.prepare_response([0, 0])
    self.assertTrue(response.endswith(b'\n'))

if __name__ == '__main__':
  unittest.main()
