import chess.engine
import chess.pgn
import os
import time
import asyncio
import pyautogui
import random
import pyscreenshot
from chesstenso import tensorflow_chessbot
from chesstenso import chessboard_finder

wait_interval = 1.5 # The wait time between taking screenshots
engine_path = r"C:\Users\FirePlank\Desktop\Coding\General Python Scripts\stockfish_13_win_x64_bmi2\stockfish_13_win_x64_bmi2.exe" # The absolute path to the engine executable
engine = chess.engine.SimpleEngine.popen_uci(engine_path)
engine_think_time = 0.2 # <----- The higher this value is the better the engine plays

os.chdir('chesstenso')
who = input("Are you playing as white or black?: ")
if who == "white":
    who = "w"
    flip = False
elif who == "black":
    who = "b"
    flip = True
else:
    quit("Invalid option given (white/black), please try again.")

prev_fen = "IDEK"
while True:
    image = pyscreenshot.grab()
    image.save("Photos/board.png")
    try:
        result = tensorflow_chessbot.main(img=r'Photos\board.png', active=who, unflip=flip)
    except:
        time.sleep(0.2)
        continue
    if str(result[0]).split(" ")[0] == prev_fen:
        time.sleep(wait_interval)
        continue

    board = chess.Board(result[0])
    while 1:
        try:
            result = engine.play(board, chess.engine.Limit(time=engine_think_time))
            break
        except asyncio.exceptions.TimeoutError:
            continue
        except chess.engine.EngineTerminatedError:
            engine = chess.engine.SimpleEngine.popen_uci(engine_path)
            continue

    print(board)
    print("Playing Move: " + str(result.move))
    move = result.move
    try:
        board.push(result.move)
        prev_fen = str(board.fen().split(" ")[0])
    except:
        print("Looks like we got checkmated! How is that even possible?")
        quit()
        break

    board_pos = chessboard_finder.main(url=os.path.abspath(r'Photos\board.png'))

    board_width = board_pos[2] - board_pos[0]
    board_height = board_pos[3] - board_pos[1]

    square_mar_wi = board_width / 8
    square_mar_he = board_height / 8

    if who == "b":
        x_square1 = 9 - (ord(str(move)[0]) - 96)
        y_square1 = int(str(move)[1])
        x_square2 = 9 - (ord(str(move)[2]) - 96)
        y_square2 = int(str(move)[3])
    else:
        x_square1 = ord(str(move)[0]) - 96
        y_square1 = 9 - int(str(move)[1])
        x_square2 = ord(str(move)[2]) - 96
        y_square2 = 9 - int(str(move)[3])

    pyautogui.click(round(board_pos[0] + (square_mar_wi * x_square1) - square_mar_wi / 2),
                    round(board_pos[1] + (square_mar_he * y_square1) - square_mar_he / 2))
    time.sleep(random.randint(1, 10) / 15) # Random sleep time between mouse clicks
    pyautogui.click(round(board_pos[0] + (square_mar_wi * x_square2) - square_mar_wi / 2),
                    round(board_pos[1] + (square_mar_he * y_square2) - square_mar_he / 2))

    try:
        if str(move)[4] == "q":
            pyautogui.click(round(board_pos[0] + (square_mar_wi * x_square2) - square_mar_wi / 2),
                    round(board_pos[1] + (square_mar_he * y_square2) - square_mar_he / 2))
        elif str(move)[4] == "n":
            pyautogui.click(round(board_pos[0] + (square_mar_wi * x_square2) - square_mar_wi / 2),
                    round(board_pos[1] + (square_mar_he * (y_square2+1)) - square_mar_he / 2))
        elif str(move)[4] == "r":
            pyautogui.click(round(board_pos[0] + (square_mar_wi * x_square2) - square_mar_wi / 2),
                        round(board_pos[1] + (square_mar_he * (y_square2 + 2)) - square_mar_he / 2))
        elif str(move)[4] == "b":
            pyautogui.click(round(board_pos[0] + (square_mar_wi * x_square2) - square_mar_wi / 2),
                    round(board_pos[1] + (square_mar_he * (y_square2 + 3)) - square_mar_he / 2))
    except:
        pass

    if board.is_game_over():
        print("Looks like we won again! Nice job!")
        quit()
        break
