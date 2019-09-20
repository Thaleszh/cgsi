import copy

import cairo
import math
import numpy as np
from gi.repository import Gdk

import shapes
import transformations as trans
import window as wind


class control:
    def __init__(self):
        self.window = wind.window(600, 400)
        self.obj_list = {}
        self.ppc_list = {}
        self.ppc_matrix = np.matrix([ [1, 0, 0],
                                      [0, 1, 0],
                                      [0, 0, 1]])

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
        print(angle)
        trans.change_coordinates([self.window.center, self.window.v_up], change_matrix)
        self.calculate_ppc()

    def calculate_ppc(self):
        # atualiza todas a cordenadas para lidar com projeçao e rotacao
        
        # calcular matrizes de translaçao. back to place won~t be used
        change_matrix = trans.matrix_translate(-self.window.center[0], -self.window.center[1])

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


        self.ppc_matrix = np.matmul(self.ppc_matrix, change_matrix)
        # calcular window com pcc
        self.window.center = [0, 0]
        # atualizar todas as informaçoes -> deletar todos os ppc calculados
        self.ppc_list = {}
        # atualizar pccs com draw all

    def draw_all(self, drawing_area, context):
        for obj in self.obj_list: # future change to check alter egos
            self.draw_shape(obj, drawing_area, context)

    def draw_shape(self, obj_name, drawing_area, context):
        # to do: clippin here - before getting the object or calculating it's ppc
        obj = self.obj_list[obj_name]
        if obj_name in self.ppc_list:
            coordinates = copy.deepcopy(self.ppc_list[obj_name])
        else:
            # apply ppc matrix
            coordinates = copy.deepcopy(obj.coordinates)
            trans.change_coordinates(coordinates, self.ppc_matrix)
            # talves n precise desse deep copy
            self.ppc_list[obj_name] = copy.deepcopy(coordinates)

        # getting screen convertions and then viewport convertions

        coordinates = self.to_viewport(coordinates, drawing_area)

        # set line's color
        context.set_source_rgba(
            obj.rgba[0], obj.rgba[1], obj.rgba[2], obj.rgba[3]
        )
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
        xv_max = drawing_area.get_allocation().width
        xv_min = 0
        yv_max = drawing_area.get_allocation().height
        yv_min = 0
        xw_min = -self.window.get_height()/2
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

    def create_shape(self, name, shape, coordinates, rgba=Gdk.RGBA(0, 0, 0, 1)):
        # check what object is to be made
        # print("created object at:")
        # print(coordinates)
        rgba = self.rgba_to_tuple(rgba)
        if shape == "Ponto":
            obj = shapes.point(coordinates, rgba)
        elif shape == "Linha":
            obj = shapes.line(coordinates, rgba)
        else:
            obj = shapes.polygon(coordinates, rgba)
    
        # add to display file
        self.obj_list[name] = obj

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
        obj = self.obj_list[name]

        if rotation == trans.ROTATE_AROUND_SELF:
            obj_center = trans.find_center(obj)
            change_matrix = trans.matrix_rotation(teta, obj_center)
        elif rotation == trans.ROTATE_AROUND_CENTER:
            change_matrix = trans.matrix_rotation(teta, (0, 0))
        elif rotation == trans.ROTATE_AROUND_POINT:
            change_matrix = trans.matrix_rotation(teta, point)

        self.change_object(obj, change_matrix)
        self.ppc_list = {}

    def scale_object(self, name, x, y):
        obj = self.obj_list[name]
        change_matrix = trans.matrix_scale(obj, x, y)
        self.change_object(obj, change_matrix)
        self.ppc_list = {}

    def translate_object(self, name, x, y):
        change_matrix = trans.matrix_translate(x, y)
        ppc_coordinates = self.ppc_list[name]
        trans.change_coordinates(ppc_coordinates, change_matrix)
        world_coordinates = self.ppc_to_world(ppc_coordinates)
        self.obj_list[name].coordinates = world_coordinates
        self.ppc_list = {}

    def ppc_to_world(self, ppc_coordinates):
        inversed_matrix = np.linalg.inv(self.ppc_matrix)
        coordinates = copy.deepcopy(ppc_coordinates)
        trans.change_coordinates(coordinates, inversed_matrix)
        return coordinates


    def rgba_to_tuple(self, rgba):
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
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))