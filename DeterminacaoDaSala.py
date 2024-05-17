from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

# Initial value of the variable
posicao_utilizador = "Initial Value"

class ButtonUI(BoxLayout):
    def __init__(self, **kwargs):
        super(ButtonUI, self).__init__(**kwargs)
        self.orientation = "vertical"
        
        # Create a label to display the variable
        self.variable_label = Label(text="Variable Value: " + posicao_utilizador)
        self.add_widget(self.variable_label)
        
        # Create buttons
        button_texts = ["Receção", "Corredor lateral", "Sala multiusos", "UATA", "Piso -1", "Entrada", "WC Homem - Copa", "WC Mulher - Área de serviço", "Button 9"]
        for text in button_texts:
            button = Button(text=text)
            button.bind(on_release=lambda btn, t=text: self.button_clicked(t))  # Pass text as a default argument
            self.add_widget(button)
    
    def update_variable(self, new_value):
        global posicao_utilizador  # Use the global variable
        posicao_utilizador = new_value
        self.variable_label.text = "Variable Value: " + posicao_utilizador
    
    def button_clicked(self, button_text):
        self.update_variable(button_text)

class ButtonUIApp(App):
    def build(self):
        return ButtonUI()

if __name__ == "__main__":
    ButtonUIApp().run()
