from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Line, Color
import time

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y




coordinates = [
            Coordinate(100, 100),
            Coordinate(800, 300),
            Coordinate(500, 200),
            Coordinate(200, 400)
        ]


class LineDrawingApp(App):


    def draw_line(self, instance):
        with self.root.canvas:
            Color(1, 1, 1)  # Set color to white
            for i in range(len(coordinates) - 1):
                # Draw lines connecting coordinates
                Line(points=[coordinates[i].x, coordinates[i].y,
                             coordinates[i + 1].x, coordinates[i + 1].y])
                

    def build(self):
        self.root = BoxLayout(orientation='vertical', padding=10)
        
        self.draw_button = Button(text='Draw Lines')
        self.draw_button.bind(on_press=self.draw_line)
        self.root.add_widget(self.draw_button)

        return self.root


if __name__ == '__main__':
    LineDrawingApp().run()
