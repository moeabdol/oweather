#!/usr/bin/env python
import requests
import json
import ujson
import argparse
from argparse import ArgumentParser
import ipdb

class OpenWeatherMapAPIWrapper:
  def __init__(self, api_key):
    self.api_key = api_key
    self.current_weather_end_point = \
      "http://api.openweathermap.org/data/2.5/weather"
    self.five_day_three_hour_forecast_end_point = \
      "http://api.openweathermap.org/data/2.5/forecast"
    self.daily_forecast_end_point = \
      "http://api.openweathermap.org/data/2.5/forecast/daily"

  def get_current_weather_by_city_name(self, city):
    city_query = "?q={}".format(city)
    appid_query = "&APPID={}".format(self.api_key)
    end_point = self.current_weather_end_point + city_query + appid_query
    return ujson.loads(requests.get(end_point).text)

  def get_five_day_three_hour_forecast_by_city_name(self, city):
    city_query = "?q={}".format(city)
    appid_query = "&APPID={}".format(self.api_key)
    end_point = self.five_day_three_hour_forecast_end_point + city_query + \
                appid_query
    return ujson.loads(requests.get(end_point).text)

  def get_daily_forecast_by_city_name(self, city, days):
    city_query = "?q={}".format(city)
    days_query = "&cnt={}".format(days)
    appid_query = "&APPID={}".format(self.api_key)
    end_point = self.daily_forecast_end_point + city_query + days_query + \
                appid_query
    return ujson.loads(requests.get(end_point).text)

class OpenWeatherMapAPIParser:
  def __init__(self, weather_json):
    self.weather_json = weather_json

  def parse_current_weather(self):
    weather_dict = {}
    try:
      weather_dict["city"] = self.weather_json["name"]
    except:
      print "Unknown city"
      return
    weather_dict["country"] = self.weather_json["sys"]["country"]
    weather_dict["humidity"] = self.weather_json["main"]["humidity"]
    weather_dict["pressure"] = self.weather_json["main"]["pressure"]
    weather_dict["temp"] = self.weather_json["main"]["temp"]
    weather_dict["weather_main"] = self.weather_json["weather"][0]["main"]
    weather_dict["weather_desc"] = \
      self.weather_json["weather"][0]["description"]
    weather_dict["wind_deg"] = self.weather_json["wind"]["deg"]
    weather_dict["wind_speed"] = self.weather_json["wind"]["speed"]
    weather_dict["clouds_perc"] = self.weather_json["clouds"]["all"]
    weather_dict["rain_volume"] = None
    weather_dict["snow_volume"] = None
    if weather_dict["weather_main"] == "Rain":
      weather_dict["rain_volume"] = self.weather_json["rain"]["3h"]
    elif weather_dict["weather_main"] == "Snow":
      weather_dict["snow_volume"] = self.weather_json["snow"]["3h"]
    return weather_dict

  def parse_five_day_three_hour_forecast(self):
    try:
      city = self.weather_json["city"]["name"]
    except:
      print "Unknown city"
      return
    country = self.weather_json["city"]["country"]
    weather_list = [{"city": city, "country": country}]
    for weather in self.weather_json["list"]:
      weather_dict = {}
      weather_dict = weather_dict["dt_txt"]
      weather_dict["humidity"] = weather["main"]["humidity"]
      weather_dict["pressure"] = weather["main"]["pressure"]
      weather_dict["temp"] = weather["main"]["temp"]
      weather_dict["weather_main"] = weather["weather"][0]["main"]
      weather_dict["weather_desc"] = weather["weather"][0]["description"]
      weather_dict["wind_deg"] = weather["wind"]["deg"]
      weather_dict["wind_speed"] = weather["wind"]["speed"]
      weather_dict["clouds_perc"] = weather["clouds"]["all"]
      weather_dict["rain_volume"] = None
      weather_dict["snow_volume"] = None
      if weather_dict["weather_main"] == "Rain":
        weather_dict["rain_volume"] = weather["rain"]["3h"]
      elif weather_dict["weather_main"] == "Snow":
        weather_dict["snow_volume"] = weather["snow"]["3h"]
      weather_list.append(weather_dict)
    return weather_list

  def parse_daily_forecast(self):
    try:
      city = self.weather_json["city"]["name"]
    except:
      print "Unknown city"
      return
    country = self.weather_json["city"]["country"]
    day_count = self.weather_json["cnt"]
    weather_list = [{"city": city, "country": country, "day_count": day_count}]
    for weather in self.weather_json["list"]:
      weather_dict = {}
      weather_dict["dt"] = weather["dt"]
      weather_dict["temp_day"] = weather["temp"]["day"]
      weather_dict["temp_min"] = weather["temp"]["min"]
      weather_dict["temp_max"] = weather["temp"]["max"]
      weather_dict["temp_night"] = weather["temp"]["night"]
      weather_dict["temp_eve"] = weather["temp"]["eve"]
      weather_dict["temp_morn"] = weather["temp"]["morn"]
      weather_dict["pressure"] = weather["pressure"]
      weather_dict["humidity"] = weather["humidity"]
      weather_dict["weather_main"] = weather["weather"][0]["main"]
      weather_dict["weather_desc"] = weather["weather"][0]["description"]
      weather_dict["wind_speed"] = weather["speed"]
      weather_dict["wind_deg"] = weather["deg"]
      weather_dict["clouds_perc"] = weather["clouds"]
      weather_dict["rain_volume"] = None
      weather_dict["snow_volume"] = None
      if weather_dict["weather_main"] == "Rain":
        weather_dict["rain_volume"] = weather["rain"]
      elif weather_dict["weather_main"] == "Snow":
        weather_dict["snow_volume"] = weather["snow"]
      weather_list.append(weather_dict)
    return weather_list

