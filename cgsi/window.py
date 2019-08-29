class window:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.position = [0.0, 0.0]
		# self.position_up = [0.0, 0.0]
		self.scale = 1.0

	def up(self, ammount):
		self.position[1] += ammount

	def down(self, ammount):
		self.position[1] -= ammount

	def left(self, ammount):
		self.position[0] += ammount

	def right(self, ammount):
		self.position[0] -= ammount

	def zoom(self, ammount):
		self.scale *= ammount

	def get_width(self):
		return self.width / self.scale

	def get_height(self):
		return self.height / self.scale

	def to_window(self, coordinates):
		# simple for now
		return coordinates
