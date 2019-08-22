import shapes
import cairo
import copy

class window:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.position = [0.0, 0.0]
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

class control:
	def __init__(self):
		self.window = window(600, 400)
		self.obj_list = {}
		# future alter egos: self.alter_egos = {}

		# starter objects
		self.create_shape("start 1", "poli", [ [50, 200],[100, 200], [100, 250], [50,250]])

	def zoom(self, ammount):
		self.window.zoom(ammount)

	def up(self, ammount):
		self.window.down(ammount)

	def down(self, ammount):
		self.window.up(ammount)

	def left(self, ammount):
		self.window.left(ammount)

	def right(self, ammount):
		self.window.right(ammount)

	def draw_all(self, drawing_area, context):
		for obj in self.obj_list: # future change to check alter egos
			self.draw_shape(self.obj_list[obj], drawing_area, context)

	def draw_shape(self, obj, drawing_area, context):
		coordinates = copy.deepcopy(obj.coordinates)
		# to do: clippin here
		# getting screen convertions and then viewport convertions

		coordinates = self.window.to_window(coordinates)
		coordinates = self.to_viewport(coordinates, drawing_area)


		# draw coordinates on viewport, it's an array of doubles
		context.new_path()
		# first point
		context.move_to(coordinates[0][0], coordinates[0][1])

		# all points in middle
		for i in range(1, len(coordinates)):
			context.line_to(coordinates[i][0], coordinates[i][1])
			# print(str(coordinates[i][0]) + " " + str(coordinates[i][1]))
		# last point to first
		context.line_to(coordinates[0][0], coordinates[0][1])
		# print(str(coordinates[0][0]) + " " + str(coordinates[0][1]))
		context.stroke()

	def to_viewport(self, coordinates, drawing_area):
		da_width = drawing_area.get_allocation().width
		da_height = drawing_area.get_allocation().height
		for i, coordinate in enumerate(coordinates):
			# (X - Xwmin) * (Xvpmax - Xvpmin) / (Xwmax - Xwmin)
			coordinates[i][0] = ((coordinate[0] - self.window.position[0]) * 
								da_width / self.window.get_width())
			# (1 - (Y - Ywmin) / (Ywmax - Ywmin)) * (Yvpmax - Yvpmin)
			coordinates[i][1] = (1 - (coordinate[1] - self.window.position[1]) / 
								self.window.get_height()) * da_height

		return coordinates


	def create_shape(self, name, shape, coordinates):
		# check what object is to be made
		print("created object at:") 
		print(coordinates)
		if shape == "point":
			obj = shapes.point(coordinates)
		elif shape == "line":
			obj = shapes.line(coordinates)
		else:
			obj = shapes.polygon(coordinates)
		# add to display file
		self.obj_list[name] = obj
		# draw shape created

	def delete_shape(self, name):
		del self.obj_list[name]

