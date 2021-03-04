# Auto-Chess
A chess bot that automatically calculates the best moves and plays them for you

## Installation
First, just install all the required libaries by doing `pip install -r requirements.txt`
 
You also need to install a chess engine. I recommend stockfish 13. You can download it here: https://stockfishchess.org/download/
After which you need to add the right path to the exe in the Auto-Chess.py file.

After that you can run the script with `python Auto-Chess.py`

## Usage
All you have to do is have a chess board ready when you excecute the script that is fully visible.
Say the side you are playing as and hit enter. The bot will start playing automatically for you and listening for new moves
made by the opponent. You don't have to do anything!

You can play around with the settings in Auto-Chess.py
You can set the thinking time, the wait time between screenshots and even the delay between mouse presses!

The bot has been tested on chess.com and lichess.org but should work on pretty much any chess site with a few tweaks!

## Troubleshooting
If the bot is not detecting the board,
on chess.com try changing the board sceme to brown and the pieces to classical in the settings.
Also i found that changing the board size very slightly smaller made it detect it way better however
the result may differ on different screen resolutions so i recommend trying out different board sizes and seeing
which works best for you.

The A.I was trained on lichess so play there for optimal results, but it should work fine on chess.com with a few tweaks!
