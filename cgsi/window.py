class window:
    def __init__(self, width, height, border_size = 10):
        self.width = width
        self.height = height
        self.center = [width/2, height/2]
        self.v_up = [0.0, height]
        self.scale = 1.0

    def up(self, ammount):
        self.center[1] -= ammount

    def down(self, ammount):
        self.center[1] += ammount

    def left(self, ammount):
        self.center[0] -= ammount

    def right(self, ammount):
        self.center[0] += ammount

    def zoom(self, ammount):
        self.scale *= ammount

    def get_width(self):
        return self.width / self.scale

    def get_height(self):
        return self.height / self.scale

    def limits(self):
        x_min = -self.get_width()/2
        x_max = self.get_width()/2
        y_min = -self.get_height()/2
        y_max = self.get_height()/2

        return x_min, y_min, x_max, y_max
