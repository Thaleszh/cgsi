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

    def down(self, ammount):
        self.window.up(ammount)
        self.ppc_list = {}

    def left(self, ammount):
        self.window.left(ammount)
        self.ppc_list = {}

    def right(self, ammount):
        self.window.right(ammount)
        self.ppc_list = {}

    def rotate_window(self, angle):

        center = self.window.get_center()
        # print("center:")
        # print(center)
        # find matrix to translate it to point
        # rotate matrix on center
        print("angle:" + str(angle))
        change_matrix = trans.matrix_rotation(angle, [0,0])
        print("change matrix:")
        print(change_matrix)
        # update coordinates after window rotation
        print("center before:")
        print(self.window.get_center())
        trans.change_coordinates([self.window.position, self.window.view_up], change_matrix)
        print("center after:")
        print(self.window.get_center())
        self.calculate_ppc()


    def calculate_ppc(self):
        # atualiza todas a cordenadas para lidar com projeçao e rotacao
        
        # calcular matrizes de translaçao. back to place won~t be used
        change_matrix, back_to_place = trans.matrixes_obj_to_point(self.window.get_center(), [0,0])


        y_axis = [0, 1]
        up = self.window.view_up

        # ver se eh paralelo ao eixo Y

        # encontrar angulo entre vup e Y:
        # scalar_product(v1,v2)/(length(v1)*length(v2) == 1 se paralelo
        # dot = scalar product, lonalg.norm = length
        costeta = np.dot(y_axis, up) / (np.linalg.norm(y_axis) * np.linalg.norm(up))
        # print(costeta)
        # possivel de por uma tolerancia de erro com >= 1 - epsilon
        # se nao forem paralelos
        if costeta != 1:
            # calcular matrix com rotaçao
            teta = math.degrees(math.acos(costeta))
            if (0 < y_axis[0] * up[1] - y_axis[1] * up[0]):
            	teta *= -1
            print("degrees:" + str(teta % 360))
            change_matrix = np.matmul(change_matrix, trans.matrix_rotation(teta, [0,0]))

        self.ppc_matrix = change_matrix
        # calcular window com pcc
        result = np.matmul([[self.window.view_up[0], self.window.view_up[1], 1]], change_matrix)
        self.window.view_up_ppc[0] = result[0, 0]
        self.window.view_up_ppc[1] = result[0, 1]
        result = np.matmul([[self.window.position[0], self.window.position[1], 1]], change_matrix)
        self.window.position_ppc[0] = result[0, 0]
        self.window.position_ppc[1] = result[0, 1]
        print("position ppc:")
        print(self.window.position_ppc)
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
        da_width = drawing_area.get_allocation().width
        da_height = drawing_area.get_allocation().height

        for i, coordinate in enumerate(coordinates):
            # (X - Xwmin) * (Xvpmax - Xvpmin) / (Xwmax - Xwmin)
            coordinates[i][0] = ((coordinate[0] - self.window.position_ppc[0]) *
                                da_width / self.window.get_width())
            # (1 - (Y - Ywmin) / (Ywmax - Ywmin)) * (Yvpmax - Yvpmin)
            coordinates[i][1] = (1 - (coordinate[1] - self.window.position_ppc[1]) /
                                self.window.get_height()) * da_height

        return coordinates

    def create_shape(self, name, shape, coordinates, rgba=Gdk.RGBA(0, 0, 0, 1)):
        # check what object is to be made
        print("created object at:")
        print(coordinates)
        rgba = self.rgba_to_tuple(rgba)
        if shape == "Ponto":
            obj = shapes.point(coordinates, rgba)
        elif shape == "Linha":
            obj = shapes.line(coordinates, rgba)
        else:
            obj = shapes.polygon(coordinates, rgba)
        # add to display file
        self.obj_list[name] = obj
        # draw shape created

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

    def scale_object(self, name, x, y):
        obj = self.obj_list[name]
        change_matrix = trans.matrix_scale(obj, x, y)
        self.change_object(obj, change_matrix)


    def translate_object(self, name, x, y):
        change_matrix = trans.matrix_translate(x, y)
        self.change_object(self.obj_list[name], change_matrix)

    def rgba_to_tuple(self, rgba):
        ''' Transforms a Gdk.RGBA object into a RGBA tuple.

        Args:
            rgba: Gdk.RGBA object.
        Returns:
            A tuple (R, G, B, A)
        '''
        return (rgba.red, rgba.green, rgba.blue, rgba.alpha)
