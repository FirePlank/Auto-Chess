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
from pyclick import HumanClicker
import pytweening
from pyclick.humancurve import HumanCurve

nums = {1:"a", 2:"b", 3:"c", 4:"d", 5:"e", 6:"f", 7:"g", 8:"h"}
def get_uci(board1, board2, who_moved):
    str_board = str(board1).split("\n")
    str_board2 = str(board2).split("\n")
    move = ""
    moved_piece = ""
    flip = False
    leave = False
    if who_moved == "w":
        for i in range(8)[::-1]:
            for x in range(15)[::-1]:
                if str_board[i][x] != str_board2[i][x]:
                    if moved_piece != "" and (str_board[i][x] != moved_piece and str_board2[i][x] != moved_piece):
                        continue
                    if str_board[i][x] == "." and move == "":
                        flip = True
                    moved_piece = str_board2[i][x]if str_board[i][x] == "."else str_board[i][x]
                    move+=str(nums.get(round(x/2)+1))+str(9-(i+1))
                    if len(move) == 4:
                        leave = True
                        break
            if leave:
                break
    else:
        for i in range(8):
            for x in range(15):
                if str_board[i][x] != str_board2[i][x]:
                    if moved_piece != "" and (str_board[i][x] != moved_piece and str_board2[i][x] != moved_piece):
                        continue
                    if str_board[i][x] == "." and move == "":
                        flip = True
                    moved_piece = str_board2[i][x] if str_board[i][x] == "." else str_board[i][x]
                    move += str(nums.get(round(x / 2) + 1)) + str(9 - (i + 1))
                    if len(move) == 4:
                        leave = True
                        break
            if leave:
                break
    if flip:
        move = move[2]+move[3]+move[0]+move[1]
    return move

wait_interval = 0.3 # The wait time between taking screenshots and retrying commands
engine_path = r"Engine Path" # The absolute path to the engine executable
engine = chess.engine.SimpleEngine.popen_uci(engine_path)
engine_think_time = 1 # <----- The higher this value is the better the engine plays, but also the slower it plays

os.chdir('chesstenso')
while 1:
    legit = input("Do you want legit mode? (y/n): ")
    if legit!="y" and legit!="n":
        print("Please type y or n.")
        continue
    break
while 1:
    who = input("Are you playing as white or black?: ")
    if who == "white":
        who = "w"
        other = "b"
        flip = False
        prev_fen = "IDEK"
    elif who == "black":
        who = "b"
        other = "w"
        flip = True
        prev_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    else:
        print("Invalid option given (white/black), please try again.")
        continue
    break

