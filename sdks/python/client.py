#!/usr/bin/python

import sys
import json
import socket

def get_score_from_tile(row: int, col: int, player: int, board: list) -> int:
  opponent = 2 if player == 1 else 1
  directions = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
  total_flipped = 0

  for dr, dc in directions:
    r, c = row + dr, col + dc
    flipped = 0
    while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
      r += dr
      c += dc
      flipped += 1
    if flipped > 0 and 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
      total_flipped += flipped

  return total_flipped


def get_move(player, board) -> list | None:
  best_score = 0
  best_move = None

  for row in range(8):
    for col in range(8):
      if board[row][col] == 0:
        score = get_score_from_tile(row, col, player, board)
        if score > best_score:
          best_score = score
          best_move = [row, col]
  print(f"Best move for player {player}: {best_move} with score {best_score}")
  return best_move

def prepare_response(move):
  response = '{}\n'.format(move).encode()
  print('sending {!r}'.format(response))
  return response

if __name__ == "__main__":
  port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 1337
  host = sys.argv[2] if (len(sys.argv) > 2 and sys.argv[2]) else socket.gethostname()

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    sock.connect((host, port))
    while True:
      data = sock.recv(1024)
      if not data:
        print('connection to server closed')
        break
      json_data = json.loads(str(data.decode('UTF-8')))
      board = json_data['board']
      maxTurnTime = json_data['maxTurnTime']
      player = json_data['player']
      print(player, maxTurnTime, board)

      move = get_move(player, board)
      response = prepare_response(move)
      sock.sendall(response)
  finally:
    sock.close()
