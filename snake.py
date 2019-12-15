# coding: utf-8
import sys
from pygame import display, image, event, init, font
from pygame.locals import *

SCREEN_WIDTH = 588
SCREEN_HEIGHT = 588
BLOCK_SIZE = 28
SCREEN_MAX_LIMIT = SCREEN_WIDTH - BLOCK_SIZE
SCREEN_MIN_LIMIT = BLOCK_SIZE
START_POSITION = 280, 280

"""" 
Array system snake direction [x,y]:
   [1,0]: Right, positive x
   [-1,0]: Left, negative x
   [0,-1]: Up, negative y
   [0,1]: Down, positive y
Default direction
"""
direction = [0, -1]
olderDirection = [0, -1]

# Points game
max_points = 0
points = 0

# Images size is BLOCK_SIZExBLOCK_SIZE
BODY = image.load('./images/body.png')
HEAD = image.load('./images/head.png')
FRUIT = image.load('./images/fruit.png')
TREE = image.load('./images/tree.png')


class Blocks:
	def __init__(self, head):
		self.blocks = [head]

	def add_block(self, block):
		self.blocks.append(block)

	def get_last_block(self):
		return self.blocks[len(self.blocks)-1]

	def get_first_block(self):
		return self.blocks[0]

	def get_blocks(self):
		return self.blocks

	def update_body_positions(self, body, screen):
		for block in self.blocks[1:]:
			block.set_last_X(block.getX())
			block.set_last_Y(block.getY())
			block.setX(block.get_before_block().get_last_X())
			block.setY(block.get_before_block().get_last_Y())
			screen.blit(body, (block.getX(), block.getY()))

	def to_string(self):
		for block in self.blocks:
			print(block.to_string())


class Block:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.last_x = 0
		self.last_y = 0

	def setX(self, x):
		self.x = x

	def setY(self, y):
		self.y = y

	def getX(self):
		return self.x

	def getY(self):
		return self.y

	def set_last_X(self, last_x):
		self.last_x = last_x

	def set_last_Y(self, last_y):
		self.last_y = last_y

	def get_last_X(self):
		return self.last_x

	def get_last_Y(self):
		return self.last_y

	def set_before_block(self, before):
		self.before_bloque = before

	def get_before_block(self):
		return self.before_bloque

	def to_string(self):
		return "X: " + str(self.x) + ",Y: " + str(self.y) + ",Last_X: " + str(self.last_x) + ",Last_Y: " + str(self.last_y)


def paint_trees(screen):

	for i in range(0,int(SCREEN_WIDTH/BLOCK_SIZE)):
		screen.blit(TREE, (i*BLOCK_SIZE,0))
	for i in range(0,int(SCREEN_HEIGHT/BLOCK_SIZE)):
		screen.blit(TREE, (SCREEN_WIDTH-BLOCK_SIZE,i*BLOCK_SIZE))
	for i in range(0,int(SCREEN_WIDTH/BLOCK_SIZE)):
		screen.blit(TREE, (i*BLOCK_SIZE,SCREEN_HEIGHT-BLOCK_SIZE))
	for i in range(0,int(SCREEN_HEIGHT/BLOCK_SIZE)):
		screen.blit(TREE, (0,i*BLOCK_SIZE))


def generate_fruit(blocks):

	from random import randint
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

	if xMovement >= SCREEN_MAX_LIMIT or xMovement < SCREEN_MIN_LIMIT or yMovement >= SCREEN_MAX_LIMIT or yMovement < SCREEN_MIN_LIMIT:
		collision = True

	return collision

def reset_game():

   global points
   global direction
   global olderDirection

   direction = [0, -1]
   olderDirection = [0, -1]
   points = 0
   event.clear()

   initialize_game()
   game()

