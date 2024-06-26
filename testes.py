from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.animation import Animation
from kivy.uix.relativelayout import RelativeLayout
from BluEase import BluEase
import DeterminacaoDaSala
import time

'''Observações:
- Os botões fora da parte visível não funcionam, por isso é que tentei criar animações:
    - Tentou-se começar a aplicação com todos os botões no ecrã e depois fazer zoom, mas não resultou :)
    - As configurações dos botões para a animação são: size=(100/2,100/2),pos=(size_x/2, size_y/2)
    - As configrações para a imagem da planta são: size=(600, 600)'''

Window.size = (312, 665)

# carrega as funcionalidades do backend
bluease = BluEase()

# guarda o edifício atual na base de dados (ISCTE-Sintra) em uma variável
building = bluease.get_building()

class Bluey(App):
    def build(self):
        root = RelativeLayout()
        Window.clearcolor = (1,1,1,1)
        inicio = Image(source='bluething.png', allow_stretch=True, keep_ratio=True,pos_hint={'center_x': 0.5, 'center_y': 0.5})
        root.add_widget(inicio)
        return root

class Andar1(App):
    def build(self):
        root = RelativeLayout()
        Window.clearcolor = (232/255, 240/255, 243/255)

        self.scatter = Scatter(do_rotation=False, auto_bring_to_front=False, size=Window.size, do_translation=True)
        map_image = Image(source='Faculdade_RC.png', allow_stretch=True, keep_ratio=False, size=(924, 1311))
        self.scatter.add_widget(map_image)
        self.button_layout = RelativeLayout(size=(map_image.size))
        self.buttons = []
        # Minha mudança foi aqui, ao invés de ir naqueles arrays pegar as informações, pedes elas ao backend
        # Para cada spot (Receção, corredor lateral, entrada, etc) dentro do edificio cria o botão para ele
        for spot in building.get_spots():
            print(spot.get_name())
            icon = "rsz_1rsz_interestpoint.png"
            size = (70,70)
            if spot.get_name() ==  DeterminacaoDaSala.posicao_utilizador:
                icon = "rsz_1interestpoint_red.png"
                size = (55,68)
                DeterminacaoDaSala.posicao_utilizador = spot
            spot_button = Button(
                size_hint=(None, None),
                size=size,                          
                pos=spot.get_pos(),
                background_normal=icon,
                background_down=icon,
                on_press=lambda instance, sp=spot, pop=spot.get_pictures(): self.on_press(instance, sp, pop))
            # TODO: Falta criar algo que receba a sala atual e altere a cor do botão de azul para vermelha

            self.button_layout.add_widget(spot_button)

            # Para cada ponto de interesse (Máquina de vendas, balcão de informação, etc) dentro do spot, cria o botão para ele
            for interestpoint in spot.getInterest_points():
                if interestpoint.getType() in ["Escadas","Elevador"]:
                    size_ = (65,65)
                else:
                    size_ = (85,85)
                ip_button = Button(
                    size_hint=(None, None),
                    size=size_,
                    pos=interestpoint.get_pos(),
                    background_normal=interestpoint.get_icon(),
                    background_down=interestpoint.get_icon(),
                    on_press=lambda instance, ip=interestpoint, pop="": self.on_press(instance, ip, pop)
                )
                self.button_layout.add_widget(ip_button)
        """
        # NODES NOVO
        for node in bluease.get_nodes():
            ponto=Button(
                size=(30,30),
                pos=(node[1],node[2]),
                background="rsz_1interestpoint_red.png"
            )
            self.button_layout.add_widget(ponto)
        """
        self.scatter.add_widget(self.button_layout)

        logo_overlay = BoxLayout(orientation='horizontal', size_hint=(None, None), size=(Window.width, 130), pos=(0, Window.height))
        with logo_overlay.canvas.before:
            Color(0, 57/255, 1)
            self.rect = Rectangle(pos=logo_overlay.pos, size=logo_overlay.size)

        logo = Image(source='BluEase_logo_sem_fundo.png', size_hint=(None, None), size=(120, 120))
        logo_overlay.add_widget(logo)

        menu = Image(source='icons/icons8-menu-100.png', size_hint=(None, None), size=(70,70), pos_hint={'center_x': 0.9, 'center_y': 0.95})
        reg = Label(text='1º Andar', font_size=50, color=(1,1,1, 1), size_hint=(0.1, 0.05), pos_hint={'center_x': 0.5})

        search = Button(background_normal='icons/icons8-search-100-2.png',
                        background_down='icons/icons8-search-100-3.png',
                        on_press=self.show_search_popup, size_hint=(None, None),
                size=(100,100), pos_hint={'center_x': 0.9, 'center_y': 0.16})
        flash = Button(background_normal='icons/icons8-flash-100.png',
                       background_down='icons/icons8-flash-100-2.png',
                       on_press=self.show_quick_search_popup, size_hint=(None, None),
                size=(100,100), pos_hint={'center_x': 0.9, 'center_y': 0.07})

        root.add_widget(self.scatter)
        root.add_widget(logo_overlay)
        root.add_widget(menu)
        root.add_widget(search)
        root.add_widget(flash)

        reg_layout = BoxLayout(size_hint_y=None, height=50, spacing=10, pos_hint={'center_x': 0.5, 'center_y': 0.965})
        space_1_reg_layout = Widget(size_hint_x=None, width=80)
        space_2_reg_layout = Widget(size_hint_x=None, width=80)
        reg_layout.add_widget(space_1_reg_layout)
        reg_layout.add_widget(reg)
        reg_layout.add_widget(space_2_reg_layout)
        root.add_widget(reg_layout)

