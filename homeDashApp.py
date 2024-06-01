# This file is part of the WeatherStation project
# and is licensed under the MIT License. For more details,
# see the LICENSE file in the root directory of this project or visit
# https://github.com/jenei-peter-dorozsma/WeatherStation

import kivy
from math import ceil
from datetime import datetime
from kivy.app import App
from kivy.lang import Builder
from kivy.graphics import Color, Line
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.image import Image

from weatherData import WeatherData
from moonPhaseCalculator import MoonPhaseCalculator
from styleWidgets import H1, H2, BoxLayoutBox, GridLayoutBox, StackLayoutBox
from comicsReader import ComicsReader
from colorSets import Colors

kivy.require('2.3.0')
# print(kivy.__version__)


# Defining a class
class HomeDashApp(App):
    # Window.fullscreen = 'auto'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.weather_data = WeatherData()
        self.comics_reader = ComicsReader()
        cs, csn = Colors().get_color_set("green")
        self.color_set = cs
        self.color_set_normalized = csn

        self.sun_is_up = True

    # Load kv file
    def build(self):
        return Builder.load_file("kv/main.kv")

    # Load initial data at the startup
    def on_start(self):
        # Initialize update functions for the screen data
        Clock.schedule_interval(self.update_clock, 1)  # Per secondly
        Clock.schedule_interval(self.update_per_minute, 60)  # Per minute
        Clock.schedule_interval(self.update_per_quarter, 900)  # Per 15 minutes
        Clock.schedule_interval(self.update_per_hour, 3600)  # Per hour

        # Bind actions for screen resize
        self.root.bind(size=self.resize_callback)

        # run initial adjustment of the screen
        self.update_per_minute(0)
        self.update_per_quarter(0)
        self.update_per_hour(0)
        self.resize_callback(self.root, (self.root.width, self.root.height))

    # Draw background lines based on the day or nigh color
    def draw_background_lines(self):
        layout = self.root
        layout.canvas.before.clear()  # Clear previous lines

        with layout.canvas.before:
            Color(*self.color_set_normalized[3])
            for y in range(0, Window.height, 10):  # Draw horizontal lines
                Line(points=[0, y, Window.width, y], width=2)

    # Change H1 and H2 font sizes when window gets resized
    def adjust_font_size(self, widget, value):
        if isinstance(widget, H1):
            updated_fontsize = (value[0] * 100) / 2768
            widget.font_size = updated_fontsize
            widget.color = self.color_set_normalized[0]
        elif isinstance(widget, H2):
            updated_fontsize = (value[0] * 40) / 2768
            widget.font_size = updated_fontsize
            widget.color = self.color_set_normalized[0]
        elif isinstance(widget, Image):
            if self.sun_is_up:
                old_str = "/night/"
                new_str = "/day/"
            else:
                old_str = "/day/"
                new_str = "/night/"
            widget.source = widget.source.replace(old_str, new_str)
            widget.reload()  # Reload the image to apply the change
        elif (isinstance(widget, BoxLayoutBox) or
              isinstance(widget, GridLayoutBox) or
              isinstance(widget, StackLayoutBox)):
            for instruction in widget.canvas.before.children:
                if isinstance(instruction, Color):
                    instruction.rgba = self.color_set_normalized[0]

        # Recursively adjust font size for each child
        if hasattr(widget, 'children'):
            for child in widget.children:
                self.adjust_font_size(child, value)

    # Window resize happened we need to adjust background and font sizes
    def resize_callback(self, instance, value):
        self.draw_background_lines()

        # Recursively adjust font size for all children of the root widget
        self.adjust_font_size(self.root, value)

    def update_clock(self, *args):
        date_box = self.root.ids.date_box
        date_box.ids.clock_label.text = datetime.now().strftime('%H:%M:%S')

    def update_date_box(self, wd):
        date_box = self.root.ids.date_box
        current_date = datetime.now()
        formatted_date = current_date.strftime("%Y.%m.%d")
        today = current_date.strftime("%A")
        date_box.ids.date_label.text = formatted_date
        date_box.ids.day_of_the_week_label.text = today

        date_box.ids.last_update_label.text = f"Last update: {wd.last_update}"

    def update_moon_box(self, wd):
        sun_and_moon_box = self.root.ids.sun_and_moon_box
        sun_and_moon_box.ids.sunrise_label.text = f"{wd.sunrise}"
        sun_and_moon_box.ids.sunset_label.text = f"{wd.sunset}"

        moon_calculator = MoonPhaseCalculator()
        moon_phase = moon_calculator.get_actual_moon_phase()
        moon_phase_label = moon_phase[0]
        moon_phase_image = moon_phase[1]
        moon_phase_image = f'icons/day/moon/{moon_phase_image}'

        sun_and_moon_box.ids.moon_phase_label.text = moon_phase_label
        sun_and_moon_box.ids.moon_phase_image.source = moon_phase_image

    def update_weather_box(self, wd):
        weather_box = self.root.ids.weather_box
        weather_box.ids.sky_icon_image.source = wd.sky_icon
        weather_box.ids.sky_status_label.text = f"{wd.sky_status}"
        weather_box.ids.temperature_label.text = f"{wd.temperature}°C"
        weather_box.ids.bottom_line_label.text = f"{wd.humidity}% / "
        weather_box.ids.bottom_line_label.text += f"{wd.pressure} hPa"

    def update_wind_box(self, wd):
        wind_box = self.root.ids.wind_box
        total_wind = ceil(wd.wind_speed * 10) / 10
        wind_box.ids.wind_speed_label.text = f"{total_wind} km/h"
        wind_box.ids.wind_description_label.text = wd.wind_description

    def update_bike_box(self, wd):
        bike_box = self.root.ids.bike_box

        if (wd.is_it_morning):
            bike_label1 = "N to S: "
            bike_label2 = "W to E: "
        else:
            bike_label1 = "E to W: "
            bike_label2 = "S to N: "

        bike_label1 += wd.bike_parts[0][1]
        wind_speed_part_1 = ceil(wd.bike_parts[0][2] * 10) / 10
        bike_label1 += f' ({wind_speed_part_1} km/h)'

        bike_label2 += wd.bike_parts[1][1]
        wind_speed_part_2 = ceil(wd.bike_parts[1][2] * 10) / 10
        bike_label2 += f' ({wind_speed_part_2} km/h)'

        bike_box.ids.bike_part_1.text = bike_label1
        bike_box.ids.bike_part_2.text = bike_label2

        bike_part1_icons = [
            bike_box.ids.part1_icon1.source,
            bike_box.ids.part1_icon2.source,
            bike_box.ids.part1_icon3.source,
            bike_box.ids.part1_icon4.source,
            bike_box.ids.part1_icon5.source
        ]

        for i in range(0, 5):
            bike_part1_icons[i] = bike_part1_icons[i].replace("_on", "_off")

        for i in range(wd.bike_parts[0][0]-1, 5):
            bike_part1_icons[i] = bike_part1_icons[i].replace("_off", "_on")

        bike_box.ids.part1_icon1.source = bike_part1_icons[0]
        bike_box.ids.part1_icon2.source = bike_part1_icons[1]
        bike_box.ids.part1_icon3.source = bike_part1_icons[2]
        bike_box.ids.part1_icon4.source = bike_part1_icons[3]
        bike_box.ids.part1_icon5.source = bike_part1_icons[4]

        bike_part2_icons = [
            bike_box.ids.part2_icon1.source,
            bike_box.ids.part2_icon2.source,
            bike_box.ids.part2_icon3.source,
            bike_box.ids.part2_icon4.source,
            bike_box.ids.part2_icon5.source
        ]

        for i in range(0, 5):
            bike_part2_icons[i] = bike_part2_icons[i].replace("_on", "_off")

        for i in range(wd.bike_parts[1][0]-1, 5):
            bike_part2_icons[i] = bike_part2_icons[i].replace("_off", "_on")

        bike_box.ids.part2_icon1.source = bike_part2_icons[0]
        bike_box.ids.part2_icon2.source = bike_part2_icons[1]
        bike_box.ids.part2_icon3.source = bike_part2_icons[2]
        bike_box.ids.part2_icon4.source = bike_part2_icons[3]
        bike_box.ids.part2_icon5.source = bike_part2_icons[4]

    def update_fun_box(self):
        self.comics_reader.refresh_image(self.color_set)
        fun_box = self.root.ids.fun_box
        fun_box.ids.comics_image.reload()

    def change_screen_colors(self, is_the_sun_up):
        if self.sun_is_up != is_the_sun_up:
            self.sun_is_up = is_the_sun_up

            if is_the_sun_up:
                color_set_name = "green"
            else:
                color_set_name = "orange"

            cs, csn = Colors().get_color_set(color_set_name)
            self.color_set = cs
            self.color_set_normalized = csn

            actual_size = (self.root.width, self.root.height)
            self.resize_callback(self.root, actual_size)

    def update_per_minute(self, dt):
        self.weather_data.update_actual_data()
        wd = self.weather_data

        self.change_screen_colors(wd.is_the_sun_up)
        self.update_weather_box(wd)
        self.update_wind_box(wd)
        self.update_bike_box(wd)

    def update_per_quarter(self, dt):
        self.update_fun_box()

    def update_per_hour(self, dt):
        wd = self.weather_data

        self.update_date_box(wd)
        self.update_moon_box(wd)


if __name__ == '__main__':
    HomeDashApp().run()