class OpenWeatherMapPrinter:
  @classmethod
  def print_current_weather(self, current_weather_json):
    try:
      city = current_weather_json["name"]
    except:
      print "Unknown city"
      return
    country = current_weather_json["sys"]["country"]
    print_json(current_weather_json)
    weather_list = self.parse_weather_json([current_weather_json])
    for weather in weather_list:
      print weather["rain_volume"], weather["humidity"]

  @classmethod
  def print_five_day_three_hour_forcast(self, current_weather_json):
    try:
      city = current_weather_json["city"]["name"]
    except:
      print "Unknown city"
      return
    country = current_weather_json["city"]["country"]
    weather_list = self.parse_weather_json(current_weather_json["list"])
    for weather in weather_list:
      print weather["rain_volume"], weather["humidity"]

  @classmethod
  def print_daily_forcast(self, current_weather_json):
    try:
      city = current_weather_json["city"]["name"]
    except:
      print "Unknown city"
      return
    country = current_weather_json["city"]["country"]
    weather_list = self.parse_weather_json(current_weather_json["list"])
    for weather in weather_list:
      print weather["rain_volume"], weather["humidity"]

  @classmethod
  def parse_weather_json(self, weather_json_list):
    parsed_weather_list = []
    for weather_json in weather_json_list:
      weather_dict = {}
      weather_dict["humidity"] = weather_json["main"]["humidity"]
      weather_dict["pressure"] = weather_json["main"]["pressure"]
      weather_dict["temp"] = weather_json["main"]["temp"]
      weather_dict["weather_name"] = weather_json["weather"][0]["main"]
      weather_dict["weather_description"] = weather_json["weather"][0]["description"]
      weather_dict["wind_deg"] = weather_json["wind"]["deg"]
      weather_dict["wind_speed"] = weather_json["wind"]["speed"]
      weather_dict["clouds_perc"] = weather_json["clouds"]["all"]
      weather_dict["rain_volume"] = None
      weather_dict["snow_volume"] = None
      if weather_dict["weather_name"] == "Rain":
        weather_dict["rain_volume"] = weather_json["rain"]["3h"]
      elif weather_dict["weather_name"] == "Snow":
        weather_dict["snow_volume"] = weather_json["snow"]["3h"]
      parsed_weather_list.append(weather_dict)
    return parsed_weather_list

def process_arguments():
  parser = ArgumentParser(description="Get weather information from the " +
                                      "Open Weather Map API")
  forecast_group = parser.add_mutually_exclusive_group()
  forecast_group.add_argument(
      "-f",
      "--forecast",
      dest="forecast",
      action="store_true",
      help="Get five day weather forcast for city")
  forecast_group.add_argument(
      "-d",
      "--days",
      dest="n",
      type=int,
      help="Get N days weather forcast for city")
  key_group = parser.add_mutually_exclusive_group(required=True)
  key_group.add_argument(
      "-k",
      "--key",
      type=str,
      help="Provide open weather map API key from command line")
  key_group.add_argument(
      "--key-file",
      dest="file",
      type=argparse.FileType("r"),
      help="Provide open weather map API key file")
  parser.add_argument(
      "city",
      help="Name of city you want to get weather for",
      nargs=1)
  return parser.parse_args()

def print_weather_info(owmaw, args):
  if args.forecast is True:
    # print_json(owmaw.get_five_day_three_hour_forcast_by_city_name(args.city[0]))
    OpenWeatherMapPrinter.print_five_day_three_hour_forcast(owmaw.get_five_day_three_hour_forcast_by_city_name(args.city[0]))
  elif args.n > 0:
    # print_json(owmaw.get_daily_forcast_by_city_name(args.city[0], days=args.n))
    OpenWeatherMapPrinter.print_daily_forcast(owmaw.get_daily_forcast_by_city_name(args.city[0], args.n))
  else:
    # print_json(owmaw.get_current_weather_by_city_name(args.city[0]))
    OpenWeatherMapPrinter.print_current_weather(owmaw.get_current_weather_by_city_name(args.city[0]))

def print_json(json_dict):
  print json.dumps(json_dict, sort_keys=True, indent=2,
                    separators=(",", ": 2"))

def get_api_key_from_file(f):
  for line in f.readlines():
    key, value = line.partition("=")[::2]
    if key.strip() == "oweather_api_key":
      return value.strip()[1:-1]

def get_api_key(args):
  if args.key is not None:
    return args.key
  elif args.file is not None:
    return get_api_key_from_file(args.file)

if __name__ == "__main__":
  args = process_arguments()
  api_key = get_api_key(args)
  owmaw = OpenWeatherMapAPIWrapper(api_key)

  # print_json(owmaw.get_current_weather_by_city_name(args.city[0]))
  # owmap = OpenWeatherMapAPIParser(owmaw.get_current_weather_by_city_name(args.city[0]))
  # print_json(owmap.parse_current_weather())
  #
  # print_json(owmaw.get_five_day_three_hour_forecast_by_city_name(args.city[0]))
  # owmap = OpenWeatherMapAPIParser(owmaw.get_five_day_three_hour_forecast_by_city_name(args.city[0]))
  # for weather in owmap.parse_five_day_three_hour_forecast():
  #   print_json(weather)

  print_json(owmaw.get_daily_forecast_by_city_name(args.city[0], args.n))
  owmap = OpenWeatherMapAPIParser(owmaw.get_daily_forecast_by_city_name(args.city[0], args.n))
  for weather in owmap.parse_daily_forecast():
    print_json(weather)
