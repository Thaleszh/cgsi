import math
import shapes
import numpy as np


ROTATE_AROUND_SELF = 0
ROTATE_AROUND_CENTER = 1
ROTATE_AROUND_POINT = 2

def change_object(obj, change_matrix):
	coordinates = obj.coordinates
	change_coordinates(coordinates, change_matrix)

def change_coordinates(coordinates, change_matrix):
	# print(change_matrix)
	for coordinate in coordinates:
		# calculate new coordinates
		result = np.matmul([[coordinate[0], coordinate[1], 1]], change_matrix)
		# update them
		coordinate[0] = result[0, 0]
		coordinate[1] = result[0, 1]


def matrixes_obj_to_point(center, point):
	# get center coordinates of thing
	x, y = center[0], center[1]
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


def matrix_translate(x, y):
	translation = np.matrix([[1, 0, 0],
							 [0, 1, 0],
							 [x, y, 1]])
	return translation


def matrix_scale(obj, x, y):
	origin = find_center(obj)
	to_center = matrix_translate(-origin[0], -origin[1])
	scaling = np.matrix([ [x, 0, 0],
						  [0, y, 0],
						  [0, 0, 1]])
	to_origin = matrix_translate(origin[0], origin[1])

	matrix = np.matmul(to_center, scaling)
	matrix = np.matmul(matrix, to_origin)
	return matrix


def matrix_rotation(teta, point):
	# covert to radians
	radian = np.deg2rad(teta)
	to_center = matrix_translate(-point[0], -point[1])

	rotation = np.matrix([[math.cos(radian), -math.sin(radian), 0],
						  [math.sin(radian),  math.cos(radian), 0],
						  [0		,  0		, 1]])
	to_origin = matrix_translate(point[0], point[1])

	matrix = np.matmul(to_center, rotation)
	matrix = np.matmul(matrix, to_origin)
	return matrix
