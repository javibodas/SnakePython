import os
import sys
sys.path.insert(1, './snake/')
from snake import main as snake
from easygui import msgbox, buttonbox

current_work_directory = ''
game_choices = ['Snake', 'Ninguno']
difficulty_choices = ["Easy", "Medium","Difficult","Pro"]

if __name__ == '__main__':
    current_work_directory = os.getcwd()

    msg = 'Which game do you want to play?'
    game = buttonbox(msg, choices=game_choices)
    msg = 'How are prepared to?'
    difficulty = buttonbox(msg, choices=difficulty_choices)

    if game == 'Snake':
        snake(difficulty)
