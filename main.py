from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.graphics import Rectangle

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

    arrButton = []

    buttonsStates = {'leftForward': False,
               'rightForward': False,
               'leftBackward': False,
               'rightBackward': False}

    states = {'forward': 'forward.png',
              'backward': 'backward.png',
              'leftTurn': 'leftTurn.png',
              'rightTurn': 'rightTurn.png',
              'leftReversal': 'leftReversal.png',
              'rightReversal': 'rightReversal.png',
              'stop': 'stop.png'}

    def motorDCRun(self, instance, state, label, arrDirection):
        direction = ''.join(arrDirection)
        contraryDirection = arrDirection[0] + (self.forward if arrDirection[1] == self.backward else self.backward)

        if state == 'down':
            if self.buttonsStates[contraryDirection]:
                instance.state = 'normal'
                return
            response = requests.get(self.url + direction)
            if response:
                self.buttonsStates[direction] = True
                label.text = response.text
        else:
            response = requests.get(self.url + arrDirection[0] + self.stop)
            if response:
                self.buttonsStates[direction] = False
                label.text = response.text

    def on_start(self, **kwargs):
        pos_y = 60
        index = 0

        for buttom in self.arrButton:
            Animation(y=pos_y, d=2, t='in_circ').start(buttom)
            if index % 2:
                pos_y += 120
            index += 1

    def stop(self):
        return

    def build(self):
        padding = (2, 2, 2, 2)

        self._app_window = Window
        Window.clearcolor = (129/255, 138/255, 81/255, 1/255)

        layout = BoxLayout(orientation="vertical")
        label = Label(text='[b]Go?[/b]\n', markup=True, valign='top')
        layout.add_widget(label)

        layoutButtonForward = BoxLayout(orientation="horizontal", size_hint = (1, .4))

        layoutButtonLeftForward = BoxLayout(orientation="horizontal", padding=padding)
        buttonLeftForward = Button(text="", background_normal='arrowTop1.png', background_down='arrowTop2.png',pos= Window.size)
        buttonLeftForward.bind(
            state=lambda instance, state: self.motorDCRun(instance, state, label, (self.left, self.forward)))
        layoutButtonLeftForward.add_widget(buttonLeftForward)

        layoutButtonRightForward = BoxLayout(orientation="horizontal", padding=padding)
        buttonRightForward = Button(text="", background_normal='arrowTop1.png', background_down='arrowTop2.png', pos= Window.size)
        buttonRightForward.bind(
            state=lambda instance, state: self.motorDCRun(instance, state, label, (self.right, self.forward)))
        layoutButtonRightForward.add_widget(buttonRightForward)

        layoutButtonForward.add_widget(layoutButtonLeftForward)
        layoutButtonForward.add_widget(layoutButtonRightForward)
        layout.add_widget(layoutButtonForward)

        layoutButtonBackward = BoxLayout(orientation="horizontal", size_hint=(1, .4))

        layoutButtonLeftBackward = BoxLayout(orientation="horizontal", padding=padding)
        buttonLeftBackward = Button(text="", background_normal='arrowDown1.png', background_down='arrowDown2.png', pos= Window.size)
        buttonLeftBackward.bind(
            state=lambda instance, state: self.motorDCRun(instance, state, label, (self.left, self.backward)))
        layoutButtonLeftBackward.add_widget(buttonLeftBackward)

        layoutButtonRightBackward = BoxLayout(orientation="horizontal", padding=padding)
        buttonRightBackward = Button(text="", background_normal='arrowDown1.png', background_down='arrowDown2.png', pos= Window.size)
        buttonRightBackward.bind(
            state=lambda instance, state: self.motorDCRun(instance, state, label, (self.right, self.backward)))
        layoutButtonRightBackward.add_widget(buttonRightBackward)

        layoutSliderSpeep = BoxLayout(orientation='vertical', size_hint=(1, .2))
        sliderSpeep = Slider(min=0, max=100, value=25, size_hint=(1, .2), cursor_image='slider.png')
        layoutSliderSpeep.add_widget(sliderSpeep)

        layoutButtonBackward.add_widget(layoutButtonLeftBackward)
        layoutButtonBackward.add_widget(layoutButtonRightBackward)
        layout.add_widget(layoutButtonBackward)
        layout.add_widget(layoutSliderSpeep)

        self.arrButton.append(buttonLeftBackward)
        self.arrButton.append(buttonRightBackward)
        self.arrButton.append(buttonLeftForward)
        self.arrButton.append(buttonRightForward)

        return layout

MyApplicationApp().run()


