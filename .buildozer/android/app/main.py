from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
import kivy.utils as utils
import getIp

import requests


class MyApplicationApp(App):

    url = 'http://' + getIp.getNetworkIp() + '/'
    # url = 'http://192.168.4.1:8081/'
    forward = 'Forward'
    backward = 'Backward'
    stop = 'Stop'
    left = 'left'
    right = 'right'

    buttons = {'leftForward': False, 'rightForward': False, 'leftBackward': False, 'rightBackward': False}

    def motorDCRun(self, instance, label, arrDirection):
        direction = ''.join(arrDirection)

        if instance.state == 'down':
            if (direction == 'leftForward' and self.buttons['leftBackward']) or (
                    direction == 'rightForward' and self.buttons['rightBackward']) or (
                    direction == 'leftBackward' and self.buttons['leftForward']) or (
                    direction == 'rightBackward' and self.buttons['rightBackward']):
                instance.state = 'normal'
                return
            response = requests.get(self.url + direction)
            if response:
                self.buttons[direction] = True
                label.text = response.text
        else:
            response = requests.get(self.url + arrDirection[0] + self.stop)
            if response:
                self.buttons[direction] = False
                label.text = response.text

    def build(self):
        padding = (5, 5, 5, 5)
        Window.clearcolor = (129/255, 138/255, 81/255, 1/255)
        layout = BoxLayout(orientation="vertical")

        label = Label(text='[b]Help Page[/b]\n', markup=True,   valign='top')
        label.bind(texture_size=label.setter('size'))
        layout.add_widget(label)


        layoutButtonForward = BoxLayout(orientation="horizontal")

        layoutButtonLeftForward = BoxLayout(orientation="horizontal", padding=padding)
        buttonLeftForward = Button(text="", background_normal='arrowTop1.png', background_down='arrowTop2.png')
        buttonLeftForward.bind(on_press=lambda x: self.motorDCRun(buttonLeftForward, label, (self.left, self.forward)))
        buttonLeftForward.bind(on_release=lambda x: self.motorDCRun(buttonLeftForward, label, (self.left, self.forward)))
        layoutButtonLeftForward.add_widget(buttonLeftForward)

        layoutButtonRightForward = BoxLayout(orientation="horizontal", padding=padding)
        buttonRightForward = Button(text="", background_normal='arrowTop1.png', background_down='arrowTop2.png')
        buttonRightForward.bind(on_press=lambda x: self.motorDCRun(buttonRightForward, label, (self.right, self.forward)))
        buttonRightForward.bind(on_release=lambda x: self.motorDCRun(buttonRightForward, label, (self.right, self.forward)))
        layoutButtonRightForward.add_widget(buttonRightForward)

        layoutButtonForward.add_widget(layoutButtonLeftForward)
        layoutButtonForward.add_widget(layoutButtonRightForward)
        layout.add_widget(layoutButtonForward)

        layoutButtonBackward = BoxLayout(orientation="horizontal")

        layoutButtonLeftBackward = BoxLayout(orientation="horizontal", padding=padding)
        buttonLeftBackward = Button(text="", background_normal='arrowDown1.png', background_down='arrowDown2.png')
        buttonLeftBackward.bind(on_press=lambda x: self.motorDCRun(buttonLeftBackward, label, (self.left, self.backward)))
        buttonLeftBackward.bind(on_release=lambda x: self.motorDCRun(buttonLeftBackward, label, (self.left, self.backward)))
        layoutButtonLeftBackward.add_widget(buttonLeftBackward)

        layoutButtonRightBackward = BoxLayout(orientation="horizontal", padding=padding)
        buttonRightBackward = Button(text="", background_normal='arrowDown1.png', background_down='arrowDown2.png')
        buttonRightBackward.bind(on_press=lambda x: self.motorDCRun(buttonRightBackward, label, (self.right, self.backward)))
        buttonRightBackward.bind(on_release=lambda x: self.motorDCRun(buttonRightBackward, label, (self.right, self.backward)))
        layoutButtonRightBackward.add_widget(buttonRightBackward)

        layoutButtonBackward.add_widget(layoutButtonLeftBackward)
        layoutButtonBackward.add_widget(layoutButtonRightBackward)
        layout.add_widget(layoutButtonBackward)

        return layout


MyApplicationApp().run()
