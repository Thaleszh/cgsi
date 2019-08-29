import shapes
import cairo
import copy
import numpy as np
import transformations as trans
import window as wind

class control:
	def __init__(self):
		self.window = wind.window(600, 400)
		self.obj_list = {}
		self.alter_egos = {}

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
		if shape == "Ponto":
			obj = shapes.point(coordinates)
		elif shape == "Linha":
			obj = shapes.line(coordinates)
		else:
			obj = shapes.polygon(coordinates)
		# add to display file
		self.obj_list[name] = obj
		# draw shape created

	def delete_shape(self, name):
		del self.obj_list[name]


	def translate_scale_rotate(self, name, x,y, x_factor, y_factor, teta, point=[0,0]):
		# get object
		obj = self.obj_list[name]
		# find matrix to translate it to point
		to_center, back_to_place = trans.matrixes_obj_to_point(obj, point)
		# apply all 3
		change_matrix = trans.matrix_rotation(to_center, teta)
		change_matrix = trans.matrix_scale(change_matrix, x_factor, y_factor)
		change_matrix = np.matmul(change_matrix, back_to_place)
		change_matrix = trans.matrix_translate(change_matrix, x, y)

		# update coordinates
		trans.change_object(obj, change_matrix)		

	def rotate_object(self, name, teta, point=[0, 0]):
		# get object
		obj = self.obj_list[name]
		# find matrix to translate it to point
		to_center, back_to_place = trans.matrixes_obj_to_point(obj, point)
		# make change matrix
		change_matrix = trans.matrix_rotation(to_center, teta)
		change_matrix = np.matmul(change_matrix, back_to_place)

		# update coordinates
		trans.change_object(obj, change_matrix)

	def scale_object(self, name, x, y, point=[0, 0]):
		# get object
		obj = self.obj_list[name]
		# find matrix to translate it to point
		to_center, back_to_place = trans.matrixes_obj_to_point(obj, point)
		# make change matrix
		change_matrix = trans.matrix_scale(to_center, x, y)
		change_matrix = np.matmul(change_matrix, back_to_place)

		# update coordinates
		trans.change_object(obj, change_matrix)

	def translate_object(self, name, x, y):
		base_matrix = np.matrix([[1,0,0],
								 [0,1,0],
								 [0,0,1]])
		# make change matrix
		change_matrix = trans.matrix_translate(base_matrix, x, y)
		# update coordinates
		trans.change_object(self.obj_list[name], change_matrix)


