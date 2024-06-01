# This file is part of the WeatherStation project
# and is licensed under the MIT License. For more details,
# see the LICENSE file in the root directory of this project or visit
# https://github.com/jenei-peter-dorozsma/WeatherStation

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout


# Define a common parent widget for H1 and H2
class CustomLabelBase(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = (0, 1, 0, 1)  # Green color
        self.font_name = 'fonts/monofonto/monofonto rg.otf'
        self.font_size = 40  # Default font size


# Define H1 class
class H1(CustomLabelBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = 100  # Override font size for H1


# Define H2 class
class H2(CustomLabelBase):
    pass


class BoxLayoutBox(BoxLayout):
    pass


class GridLayoutBox(GridLayout):
    pass


class StackLayoutBox(StackLayout):
    pass