invalid = 0
board = chess.Board()
first_move = True
while True:
    image = pyscreenshot.grab()
    image.save("board.png")
    try:
        result = tensorflow_chessbot.main(img='board.png', active=who, unflip=flip)
        accuracy = result[1]
    except:
        time.sleep(wait_interval)
        continue
    if str(result[0]).split(" ")[0] == prev_fen:
        time.sleep(wait_interval)
        continue

    board1 = chess.Board(result[0])
    if not board1.is_valid():
        if invalid >= 10:
            print(f"Unable to detect a valid board position... Detected board position with {round(accuracy, 2)}% confidence was:")
            print(board1)
            break
        print("Invalid board position detected, retrying...")
        invalid+=1
        time.sleep(wait_interval)
        continue
    invalid = 0

    if not first_move:
        try:
            move_made = get_uci(board, board1, other)
            print("Detected move was: " + move_made)
            board.push_uci(move_made)
            if str(board) != str(board1):
                board = chess.Board(result[0])
        except:
            board = chess.Board(result[0])
    else:
        first_move = False
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
    print(f"Detected board position with {round(accuracy, 2)}% confidence:")
    print(board)
    print("Playing Move: " + str(result.move))
    print()
    move = result.move
    try:
        board.push(result.move)
        prev_fen = str(board.fen().split(" ")[0])
    except:
        print("Looks like I got checkmated, how is that even possible?")
        break

    board_pos = chessboard_finder.main(url=os.path.abspath('board.png'))

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


    if legit == "y":
        time.sleep(random.randint(1,35)/10)
        hc = HumanClicker()
        curve = HumanCurve(pyautogui.position(), (round(board_pos[0] + (square_mar_wi * x_square1) - square_mar_wi / 2)-random.randint(-13,13),
                    round(board_pos[1] + (square_mar_he * y_square1) - square_mar_he / 2)-random.randint(-13,13)), distortionFrequency=0, tweening=pytweening.easeInOutQuad,
                           offsetBoundaryY=8, offsetBoundaryX=8, targetPoints=random.randint(30,40))
        hc.move((round(board_pos[0] + (square_mar_wi * x_square1) - square_mar_wi / 2),
                    round(board_pos[1] + (square_mar_he * y_square1) - square_mar_he / 2)), duration=0.1, humanCurve=curve)
        pyautogui.click()
        curve = HumanCurve(pyautogui.position(), (round(board_pos[0] + (square_mar_wi * x_square2) - square_mar_wi / 2)-random.randint(-5,5),
                 round(board_pos[1] + (square_mar_he * y_square2) - square_mar_he / 2)-random.randint(-10,10)),
                           distortionFrequency=0, tweening=pytweening.easeInOutQuad,
                           offsetBoundaryY=8, offsetBoundaryX=8, targetPoints=random.randint(30,40))
        hc.move((round(board_pos[0] + (square_mar_wi * x_square2) - square_mar_wi / 2),
                 round(board_pos[1] + (square_mar_he * y_square2) - square_mar_he / 2)), duration=0.1, humanCurve = curve)
        pyautogui.click()
    else:
        pyautogui.click(round(board_pos[0] + (square_mar_wi * x_square1) - square_mar_wi / 2),
                    round(board_pos[1] + (square_mar_he * y_square1) - square_mar_he / 2))
        pyautogui.click(round(board_pos[0] + (square_mar_wi * x_square2) - square_mar_wi / 2),
                    round(board_pos[1] + (square_mar_he * y_square2) - square_mar_he / 2))

    try:
        if str(move)[4] == "q":
            pyautogui.click()
        elif str(move)[4] == "n":
            if legit=="y":
                curve = HumanCurve(pyautogui.position(),
                                   (round(board_pos[0] + (square_mar_wi * x_square2) - square_mar_wi / 2)-random.randint(-7,7),
                    round(board_pos[1] + (square_mar_he * (y_square2+1)) - square_mar_he / 2)-random.randint(-7,7)),
                                   distortionFrequency=0, tweening=pytweening.easeInOutQuad,
                                   offsetBoundaryY=8, offsetBoundaryX=8, targetPoints=random.randint(30,40))
                hc.move((round(board_pos[0] + (square_mar_wi * x_square2) - square_mar_wi / 2),
                    round(board_pos[1] + (square_mar_he * (y_square2+1)) - square_mar_he / 2)), duration=0.1,
                        humanCurve=curve)
                pyautogui.click()
            else:
                pyautogui.click(round(board_pos[0] + (square_mar_wi * x_square2) - square_mar_wi / 2),
                        round(board_pos[1] + (square_mar_he * (y_square2+1)) - square_mar_he / 2))
        elif str(move)[4] == "r":
            if legit == "y":
                curve = HumanCurve(pyautogui.position(),
                                   (round(board_pos[0] + (square_mar_wi * x_square2) - square_mar_wi / 2)-random.randint(-7,7),
                                    round(board_pos[1] + (square_mar_he * (y_square2 + 2)) - square_mar_he / 2)-random.randint(-7,7)),
                                   distortionFrequency=0, tweening=pytweening.easeInOutQuad,
                                   offsetBoundaryY=8, offsetBoundaryX=8, targetPoints=random.randint(30,40))
                hc.move((round(board_pos[0] + (square_mar_wi * x_square2) - square_mar_wi / 2),
                         round(board_pos[1] + (square_mar_he * (y_square2 + 2)) - square_mar_he / 2)), duration=0.1,
                        humanCurve=curve)
                pyautogui.click()
            else:
                pyautogui.click(round(board_pos[0] + (square_mar_wi * x_square2) - square_mar_wi / 2),
                                round(board_pos[1] + (square_mar_he * (y_square2 + 2)) - square_mar_he / 2))
        elif str(move)[4] == "b":
            if legit == "y":
                curve = HumanCurve(pyautogui.position(),
                                   (round(board_pos[0] + (square_mar_wi * x_square2) - square_mar_wi / 2)-random.randint(-7,7),
                                    round(board_pos[1] + (square_mar_he * (y_square2 + 3)) - square_mar_he / 2)-random.randint(-7,7)),
                                   distortionFrequency=0, tweening=pytweening.easeInOutQuad,
                                   offsetBoundaryY=8, offsetBoundaryX=8, targetPoints=random.randint(30,40))
                hc.move((round(board_pos[0] + (square_mar_wi * x_square2) - square_mar_wi / 2),
                         round(board_pos[1] + (square_mar_he * (y_square2 + 3)) - square_mar_he / 2)), duration=0.1,
                        humanCurve=curve)
                pyautogui.click()
            else:
                pyautogui.click(round(board_pos[0] + (square_mar_wi * x_square2) - square_mar_wi / 2),
                                round(board_pos[1] + (square_mar_he * (y_square2 + 3)) - square_mar_he / 2))
    except:
        pass


    if board.is_game_over():
        print("Looks like I won again!")
        break
