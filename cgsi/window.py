class window:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.position = [0.0, 0.0]
		self.view_up = [0.0, height]
		self.scale = 1.0
		self.position_ppc = [0.0, 0.0]
		self.view_up_ppc = [0.0, height]

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

	def get_center(self):
		return [self.position[0] + self.width / 2, self.position[1] + self.height / 2]
