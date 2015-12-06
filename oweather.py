#!/usr/bin/env python
import argparse
from argparse import ArgumentParser
from oweather_model import OpenWeatherMapModel
from oweather_controller import OpenWeatherMapController
from oweather_view import OpenWeatherMapView
import os.path
import ipdb
import sys

# class OpenWeatherMap:
#     def __init__(self):
#         self.args = self.process_arguments()
#         self.model = OpenWeatherMapModel(self.get_api_token())
        # self.controller = OpenWeatherMapController()
        # self.view = OpenWeatherMapView()

    # def get_weather(self):
    #     if self.args.forecast is True:
    #         self.printer.print_five_day_three_hour_forecast(
    #             self.parser.parse_five_day_three_hour_forecast(
    #                 self.wrapper.get_five_day_three_hour_forecast(
    #                     self.args.city[0], self.args.units)))
    #     elif self.args.n > 0:
    #         self.printer.print_daily_forcast(
    #             self.parser.parse_daily_forecast(
    #                 self.wrapper.get_daily_forecast(
    #                     self.args.city[0], self.args.n, self.args.units)))
    #     else:
    #         self.printer.print_current_weather(
    #             self.parser.parse_current_weather(
    #                 self.wrapper.get_current_weather(
    #                     self.args.city[0], self.args.units)))
    #
if __name__ == "__main__":
    # ow = OpenWeatherMap()
    # ow.model.get_current_weather(ow.args.city[0], ow.args.units)
    # ow.model.get_five_day_three_hour_forecast(ow.args.city[0], ow.args.units)
    # ow.model.get_daily_forecast(ow.args.city[0], 16, ow.args.units)
    pass
