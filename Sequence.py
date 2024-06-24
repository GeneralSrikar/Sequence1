import random
import pandas as pd


def generate():
    suits = ['H', 'D', 'S', 'C' ]
    cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Q', 'K', 'A']
    deck = [f'{card}{suit}' for suit in suits for card in cards]
    return deck + deck


def distribute(players, num):
    deck = generate()
    random.shuffle(deck)
    hands = []
    for x in range(players):
        hand = []
        for i in range(num):
            hand.append(deck.pop())
        hands.append(hand)
    return hands


def status_board():
    return [[0 for _ in range(10)] for _ in range(10)]


def place_marker(board, row, col, marker):
    board[row][col] = marker
    return board


def check_start(board, seq_status, i, j, team):
    count = 0
    board[0][0] = team
    board[0][9] = team
    board[9][0] = team
    board[9][9] = team
    if j <= 5:
        if "H" not in seq_status[i][j] and board[i][j:j + 5] == [team] * 5:
            count += 1
            for k in range(5):
                seq_status[i][j+k].append("H")
    if j <= 5 and i <= 5:
        if "DR" not in seq_status[i][j] and [board[i + k][j + k] for k in range(5)] == [team] * 5:
            count += 1
            for k in range(5):
                seq_status[i + k][j + k].append("DR")
    if i <= 5:
        if "D" not in seq_status[i][j] and [board[i + k][j] for k in range(5)] == [team] * 5:
            count += 1
            for k in range(5):
                seq_status[i + k][j].append("D")
    if j >= 4 and i <= 5:
        if "DL" not in seq_status[i][j] and [board[i + k][j - k] for k in range(5)] == [team] * 5:
            count += 1
            for k in range(5):
                seq_status[i + k][j - k].append("DL")
    return count, seq_status


def check_seq(board):
    seq1 = 0
    seq2 = 0
    seq_status = [[[] for _ in range(10)] for _ in range(10)]
    for i in range(10):
        for j in range(10):
            if board[i][j] == 1:
                temp, seq_status = check_start(board, seq_status, i, j, 1)
                seq1 += temp
            elif board[i][j] == 2:
                temp, seq_status = check_start(board, seq_status, i, j, 2)
                seq2 += temp
    return seq1, seq2


def generate_board(board, x, y, suit, direction, rotation):
    old_arr = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Q', 'K', 'A']
    arr = [old_arr[11 - i] for i in range(12)]
    for num in arr:
        board[x][y] = num + suit
        if direction == "Up":
            x -= 1
            if (x, y) in [(0, 0), (0, 9), (9, 0), (9, 9)] or board[x][y] != "":
                if board[x][y] != "":
                    x += 1
                if rotation == "Counterclockwise":
                    direction = "Left"
                    y -= 1
                    if board[x][y] != "":
                        x += 1
                else:
                    direction = "Right"
                    y += 1
                    if board[x][y] != "":
                        x += 1
            elif x in [0, 9]:
                if rotation == "Counterclockwise":
                    direction = "Left"
                else:
                    direction = "Right"
        elif direction == "Down":
            x += 1
            if (x, y) in [(0, 0), (0, 9), (9, 0), (9, 9)] or board[x][y] != "":
                if board[x][y] != "":
                    x -= 1
                if rotation == "Counterclockwise":
                    direction = "Right"
                    y += 1
                    if board[x][y] != "":
                        x -= 1
                else:
                    direction = "Left"
                    y -= 1
                    if board[x][y] != "":
                        x -= 1
            elif x in [0, 9]:
                if rotation == "Counterclockwise":
                    direction = "Right"
                else:
                    direction = "Left"
        elif direction == "Left":
            y -= 1
            if (x, y) in [(0, 0), (0, 9), (9, 0), (9, 9)] or board[x][y] != "":
                if board[x][y] != "":
                    y += 1
                if rotation == "Counterclockwise":
                    direction = "Down"
                    x += 1
                else:
                    direction = "Up"
                    x -= 1
            elif y in [0, 9]:
                if rotation == "Counterclockwise":
                    direction = "Down"
                else:
                    direction = "Up"
        elif direction == "Right":
            y += 1
            if (x, y) in [(0, 0), (0, 9), (9, 0), (9, 9)] or board[x][y] != "":
                if board[x][y] != "":
                    y -= 1
                if rotation == "Counterclockwise":
                    direction = "Up"
                    x -= 1
                else:
                    direction = "Down"
                    x += 1
            elif y in [0, 9]:
                if rotation == "Counterclockwise":
                    direction = "Up"
                else:
                    direction = "Down"
    return board


def print_board(board):
    for row in board:
        print(' '.join(row))

def find_card(card, board, status):
    for i in range(10):
        for j in range(10):
            if board[i][j] == card and status[i][j] == 0:
                return i,j

def init_game():
    board = generate_board([[''] * 10 for _ in range(10)], 9, 1, 'D', 'Right', 'Counterclockwise')
    board = generate_board(board, 4, 9, 'S', 'Up', 'Counterclockwise')
    board = generate_board(board, 8, 0, 'C', 'Up', 'Clockwise')
    board = generate_board(board, 2, 1, 'S', "Down", "Counterclockwise")
    board = generate_board(board, 1, 5, 'H', "Right", "Clockwise")
    board = generate_board(board, 7, 6, 'D', "Right", "Counterclockwise")
    board = generate_board(board, 7, 5, 'C', "Left", "Clockwise")
    board = generate_board(board, 4, 6, 'H', "Down", "Clockwise")
    # print(pd.DataFrame(board))
    cards = generate()
    status = status_board()
    status = place_marker(status, 0, 0, 3)
    status = place_marker(status, 0, 9, 3)
    status = place_marker(status, 9, 0, 3)
    status = place_marker(status, 9, 9, 3)
    return board, cards, status

def choose_card(board, status, p1, p2, player):
    if player == 1:
        card = p1.pop()
    if player == 2:
        card = p2.pop()
    return card, p1, p2

def simulate_game():
    board, cards, status = init_game()
    random.shuffle(cards)
    seq1 = 0
    seq2 = 0
    player = 1
    player1 = []
    player2 = []
    for k in range(7):
        player1.append(cards.pop())
        player2.append(cards.pop())
    while seq1 < 3 and seq2 < 3:
        curr_card, player1, player2 = choose_card(board, status, player1, player2, player)
        if player == 1:
            player1.append(cards.pop())
        else:
            player2.append(cards.pop())
        x,y = find_card(curr_card, board, status)
        status = place_marker(status, x, y, player)
        seq1, seq2 = check_seq(status)
        player = 3 - player
        if len(cards) == 0:
            break
    return seq1, seq2

count1 = 0
count2 = 0
for i in range(1000):
    seq1, seq2 = simulate_game()
    if seq1 > seq2:
        count1 += 1
    elif seq2 > seq1:
        count2 += 1
    if i%100 == 0:
        print(i)

print(count1)
print(count2)