def initialize_game():
   global blocks
   global screen
   global points
   global posFruit
   global labelPoints
   global myfont

   init()
   screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
   myfont = font.SysFont('monospace', 20)
   blocks = Blocks(Block(*START_POSITION))
   posFruit = (-1, -1)

   # INITIALIZE SCREEN POSITIONS
   screen.blit(HEAD, (BLOCK_SIZE, BLOCK_SIZE))
   screen.blit(BODY, (START_POSITION[0] - BLOCK_SIZE, START_POSITION[1]))
   labelPoints = myfont.render("Score: " + str(points), 1, (255, 255, 0))
   screen.blit(labelPoints, (14, 7))
   paint_trees(screen)
   blocks.add_block(Block(BLOCK_SIZE, START_POSITION[1] - BLOCK_SIZE))
   blocks.get_last_block().set_before_block(blocks.get_first_block())
   display.flip()

def game():

	from time import sleep
	from easygui import ynbox

	global points
	global direction
	global olderDirection
	global blocks
	global screen
	global posFruit
	global labelPoints
	global myfont

	while 1:
		sleep(.1)

		screen.fill((0, 0, 0))
		paint_trees(screen)
		screen.blit(labelPoints, (14, 7))
		if posFruit[0] == -1 and posFruit[1] == -1:
			posFruit = generate_fruit(blocks)

		elif posFruit[0] == blocks.get_first_block().getX() and posFruit[1] == blocks.get_first_block().getY():
			blocks.add_block(Block(blocks.get_last_block().getX() - BLOCK_SIZE * direction[0],
                                 blocks.get_last_block().getY() - BLOCK_SIZE * direction[1]))
			blocks.get_last_block().set_before_block(blocks.get_blocks()[len(blocks.get_blocks()) - 2])
			posFruit = generate_fruit(blocks)
			points = points + 100
			labelPoints = myfont.render("Score: " + str(points), 1, (255, 255, 0))

		screen.blit(FRUIT, posFruit)
		next_x = blocks.get_first_block().getX()
		next_y = blocks.get_first_block().getY()

		eventP = event.poll()
		if eventP.type == NOEVENT:
			next_x = next_x + BLOCK_SIZE * direction[0]
			next_y = next_y + BLOCK_SIZE * direction[1]

		elif eventP.type == KEYDOWN and eventP.key == 275:  # Right direction
			direction[0] = 1
			direction[1] = 0
			next_x = next_x + BLOCK_SIZE * direction[0]
			next_y = next_y + BLOCK_SIZE * direction[1]

		elif eventP.type == KEYDOWN and eventP.key == 276:  # Left direction
			direction[0] = -1
			direction[1] = 0
			next_x = next_x + BLOCK_SIZE * direction[0]
			next_y = next_y + BLOCK_SIZE * direction[1]

		elif eventP.type == KEYDOWN and eventP.key == 274:  # Down direction
			direction[0] = 0
			direction[1] = 1
			next_x = next_x + BLOCK_SIZE * direction[0]
			next_y = next_y + BLOCK_SIZE * direction[1]

		elif eventP.type == KEYDOWN and eventP.key == 273:  # Up direction
			direction[0] = 0
			direction[1] = -1
			next_x = next_x + BLOCK_SIZE * direction[0]
			next_y = next_y + BLOCK_SIZE * direction[1]

		else:
			next_x = next_x + BLOCK_SIZE * direction[0]
			next_y = next_y + BLOCK_SIZE * direction[1]

		if (olderDirection[0] + direction[0]) == 0 and (olderDirection[1] + direction[1]) == 0:
			direction = olderDirection
			next_x = next_x + BLOCK_SIZE * direction[0]
			next_y = next_y + BLOCK_SIZE * direction[1]

		if check_collision(next_x, next_y):
			if ynbox('Total Score: ' + str(points) + ' . Do you want to play again?', 'End Game', ('Yes', 'No')):
				break
			else:
				sys.exit()

		blocks.get_first_block().set_last_X(blocks.get_first_block().getX())
		blocks.get_first_block().set_last_Y(blocks.get_first_block().getY())
		blocks.get_first_block().setX(next_x)
		blocks.get_first_block().setY(next_y)
		screen.blit(HEAD, (next_x, next_y))
		olderDirection = [direction[0],direction[1]]

		blocks.update_body_positions(BODY, screen)
		display.flip()

	reset_game()


def main():
	initialize_game()
	game()


if __name__ == '__main__':
	main()
