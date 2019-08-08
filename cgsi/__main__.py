from gi.repository import Gtk
import cairo
import control


class UI:
    def __init__(self):
        # builder.add_from_file('pytaca/add_obj_window.glade')
        # builder.add_from_file('pytaca/obj_right_click_menu.glade')
        # builder.add_from_file('pytaca/modification_dialog.glade')
        builder = Gtk.Builder()
        builder.add_from_file('pytaca/pytaca_1.glade')

        # self.add_object_window = builder.get_object('add_obj_window')
        self.right_click_menu = builder.get_object('obj_right_click_menu')
        # self.modification_dialog = builder.get_object('modification_dialog')
        self.main_window = builder.get_object('applicationwindow')

        # builder.connect_signals(self)
        self.main_window.connect('destroy', Gtk.main_quit)
        self.main_window.show()

    # WindowHandler
    def cancel(self, *args):
        """
        fecha janela enviada
        """
        for arg in args:
            print('cancel', arg, ', '.join(dir(arg)))

    # AddObjectHandler
    def add_object(self, *args):
        """
        Pegar nome de "name_entry" da add_obj_window
        Ver qual aba esta selecionada no obj_tab, em ordem sao: Ponto, linha e poligono.
        Pegar x_entry, y_entry se for um ponto
        Pegar x1_line, x2_line, y1_line e y2_line se for uma reta
        Pegar string x_poli, y_poli se for um poligono. Pode decidir como tratamos a string
        gerar objeto na lista e adicionar um objeto na object_list, com nome ou tipo. Ou so dar um refresh
        fecha add_obj_window
        """
        for arg in args:
            print('add_object', arg, ', '.join(dir(arg)))

    # ApplicationHandler
    def zoom_in(self, *args):
        """
        pegar % de zoom do step_item
        aplicar zoom na conversao da jabela(usa um zoom_factor no intermedio)
        """
        for arg in args:
            print('zoom_in', arg, ', '.join(dir(arg)))

    def zoom_out(self, *args):
        """
        pegar % de zoom do step_item
        aplicar zoom na conversao da jabela(usa um zoom_factor no intermedio)
        """
        for arg in args:
            print('zoom_out', arg, ', '.join(dir(arg)))

    def up_but_clicked(self, *args):
        """
        pegar valor do step_item
        aplicar movimentaçao na janela
        dar refresh no draw_area(faz uma funcao refresh pra isso)
        """
        for arg in args:
            print('up_but_clicked', arg, ', '.join(dir(arg)))

    def down_but_clicked(self, *args):
        """
        pegar valor do step_item
        aplicar movimentaçao na janela
        dar refresh no draw_area(faz uma funcao refresh pra isso)
        """
        for arg in args:
            print('down_but_clicked', arg, ', '.join(dir(arg)))

    def left_but_clicked(self, *args):
        """
        pegar valor do step_item
        aplicar movimentaçao na janela
        dar refresh no draw_area(faz uma funcao refresh pra isso)
        """
        for arg in args:
            print('left_but_clicked', arg, ', '.join(dir(arg)))

    def right_but_clicked(self, *args):
        """
        pegar valor do step_item
        aplicar movimentaçao na janela
        dar refresh no draw_area(faz uma funcao refresh pra isso)
        """
        for arg in args:
            print('right_but_clicked', arg, ', '.join(dir(arg)))

    def object_clicked(self, treeview, event):
        """
        verifica se botao direito (== 3)
        abre um popup com o obj_right_click_menu
        """
        if event.button != 3:
            return 
        right_click_menu.set_relative_to(event)
        right_click_menu.show_all()
        right_click_menu.popup()

    def draw(self, drawing_area, context):
        context.set_source_rgb(1, 1, 0)
        context.arc(320, 240, 100, 0, 2*3.1416)
        context.fill_preserve()

        context.set_source_rgb(0, 0, 0)
        context.stroke()

        context.arc(280, 210, 20, 0, 2*3.1416)
        context.arc(360, 210, 20, 0, 2*3.1416)
        context.fill()

        context.set_line_width(10)
        context.set_line_cap(cairo.LINE_CAP_ROUND)
        context.arc(320, 240, 60, 3.1416/4, 3.1416*3/4)
        context.stroke()

    # ObjectRightClickMenuHandler
    def delete_item(self, *args):
        """
        pegar o item em foco na tree_view_object_list
        deletar o item
        atualizar tela e lista
        """
        for arg in args:
            print('delete_item', arg, ', '.join(dir(arg)))

    def create_item(self, *args):
        """
        abrir add_obj_window
        """
        for arg in args:
            print('create_item', arg, ', '.join(dir(arg)))

    def modify_item(self, *args):
        """
        (invisivel, entrega II)
        abrir modification_dialog
        """
        for arg in args:
            print('modify_item', arg, ', '.join(dir(arg)))

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
            print('modify', arg, ', '.join(dir(arg)))


def run():
    UI()
    Gtk.main()


if __name__ == '__main__':
    run()
