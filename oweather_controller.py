import sys
import os.path
import argparse
from oweather_model import OpenWeatherModel

class OpenWeatherController:
    def __init__(self):
        self.args = self.process_arguments()
        self.model = OpenWeatherModel(self.get_api_token())

    def process_arguments(self):
        parser = argparse.ArgumentParser(
            description="Display weather information on the command line " +
            "using Open Weather Map API")
        parser.add_argument(
            "-v",
            "--version",
            action="version",
            version="%(prog)s 0.0.1")
        parser.add_argument(
            "-k",
            dest="api_token",
            type=str,
            default=None,
            help="connect to open weather map using API key token")
        forecast_group = parser.add_mutually_exclusive_group(required=False)
        forecast_group.add_argument(
            "-f",
            "--forecast",
            dest="forecast",
            action="store_true",
            help="show five day three hour weather forcast")
        forecast_group.add_argument(
            "-d",
            "--days",
            dest="n",
            type=self.check_days,
            help="show N days daily weather forcast (N >= 16)")
        unit_group = parser.add_mutually_exclusive_group(required=False)
        unit_group.add_argument(
            "-m",
            "--metric",
            dest="units",
            const="metric",
            action="store_const",
            default="metric",
            help="show weather data in metric system (default)")
        unit_group.add_argument(
            "-i",
            "--imperial",
            dest="units",
            const="imperial",
            action="store_const",
            help="show weather data in imperial system")
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

    def get_api_token(self):
        if self.args.api_token is None:
            try:
                return self.get_rc_configs()["api_key"]
            except:
                print "api key is not set in .oweatherrc file"
                sys.exit(1)
        else:
            return self.args.api_token

    def get_rc_configs(self):
        try:
            if os.path.isfile("./.oweatherrc"):
                return self.read_rc_configs_from_file("./.oweatherrc")
            elif os.path.isfile("~/.oweatherrc"):
                return self.read_rc_configs_from_file("~/.oweatherrc")
            else:
                raise IOError
        except IOError:
            print ".oweatherrc file does not exist"
            sys.exit(1)

    def read_rc_configs_from_file(self, file_path):
        rc_configs = {}
        with open(file_path) as f:
            for line in f:
                key, value = line.partition("=")[::2]
                rc_configs[key.strip()] = value.strip()[1:-1]
        return rc_configs

    def get_weather(self):
        city = self.args.city[0]
        forecast = self.args.forecast
        days = self.args.n
        units = self.args.units
        if forecast:
            return self.model.get_five_day_forecast(city, units)
        elif days:
            return self.model.get_daily_forecast(city, days, units)
        else:
            return self.model.get_current_weather(city, units)

if __name__ == "__main__":
    controller = OpenWeatherController()
    data = controller.get_weather()
    controller.model.print_json(data)