# Animação
        '''anim = Animation(width=map_image.width * 2, height=map_image.height * 2, transition='out_circ', duration=2)
        anim.start(map_image)'''

        return root


    def show_path(self, destino):
        print(destino)
        with self.root.canvas:
            path = bluease.wayfind(DeterminacaoDaSala.posicao_utilizador.get_node(), destino)
            print(path)
            with self.scatter.canvas:
                try:
                    for line in self.path_lines:
                        self.scatter.canvas.remove(line)
                except: self.path_lines = []
                Color(1, 0, 0)
                for i in range(len(path) - 1):
                    # Draw lines connecting coordinates
                    self.path_lines.append(Line(points=[int(bluease.get_nodes()[path[i]][0]), int(bluease.get_nodes()[path[i]][1]),
                                 int(bluease.get_nodes()[path[i+1]][0]), int(bluease.get_nodes()[path[i+1]][1])]))


    def on_directions_button_press(self, instance, destino, pop):
        # fecha o popup e chama a função faustas
        print(destino)
        pop.dismiss()
        self.show_path(destino)

    def on_press(self, instance, info, pop):
        print(info.get_name(), info.get_node())
        content = BoxLayout(orientation='vertical', spacing=10)
        image = Image(source=pop, size_hint=(1, 0.8), allow_stretch=True)

        button1 = Button(text='Informações', size_hint_y=None, height=50)
# chama a função acima
        button2 = Button(text='Direções', size_hint_y=None, height=50)

        content.add_widget(image)
        content.add_widget(button1)
        content.add_widget(button2)
        popup = Popup(title=f'{info.get_name()}', content=content, size_hint=(0.8, 0.6), separator_color=[0, 57 / 255, 1, 1],
                          background_color=[1, 1, 1, 1])
        button2.bind(on_press=lambda instance: self.on_directions_button_press(instance, info.get_node(), popup))

        popup.open()

        # background='bluething.png'
    def show_search_popup(self, instance):
            content = BoxLayout(orientation='vertical', spacing=10)
            text_input = TextInput(hint_text='Type here', multiline=False)
            search_button = Button(text='Search', size_hint=(None, None), size=(100, 50))
            content.add_widget(text_input)
            content.add_widget(search_button)
            search_popup = Popup(title=f'Procurar Sala', content=content, size_hint=(0.8, 0.6),
                          separator_color=[0, 57 / 255, 1, 1],
                          background_color=[1, 1, 1, 1])
            search_popup.open()

    def show_quick_search_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10)
        ips = []
        for spot in building.get_spots(): # Muitos ciclos, provavelmente é melhor buscar da database.
            for interest_point in spot.getInterest_points():
                ips.append(interest_point)
        for interest_point in ips:
            button = Button(text=interest_point.get_description(), on_press=lambda instance, ip = interest_point: self.on_directions_button_press(instance, ip.get_node(), quick_search_popup))
            content.add_widget(button)
        quick_search_popup = Popup(title='Procura rápida', size_hint=(0.6, 0.6), content=content)
        quick_search_popup.open()
# background='bluething.png'

    


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

if __name__ == '__main__':
    DeterminacaoDaSala.ButtonUIApp().run()
    Andar1().run()
    
    