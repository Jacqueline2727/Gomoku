def get_size(board):
  cols = 0
  rows = 0
  for element in board:
    cols += 1
    for row in element:
      rows += 1
  return rows, cols


def is_full(board):
  for i in range(len(board)):
    for j in range(len(board[0])):
      if board[i][j] == ' ':
        return False
  return True


def is_empty(board):
  for i in range(len(board)):
    for j in range(len(board[0])):
      if board[i][j] != ' ':
        return False
  return True

def is_bounded(board, y_end, x_end, length, d_y, d_x):
  check = board[y_end][x_end]
  opp = ' '
  if check == 'b':
    opp = 'w'
  else:
    opp = 'b'
  size = len(board) - 1
  end_open = True
  start_open = True

  if y_end+d_y>size or x_end+d_x>size:
    end_open = False
  elif y_end+d_y<0 or x_end+d_x<0:
    end_open = False
  else:
    if board[y_end+d_y][x_end+d_x]==opp:
      end_open=False

  change_y=d_y*length
  change_x=d_x*length
  if y_end-change_y<0 or x_end-change_x<0:
    start_open = False
  elif y_end-change_y>size or x_end-change_x>size:
    start_open = False
  else:
      if board[y_end-change_y][x_end-change_x]==opp:
          start_open=False
  if end_open and start_open:
    return "OPEN"
  elif end_open or start_open:
    return "SEMIOPEN"
  else:
    return "CLOSED"




def detect_row(board, col, y_start, x_start, length, d_y, d_x):
  open_seq_count = 0
  semi_open_seq_count = 0
  num = 0
  start_open = True
  end_open = True
  #Start from opposite side start at the edge
  if d_y ==1 and d_x==1 and (y_start==len(board)-1 or x_start==len(board)):
    pass
  else:
    if y_start == len(board) - 1:
      d_y *= -1
    if x_start == len(board) - 1:
      d_x *= -1

  if col == 'w':
    opposite = 'b'
  else:
    opposite = 'w'

  j, i = y_start, x_start
  n = len(board)
  count = 0
  while i < n and j < n and i > -1 and j > -1:
    current = board[j][i]
    if current == col:
      count += 1
      if j == y_start and i == x_start:
        start_open = False
      elif board[j - d_y][i - d_x] == opposite:
        start_open = False
      elif board[j - d_y][i - d_x] == ' ':
        start_open = True
      elif j == n - 1 and d_y!=0:
        end_open = False
      elif i==n-1 and d_x!=0:
        end_open=False
      elif board[j + d_y][i + d_x] == opposite:
        end_open = False
      elif board[j + d_y][i + d_x] == ' ':
        end_open = True
      if count == length:
        valid = True
        if j < n - 1 and i < n - 1:
          if board[j + d_y][i + d_x] == col:
            valid = False
        if i > 0 and j > 0:
          if j-length<0 or i-length<0:
            pass
          elif board[j - length][i - length] == col:
            valid = False
        if valid:
          if not end_open and start_open:
            semi_open_seq_count += 1
          elif not start_open and end_open:
            semi_open_seq_count += 1
          elif end_open and start_open:
            open_seq_count += 1
          start_open = True
          end_open = True
          count = 0
    else:
      count = 0
    j += d_y
    i += d_x

  return open_seq_count, semi_open_seq_count


def detect_closed_row(board, col, y_start, x_start, length, d_y, d_x):
  closed_count = 0
  num = 0
  if y_start == len(board) - 1 or x_start == len(board[0]) - 1:
    d_y *= -1
    d_x *= -1

  if col == 'w':
    opposite = 'b'
  else:
    opposite = 'w'

  start_open = True
  end_open = True
  j, i = y_start, x_start
  n = len(board)
  count = 0
  while i < n and j < n and i > -1 and j > -1:
    current = board[j][i]
    if current == col:
      count += 1
      if j == y_start and i == x_start:
        start_open = False
      elif board[j - d_y][i - d_x] == opposite:
        start_open = False
      elif board[j - d_y][i - d_x] == ' ':
        start_open = True
      elif j == n - 1 or i == n - 1:
        end_open = False
      elif board[j + d_y][i + d_x] == opposite:
        end_open = False
      elif board[j + d_y][i + d_x] == ' ':
        end_open = True
      if count == length:
        if not end_open and not start_open:
          closed_count += 1
          start_open = True
          end_open = True
          count = 0
    else:
      count = 0
    j += d_y
    i += d_x

  return closed_count


