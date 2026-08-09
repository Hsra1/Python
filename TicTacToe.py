from tkinter import Tk, Canvas
from random import randrange


class boards:
    def __init__(self, board):
        self.board = board

    def __getitem__(self, key):
        key -= 1
        x = int(key // 3)
        y = int(key % 3)
        return self.board[x][y]

    def __setitem__(self, key, value):
        key -= 1
        x = int(key // 3)
        y = int(key % 3)
        self.board[x][y] = value


def bot():
    move = logic()
    if move:
        if not game[move]:
            game[move] = "O"
    else:
        move = randrange(1, 10)
        if not game[move]:
            game[move] = "O"
        else:
            bot()


def play(event):
    if win() and over():
        last = is_last()
        move = (event.x // sq * 3) + (event.y // sq) + 1
        if not game[move]:
            game[move] = "X"
            if win() and last:
                bot()
        draw_board()

        if not (win() and over()):
            screen.delete("all")
            screen.create_text(
                side / 2, side / 2, text=winner, font=("Arial", 42), fill="#FF0000"
            )
            screen.create_text(
                side / 2,
                side / 2 + cen,
                text="Press Enter To Play Again",
                font=("Arial", 36),
                fill="#FF0000",
            )


def win():
    global winner
    con = [
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 9),
        (1, 4, 7),
        (2, 5, 8),
        (3, 6, 9),
        (1, 5, 9),
        (3, 5, 7),
    ]
    for a, b, c in con:
        if game[a] == game[b] == game[c] != "":
            winner = f"Player {game[a]} Wins"
            return False
    return True


def logic():
    con = [
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 9),
        (1, 4, 7),
        (2, 5, 8),
        (3, 6, 9),
        (1, 5, 9),
        (3, 5, 7),
    ]
    for a, b, c in con:
        if (
            game[a] == game[b] == "O"
            and game[c] == ""
        ):
            return c
        elif (
            game[a] == game[c] == "O"
            and game[b] == ""
        ):
            return b
        elif (
            game[b] == game[c] == "O"
            and game[a] == ""
        ):
            return a
    for a, b, c in con:
        if (
            game[a] == game[b] == "X"
            and game[c] == ""
        ):
            return c
        elif (
            game[a] == game[c] == "X"
            and game[b] == ""
        ):
            return b
        elif (
            game[b] == game[c] == "X"
            and game[a] != game[c]
            and game[a] == ""
        ):
            return a


def is_last():
    temp = [game[i] for i in range(1, 10)]
    if temp.count("") == 1:
        return False
    else:
        return True


def over():
    temp = [game[i] for i in range(1, 10)]
    if temp.count("") == 0:
        return False
    else:
        return True


def draw_board():
    global txt
    screen.delete("all")
    for i in range(1, 3):
        i *= sq
        screen.create_line(i, 0, i, side, width=10)
        screen.create_line(0, i, side, i, width=10)
    for x, i in enumerate(game.board):
        for y, j in enumerate(i):
            screen.create_text(x * sq + cen, y * sq + cen, text=j, font=("Arial", 16))


def clear(event):
    global game, winner
    screen.delete("all")
    game = boards([["", "", ""], ["", "", ""], ["", "", ""]])
    winner = "Draw"
    draw_board()


game = boards([["", "", ""], ["", "", ""], ["", "", ""]])
side = 732
sq = side / 3
cen = sq / 2
winner = "Draw"

root = Tk()
root.title("Tic Tac Toe")
root.geometry(f"{side}x{side}")

screen = Canvas(height=side, width=side, bg="#0000FF")
screen.pack()

screen.bind("<Button-1>", play)
root.bind("<Return>", clear)

draw_board()
root.mainloop()
