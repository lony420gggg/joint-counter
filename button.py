from kivy.uix.button import Button as KivyButton
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.core.image import Image as CoreImage


class Button(FloatLayout):
    def __init__(self, x, y, w, h, text, color, image_path=None, **kwargs):
        super().__init__(**kwargs)
        self.pos = (x, y)
        self.size = (w, h)
        self.text = text
        self.color = color
        self.pressed = False

        self._callback = None

        self.btn = KivyButton(
            text=text,
            size_hint=(None, None),
            size=(w, h),
            pos=(0, 0),
            background_normal="",
            background_down="",
            background_color=(*[c / 255 for c in color], 1),
        )
        self.btn.bind(on_press=self._on_press, on_release=self._on_release)
        self.add_widget(self.btn)

        self.image = None
        if image_path:
            try:
                self.image = Image(
                    source=image_path,
                    size_hint=(None, None),
                    size=(w, h),
                    pos=(0, 0),
                )
                self.add_widget(self.image)
                self.btn.background_color = (0, 0, 0, 0)
            except:
                self.image = None

    def _on_press(self, *_):
        self.pressed = True
        self.btn.size = (self.width - 10, self.height - 10)
        self.btn.pos = (5, 5)

    def _on_release(self, *_):
        was_pressed = self.pressed
        self.pressed = False
        self.btn.size = (self.width, self.height)
        self.btn.pos = (0, 0)
        if was_pressed and self._callback:
            self._callback()

    def is_clicked(self, callback):
        self._callback = callback

    def draw(self, screen):
        pass

