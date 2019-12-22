class Block:
	def __init__(self, x, y):
		self._x = x
		self._y = y
		self._last_x = 0
		self._last_y = 0

	def setX(self, x):
		self._x = x

	def setY(self, y):
		self._y = y

	def getX(self):
		return self._x

	def getY(self):
		return self._y

	def set_last_X(self, last_x):
		self._last_x = last_x

	def set_last_Y(self, last_y):
		self._last_y = last_y

	def get_last_X(self):
		return self._last_x

	def get_last_Y(self):
		return self._last_y

	def set_before_block(self, before):
		self._before_bloque = before

	def get_before_block(self):
		return self._before_bloque

	def to_string(self):
		return "X: " + str(self._x) + ",Y: " + str(self._y) + ",Last_X: " + str(self._last_x) + ",Last_Y: " + str(self._last_y)