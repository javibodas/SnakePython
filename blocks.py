class Blocks:
	def __init__(self, head):
		self._blocks = [head]

	def add_block(self, block):
		self._blocks.append(block)

	def get_last_block(self):
		return self._blocks[len(self._blocks)-1]

	def get_first_block(self):
		return self._blocks[0]

	def get_blocks(self):
		return self._blocks

	def set_blocks(self, blocks):
		if not isinstance(blocks, Blocks):
			raise ValueError("Blocks must be type of Blocks.")
		self._blocks = blocks

	def to_string(self):
		for block in self._blocks:
			print(block.to_string())