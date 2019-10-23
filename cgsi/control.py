import copy

import cairo
import math
import numpy as np
from gi.repository import Gdk

import shapes
import transformations as trans
import window as wind
from obj_descriptor import OBJDescriptor


class control:
    def __init__(self):
        self.window = wind.window(600, 400)
        self.obj_list = {}
        self.ppc_list = {}
        self.ppc_translation_matrix = np.matrix([ [1, 0, 0],
                                                [0, 1, 0],
                                                [0, 0, 1]])
        self.descriptor = OBJDescriptor()

    def zoom(self, ammount):
        self.window.zoom(ammount)

    def up(self, ammount):
        self.window.down(ammount)
        self.calculate_ppc()

    def down(self, ammount):
        self.window.up(ammount)
        self.calculate_ppc()

    def left(self, ammount):
        self.window.left(ammount)
        self.calculate_ppc()

    def right(self, ammount):
        self.window.right(ammount)
        self.calculate_ppc()

    def rotate_window(self, angle):

        # find matrix to translate it to point
        # rotate matrix on center
        change_matrix = trans.matrix_rotation(angle, self.window.center)
        # update coordinates after window rotation
        trans.change_coordinates([self.window.center, self.window.v_up], change_matrix)
        self.calculate_ppc()

    def calculate_ppc(self):
        # atualiza todas a cordenadas para lidar com projeçao e rotacao

        # calcular matrizes de translaçao. back to place won~t be used
        change_matrix = trans.matrix_translate(-self.window.center[0], -self.window.center[1])
        self.ppc_translation_matrix = np.matmul(self.ppc_translation_matrix, change_matrix)

        # ver se eh paralelo ao eixo Y

        y_axis_x = 0
        y_axis_y = 1
        y_axis_z = 0
        vp_x = self.window.v_up[0]
        vp_y = self.window.v_up[1]
        vp_z = 0

        angle = angle_between(
            (y_axis_x, y_axis_y, y_axis_z), (vp_x, vp_y, vp_z)
        )
        angle = np.degrees(angle)
        if angle != 0:
            rotation_matrix = trans.matrix_rotation(-angle, [0,0])
            change_matrix = np.matmul(change_matrix, rotation_matrix)
            result = np.matmul([[self.window.v_up[0], self.window.v_up[1], 1]], rotation_matrix)
            self.window.v_up[0] = result[0, 0]
            self.window.v_up[1] = result[0, 1]

        # calcular window com pcc
        self.window.center = [0, 0]
        # atualizar todas as informaçoes
        for obj in self.obj_list:
            if obj in self.ppc_list:
                trans.change_coordinates(self.ppc_list[obj], change_matrix)
            else:
                coordinates = copy.deepcopy(self.obj_list[obj].coordinates)
                trans.change_coordinates(coordinates, self.ppc_translation_matrix)
                self.ppc_list[obj] = coordinates

    def draw_all(self, drawing_area, context):
        for obj in self.obj_list: # future change to check alter egos
            self.draw_shape(obj, drawing_area, context)

        self.draw_border(drawing_area, context)

    def draw_border(self, drawing_area, context):
        max_height = self.window.height
        max_width = self.window.width
        border_size = self.window.border_size
        border_coordinates = [
            [border_size, border_size],
            [border_size, max_height - border_size],
            [max_width - border_size, max_height - border_size],
            [max_width - border_size, border_size]
        ]
        self.draw_coordinates(border_coordinates, drawing_area, context)

    def draw_shape(self, obj_name, drawing_area, context):
        # to do: clippin here - before getting the object or calculating it's ppc
        obj = self.obj_list[obj_name]
        coordinates = copy.deepcopy(self.ppc_list[obj_name])
        coordinates = self.to_viewport(coordinates, drawing_area)
        self.draw_coordinates(coordinates, drawing_area, context, obj.rgba)

    def draw_coordinates(self, coordinates, drawing_area, context, rgba=(0,0,0,1)):

        # getting screen convertions and then viewport convertions


        # set line's color
        context.set_source_rgba(
            rgba[0], rgba[1], rgba[2], rgba[3]
        )
        # draw coordinates on viewport, it's an array of doubles
        context.new_path()
        # first point
        context.move_to(coordinates[0][0], coordinates[0][1])
        last_point = coordinates[0][0], coordinates[0][1]

        # all points in middle  
        for i in range(1, len(coordinates)):
            last_point = coordinates[i-1][0], coordinates[i-1][1]
            next_point = coordinates[i][0], coordinates[i][1]
            discart = self.should_discart(last_point, next_point)
            if discart:
                continue

            last_point, next_point = self.clip_points(last_point, next_point)
            context.move_to(last_point[0], last_point[1])
            context.line_to(next_point[0], next_point[1])
            # print(str(coordinates[i][0]) + " " + str(coordinates[i][1]))
        # last point to first
        next_point = (coordinates[0][0], coordinates[0][1])
        last_point = coordinates[-1][0], coordinates[-1][1]
        discart = self.should_discart(last_point, next_point)
        if not discart:
            last_point, next_point = self.clip_points(last_point, next_point)
            context.move_to(last_point[0], last_point[1])
            context.line_to(next_point[0], next_point[1])

        context.stroke()

    def clip_points(self, p1, p2):
        p1_area_code = self.point_area_code(p1)
        p2_area_code = self.point_area_code(p2)

        if p1_area_code == 0 and p1_area_code == p2_area_code:
            return p1, p2

        m = (p2[1] - p1[1])/(p2[0] - p1[0])
        border_size = self.window.border_size
        if p1_area_code != 0:
            p1 = self.window_intersection(p1, p1_area_code, m)
        if p2_area_code != 0:
            p2 = self.window_intersection(p2, p2_area_code, m)
        return p1, p2

    def window_intersection(self, point, point_area_code, m):
        # left
        if point_area_code == 1:
            x = self.window.border_size
            y = m*(x - point[0]) + point[1]
            return (x, y)
        # up
        if point_area_code == 8:
            y = self.window.height - self.window.border_size
            x = point[0] + 1/m * (y - point[1])
            return (x, y)
        # right
        if point_area_code == 2:
            x = self.window.width - self.window.border_size
            y = m * (x - point[0]) + point[1]
            return (x, y)
        # down
        if point_area_code == 4:
            y = self.window.border_size
            x = point[0] + 1/m * (y - point[1])
            return (x, y)

    def should_discart(self, p1, p2):
        p1_area_code = self.point_area_code(p1)
        p2_area_code = self.point_area_code(p2)

        if p1_area_code & p2_area_code == 0:
            return False
        return True

    def point_area_code(self, point):
        area_code = 0
        x_min = self.window.border_size
        x_max = self.window.get_width() - self.window.border_size
        y_min = self.window.border_size
        y_max = self.window.get_height() - self.window.border_size

        if point[0] < x_min:
            area_code = area_code | 1
        elif point[0] > x_max:
            area_code = area_code | 2
        if point[1] < y_min:
            area_code = area_code | 4
        elif point[1] > y_max:
            area_code = area_code | 8

        return area_code

    def to_viewport(self, coordinates, drawing_area):
        xv_max = drawing_area.get_allocation().width
        xv_min = 0
        yv_max = drawing_area.get_allocation().height
        yv_min = 0
        xw_min = -self.window.get_width()/2
        xw_max = self.window.get_width()/2
        yw_min = -self.window.get_height()/2
        yw_max = self.window.get_height()/2

        for i, coordinate in enumerate(coordinates):
            xw = coordinate[0]
            yw = coordinate[1]
            # (X - Xwmin) * (Xvpmax - Xvpmin) / (Xwmax - Xwmin)
            coordinates[i][0] = (xw - xw_min) * (xv_max - xv_min) / (xw_max - xw_min)
            coordinates[i][1] = (1-((yw - yw_min)/(yw_max - yw_min))) * (yv_max - yv_min)

        #print(coordinates)
        return coordinates

    def create_shape(self, name, shape, coordinates, rgba=Gdk.RGBA(0, 0, 0, 1), step=0):
        ''' Create a shape and draw it according to it's ppc
        Args:
            name: name of the shape (as in the object's name)
            shape: what shape it belongs
            coordinates: points that discribe the shape
            rgba: object color
            step: used to render curves. set the step for the drawing
        '''

        rgba = rgba_to_tuple(rgba)
        if shape == "Ponto":
            obj = shapes.point(coordinates, rgba)
        elif shape == "Linha":
            obj = shapes.line(coordinates, rgba)
        elif shape == "Poligono":
            obj = shapes.polygon(coordinates, rgba)
        else:
            pass

        # add to display file
        self.obj_list[name] = obj
        self.calculate_ppc()

    def delete_shape(self, name):
        del self.obj_list[name]
        del self.ppc_list[name]

    def change_object(self, obj, change_matrix):
        trans.change_object(obj, change_matrix)
        # update ppc

    # def translate_scale_rotate(self, name, x,y, x_factor, y_factor, teta, point=[0,0]):
    #     # get object
    #     obj = self.obj_list[name]
    #     center = trans.find_center(obj)
    #     # find matrix to translate it to point
    #     to_center, back_to_place = trans.matrixes_obj_to_point(center, point)
    #     # apply all 3
    #     change_matrix = trans.matrix_rotation(to_center, teta)
    #     change_matrix = trans.matrix_scale(change_matrix, x_factor, y_factor)
    #     change_matrix = np.matmul(change_matrix, back_to_place)
    #     change_matrix = trans.matrix_translate(change_matrix, x, y)

        # update coordinates
        # self.change_object(obj, change_matrix)

    def rotate_object(self, name, teta, rotation, point=[0,0]):
        world_coordinates = self.obj_list[name].coordinates
        world_coordinates = self.rotate_coordinates(
            world_coordinates, teta, rotation, point
        )
        self.obj_list[name].coordinates = world_coordinates

        ppc_coordinates = self.ppc_list[name]
        point = [point]
        trans.change_coordinates(point, self.ppc_translation_matrix)
        self.ppc_list[name] = self.rotate_coordinates(
            ppc_coordinates, teta, rotation, point[0]
        )

    def rotate_coordinates(self, coordinates, teta, rotation, point):
        dummy_obj = shapes.shape(coordinates)

        if rotation == trans.ROTATE_AROUND_SELF:
            obj_center = trans.find_center(dummy_obj)
            change_matrix = trans.matrix_rotation(teta, obj_center)
        else:
            change_matrix = trans.matrix_rotation(teta, point)

        trans.change_object(dummy_obj, change_matrix)
        return dummy_obj.coordinates

    def scale_object(self, name, x, y):
        world_coordinates = self.obj_list[name].coordinates
        world_coordinates = self.scale_coordinates(world_coordinates, x, y)
        self.obj_list[name].coordinates = world_coordinates
        ppc_coordinates = self.ppc_list[name]
        self.ppc_list[name] = self.scale_coordinates(ppc_coordinates, x, y)

    def scale_coordinates(self, coordinates, x, y):
        coordinates = copy.deepcopy(coordinates)
        dummy_obj = shapes.shape(coordinates)
        change_matrix = trans.matrix_scale(dummy_obj, x, y)
        self.change_object(dummy_obj, change_matrix)
        return dummy_obj.coordinates

    def translate_object(self, name, x, y):
        world_coordinates = self.obj_list[name].coordinates
        world_coordinates = translate_coordinates(world_coordinates, x, y)
        self.obj_list[name].coordinates = world_coordinates
        ppc_coordinates = self.ppc_list[name]
        self.ppc_list[name] = translate_coordinates(ppc_coordinates, x, y)

    def export(self, path):
        for obj_name in self.obj_list:
            file_path = path + '/' + obj_name + '.obj'
            self.descriptor.write_obj(obj_name, self.obj_list[obj_name], file_path)

    def import_object(self, path):
        name, coordinates = self.descriptor.read_obj(path)
        if len(coordinates) == 1:
            shape = 'Ponto'
        elif len(coordinates) == 2:
            shape = 'Linha'
        else:
            shape = 'Poligono'
        self.create_shape(name, shape, coordinates)

def translate_coordinates(coordinates, x, y):
    coordinates = copy.deepcopy(coordinates)
    change_matrix = trans.matrix_translate(x, y)
    trans.change_coordinates(coordinates, change_matrix)
    return coordinates


def rgba_to_tuple(rgba):
    ''' Transforms a Gdk.RGBA object into a RGBA tuple.

    Args:
        rgba: Gdk.RGBA object.
    Returns:
        A tuple (R, G, B, A)
    '''
    return (rgba.red, rgba.green, rgba.blue, rgba.alpha)


def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::
            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    result = np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
    if (0 < (v1[0] * v2[1]) - (v1[1]* v2[0])):
        result *= -1
    return result

