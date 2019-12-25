# coding: utf-8
import sys
import score as scoremodule
from block import Block
from blocks import Blocks
from pygame import display, image, event, init, font
from pygame.locals import *


__alls__ = ["SCREEN_WIDTH", "SCREEN_HEIGHT", "BLOCK_SIZE", "START_POSITION", "main"]
# IT CAN BE POSSIBLE TO CHANGE THIS PARAMETERS TO CHANGE THE SIZE ELEMENTS AND THE START POSITION SNAKE.
SCREEN_WIDTH = 588
SCREEN_HEIGHT = 588
BLOCK_SIZE = 28
START_POSITION = 280, 280
# IT CANT BE POSSIBLE TO CHANGE THIS PARAMETERS BECAUSE OF THE CORRECT FUNCTION OF THE CODE.
_SCREEN_MAX_LIMIT = SCREEN_WIDTH - BLOCK_SIZE
_SCREEN_MIN_LIMIT = BLOCK_SIZE

"""" 
Array system snake direction [x,y]:
   [1,0]: Right, positive x
   [-1,0]: Left, negative x
   [0,-1]: Up, negative y
   [0,1]: Down, positive y
"""
_direction = [0, -1]
_olderDirection = [_direction[0], _direction[1]]

# Difficulty
_velocity = .05

# Images size is BLOCK_SIZExBLOCK_SIZE
# It is necessary to change the images when is changed the size of the elements in screen.
BODY = image.load('./images/snake/body.png')
HEAD = image.load('./images/snake/head.png')
FRUIT = image.load('./images/snake/fruit.png')
TREE = image.load('./images/snake/tree.png')


def update_body_snake_positions():
	global blocks
	global screen

	screen.blit(HEAD, (blocks.get_first_block().getX(), 
                        blocks.get_first_block().getY()))

	for block in blocks.get_blocks()[1:]:
		block.set_last_X(block.getX())
		block.set_last_Y(block.getY())
		block.setX(block.get_before_block().get_last_X())
		block.setY(block.get_before_block().get_last_Y())
		screen.blit(BODY, (block.getX(), block.getY()))

def paint_trees():
	global screen

	for i in range(0,int(SCREEN_WIDTH/BLOCK_SIZE)):
		screen.blit(TREE, (i*BLOCK_SIZE,0))
	for i in range(0,int(SCREEN_HEIGHT/BLOCK_SIZE)):
		screen.blit(TREE, (SCREEN_WIDTH-BLOCK_SIZE,i*BLOCK_SIZE))
	for i in range(0,int(SCREEN_WIDTH/BLOCK_SIZE)):
		screen.blit(TREE, (i*BLOCK_SIZE,SCREEN_HEIGHT-BLOCK_SIZE))
	for i in range(0,int(SCREEN_HEIGHT/BLOCK_SIZE)):
		screen.blit(TREE, (0,i*BLOCK_SIZE))


def generate_fruit():
	from random import randint
	global blocks

	posFruit = (randint(1,19)*BLOCK_SIZE,randint(1,19)*BLOCK_SIZE)

	while 1:
		posAvailable = True
		for block in blocks.get_blocks():
			if block.getX() == posFruit[0] and block.getY() == posFruit[1]:
				posAvailable = False
				break
		if not posAvailable:
			posFruit = (randint(1,19)*BLOCK_SIZE,randint(1,19)*BLOCK_SIZE)
		else:
			break

	return posFruit

def check_collision(xMovement, yMovement):

	collision = False

	for block in blocks.get_blocks()[1:]:
		if block.getX() == xMovement and block.getY() == yMovement:
			collision = True
			break

	if xMovement >= _SCREEN_MAX_LIMIT or xMovement < _SCREEN_MIN_LIMIT 
        or yMovement >= _SCREEN_MAX_LIMIT or yMovement < _SCREEN_MIN_LIMIT:
		collision = True

	return collision

def reset_game():
	global score
	global _direction
	global _olderDirection

	_direction = [0, -1]
	_olderDirection = [_direction[0], _direction[1]]
	if score.points > score.max_points:
		score.max_points = score.points
	score.points = 0
	event.clear()

	initialize_game()
	game()

def initialize_game():
	global blocks
	global screen
	global score
	global posFruit
	global labelPoints
	global myfont

	init() # Pygame init
	screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	myfont = font.SysFont('monospace', 20)
	blocks = Blocks(Block(*START_POSITION))
	posFruit = (-1, -1)

	# INITIALIZE SCREEN POSITIONS
	screen.blit(HEAD, (BLOCK_SIZE, BLOCK_SIZE))
	screen.blit(BODY, (START_POSITION[0] - BLOCK_SIZE, START_POSITION[1]))
	labelPoints = myfont.render("Score: " + str(score.points) + "  " 
                                + " Max. Score:" + str(score.max_points), 1, (255, 255, 0))
	screen.blit(labelPoints, (14, 7))
	paint_trees()
	blocks.add_block(Block(BLOCK_SIZE, START_POSITION[1] - BLOCK_SIZE))
	blocks.get_last_block().set_before_block(blocks.get_first_block())
	display.flip()

