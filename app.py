#utf-8
import sys
sys.path.insert(1, './snake/')
sys.path.insert(1, './templates/')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button


class MultigameApp(App):

    @staticmethod
    def click_snake():
        import snake
        exit(snake.main('Medium'))

    @staticmethod
    def click_cancel():
        exit(0)

    #def build(self):
        # fl = FloatLayout()
        #
        # btn_snake = Button()
        # btn_snake.text = 'Snake'
        # btn_snake.on_press = self.click_snake
        # btn_snake.size_hint = None, None
        # btn_snake.height = 50
        # btn_snake.width = 200
        # btn_snake.x = 150
        # btn_snake.y = 300
        #
        # btn_cancel = Button()
        # btn_cancel.text = 'Cancel'
        # btn_cancel.on_press = self.click_cancel
        # btn_cancel.size_hint = None, None
        # btn_cancel.height = 50
        # btn_cancel.width = 200
        # btn_cancel.x = 450
        # btn_cancel.y = 300
        #
        # fl.add_widget(btn_snake)
        # fl.add_widget(btn_cancel)
        #
        # return fl

if __name__ == '__main__':

    m = MultigameApp()
    m.run()

