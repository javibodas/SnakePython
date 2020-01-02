import os
import sys
sys.path.insert(1, './snake/')
from snake import main as snake
from easygui import buttonbox

current_work_directory = ''
difficulty_choices = ["Easy", "Medium","Difficult","Pro"]

if __name__ == '__main__':
    current_work_directory = os.getcwd()

    msg = 'WHich difficulty you want?'
    difficulty = 'Easy'
    difficulty = buttonbox(msg, choices=difficulty_choices)

    exit(snake(difficulty))
