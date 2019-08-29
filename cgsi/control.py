import shapes
import cairo
import copy
import numpy as np
import math

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
		to_center, back_to_place = self.matrixes_obj_to_point(obj, point)
		# apply all 3
		change_matrix = self.matrix_rotation(to_center, teta)
		change_matrix = self.matrix_scale(change_matrix, x_factor, y_factor)
		change_matrix = np.matmul(change_matrix, back_to_place)
		change_matrix = self.matrix_translate(change_matrix, x, y)

		# update coordinates
		self.change_object(obj, change_matrix)		

	def rotate_object(self, name, teta, point=[0, 0]):
		# get object
		obj = self.obj_list[name]
		# find matrix to translate it to point
		to_center, back_to_place = self.matrixes_obj_to_point(obj, point)
		# make change matrix
		change_matrix = self.matrix_rotation(to_center, teta)
		change_matrix = np.matmul(change_matrix, back_to_place)

		# update coordinates
		self.change_object(obj, change_matrix)

	def scale_object(self, name, x, y, point=[0, 0]):
		# get object
		obj = self.obj_list[name]
		# find matrix to translate it to point
		to_center, back_to_place = self.matrixes_obj_to_point(obj, point)
		# make change matrix
		change_matrix = self.matrix_scale(to_center, x, y)
		change_matrix = np.matmul(change_matrix, back_to_place)

		# update coordinates
		self.change_object(obj, change_matrix)

	def translate_object(self, name, x, y):
		base_matrix = np.matrix([[1,0,0],
								 [0,1,0],
								 [0,0,1]])
		# make change matrix
		change_matrix = self.matrix_translate(base_matrix, x, y)
		# update coordinates
		self.change_object(self.obj_list[name], change_matrix)

	def change_object(self, obj, change_matrix):
		# get all coordinates reference
		# print(change_matrix)
		coordinates = obj.coordinates
		for coordinate in coordinates:
			# calculate new coordinates
			result = np.matmul([[coordinate[0], coordinate[1], 1]], change_matrix)
			# update them
			coordinate[0] = result[0, 0]
			coordinate[1] = result[0, 1]


	def matrixes_obj_to_point(self, obj, point):
		# get center coordinates of thing
		x, y = self.find_center(obj) 
		# find translation vector
		x_translation = (point[0] - x)
		y_translation = (point[1] - y)
		# make matrixes
		to_center = np.matrix([ [1, 0, 0],
								[0, 1, 0],
								[x_translation, y_translation, 1]])
		back_to_place = np.matrix([ [1, 0, 0],
									[0, 1, 0],
									[-x_translation, -y_translation, 1]])
		print("Matrixes:")
		print(to_center)
		print(back_to_place)
		return [to_center, back_to_place]

	def find_center(self, obj):
		x_center = 0
		y_center = 0
		coordinates = obj.coordinates
		# sum all x and y
		for coordinate in coordinates:
			x_center += coordinate[0]
			y_center += coordinate[1]
		# divides by number of items
		x_center /= len(coordinates)
		y_center /= len(coordinates)
		return [x_center, y_center]


	def matrix_translate(self, matrix, x, y):
		translation = np.matrix([[1, 0, 0],
								 [0, 1, 0],
								 [x, y, 1]])
		return np.matmul(matrix, translation)

	def matrix_scale(self, matrix, x, y):
		scaling = np.matrix([ [x, 0, 0],
							  [0, y, 0],
							  [0, 0, 1]])
		# print("Scale Matrix:")
		# print(scaling)
		return np.matmul(matrix, scaling)

	def matrix_rotation(self, matrix, teta):
		# covert to radians
		radian = np.deg2rad(teta)
		print(radian)
		rotation = np.matrix([[math.cos(radian), -math.sin(radian), 0],
							  [math.sin(radian),  math.cos(radian), 0],
							  [0		,  0		, 1]])
		print("Rotation:")
		print(rotation)
		return np.matmul(matrix, rotation)


