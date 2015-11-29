#!/usr/bin/env python
import requests
import json
import ujson
import argparse
from argparse import ArgumentParser
from oweather_printer import OpenWeatherMapPrinter

def process_arguments():
  parser = ArgumentParser(description="Display weather information on the " +
                          "command line using Open Weather Map API")
  forecast_group = parser.add_mutually_exclusive_group()
  forecast_group.add_argument(
      "-f",
      "--forecast",
      dest="forecast",
      action="store_true",
      help="five day three hour weather forcast")
  forecast_group.add_argument(
      "-d",
      "--days",
      dest="n",
      type=int,
      help="N days weather forcast")
  key_group = parser.add_mutually_exclusive_group(required=True)
  key_group.add_argument(
      "-k",
      dest="token",
      type=str,
      help="provide open weather map API key token from command line")
  key_group.add_argument(
      "-K",
      dest="file",
      type=argparse.FileType("r"),
      help="provide open weather map API key file")
  parser.add_argument(
      "city",
      help="name of city you want to get weather for",
      nargs=1)
  return parser.parse_args()

def print_weather_info(args, api_key):
  printer = OpenWeatherMapPrinter(api_key)
  if args.forecast is True:
    printer.print_five_day_three_hour_forecast(args.city[0])
  elif args.n > 0:
    printer.print_daily_forcast(args.city[0], args.n)
    pass
  else:
    printer.print_current_weather(args.city[0])

def get_api_key(args):
  if args.token is not None:
    return args.token
  elif args.file is not None:
    for line in args.file.readlines():
      key, value = line.partition("=")[::2]
      if key.strip() == "oweather_api_key":
        return value.strip()[1:-1]

if __name__ == "__main__":
  args = process_arguments()
  api_key = get_api_key(args)
  print_weather_info(args, api_key)
