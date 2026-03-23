from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.core.window import Window

# 设置窗口大小（桌面测试用）
Window.size = (360, 640)


class CalculatorButton(Button):
    """自定义计算器按钮"""
    pass


class Calculator(BoxLayout):
    display_text = StringProperty('0')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current = '0'
        self.previous = ''
        self.operator = None
        self.waiting_for_operand = False
    
    def on_button_press(self, button_text):
        """处理按钮按下事件"""
        if button_text.isdigit() or button_text == '.':
            self.input_digit(button_text)
        elif button_text == 'C':
            self.clear()
        elif button_text == '±':
            self.negate()
        elif button_text == '%':
            self.percentage()
        elif button_text == '=':
            self.calculate()
        elif button_text in ['+', '-', '×', '÷']:
            self.set_operator(button_text)
    
    def input_digit(self, digit):
        """输入数字或小数点"""
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
        self.display_text = self.current
    
    def clear(self):
        """清除所有"""
        self.current = '0'
        self.previous = ''
        self.operator = None
        self.waiting_for_operand = False
        self.display_text = '0'
    
    def negate(self):
        """取反"""
        if self.current != '0':
            if self.current.startswith('-'):
                self.current = self.current[1:]
            else:
                self.current = '-' + self.current
            self.display_text = self.current
    
    def percentage(self):
        """百分比"""
        try:
            value = float(self.current) / 100
            self.current = str(value)
            self.display_text = self.current
        except ValueError:
            pass
    
    def set_operator(self, op):
        """设置运算符"""
        if self.operator and not self.waiting_for_operand:
            self.calculate()
        
        self.operator = op
        self.previous = self.current
        self.waiting_for_operand = True
    
    def calculate(self):
        """执行计算"""
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
                    self.display_text = 'Error'
                    self.current = '0'
                    self.previous = ''
                    self.operator = None
                    return
                result = prev / curr
            else:
                return
            
            # 格式化结果，移除不必要的零
            if result == int(result):
                self.current = str(int(result))
            else:
                self.current = str(result)
            
            self.display_text = self.current
            self.operator = None
            self.previous = ''
            self.waiting_for_operand = True
            
        except ValueError:
            self.display_text = 'Error'
            self.current = '0'


class CalculatorApp(App):
    def build(self):
        from kivy.lang import Builder
        
        kv = '''
<CalculatorButton>:
    font_size: 28
    background_normal: ''
    background_color: 0.2, 0.2, 0.2, 1
    color: 1, 1, 1, 1
    
    canvas.after:
        Color:
            rgba: 0.3, 0.3, 0.3, 1
        Line:
            rectangle: self.pos[0], self.pos[1], self.size[0], self.size[1]

<Calculator>:
    orientation: 'vertical'
    spacing: 1
    padding: 5
    
    Label:
        id: display
        text: root.display_text
        font_size: 48
        size_hint_y: 0.25
        halign: 'right'
        valign: 'middle'
        text_size: self.size
        color: 1, 1, 1, 1
        canvas.before:
            Color:
                rgba: 0.1, 0.1, 0.1, 1
            Rectangle:
                pos: self.pos
                size: self.size
    
    BoxLayout:
        orientation: 'vertical'
        spacing: 1
        size_hint_y: 0.75
        
        # 第一行: C, ±, %, ÷
        BoxLayout:
            spacing: 1
            CalculatorButton:
                text: 'C'
                background_color: 0.3, 0.3, 0.3, 1
                on_press: root.on_button_press(self.text)
            CalculatorButton:
                text: '±'
                background_color: 0.3, 0.3, 0.3, 1
                on_press: root.on_button_press(self.text)
            CalculatorButton:
                text: '%'
                background_color: 0.3, 0.3, 0.3, 1
                on_press: root.on_button_press(self.text)
            CalculatorButton:
                text: '÷'
                background_color: 1, 0.58, 0, 1
                on_press: root.on_button_press(self.text)
        
        # 第二行: 7, 8, 9, ×
        BoxLayout:
            spacing: 1
            CalculatorButton:
                text: '7'
                on_press: root.on_button_press(self.text)
            CalculatorButton:
                text: '8'
                on_press: root.on_button_press(self.text)
            CalculatorButton:
                text: '9'
                on_press: root.on_button_press(self.text)
            CalculatorButton:
                text: '×'
                background_color: 1, 0.58, 0, 1
                on_press: root.on_button_press(self.text)
        
        # 第三行: 4, 5, 6, -
        BoxLayout:
            spacing: 1
            CalculatorButton:
                text: '4'
                on_press: root.on_button_press(self.text)
            CalculatorButton:
                text: '5'
                on_press: root.on_button_press(self.text)
            CalculatorButton:
                text: '6'
                on_press: root.on_button_press(self.text)
            CalculatorButton:
                text: '-'
                background_color: 1, 0.58, 0, 1
                on_press: root.on_button_press(self.text)
        
        # 第四行: 1, 2, 3, +
        BoxLayout:
            spacing: 1
            CalculatorButton:
                text: '1'
                on_press: root.on_button_press(self.text)
            CalculatorButton:
                text: '2'
                on_press: root.on_button_press(self.text)
            CalculatorButton:
                text: '3'
                on_press: root.on_button_press(self.text)
            CalculatorButton:
                text: '+'
                background_color: 1, 0.58, 0, 1
                on_press: root.on_button_press(self.text)
        
        # 第五行: 0, .
        BoxLayout:
            spacing: 1
            CalculatorButton:
                text: '0'
                size_hint_x: 2
                on_press: root.on_button_press(self.text)
            CalculatorButton:
                text: '.'
                on_press: root.on_button_press(self.text)
            CalculatorButton:
                text: '='
                background_color: 1, 0.58, 0, 1
                on_press: root.on_button_press(self.text)
'''
        
        return Builder.load_string(kv)


if __name__ == '__main__':
    CalculatorApp().run()
