import json
from oweather_api_parser import OpenWeatherMapAPIParser
import ipdb

class OpenWeatherMapPrinter:
  def __init__(self, api_key):
    self.parser = OpenWeatherMapAPIParser(api_key)

  def print_current_weather(self, city):
    self.print_json(self.parser.parse_current_weather(city))

  def print_five_day_three_hour_forecast(self, city):
    weather_json_list = self.parser.parse_five_day_three_hour_forecast(city)
    for weather_dict in weather_json_list:
      self.print_json(weather_dict)

  def print_daily_forcast(self, city, days):
    weather_json_list = self.parser.parse_daily_forecast(city, days)
    for weather_dict in weather_json_list:
      self.print_json(weather_dict)

  def print_json(self, json_dict):
    print json.dumps(json_dict, sort_keys=True, indent=4,
                      separators=(",", ": "))
