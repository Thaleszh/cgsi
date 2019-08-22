class shape:
	def coordinates(self):
		return None

class point(shape):
	def __init__(self, coordinates):
		self.coordinates = [coordinates[0]]

class line(shape):
	def __init__(self, coordinates):
		self.coordinates = coordinates[0:2]

class rectangle(shape):
	def __init__(self, coordinates):
		self.coordinates = coordinates[0:4]

	def coordinates(self):
		return coordinates

class polygon(shape):
	def __init__(self, coordinates):
		self.coordinates = coordinates

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