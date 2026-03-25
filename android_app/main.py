from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.config import Config

# 适配手机全屏
Config.set('graphics', 'fullscreen', '0')
Config.set('graphics', 'width', '0')
Config.set('graphics', 'height', '0')
Config.set('graphics', 'resizable', '1')

from kivy.metrics import sp, dp


class CalculatorApp(App):
    def build(self):
        from kivy.core.window import Window
        Window.clearcolor = (0.05, 0.05, 0.05, 1)

        self.display_text = '0'
        self.current = '0'
        self.previous = ''
        self.operator = None
        self.waiting_for_operand = False
        
        # 主布局 - 使用 size_hint 填满屏幕
        main_layout = BoxLayout(
            orientation='vertical',
            padding=dp(10),
            spacing=dp(8)
        )
        
        # 表达式显示（显示计算过程）
        self.expression = Label(
            text='',
            font_size=sp(18),
            size_hint_y=0.12,
            size_hint_x=1,
            color=(0.7, 0.7, 0.7, 1),
            halign='right',
            valign='middle',
            text_size=(None, None)
        )
        main_layout.add_widget(self.expression)
        
        # 结果显示屏
        self.display = Label(
            text='0',
            font_size=sp(48),
            size_hint_y=0.18,
            size_hint_x=1,
            color=(1, 1, 1, 1),
            halign='right',
            valign='middle',
            text_size=(None, None)
        )
        main_layout.add_widget(self.display)
        
        # 按钮网格 - 填满剩余空间
        grid = GridLayout(
            cols=4,
            spacing=dp(5),
            size_hint_y=0.70,
            size_hint_x=1
        )
        
        buttons = [
            ('C', (0.3, 0.3, 0.3, 1)),
            ('±', (0.3, 0.3, 0.3, 1)),
            ('%', (0.3, 0.3, 0.3, 1)),
            ('÷', (1, 0.58, 0, 1)),
            
            ('7', (0.2, 0.2, 0.2, 1)),
            ('8', (0.2, 0.2, 0.2, 1)),
            ('9', (0.2, 0.2, 0.2, 1)),
            ('×', (1, 0.58, 0, 1)),
            
            ('4', (0.2, 0.2, 0.2, 1)),
            ('5', (0.2, 0.2, 0.2, 1)),
            ('6', (0.2, 0.2, 0.2, 1)),
            ('-', (1, 0.58, 0, 1)),
            
            ('1', (0.2, 0.2, 0.2, 1)),
            ('2', (0.2, 0.2, 0.2, 1)),
            ('3', (0.2, 0.2, 0.2, 1)),
            ('+', (1, 0.58, 0, 1)),
            
            ('0', (0.2, 0.2, 0.2, 1)),
            ('.', (0.2, 0.2, 0.2, 1)),
            ('=', (1, 0.58, 0, 1)),
        ]
        
        for text, color in buttons:
            btn = Button(
                text=text,
                font_size=sp(24),
                background_color=color,
                background_normal='',
                color=(1, 1, 1, 1),
                size_hint_x=1,
                size_hint_y=1
            )
            btn.bind(on_press=self.on_button_press)
            grid.add_widget(btn)
        
        main_layout.add_widget(grid)
        return main_layout
    
    def update_expression(self):
        if self.operator:
            expr = f"{self.previous} {self.operator} {self.current}"
        else:
            expr = ""
        self.expression.text = expr
    
    def on_button_press(self, instance):
        text = instance.text
        
        if text.isdigit() or text == '.':
            self.input_digit(text)
        elif text == 'C':
            self.clear()
        elif text == '±':
            self.negate()
        elif text == '%':
            self.percentage()
        elif text == '=':
            self.calculate()
        elif text in ['+', '-', '×', '÷']:
            self.set_operator(text)
    
    def input_digit(self, digit):
        if self.waiting_for_operand:
            self.current = digit if digit != '.' else '0.'
            self.waiting_for_operand = False
        else:
            if digit == '.':
                if '.' not in self.current:
                    self.current += '.'
            else:
                if self.current == '0':
                    self.current = digit
                else:
                    self.current += digit
        self.display.text = self.current
        self.update_expression()
    
    def clear(self):
        self.current = '0'
        self.previous = ''
        self.operator = None
        self.waiting_for_operand = False
        self.display.text = '0'
        self.expression.text = ''
    
    def negate(self):
        if self.current != '0':
            if self.current.startswith('-'):
                self.current = self.current[1:]
            else:
                self.current = '-' + self.current
            self.display.text = self.current
            self.update_expression()
    
    def percentage(self):
        try:
            value = float(self.current) / 100
            self.current = str(value)
            self.display.text = self.current
            self.update_expression()
        except ValueError:
            pass
    
    def set_operator(self, op):
        if self.operator and not self.waiting_for_operand:
            self.calculate()
        
        self.operator = op
        self.previous = self.current
        self.waiting_for_operand = True
        self.update_expression()
    
    def calculate(self):
        if not self.operator or self.waiting_for_operand:
            return
        
        try:
            prev = float(self.previous)
            curr = float(self.current)
            
            if self.operator == '+':
                result = prev + curr
            elif self.operator == '-':
                result = prev - curr
            elif self.operator == '×':
                result = prev * curr
            elif self.operator == '÷':
                if curr == 0:
                    self.display.text = 'Error'
                    self.expression.text = 'Cannot divide by zero'
                    self.current = '0'
                    self.previous = ''
                    self.operator = None
                    return
                result = prev / curr
            else:
                return
            
            if result == int(result):
                result_str = str(int(result))
            else:
                result_str = str(result)
            
            self.expression.text = f"{self.previous} {self.operator} {self.current} = {result_str}"
            self.display.text = result_str
            
            self.current = result_str
            self.operator = None
            self.previous = ''
            self.waiting_for_operand = True
            
        except ValueError:
            self.display.text = 'Error'
            self.current = '0'


if __name__ == '__main__':
    CalculatorApp().run()
