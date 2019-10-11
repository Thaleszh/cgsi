class window:
	def __init__(self, width, height, border_size = 10):
		self.width = width
		self.height = height
		self.center = [width/2, height/2]
		self.v_up = [0.0, height]
		self.scale = 1.0
		self.border_size = border_size

	def up(self, ammount):
		self.center[1] -= ammount

	def down(self, ammount):
		self.center[1] += ammount

	def left(self, ammount):
		self.center[0] -= ammount

	def right(self, ammount):
		self.center[0] += ammount

	def zoom(self, ammount):
		self.scale *= ammount

	def get_width(self):
		return self.width / self.scale

	def get_height(self):
		return self.height / self.scale
