#!/usr/bin/env python
from oweather_controller import OpenWeatherController

owc = OpenWeatherController()
data = owc.get_weather()
owc.view.print_weather(data)
