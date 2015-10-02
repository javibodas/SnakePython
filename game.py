
import sys
import time 
import random
from colorama import Fore,Back,Style
import pygame
from pygame.locals import *

class Bloques:

	def __init__(self,cabeza):
		self.bloques = [cabeza]
	def anadirBloque(self,bloque):
		self.bloques.append(bloque)
	def getUltimoBloque(self):
		return self.bloques[len(self.bloques)-1]
	def getPrimerBloque(self):
		return self.bloques[0]
	def getBloques(self):
		return self.bloques
	def actualizarPosicionesCuerpo(self,cuerpo,screen):
		for bloque in self.bloques[1:]:
			bloque.setLastX(bloque.getX())
			bloque.setLastY(bloque.getY())
			bloque.setX(bloque.getBeforeBloque().getLastX())
			bloque.setY(bloque.getBeforeBloque().getLastY())
			screen.blit(cuerpo, (bloque.getX(),bloque.getY()))

	def toString(self):
		for bloque in self.bloques:
			print bloque.toString()

class Bloque:
	
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.last_x = 0
		self.last_y = 0
	def setX(self,x):
		self.x = x
	def setY(self,y):
		self.y = y
	def getX(self):
		return self.x
	def getY(self):
		return self.y
	def setLastX(self,last_x):
		self.last_x = last_x
	def setLastY(self,last_y):
		self.last_y = last_y
	def getLastX(self):
		return self.last_x
	def getLastY(self):
		return self.last_y
	def setBeforeBloque(self,before):
		self.before_bloque = before
	def getBeforeBloque(self):
		return self.before_bloque
	def toString(self):
		return "X: " + str(self.x) + ",Y: " + str(self.y) + ",Last_X: " + str(self.last_x) + ",Last_Y: " + str(self.last_y)

def generarFruta(bloques):

	tuple = (random.randint(0,20)*28,random.randint(0,20)*28)	
	#print str(tuple[0]) + ":" + str(tuple[1])
	
	while 1:
		bool = True
		for bloque in bloques.getBloques():
			if(bloque.getX() == tuple[0] and bloque.getY() == tuple[1]):
				bool = False	
				break
			
		if(not bool):
			tuple = (random.randint(0,20)*28,random.randint(0,20)*28)
		else:
			break
	return tuple


def main():

	pygame.init()

	#VARIABLES GLOBALES

	# Sistema de array para almacenar la direccion que sigue la serpiente [x,y]:
	#	- [1,0]: Direccion derecha, es decir, x suma positiva 
	#	- [-1,0]: Direccion izquierda, es decir, x suma negativa
	#	- [0,-1]: Direccion arriba, es decir, y suma negativa
	#	- [0,1]: Direccion abajo, es decir, y suma positiva	
	DIRECCION = [0,-1] 
	
	# Las imagenes miden 28x28
	CUERPO = pygame.image.load('cuerpo.png')
	CABEZA = pygame.image.load('cabeza.png')
	FRUTA = pygame.image.load('fruta.png')
	screen = pygame.display.set_mode((560,560))
	bloques = Bloques(Bloque(280,280))
	pos_fruta = (-1,-1)
	 

	screen.blit(CABEZA, (28,28))
	screen.blit(CUERPO, (280,308))
	bloques.anadirBloque(Bloque(28,308)) #Anadimos nuevo bloque
	bloques.getUltimoBloque().setBeforeBloque(bloques.getPrimerBloque())
	pygame.display.flip()


	while 1:
		time.sleep(.2)
		
		screen.fill((0,0,0)) 
		if((pos_fruta[0] == -1 and pos_fruta[1] == -1)):
			pos_fruta = generarFruta(bloques)
			print pos_fruta
		elif (pos_fruta[0] == bloques.getPrimerBloque().getX() and pos_fruta[1] == bloques.getPrimerBloque().getY()):
			bloques.anadirBloque(Bloque(bloques.getUltimoBloque().getX()-28*DIRECCION[0], bloques.getUltimoBloque().getY()-28*DIRECCION[1]))
			bloques.getUltimoBloque().setBeforeBloque(bloques.getBloques()[len(bloques.getBloques())-2])
			pos_fruta = generarFruta(bloques)
			print pos_fruta
					
		screen.blit(FRUTA, pos_fruta)
		next_x = bloques.getPrimerBloque().getX()
		next_y = bloques.getPrimerBloque().getY()
		
		event = pygame.event.poll()
		if(event.type == NOEVENT):
			next_x = next_x + 28*DIRECCION[0]
			next_y = next_y	+ 28*DIRECCION[1]
		elif(event.type == KEYDOWN and event.key == 275): # Direccion derecha
			DIRECCION[0] = 1
			DIRECCION[1] = 0
			next_x = next_x + 28*DIRECCION[0]
			next_y = next_y + 28*DIRECCION[1]

		elif(event.type == KEYDOWN and event.key == 276): #Direccion izquierda
			DIRECCION[0] = -1
                        DIRECCION[1] = 0
                        next_x = next_x + 28*DIRECCION[0]
                        next_y = next_y + 28*DIRECCION[1]
		
		elif(event.type == KEYDOWN and event.key == 274): #Direccion abajo
			DIRECCION[0] = 0
                        DIRECCION[1] = 1
                        next_x = next_x + 28*DIRECCION[0]
                        next_y = next_y + 28*DIRECCION[1]

		elif(event.type == KEYDOWN and event.key == 273): #Direccion arriba
			DIRECCION[0] = 0
                        DIRECCION[1] = -1
                        next_x = next_x + 28*DIRECCION[0]
                        next_y = next_y + 28*DIRECCION[1]
		
		elif(event.type == QUIT):
			print(Back.YELLOW + Fore.RED + "Exit Game")
			sys.exit()
		else: # Si no se ha registrado ningun evento de movimiento avanza en la misma direccion  
			next_x = next_x + 28*DIRECCION[0]
			next_y = next_y + 28*DIRECCION[1]
	
		if(next_x > 560 or next_x < 0 or next_y > 560 or next_y < 0):
			sys.exit()

			
		bloques.getPrimerBloque().setLastX(bloques.getPrimerBloque().getX())
		bloques.getPrimerBloque().setLastY(bloques.getPrimerBloque().getY())
		bloques.getPrimerBloque().setX(next_x)
		bloques.getPrimerBloque().setY(next_y)
		screen.blit(CABEZA, (next_x,next_y))
	
		bloques.actualizarPosicionesCuerpo(CUERPO,screen)
		pygame.display.flip()


if __name__ == '__main__':
	main()
