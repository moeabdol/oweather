#!/usr/bin/env python
# -*- coding: utf-8 -*-

from oweather_controller import OpenWeatherController

owc = OpenWeatherController()
data = owc.get_weather()
owc.view.print_weather(data)