def game():
	from time import sleep
	from easygui import ynbox

	global score
	global _direction
	global _olderDirection
	global _velocity
	global blocks
	global screen
	global posFruit
	global labelPoints
	global myfont


	while 1:
		sleep(_velocity)

		screen.fill((0, 0, 0))
		paint_trees()
		screen.blit(labelPoints, (14, 7))
		if posFruit[0] == -1 and posFruit[1] == -1:  # Default fruit position
			posFruit = generate_fruit()

		elif posFruit[0] == blocks.get_first_block().getX() and posFruit[1] == blocks.get_first_block().getY():
            b = Block(blocks.get_last_block().getX() - BLOCK_SIZE * _direction[0], blocks.get_last_block().getY() - BLOCK_SIZE * _direction[1])
			b.set_before_block(blocks.get_last_block())
            blocks.add_block(b)
			#blocks.get_last_block().set_before_block(blocks.get_blocks()[len(blocks.get_blocks()) - 2])
			posFruit = generate_fruit()
			score.points = score.points + 100
			labelPoints = myfont.render("Score: " + str(score.points) + "  " 
                                        + " Max. Score:" + str(score.max_points), 1, (255, 255, 0))

		screen.blit(FRUIT, posFruit)
		next_x = blocks.get_first_block().getX()
		next_y = blocks.get_first_block().getY()

		eventP = event.poll()
		if eventP.type == NOEVENT:
			next_x = next_x + (BLOCK_SIZE * _direction[0])
			next_y = next_y + (BLOCK_SIZE * _direction[1])

		elif eventP.type == KEYDOWN and eventP.key == 275:  # Right direction
			_direction[0] = 1
			_direction[1] = 0
			next_x = next_x + (BLOCK_SIZE * _direction[0])
			next_y = next_y + (BLOCK_SIZE * _direction[1])

		elif eventP.type == KEYDOWN and eventP.key == 276:  # Left direction
			_direction[0] = -1
			_direction[1] = 0
			next_x = next_x + (BLOCK_SIZE * _direction[0])
			next_y = next_y + (BLOCK_SIZE * _direction[1])

		elif eventP.type == KEYDOWN and eventP.key == 274:  # Down direction
			_direction[0] = 0
			_direction[1] = 1
			next_x = next_x + (BLOCK_SIZE * _direction[0])
			next_y = next_y + (BLOCK_SIZE * _direction[1])

		elif eventP.type == KEYDOWN and eventP.key == 273:  # Up direction
			_direction[0] = 0
			_direction[1] = -1
			next_x = next_x + (BLOCK_SIZE * _direction[0])
			next_y = next_y + (BLOCK_SIZE * _direction[1])

		else: # No controlled event
			next_x = next_x + (BLOCK_SIZE * _direction[0])
			next_y = next_y + (BLOCK_SIZE * _direction[1])

		if (_olderDirection[0] + _direction[0]) == 0 
            and (_olderDirection[1] + _direction[1]) == 0:  # Event direction equals to current direction. No changes.
			_direction = [_olderDirection[0],_olderDirection[1]]
			next_x = next_x + (BLOCK_SIZE * _direction[0])
			next_y = next_y + (BLOCK_SIZE * _direction[1])

		if check_collision(next_x, next_y):
			if ynbox('Total Score: ' + str(score.points) + ' . Do you want to play again?', 'End Game', ('Yes', 'No')):
				break
			else:
				score.write_score_file()
				return()

		blocks.get_first_block().set_last_X(blocks.get_first_block().getX())
		blocks.get_first_block().set_last_Y(blocks.get_first_block().getY())
		blocks.get_first_block().setX(next_x)
		blocks.get_first_block().setY(next_y)
		_olderDirection = [_direction[0], _direction[1]]

		update_body_snake_positions()
		display.flip()

	reset_game()


def main(difficulty):
	global score
	global _velocity

	score = scoremodule.Score('SNAKE')
	score.read_score_file()

	if difficulty == 'Easy':
		_velocity = .2
	elif difficulty == 'Medium':
		_velocity = .1
	elif difficulty == 'Difficult':
		_velocity = .05
	elif difficulty == 'Pro':
		_velocity = .035

	initialize_game()
	game()
