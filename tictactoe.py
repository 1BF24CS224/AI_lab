board = [' '] * 9

def display():
    print(f"\n {board[0]} | {board[1]} | {board[2]}")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]}")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]}\n")

def winner(p):
    wins = [(0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)]
    return any(board[a] == board[b] == board[c] == p for a,b,c in wins)

def computer():
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            if winner('O'): return
            board[i] = ' '

    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X'
            if winner('X'):
                board[i] = 'O'
                return
            board[i] = ' '

    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            return

print("TIC-TAC-TOE")
print("You = X | Computer = O")

while True:
    display()
    try:
        pos = int(input("Enter position (1-9): ")) - 1
        if pos not in range(9) or board[pos] != ' ':
            print("Invalid position!")
            continue
    except ValueError:
        print("Enter a number!")
        continue

    board[pos] = 'X'

    if winner('X'):
        display()
        print("You Win!")
        break

    if ' ' not in board:
        display()
        print("Draw!")
        break

    computer()

    if winner('O'):
        display()
        print("Computer Wins!")
        break

    if ' ' not in board:
        display()
        print("Draw!")
        break