# -*- coding: utf-8 -*-
import json as jjson
from oweather_wrapper import OpenWeatherWrapper
from oweather_parser import OpenWeatherParser

class OpenWeatherModel(object):
    def __init__(self, api_key):
        self.wrapper = OpenWeatherWrapper(api_key)
        self.parser = OpenWeatherParser()

    def get_current_weather(self, city, units):
        json = self.wrapper.get_current_weather(city, units)
        data = self.parser.parse_current_weather(json)
        return data

    def get_five_day_forecast(self, city, units):
        json = self.wrapper.get_five_day_forecast(city, units)
        data = self.parser.parse_five_day_forecast(json)
        return data

    def get_daily_forecast(self, city, days, units):
        json = self.wrapper.get_daily_forecast(city, days, units)
        data = self.parser.parse_daily_forecast(json)
        return data

    def print_json(self, json):
        print jjson.dumps(json, indent=4, sort_keys=True)

# if __name__ == "__main__":
#     key = "d0fc78d57e3d1d08f2a3241f8bc47d3c"
#     m = OpenWeatherModel(key)
#     data = m.get_current_weather("riyadh", "metric")
#     data = m.get_five_day_forecast("riyadh", "metric")
#     data = m.get_daily_forecast("riyadh", 3, "imperial")
#     m.print_json(data)
