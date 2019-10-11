class shape:
	def __init__(self, coordinates, rgba=(0,0,0,1)):
		self.coordinates = coordinates
		self.rgba = rgba


class point(shape):
	pass


class line(shape):
	pass


class polygon(shape):
	pass


if __name__ == '__main__':
    rect = rectangle([[0,0],[1,0],[1,1],[0,1]])
    for coordinate in rect.coordinates:
    	print(str(coordinate[0]) +  str(coordinate[1]))
    pol = polygon( [[0,0],[1,0],[1,1],[0,1], [-1,-1]])
    for coordinate in pol.coordinates:
    	print(str(coordinate[0]) +  str(coordinate[1]))
    pt = point([[0,0]])
    for coordinate in pt.coordinates:
    	print(str(coordinate[0]) +  str(coordinate[1]))
