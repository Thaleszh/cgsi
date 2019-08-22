from gi.repository import Gtk
import cairo
import control as ct


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
        self.step_item = self.builder.get_object('step_item')
        self.drawing_area = self.builder.get_object('viewport')


        self.builder.connect_signals(self)
        self.main_window.connect('destroy', Gtk.main_quit)
        
        # init do controle
        # self.control = control.control(drawing_area, context)
        self.control = ct.control()
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
        for arg in args:
            print('add_object ' + name)
        tab = self.builder.get_object("object_tab")
        page = tab.get_current_page()

        coordinates = []
        if page == 0:
            shape = "point"
            x_entry = self.builder.get_object("x_point")
            y_entry = self.builder.get_object("y_point")

            coordinates = [[int(x_entry.get_text()), int(y_entry.get_text())]]
        elif page == 1:
            shape = "line"
            x1_entry = self.builder.get_object("x1_line")
            y1_entry = self.builder.get_object("y1_line")
            x2_entry = self.builder.get_object("x2_line")
            y2_entry = self.builder.get_object("y2_line")
            coordinates = [[int(x1_entry.get_text()), int(y1_entry.get_text())],
                            [int(x2_entry.get_text()), int(y2_entry.get_text())] ]
        else:
            shape = "poli"
            x_entry = self.builder.get_object("x_poli")
            y_entry = self.builder.get_object("y_poli")
            # removes spaces and splits on commas
            x_entries = x_entry.get_text().replace(" ", "").split(",")
            y_entries = y_entry.get_text().replace(" ", "").split(",")
            #parse
            for x, y in zip(x_entries, y_entries):
                coordinates.append([int(x), int(y)])

        self.control.create_shape(name, shape, coordinates)
        # to do: resetar campos
        # fecha janela
        self.cancel(self.add_object_window)
        self.refresh()



    def modify_item(self, *args):
        """
        (invisivel, entrega II)
        abrir modification_dialog
        """

        # resetar campos
        self.modification_dialog.show()

    # ModificationDialogHandler
    def modify(self, *args):
        """
        pega valores de x_translation, y_translation, x_scale, y_scale e angle_entry
        faz uma matriz com as modifcaçoes disso
        aplica matriz ao objeto do tree_view_object_list selecionado
        refresh na tela
        (fecha aba? pode deixar aberto pra por de lado e modificar de novo)
        """
        for arg in args:
            print('modify')
        self.refresh()


def run():
    UI()
    Gtk.main()


if __name__ == '__main__':
    run()
