from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line
from kivy.properties import NumericProperty

class Speedometer(Widget):
    value = NumericProperty(0)

    def __init__(self, **kwargs):
        super(Speedometer, self).__init__(**kwargs)
        self.bind(pos=self.update_canvas, size=self.update_canvas, value=self.update_canvas)
        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(0.2, 0.2, 0.2)
            Ellipse(pos=self.pos, size=self.size, angle_start=0, angle_end=360)
            Color(1, 0, 0)
            Line(circle=(self.center_x, self.center_y, self.width / 2, 0, 360), width=2)
            Color(0, 1, 0)
            Line(circle=(self.center_x, self.center_y, self.width / 2, 0, self.value * 3.6), width=4)