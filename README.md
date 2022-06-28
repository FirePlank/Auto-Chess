# Auto-Chess
A chess bot that automatically calculates the best moves and plays them for you

## Installation
First, just install all the required libaries by doing `pip install -r requirements.txt`
 
You also need to install a chess engine. I recommend stockfish 13. You can download it here: https://stockfishchess.org/download/
After which you need to add the right path to the exe in the Auto-Chess.py file.
edit line no 58 and change it to something like `engine_path = r"D:\chess\stockfish\stockfish.exe"` path to your stockfish exe file

After that you can run the script with `python Auto-Chess.py`

## Usage
All you have to do is have a chess board ready when you excecute the script that is fully visible.
Say the side you are playing as and hit enter. The bot will start playing automatically for you and listening for new moves
made by the opponent. You don't have to do anything!

You can play around with the settings in Auto-Chess.py
You can set the thinking time, the wait time between screenshots!

There is also a legit mode that you can use to hide the fact that you are botting and maybe bybass some bot detection softwares.
It will move the mouse to the pieces in a human like way and it won't click on the very center of the piece but a little on the side
and it also will wait random intervals and move the mouse at random speeds.

The bot has been tested on chess.com and lichess.org but should work on pretty much any chess site with a few tweaks!

## Showcase
I made a little video showcasing the bot which can be viewed on my google drive here: 
https://drive.google.com/file/d/1XvPG42slB2txM0sW6VHnB4g4HXXF496n/view?usp=sharing

The video is quite outdated and the bot has been redifined a lot since then so please take a look at the bot yourself!

## Troubleshooting
If the bot is not detecting the board,
on chess.com try changing the board sceme to brown and the pieces to classical in the settings.
Also i found that changing the board size very slightly smaller made it detect it way better however
the result may differ on different screen resolutions so I recommend trying out different board sizes and seeing
which works best for you.

If the bot is detecting the wrong position or saying invalid position,
disable piece animations cuz I have had the screenshots be taken mid animation making the piece appear to be in a different square.
Also disable highlight last move cuz that has thrown off the bot as well.

The A.I was trained on lichess so play there for optimal results, but it should work fine on chess.com and other chess sites with a few tweaks!

## Disclaimer
This is meant only for educational purposes and I will not be responsible for what happens if you use this script to cheat.

This was not meant to be used as cheating. You can already freely do so without this script. This was just so I can see how machine learning works and how I can implement it. I saw this as a really cool idea to have a script do something automatically. I've always liked these kinds of automation projects. This was not meant to be used as a cheating tool.

## Credits
I have not made the actual detection of the chess board. That has been taken from Elucidation's
Github that can be found here: https://github.com/Elucidation/tensorflow_chessbot

I did however modify the files to suit my needs better.