def detect_rows(board, col, length):
  open_seq_count, semi_open_seq_count = 0, 0
  open, semi = 0, 0
  for i in range(len(board)):
    open, semi = detect_row(board, col, i, 0, length, 0, 1)
    open_seq_count += open
    semi_open_seq_count += semi
    open, semi = detect_row(board, col, i, 0, length, 1, 1)
    open_seq_count += open
    semi_open_seq_count += semi
  for a in range(len(board)):
    open, semi = detect_row(board, col, 0, a, length, 1, 0)
    open_seq_count += open
    semi_open_seq_count += semi
    if (a != 0):
      open, semi = detect_row(board, col, 0, a, length, 1, 1)
      open_seq_count += open
      semi_open_seq_count += semi
  for j in range(len(board)):
    open, semi = detect_row(board, col, 0, j, length, 1, -1)
    open_seq_count += open
    semi_open_seq_count += semi
    if j != 0 and j != 7:
      open, semi = detect_row(board, col, j, 7, length, 1, 1)
      open_seq_count += open
      semi_open_seq_count += semi
  return open_seq_count, semi_open_seq_count


def detect_closed_rows(board, col, length):
  num_closed = 0
  for i in range(len(board)):
    close = detect_closed_row(board, col, i, 0, length, 0, 1)
    num_closed += close
    close = detect_closed_row(board, col, i, 0, length, 1, 1)
    num_closed += close
  for a in range(len(board)):
    close = detect_closed_row(board, col, 0, a, length, 1, 0)
    num_closed += close
    if (a != 0):
      close = detect_closed_row(board, col, 0, a, length, 1, 1)
      num_closed += close
  for j in range(len(board)):
    close = detect_closed_row(board, col, 0, j, length, 1, -1)
    num_closed += close
    if j != 0:
      close = detect_closed_row(board, col, j, 7, length, 1, 1)
      num_closed += close
  return num_closed


def search_max(board):
  empty = get_empty(board)
  move_y, move_x = 0, 0
  max_score = 0
  for i in range(0, len(empty), 2):
    col = empty[i]
    row = empty[i + 1]
    original = board[col][row]
    test = board.copy()
    test[col][row] = 'b'
    test_score = score(test)
    test[col][row] = original

    if detect_closed_rows(board, 'b', 5) > 1:
      return col, row

    if test_score == 100000:
      return col, row

    if test_score > max_score:
      move_y = col
      move_x = row
      max_score = test_score
  return move_y, move_x


def get_empty(board):
  empty = []
  for i in range(len(board)):
    for a in range(len(board)):
      if board[i][a] == ' ':
        empty.append(i)
        empty.append(a)
  return empty


def score(board):
  MAX_SCORE = 100000

  open_b = {}
  semi_open_b = {}
  open_w = {}
  semi_open_w = {}

  for i in range(2, 6):
    open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
    open_w[i], semi_open_w[i] = detect_rows(board, "w", i)

  if open_b[5] >= 1 or semi_open_b[5] >= 1:
    return MAX_SCORE

  elif open_w[5] >= 1 or semi_open_w[5] >= 1:
    return -MAX_SCORE

  return (-10000 * (open_w[4] + semi_open_w[4]) + 500 * open_b[4] +
          50 * semi_open_b[4] + -100 * open_w[3] + -30 * semi_open_w[3] +
          50 * open_b[3] + 10 * semi_open_b[3] + open_b[2] + semi_open_b[2] -
          open_w[2] - semi_open_w[2])


def is_win(board):
  if is_full(board) == True:
    return "Draw"
  else:
    closed_b = detect_closed_rows(board, 'b', 5)
    closed_w = detect_closed_rows(board, 'w', 5)
    if closed_b >= 1:
      return "Black won"
    elif closed_w >= 1:
      return "White won"
    else:
      if score(board) == 100000:
        return "Black won"
      elif score(board) == -100000:
        return "White won"
  return "Continue playing"


def print_board(board):

  s = "*"
  for i in range(len(board[0]) - 1):
    s += str(i % 10) + "|"
  s += str((len(board[0]) - 1) % 10)
  s += "*\n"

  for i in range(len(board)):
    s += str(i % 10)
    for j in range(len(board[0]) - 1):
      s += str(board[i][j]) + "|"
    s += str(board[i][len(board[0]) - 1])

    s += "*\n"
  s += (len(board[0]) * 2 + 1) * "*"

  print(s)


