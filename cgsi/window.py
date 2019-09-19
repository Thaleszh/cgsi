class window:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.center = [0.0, 0.0]
		self.view_up = [0.0, height/2]
		self.scale = 1.0
		self.view_up_ppc = [0.0, height/2]

	def up(self, ammount):
		self.center[1] += ammount

	def down(self, ammount):
		self.center[1] -= ammount

	def left(self, ammount):
		self.center[0] += ammount

	def right(self, ammount):
		self.center[0] -= ammount

	def zoom(self, ammount):
		self.scale *= ammount

	def get_width(self):
		return self.width / self.scale

	def get_height(self):
		return self.height / self.scale
