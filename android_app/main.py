from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.label = Label(
            text='Hello Android!',
            font_size=32,
            size_hint=(1, 0.5)
        )
        
        btn = Button(
            text='Click Me',
            font_size=24,
            size_hint=(1, 0.5)
        )
        btn.bind(on_press=self.on_button_click)
        
        layout.add_widget(self.label)
        layout.add_widget(btn)
        
        return layout
    
    def on_button_click(self, instance):
        self.label.text = 'Button Clicked!'


if __name__ == '__main__':
    MyApp().run()
