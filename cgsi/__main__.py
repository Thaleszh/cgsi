from textwrap import dedent

import cairo
from gi.repository import Gtk

import control as ct
import transformations as trans


class UI:
    def __init__(self):
        # builder.add_from_file('cgsi/add_obj_window.glade')
        # builder.add_from_file('cgsi/obj_right_click_menu.glade')
        # builder.add_from_file('cgsi/modification_dialog.glade')
        self.builder = Gtk.Builder()
        self.builder.add_from_file('cgsi/cgsi_1.glade')

        self.add_object_window = self.builder.get_object('add_obj_window')
        self.modification_dialog = self.builder.get_object('modification_dialog')
        self.main_window = self.builder.get_object('application_window')
        self.warning_dialog = self.builder.get_object('warning_dialog')
        self.step_item = self.builder.get_object('step_item')
        self.drawing_area = self.builder.get_object('viewport')
        self.list = self.builder.get_object('object_list')
        self.tree_view = self.builder.get_object('tree_view_object_list')
        self.file_chooser_window = self.builder.get_object('file_chooser')
        self.import_file_chooser_window = self.builder.get_object('import_file_chooser')

        self.builder.connect_signals(self)
        self.main_window.connect('destroy', Gtk.main_quit)

        # init do controle
        # self.control = control.control(drawing_area, context)
        self.control = ct.control()
        self.control.calculate_ppc()

        self.control.create_shape("start 1", "Poligono", [ [200, 200],[300, 200], [300, 300], [200,300]])
        self.list.append(["start 1", "Poligono"])
        self.control.create_shape("start 2", "Poligono", [ [100, 200],[150, 200], [150, 250], [100,250]])
        self.list.append(["start 2", "Poligono"])
        self.control.create_shape("start 3", "Linha", [ [10, 10],[50, 50] ])
        self.list.append(["start 3", "Linha"])

        self.control.scale_object("start 1", 2, 1)
        self.control.rotate_object("start 1", 90, trans.ROTATE_AROUND_SELF)

        # self.control.rotate_window(-45)

        self.main_window.show()

    # WindowHandler
    def cancel(self, *args):
        """
        fecha janela enviada
        """
        for arg in args:
            arg.hide()

    # ApplicationHandler
    def zoom_in(self, *args):
        """
        pegar % de zoom do step_item
        aplicar zoom na conversao da jabela(usa um zoom_factor no intermedio)
        """
        text = self.step_item.get_text()
        self.control.zoom(1 + int(text)/100)
        self.refresh()

    def zoom_out(self, *args):
        """
        pegar % de zoom do step_item
        aplicar zoom na conversao da jabela(usa um zoom_factor no intermedio)
        """
        text = self.step_item.get_text()
        self.control.zoom(1 - int(text)/100)
        self.refresh()

    def up_but_clicked(self, *args):
        """
        pegar valor do step_item
        aplicar movimentaçao na janela
        dar refresh no draw_area(faz uma funcao refresh pra isso)
        """
        text = self.step_item.get_text()
        self.control.up(int(text))
        self.refresh()

    def down_but_clicked(self, *args):
        """
        pegar valor do step_item
        aplicar movimentaçao na janela
        dar refresh no draw_area(faz uma funcao refresh pra isso)
        """
        text = self.step_item.get_text()
        self.control.down(int(text))
        self.refresh()


    def left_but_clicked(self, *args):
        """
        pegar valor do step_item
        aplicar movimentaçao na janela
        dar refresh no draw_area(faz uma funcao refresh pra isso)
        """
        text = self.step_item.get_text()
        self.control.left(int(text))
        self.refresh()


    def right_but_clicked(self, *args):
        """
        pegar valor do step_item
        aplicar movimentaçao na janela
        dar refresh no draw_area(faz uma funcao refresh pra isso)
        """
        text = self.step_item.get_text()
        self.control.right(int(text))
        self.refresh()

    def object_clicked(self, treeview, event):
        """
        verifica se botao direito (== 3)
        abre um popup com o obj_right_click_menu
        """
        if event.button != 3:
            return
        self.right_click_menu = self.builder.get_object('obj_right_click_menu')
        self.right_click_menu.popup(None, None, None, None, event.button, event.time)



    def object_click(self, treeview, event):
        """
        verifica se botao direito (== 3)
        abre um popup com o obj_right_click_menu
        """
        if event.button != 3:
            return
        for arg in args:
            print('object_clicked')

    def draw(self, drawing_area, context):
        self.control.draw_all(drawing_area, context)

    def refresh(self):
    	self.drawing_area.queue_draw()

    # ObjectRightClickMenuHandler
    def delete_item(self, *args):
        """
        pegar o item em foco na tree_view_object_list
        deletar o item
        atualizar tela e lista
        """
        for arg in args:
            print('delete_item')
        (model, it) = self.tree_view.get_selection().get_selected_rows()
        iterator = model.get_iter(it[0])
        name = model.get_value(iterator, 0)
        model.remove(iterator)
        self.control.delete_shape(name)
        self.refresh()

    def create_item(self, *args):
        """
        abrir add_obj_window
        """

        self.add_object_window.show()

    # AddObjectHandler
    def add_object(self, *args):
        """
        Pegar nome de "name_entry" da add_obj_window
        Ver qual aba esta selecionada no obj_tab, em ordem sao: Ponto, linha e poligono.
        Pegar x_poinjt, y_point se for um ponto
        Pegar x1_line, x2_line, y1_line e y2_line se for uma reta
        Pegar string x_poli, y_poli se for um poligono. Pode decidir como tratamos a string
        gerar objeto na lista e adicionar um objeto na object_list, com nome ou tipo. Ou so dar um refresh
        fecha add_obj_window
        """
        name_entry = self.builder.get_object("name_entry")
        name = name_entry.get_text()
        if name in self.control.obj_list:
            return self.show_warning(
                'Nome inválido',
                'Um objeto come esse nome já existe'
            )
        color_rgba = self.builder.get_object('add_obj_color').get_rgba()

        for arg in args:
            print('add_object ' + name)
        tab = self.builder.get_object("object_tab")
        page = tab.get_current_page()

        coordinates = []
        if page == 0:
            shape = "Ponto"
            x_entry = self.builder.get_object("x_point")
            y_entry = self.builder.get_object("y_point")

            coordinates = [[int(x_entry.get_text()), int(y_entry.get_text())]]
            self.control.create_shape(name, shape, coordinates, color_rgba)

        elif page == 1:
            shape = "Linha"
            x1_entry = self.builder.get_object("x1_line")
            y1_entry = self.builder.get_object("y1_line")
            x2_entry = self.builder.get_object("x2_line")
            y2_entry = self.builder.get_object("y2_line")
            coordinates = [[int(x1_entry.get_text()), int(y1_entry.get_text())],
                            [int(x2_entry.get_text()), int(y2_entry.get_text())] ]
            self.control.create_shape(name, shape, coordinates, color_rgba)

        elif page == 2:
            shape = "Poligono"
            coordinates = self.read_coordinates('poli')
            self.control.create_shape(name, shape, coordinates, color_rgba)

        elif page == 3:
            shape = "Bezier"
            coordinates = self.read_coordinates('bezier')
            if len(coordinates) < 4 or (len(coordinates) - 4) % 3 != 0:
                return self.show_warning(
                    'Número de coordenadas incorreto',
                    dedent(
                        '''
                        Uma curva de Bezier possui no mínimo 4 pontos. 
                        Para adicionar mais curvas com continuidade 0,
                        adicione os 4 pontos da primeira curva e depois os
                        pontos 2, 3 e 4 das próximas, o ponto 1 será o ponto
                        4 da curva anterior.
                        '''
                    )
                )

            step_entry = self.builder.get_object("step_bezier")
            step = float(step_entry.get_text())
            self.control.create_shape(
                name, shape, coordinates, color_rgba, step
            )

        else:
            shape = 'Spline'
            coordinates = self.read_coordinates('spline')
            if len(coordinates) < 4:
                return self.show_warning(
                    'Número de coordenadas incorreto',
                    'Splines precisam de pelo menos 4 pontos de controle'
                )

            self.control.create_shape(
                name, shape, coordinates, color_rgba
            )

        self.list.append([name, shape])
        # to do: resetar campos
        # fecha janela
        self.cancel(self.add_object_window)
        self.refresh()

    def read_coordinates(self, label: str):
        ''' Reads coordinates x, y from input and create a list.
        GTKEntry object must be named in the format 'coordinate_label'.
        Ex: 'x_poli'
        
        Args:
            label: label to be concatenated with the coordinate and underscore
        Returns:
            List of lists w/ point's coordinates
        '''
        x_entry = self.builder.get_object("x_{}".format(label))
        y_entry = self.builder.get_object("y_{}".format(label))
        
        # removes spaces and splits on commas
        x_entries = x_entry.get_text().replace(" ", "").split(",")
        y_entries = y_entry.get_text().replace(" ", "").split(",")
        
        #parse    
        return [[int(x), int(y)] for x, y in zip(x_entries, y_entries)]

    def modify_item(self, *args):
        """
        (invisivel, entrega II)
        abrir modification_dialog
        """

        # resetar campos
        self.modification_dialog.show()

    def select_export(self, *args):
        self.file_chooser_window.show()

    def select_import(self, *args):
        self.import_file_chooser_window.show()

    # ModificationDialogHandler
    def modify(self, *args):
        """
        pega valores de x_translation, y_translation, x_scale, y_scale e angle_entry
        faz uma matriz com as modifcaçoes disso
        aplica matriz ao objeto do tree_view_object_list selecionado
        refresh na tela
        (fecha aba? pode deixar aberto pra por de lado e modificar de novo)
        """
        (model, it) = self.tree_view.get_selection().get_selected_rows()
        iterator = model.get_iter(it[0])
        name = model.get_value(iterator, 0)

        modification_tab = self.builder.get_object('modification_tab')
        page = modification_tab.get_current_page()
        if page == 0:
            x = int(self.builder.get_object("translation_x").get_text())
            y = int(self.builder.get_object("translation_y").get_text())
            self.control.translate_object(name, x, y)
        elif page == 1:
            x = float(self.builder.get_object("scale_x").get_text().replace(',', '.'))
            y = float(self.builder.get_object("scale_y").get_text().replace(',', '.'))
            self.control.scale_object(name, x, y)
        elif page == 2:
            angle = int(self.builder.get_object("rotation_angle").get_text())

            around_self = self.builder.get_object("rotation_self").get_active()
            around_center = self.builder.get_object("rotation_center").get_active()
            around_point = self.builder.get_object("rotation_point").get_active()
            if around_self:
                self.control.rotate_object(name, angle, trans.ROTATE_AROUND_SELF)
            elif around_center:
                self.control.rotate_object(name, angle, trans.ROTATE_AROUND_CENTER)
            elif around_point:
                x = int(self.builder.get_object("rotation_x").get_text())
                y = int(self.builder.get_object("rotation_y").get_text())
                self.control.rotate_object(
                    name, angle, trans.ROTATE_AROUND_POINT, [x, y]
                )

        self.refresh()

    def rotate_right(self, *args):
        text = self.step_item.get_text()
        self.control.rotate_window(int(text))
        self.refresh()

    def rotate_left(self, *args):
        text = self.step_item.get_text()
        self.control.rotate_window(-1 * int(text))
        self.refresh()

    def show_warning(self, title, text):
        title_label = self.builder.get_object('warning_dialog_title')
        title_label.set_text(title)
        text_label = self.builder.get_object('warning_dialog_text')
        text_label.set_text(text)
        self.warning_dialog.show()

    def select_path(self, title, text):
        file_path = self.file_chooser_window.get_current_folder()
        text_label = self.builder.get_object('file_path')
        text_label.get_buffer().set_text(file_path)

    def select_file_path(self, title, text):
        file_path = self.import_file_chooser_window.get_uri()
        text_label = self.builder.get_object('import_file_path')
        text_label.get_buffer().set_text(file_path[7:])

    def export(self, text_view):
        buffer = text_view.get_buffer()
        start_iter = buffer.get_start_iter()
        end_iter = buffer.get_end_iter()
        text = buffer.get_text(start_iter, end_iter, True)
        self.control.export(text)

    def import_object(self, text_view):
        buffer = text_view.get_buffer()
        start_iter = buffer.get_start_iter()
        end_iter = buffer.get_end_iter()
        text = buffer.get_text(start_iter, end_iter, True)
        text = text.replace("%20", " ")
        self.control.import_object(text)

def run():
    UI()
    Gtk.main()


if __name__ == '__main__':
    run()
