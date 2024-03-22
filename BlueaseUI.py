from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
from BluEase import BluEase

class SpotButton(Button):
    def __init__(self, spot_name, **kwargs):
        super(SpotButton, self).__init__(**kwargs)
        self.spot = bluease.get_spot_info(spot_name)

        self.text = f'{self.spot.get_name()}'
        self.pos = self.spot.get_pos()

    def on_press(self):
        # Show popup with blank image and two buttons
        content = BoxLayout(orientation='vertical', spacing=10)
        blank_image = Image(source='', size_hint=(1, 0.8), allow_stretch=True)
        button1 = Button(text='Button 1', size_hint_y=None, height=50)
        button2 = Button(text='Button 2', size_hint_y=None, height=50)

        content.add_widget(blank_image)
        content.add_widget(button1)
        content.add_widget(button2)
        popup = Popup(title=f'{self.spot.get_name()} Popup', content=content, size_hint=(0.8, 0.6))
        popup.open()

class SearchPopup(Popup):
    def __init__(self, **kwargs):
        super(SearchPopup, self).__init__(**kwargs)
        content = BoxLayout(orientation='vertical', spacing=10)
        text_input = TextInput(hint_text='Type here', multiline=False)
        search_button = Button(text='Search', on_press=self.dismiss, size_hint=(None, None), size=(100, 50))
        content.add_widget(text_input)
        content.add_widget(search_button)
        self.content = content

class QuickSearchPopup(Popup):
    def __init__(self, **kwargs):
        super(QuickSearchPopup, self).__init__(**kwargs)
        content = BoxLayout(orientation='vertical', spacing=10)
        locations = ["WC", "Elevator", "Cafeteria", "Exit", "Meeting Room"]  # Automatizar
        for location in locations:
            button = Button(text=location, on_press=self.dismiss)
            content.add_widget(button)
        self.content = content

class MyRoot(BoxLayout):
    def __init__(self, **kwargs):
        super(MyRoot, self).__init__(orientation='vertical', spacing=10, **kwargs)

        # Create spot buttons without setting positions
        self.spot_buttons = [SpotButton(spot_name=spot, on_press=lambda instance: instance.on_press()) for spot in bluease.get_spots()]  # Aqui os botões são criados
        for spot_button in self.spot_buttons:
            spot_button.size_hint = (None, None)
            spot_button.size = (50, 50)
            self.add_widget(spot_button)

        # Add Quick Search button (bottom right)
        quick_search_button = Button(text='Quick Search', on_press=self.show_quick_search_popup, size_hint=(None, None), size=(120, 50))
        quick_search_button.pos_hint = {'right': 1, 'bottom': 0}
        self.add_widget(quick_search_button)

        # Add Search button (bottom right)
        search_button = Button(text='Search', on_press=self.show_search_popup, size_hint=(None, None), size=(100, 50))
        search_button.pos_hint = {'right': 1, 'bottom': 0.15}
        self.add_widget(search_button)

        # Schedule setting positions after layout initialization
        Clock.schedule_once(self.set_spot_button_positions, 0.1)


    def set_spot_button_positions(self, dt):
        # Set specific positions for the Spot buttons after the layout has been fully initialized
        #spot_positions = [(100, 100), (200, 200), (300, 300), (250, 500)]
        spot_positions = [bluease.get_spots()[spot].get_pos() for spot in bluease.get_spots()]
        print(spot_positions)
        for spot_button, pos in zip(self.spot_buttons, spot_positions):
            spot_button.pos = pos


    def show_search_popup(self, instance):
        search_popup = SearchPopup(title='Search Popup', size_hint=(0.6, 0.4))
        search_popup.open()

    def show_quick_search_popup(self, instance):
        quick_search_popup = QuickSearchPopup(title='Quick Search Popup', size_hint=(0.6, 0.6))
        quick_search_popup.open()

class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__()
        global bluease
        bluease = BluEase()

    def build(self):
        # Set the window size to match a 16:9 aspect ratio
        Window.size = (360, 640)  # Adjust the values as needed
        return MyRoot()



if __name__ == '__main__':
    myapp = MyApp()
    myapp.run()
