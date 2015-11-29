import json
from oweather_api_parser import OpenWeatherMapAPIParser
from prettytable import PrettyTable
import ipdb

class OpenWeatherMapPrinter:
  def __init__(self, api_key):
    self.parser = OpenWeatherMapAPIParser(api_key)

  def print_current_weather(self, city):
    current_weather = self.parser.parse_current_weather(city)
    print
    print "Location:\t", current_weather["city"], ", ", \
          current_weather["country"]
    print "Weather:\t", current_weather["weather_main"], ", ", \
          current_weather["weather_desc"]
    table = PrettyTable(["Variable", "Measurement", "Unit"])
    table.align["Variable"] = "l"
    table.add_row(["Temperature", current_weather["temp"], "Kelvin"])
    table.add_row(["Humidity", current_weather["humidity"], "%"])
    table.add_row(["Pressure", current_weather["pressure"], "hPa"])
    table.add_row(["Wind Speed", current_weather["wind_speed"], "meter/sec"])
    table.add_row(["Wind Direction", current_weather["wind_deg"], ""])
    table.add_row(["Clouds", current_weather["clouds_perc"], "%"])
    if current_weather["rain_volume"] is None:
      table.add_row(["Rain Volume", 0, "mm"])
    else:
      table.add_row(["Rain Volume", current_weather["rain_volume"], "mm"])
    if current_weather["snow_volume"] is None:
      table.add_row(["Snow Volume", 0, "mm"])
    else:
      table.add_row(["Snow Volume", current_weather["snow_volume"], "mm"])
    print table

  def print_five_day_three_hour_forecast(self, city):
    # weather_json_list = self.parser.parse_five_day_three_hour_forecast(city)
    # for weather_dict in weather_json_list:
    #   self.print_json(weather_dict)
    forecast_list = self.parser.parse_five_day_three_hour_forecast(city)
    city, country = forecast_list[0]["city"], forecast_list[0]["country"]
    for forecast in forecast_list[1:]:
      print "Location:\t", city, ", ", country
      print "Date/Time:\t", forecast["dt_text"]
      print "Weather:\t", forecast["weather_main"], ", ", \
            forecast["weather_desc"]
      table = PrettyTable(["Variable", "Measurement", "Unit"])
      table.align["Variable"] = "l"
      table.add_row(["Temperature", forecast["temp"], "Kelvin"])
      table.add_row(["Humidity", forecast["humidity"], "%"])
      table.add_row(["Pressure", forecast["pressure"], "hPa"])
      table.add_row(["Wind Speed", forecast["wind_speed"], "meter/sec"])
      table.add_row(["Wind Direction", forecast["wind_deg"], ""])
      table.add_row(["Clouds", forecast["clouds_perc"], "%"])
      if forecast["rain_volume"] is None:
        table.add_row(["Rain Volume", 0, "mm"])
      else:
        table.add_row(["Rain Volume", forecast["rain_volume"], "mm"])
      if forecast["snow_volume"] is None:
        table.add_row(["Snow Volume", 0, "mm"])
      else:
        table.add_row(["Snow Volume", forecast["snow_volume"], "mm"])
      print table
      print

  def print_daily_forcast(self, city, days):
    weather_json_list = self.parser.parse_daily_forecast(city, days)
    for weather_dict in weather_json_list:
      self.print_json(weather_dict)

  def print_json(self, json_dict):
    print json.dumps(json_dict, sort_keys=True, indent=4,
                      separators=(",", ": "))