def make_empty_board(sz):
  board = []
  for i in range(sz):
    board.append([" "] * sz)
  return board


def analysis(board):
  for c, full_name in [["b", "Black"], ["w", "White"]]:
    print("%s stones" % (full_name))
    for i in range(2, 6):
      open, semi_open = detect_rows(board, c, i)
      print("Open rows of length %d: %d" % (i, open))
      print("Semi-open rows of length %d: %d" % (i, semi_open))


def play_gomoku(board_size):
  board = make_empty_board(board_size)
  board_height = len(board)
  board_width = len(board[0])

  while True:
    print_board(board)
    if is_empty(board):
      move_y = board_height // 2
      move_x = board_width // 2
    else:
      move_y, move_x = search_max(board)

    print("Computer move: (%d, %d)" % (move_y, move_x))
    board[move_y][move_x] = "b"
    print_board(board)
    analysis(board)

    game_res = is_win(board)
    if game_res in ["White won", "Black won", "Draw"]:
      return game_res

    print("Your move:")
    move_y = int(input("y coord: "))
    move_x = int(input("x coord: "))
    board[move_y][move_x] = "w"
    print_board(board)
    analysis(board)

    game_res = is_win(board)
    print(game_res)
    if game_res in ["White won", "Black won", "Draw"]:
      return game_res


def put_seq_on_board(board, y, x, d_y, d_x, length, col):
  for i in range(length):
    board[y][x] = col
    y += d_y
    x += d_x


def test_is_empty():
  board = make_empty_board(8)
  if is_empty(board):
    print("TEST CASE for is_empty PASSED")
  else:
    print("TEST CASE for is_empty FAILED")


def test_is_bounded():
  board = make_empty_board(8)
  x = 5
  y = 1
  d_x = 0
  d_y = 1
  length = 3
  put_seq_on_board(board, y, x, d_y, d_x, length, "w")
  print_board(board)

  y_end = 3
  x_end = 5

  if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
    print("TEST CASE for is_bounded PASSED")
  else:
    print("TEST CASE for is_bounded FAILED")


def test_detect_row():
  board = make_empty_board(8)
  x = 5
  y = 1
  d_x = 0
  d_y = 1
  length = 3
  put_seq_on_board(board, y, x, d_y, d_x, length, "w")
  print_board(board)
  if detect_row(board, "w", 0, x, length, d_y, d_x) == (1, 0):
    print("TEST CASE for detect_row PASSED")
  else:
    print("TEST CASE for detect_row FAILED")


def test_detect_rows():
  board = make_empty_board(8)
  x = 5
  y = 1
  d_x = 0
  d_y = 1
  length = 3
  col = 'w'
  put_seq_on_board(board, y, x, d_y, d_x, length, "w")
  print_board(board)
  if detect_rows(board, col, length) == (1, 0):
    print("TEST CASE for detect_rows PASSED")
  else:
    print("TEST CASE for detect_rows FAILED")


def test_search_max():
  board = make_empty_board(8)
  x = 5
  y = 0
  d_x = 0
  d_y = 1
  length = 4
  col = 'w'
  put_seq_on_board(board, y, x, d_y, d_x, length, col)
  x = 6
  y = 0
  d_x = 0
  d_y = 1
  length = 4
  col = 'b'
  put_seq_on_board(board, y, x, d_y, d_x, length, col)
  if search_max(board) == (4, 6):
    print("TEST CASE for search_max PASSED")
  else:
    print("TEST CASE for search_max FAILED")


def easy_testset_for_main_functions():
  test_is_empty()
  test_is_bounded()
  test_detect_row()
  test_detect_rows()
  test_search_max()


def some_tests():
  board = make_empty_board(8)

  board[0][5] = "w"
  board[0][6] = "b"
  y = 5
  x = 2
  d_x = 0
  d_y = 1
  length = 3
  put_seq_on_board(board, y, x, d_y, d_x, length, "w")
  print_board(board)
  analysis(board)


  y = 3
  x = 5
  d_x = -1
  d_y = 1
  length = 2

  put_seq_on_board(board, y, x, d_y, d_x, length, "b")
  print_board(board)
  analysis(board)


  y = 5
  x = 3
  d_x = -1
  d_y = 1
  length = 1
  put_seq_on_board(board, y, x, d_y, d_x, length, "b")
  print_board(board)
  analysis(board)


if __name__ == '__main__':
  play_gomoku(8)
