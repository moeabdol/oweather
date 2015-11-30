#!/usr/bin/env python
import argparse
from argparse import ArgumentParser
from oweather_api_wrapper import OpenWeatherMapAPIWrapper
from oweather_api_parser import OpenWeatherMapAPIParser
from oweather_printer import OpenWeatherMapPrinter

class OpenWeatherMap:
    def __init__(self):
        self.args = self.process_arguments()
        self.wrapper = OpenWeatherMapAPIWrapper(self.get_api_key())
        self.parser = OpenWeatherMapAPIParser()
        self.printer = OpenWeatherMapPrinter()

    def process_arguments(self):
        parser = ArgumentParser(description="Display weather information on " +
                                "the command line using Open Weather Map API")
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
        forecast_group = parser.add_mutually_exclusive_group(required=False)
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
            type=self.check_days,
            help="N days daily weather forcast (N >= 16)")
        unit_group = parser.add_mutually_exclusive_group(required=False)
        unit_group.add_argument(
            "-m",
            "--metric",
            dest="units",
            const="metric",
            action="store_const",
            default="metric",
            help="print weather data in metric system (default)")
        unit_group.add_argument(
            "-i",
            "--imperial",
            dest="units",
            const="imperial",
            action="store_const",
            help="print weather data in imperial system")
        parser.add_argument(
            "city",
            help="name of city you want to get weather for",
            nargs=1)
        return parser.parse_args()

    def check_days(self, days):
        try:
            d = int(days)
            if d > 16 or d < 1:
                raise ValueError
        except:
            raise argparse.ArgumentTypeError("%s is not a valid value for days"
                                             % days)
        return d

    def get_api_key(self):
        if self.args.token is not None:
            return self.args.token
        elif self.args.file is not None:
            for line in self.args.file.readlines():
                key, value = line.partition("=")[::2]
                if key.strip() == "oweather_api_key":
                    return value.strip()[1:-1]

    def get_weather(self):
        if self.args.forecast is True:
            self.printer.print_five_day_three_hour_forecast(
                self.parser.parse_five_day_three_hour_forecast(
                    self.wrapper.get_five_day_three_hour_forecast_by_city_name(
                        self.args.city[0], self.args.units)))
        elif self.args.n > 0:
            self.printer.print_daily_forcast(
                self.parser.parse_daily_forecast(
                    self.wrapper.get_daily_forecast_by_city_name(
                        self.args.city[0], self.args.n, self.args.units)))
        else:
            self.printer.print_current_weather(
                self.parser.parse_current_weather(
                    self.wrapper.get_current_weather_by_city_name(
                        self.args.city[0], self.args.units)))

if __name__ == "__main__":
    oweather = OpenWeatherMap()
    oweather.get_weather()
