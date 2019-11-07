import window as wind
import shapes

def clip(coordinates, window, close_shape):
    clipped_coordinates = []
    last_point = coordinates[0][0], coordinates[0][1]
    for i in range(1, len(coordinates)):
        last_point = [coordinates[i-1][0], coordinates[i-1][1]]
        next_point = [coordinates[i][0], coordinates[i][1]]
        discart = should_discart(last_point, next_point, window)
        if discart:
            continue

        last_point, next_point = clip_points(last_point, next_point, window)
        clipped_coordinates.append(last_point)
        clipped_coordinates.append(next_point)
    # last point to first
    if close_shape:
        next_point = [coordinates[0][0], coordinates[0][1]]
        last_point = [coordinates[-1][0], coordinates[-1][1]]
        discart = should_discart(last_point, next_point, window)
        if not discart:
            last_point, next_point = clip_points(last_point, next_point, window)
            clipped_coordinates.append(last_point)
            clipped_coordinates.append(next_point)

    return clipped_coordinates

def clip_points(p1, p2, window):
    p1_area_code = point_area_code(p1, window)
    p2_area_code = point_area_code(p2, window)

    if p1_area_code == 0 and p1_area_code == p2_area_code:
        return p1, p2

    m = (p2[1] - p1[1])/(p2[0] - p1[0])
    if p1_area_code != 0:
        p1 = window_intersection(p1, p1_area_code, m, window)
    if p2_area_code != 0:
        p2 = window_intersection(p2, p2_area_code, m, window)
    return p1, p2

def window_intersection(point, point_area_code, m, window):
    # left
    if point_area_code == 1:
        x = -window.get_width()/2
        y = m*(x - point[0]) + point[1]
        return [x, y]
    # up
    if point_area_code == 8:
        y = window.get_height()/2
        x = point[0] + 1/m * (y - point[1])
        return [x, y]
    # right
    if point_area_code == 2:
        x = window.get_width()/2
        y = m * (x - point[0]) + point[1]
        return [x, y]
    # down
    if point_area_code == 4:
        y = -window.get_height()/2
        x = point[0] + 1/m * (y - point[1])
        return [x, y]

    x_min = -window.get_width()/2
    x_max = window.get_width()/2
    y_min = -window.get_height()/2
    y_max = window.get_height()/2
    # bottm left
    if point_area_code == 5:
        y = -window.get_height()/2
        x = point[0] + 1/m * (y - point[1])
        if x >= x_min and x <= x_max:
            return [x, y]

        x = -window.get_width()/2
        y = m * (x - point[0]) + point[1]
        if y >= y_min and y <= x_max:
            return [x, y]

    # top left
    if point_area_code == 9:
        y = window.get_height()/2
        x = point[0] + 1/m * (y - point[1])
        if x >= x_min and x <= x_max:
            return [x, y]

        x = -window.get_width()/2
        y = m * (x - point[0]) + point[1]
        if y >= y_min and y <= x_max:
            return [x, y]

    # top right
    if point_area_code == 10:
        y = window.get_height()/2
        x = point[0] + 1/m * (y - point[1])
        if x >= x_min and x <= x_max:
            return [x, y]

        x = window.get_width()/2
        y = m * (x - point[0]) + point[1]
        if y >= y_min and y <= x_max:
            return [x, y]

    # bottom right
    if point_area_code == 6:
        y = -window.get_height()/2
        x = point[0] + 1/m * (y - point[1])
        if x >= x_min and x <= x_max:
            return [x, y]

        x = window.get_width()/2
        y = m * (x - point[0]) + point[1]
        if y >= y_min and y <= x_max:
            return [x, y]

def should_discart(p1, p2, window):
    p1_area_code = point_area_code(p1, window)
    p2_area_code = point_area_code(p2, window)

    if p1_area_code & p2_area_code == 0:
        return False
    return True

def point_area_code(point, window):
    area_code = 0
    x_min = -window.get_width()/2
    x_max = window.get_width()/2
    y_min = -window.get_height()/2
    y_max = window.get_height()/2

    if point[0] < x_min:
        area_code = area_code | 1
    elif point[0] > x_max:
        area_code = area_code | 2
    if point[1] < y_min:
        area_code = area_code | 4
    elif point[1] > y_max:
        area_code = area_code | 8

    return area_code