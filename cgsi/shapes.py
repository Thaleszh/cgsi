import numpy as np

class shape:
    def __init__(self, coordinates, rgba=(0,0,0,1), closed_shape=True):
        self.coordinates = coordinates
        self.rgba = rgba
        self.closed_shape = closed_shape


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
        for i in range(1, len(coordinates), 3):
            points = [coordinates[x] for x in range(i-1, i+3)]
            self.calculate_curve(points, step)

        self.rgba = rgba
        self.closed_shape = False
        self.points = points

    def calculate_curve(self, points, step):
        i = 0
        while i <= 1:
            point_x = self.calculate_point(i, points, 0)
            point_y = self.calculate_point(i, points, 1)
            self.coordinates.append([point_x, point_y])
            i += step

    def calculate_point(self, t, points, point_index):
        return (points[0][point_index]*(-(t*t*t) + 3*t*t - 3*t + 1) +
                points[1][point_index]*(3*t*t*t - 6*t*t + 3*t) +
                points[2][point_index]*(-3*t*t*t + 3*t*t) +
                points[3][point_index]*(t*t*t))

class B-spline(shape):
    def __init(self, control_points, n_points, rgba=(0,0,0,1))
        self.rgba = rgba
        self.closed_shape = false
        proj_x = np.array([v.x for v in control_points], dtype=float)
        proj_y = np.array([v.y for v in control_points], dtype=float)
        self.coordinates = []
        for i in range(0, len(control_points) - 3):
            Gbs_x = proj_x[i:i + 4]
            Gbs_y = proj_y[i:i + 4]

            Cx = self.bspline_matrix() @ Gbs_x
            Cy = self.bspline_matrix() @ Gbs_y

            Dx = self.fd_matrix(1.0 / n_points) @ Cx
            Dy = self.fd_matrix(1.0 / n_points) @ Cy

            for k in range(n_points + 1):
                x = Dx[0]
                y = Dy[0]
                # print(f'{k}:')
                # print(f'\tx={x}')
                # print(f'\ty={y}')

                Dx = Dx + np.append(Dx[1:], 0)
                Dy = Dy + np.append(Dy[1:], 0)

                self.coordinates.append([x, y])

    def bspline_matrix(self):
        return np.array(
            [
                -1, 3, -3, 1,
                3, -6, 3, 0,
                -3, 0, 3, 0,
                1, 4, 1, 0
            ],
            dtype=float
        ).reshape(4, 4) / 6

    def fd_matrix(self, delta):
        return np.array(
            [
                0, 0, 0, 1,
                delta**3, delta**2, delta, 0,
                6 * delta**3, 2 * delta**2, 0, 0,
                6 * delta**3, 0, 0, 0,
            ],
            dtype=float
        ).reshape(4, 4)

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
