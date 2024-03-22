from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Line, Color, Ellipse


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y


coordinates = [
    Coordinate(100, 100),
    Coordinate(800, 300),
    Coordinate(500, 200),
    Coordinate(200, 400),
    Coordinate(50, 400)
]


class LineDrawingApp(App):

    def draw_lines_and_dots(self, instance):
        with self.root.canvas:
            Color(1, 1, 1)  # Set color to white
            # Draw lines
            for i in range(len(coordinates) - 1):
                Line(points=[coordinates[i].x, coordinates[i].y,
                             coordinates[i + 1].x, coordinates[i + 1].y])
            # Draw dots
            for coordinate in coordinates:
                Ellipse(pos=(coordinate.x - 5, coordinate.y - 5), size=(10, 10))

    def build(self):
        self.root = BoxLayout(orientation='vertical', padding=10)

        self.draw_button = Button(text='Draw Lines and Dots')
        self.draw_button.bind(on_press=self.draw_lines_and_dots)
        self.root.add_widget(self.draw_button)

        return self.root


if __name__ == '__main__':
    LineDrawingApp().run()
