import numpy as np

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


class Bezier(shape):
    def __init__(self, coordinates, step, rgba=(0,0,0,1)):
        mb = np.array([
            [-1, 3, -3, 1],
            [3, -6, 3, 0],
            [-3, 3, 0, 0],
            [1, 0, 0, 0]
        ])
        self.coordinates = []
        self.calculate_curve(coordinates, step)

    def calculate_curve(self, points, step):
        gbx = np.array([
            [points[0][0]],
            [points[1][0]],
            [points[2][0]],
            [points[3][0]],
        ])
        gby = np.array([
            [points[0][1]],
            [points[1][1]],
            [points[2][1]],
            [points[3][1]],
        ])
        while i <= 1:
            point_x = calculate_bezier_point(i, [p1,p2,p3,p4], 0)
            point_y = calculate_bezier_point(i, [p1,p2,p3,p4], 1)
            self.coordinates.append([point_x, point_y])
            i += 0.2

    def calculate_point(t, points, point_index):
        return (points[0][point_index]*(-(t*t*t) + 3*t*t - 3*t + 1) +
                points[1][point_index]*(3*t*t*t - 6*t*t + 3*t) +
                points[2][point_index]*(-3*t*t*t + 3*t*t) +
                points[3][point_index]*(t*t*t))


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
