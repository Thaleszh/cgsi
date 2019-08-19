from gi.repository import Gtk
import cairo
import control


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


        self.builder.connect_signals(self)
        self.main_window.connect('destroy', Gtk.main_quit)
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
        for arg in args:
            print('zoom_in ' + text)

    def zoom_out(self, *args):
        """
        pegar % de zoom do step_item
        aplicar zoom na conversao da jabela(usa um zoom_factor no intermedio)
        """
        text = self.step_item.get_text()
        for arg in args:
            print('zoom_out')

    def up_but_clicked(self, *args):
        """
        pegar valor do step_item
        aplicar movimentaçao na janela
        dar refresh no draw_area(faz uma funcao refresh pra isso)
        """
        text = self.step_item.get_text()
        for arg in args:
            print('up_but_clicked')

    def down_but_clicked(self, *args):
        """
        pegar valor do step_item
        aplicar movimentaçao na janela
        dar refresh no draw_area(faz uma funcao refresh pra isso)
        """
        text = self.step_item.get_text()
        for arg in args:
            print('down_but_clicked')

    def left_but_clicked(self, *args):
        """
        pegar valor do step_item
        aplicar movimentaçao na janela
        dar refresh no draw_area(faz uma funcao refresh pra isso)
        """
        text = self.step_item.get_text()
        for arg in args:
            print('left_but_clicked')

    def right_but_clicked(self, *args):
        """
        pegar valor do step_item
        aplicar movimentaçao na janela
        dar refresh no draw_area(faz uma funcao refresh pra isso)
        """
        text = self.step_item.get_text()
        for arg in args:
            print('right_but_clicked')

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
            print('delete_item')

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
        Pegar x_entry, y_entry se for um ponto
        Pegar x1_line, x2_line, y1_line e y2_line se for uma reta
        Pegar string x_poli, y_poli se for um poligono. Pode decidir como tratamos a string
        gerar objeto na lista e adicionar um objeto na object_list, com nome ou tipo. Ou so dar um refresh
        fecha add_obj_window
        """
        name_entry = self.builder.get_object("name_entry")
        name = name_entry.get_text()
        for arg in args:
            print('add_object ' + name)
        self.cancel(self.add_object_window)


    def modify_item(self, *args):
        """
        (invisivel, entrega II)
        abrir modification_dialog
        """
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


def run():
    UI()
    Gtk.main()


if __name__ == '__main__':
    run()
