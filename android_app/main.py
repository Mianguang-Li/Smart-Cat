from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window

Window.size = (400, 600)


class CalculatorApp(App):
    def build(self):
        self.display_text = '0'
        self.current = '0'
        self.previous = ''
        self.operator = None
        self.waiting_for_operand = False
        
        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 表达式显示（显示计算过程）
        self.expression = Label(
            text='',
            font_size='18sp',
            size_hint_y=0.1,
            color=(0.7, 0.7, 0.7, 1),
            halign='right'
        )
        main_layout.add_widget(self.expression)
        
        # 结果显示屏
        self.display = Label(
            text='0',
            font_size='48sp',
            size_hint_y=0.15,
            color=(1, 1, 1, 1),
            halign='right'
        )
        main_layout.add_widget(self.display)
        
        # 按钮网格
        grid = GridLayout(cols=4, spacing=5, size_hint_y=0.75)
        
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
                font_size='24sp',
                background_color=color,
                background_normal='',
                color=(1, 1, 1, 1)
            )
            btn.bind(on_press=self.on_button_press)
            grid.add_widget(btn)
        
        main_layout.add_widget(grid)
        return main_layout
    
    def update_expression(self):
        """更新表达式显示"""
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
            
            # 格式化结果
            if result == int(result):
                result_str = str(int(result))
            else:
                result_str = str(result)
            
            # 显示完整的计算过程
            if self.operator == '×':
                op_display = '×'
            elif self.operator == '÷':
                op_display = '÷'
            else:
                op_display = self.operator
            
            self.expression.text = f"{self.previous} {op_display} {self.current} = {result_str}"
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
