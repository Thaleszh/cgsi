import shapes

class window:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.position = [0.0, 0.0]
		self.scale = 1.0

	def up(self, ammount):
		position[1] += ammount

	def down(self, ammount):
		position[1] -= ammount

	def left(self, ammount):
		position[0] -= ammount

	def right(self, ammount):
		position[0] -= ammount

	def zoom_in(self, ammount):
		scale += ammount

	def zoom_out(self, ammount):
		scale -= ammount

	def to_window(self, coordinates):
		return coordinates

class control:
	def __init__(self, drawing_area, context):
		self.window = window(600, 400)
		self.obj_list = {}
		# future alter egos: self.alter_egos = {}

	def zoom_in(self, ammount):
		window.zoom_in(ammount)

	def zoom_out(self, ammount):
		window.zoom_in(ammount)

	def up(self, ammount):
		window.up(ammount)

	def down(self, ammount):
		window.down(ammount)

	def left(self, ammount):
		window.left(ammount)

	def right(self, ammount):
		window.right(ammount)

	def draw_all(self, drawing_area, context):
		for obj in obj_list: # future change to check alter egos
			draw_shape(obj, drawing_area, context)

	def draw_shape(self, obj, drawing_area, context):
		coordinates = obj.coordinates()
		# future addition for clippin here
		# getting screen convertions and then viewport convertions
		coordinates = window.to_window(coordinates)
		coordinates = to_viewport(coordinates, drawing_area)

		# draw coordinates on viewport, it's an array of doubles
		context.new_path()
		# first point
		context.move_to(coordinates[0][0], coordinates[0][1])
		# all points in middle
		for i in range(1, len(coordinates)):
			context.rel_line_to(coordinates[i][0], coordinates[i][1])
		# last point to first
		contex.rel_line_to(coordinates[0][0], coordinates[0][1])
		context.stroke()

	def to_viewport(self, coordinates, drawing_area):
		da_width = drawing_area.get_allocation().width
		da_height = drawing_area.get_allocation().height

		for i, cordinate in enumerate(coordinates):
			# (X - Xwmin) * (Xvpmax - Xvpmin) / (Xwmax - Xwmin)
			coordinates[i][0] = ((coordinates[i][0] - window.position[0]) * 
								da_width / window.width)
			# (1 - (Y - Ywmin) / (Ywmax - Ywmin)) * (Yvpmax - Yvpmin)
			coordinates[i][1] = (1 - (coordinates[i][1] - window.position[1]) / 
								indow.height) * da_height

		return coordinates


	def create_shape(self, name, shape, coordinates):
		if shape == "point":
			obj = point(coordinates)
		elif shape == "rectangle":
			obj = rectangle(coordinates)
		else:
			obj = polygon(coordinates)
		obj_list[name] = obj

	def delete_shape(self, name):
		del obj_list[name]

