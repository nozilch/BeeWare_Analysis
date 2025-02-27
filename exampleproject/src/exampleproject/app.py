"""
My first application
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from pysnooper import snoop

class HelloWorld(toga.App):

    @snoop()  # 添加这个装饰器来跟踪函数
    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """

        '''
        main_box = toga.Box()

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()
        '''

        main_box = toga.Box(style=Pack(direction=COLUMN))
        name_label = toga.Label(
            'Your name: ',
            style=Pack(padding=(0, 5))
        )
        self.name_input = toga.TextInput(style=Pack(flex=1))

        name_box = toga.Box(style=Pack(direction=ROW, padding=5))

        name_box.add(name_label)
        name_box.add(self.name_input)

        button = toga.Button(
        'Say Hello!',
              on_press = self.say_hello,
              style = Pack(padding=5)
        )
        main_box.add(name_box)
        main_box.add(button)
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    @snoop()  # 同样可以装饰其他需要追踪的方法
    def say_hello(self, widget):
        if self.name_input.value:
            name = self.name_input.value
        else:
            name = 'stranger'


        self.main_window.info_dialog(
            'Hello, {}'.format(name),
            'Hi there!'
        )

def main():
    return HelloWorld()
