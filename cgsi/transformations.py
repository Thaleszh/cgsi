import math
import shapes
import numpy as np

def change_object(obj, change_matrix):
	# get all coordinates reference
	# print(change_matrix)
	coordinates = obj.coordinates
	for coordinate in coordinates:
		# calculate new coordinates
		result = np.matmul([[coordinate[0], coordinate[1], 1]], change_matrix)
		# update them
		coordinate[0] = result[0, 0]
		coordinate[1] = result[0, 1]


def matrixes_obj_to_point(obj, point):
	# get center coordinates of thing
	x, y = find_center(obj) 
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
	# print("Matrixes:")
	# print(to_center)
	# print(back_to_place)
	return [to_center, back_to_place]

def find_center(obj):
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


def matrix_translate(matrix, x, y):
	translation = np.matrix([[1, 0, 0],
							 [0, 1, 0],
							 [x, y, 1]])
	return np.matmul(matrix, translation)

def matrix_scale(matrix, x, y):
	scaling = np.matrix([ [x, 0, 0],
						  [0, y, 0],
						  [0, 0, 1]])
	# print("Scale Matrix:")
	# print(scaling)
	return np.matmul(matrix, scaling)

def matrix_rotation(matrix, teta):
	# covert to radians
	radian = np.deg2rad(teta)
	# print(radian)
	rotation = np.matrix([[math.cos(radian), -math.sin(radian), 0],
						  [math.sin(radian),  math.cos(radian), 0],
						  [0		,  0		, 1]])
	# print("Rotation:")
	# print(rotation)
	return np.matmul(matrix, rotation)