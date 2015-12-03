import sys
import ujson
import requests
import json as jjson

class OpenWeatherMapModel:
    def __init__(self, api_key):
        self.api_key = api_key
        self.current_weather_api_end_point = \
            "http://api.openweathermap.org/data/2.5/weather"
        self.five_day_three_hour_forecast_api_end_point = \
            "http://api.openweathermap.org/data/2.5/forecast"
        self.daily_forecast_api_end_point = \
            "http://api.openweathermap.org/data/2.5/forecast/daily"

    def get_current_weather(self, city, units):
        c = "?q={}".format(city)
        u = "&units={}".format(units)
        aid = "&APPID={}".format(self.api_key)
        api_end_point = self.current_weather_api_end_point + c + u + aid
        try:
            json = ujson.loads(requests.get(api_end_point).text)
            if int(json["cod"]) == 404:
                sys.exit("City not found")
            return {"json": json, "units": units}
        except requests.exceptions.ConnectionError:
            sys.exit("Network error")
        except ValueError:
            sys.exit("Invalid API key")

    def get_five_day_three_hour_forecast(self, city, units):
        c = "?q={}".format(city)
        u = "&units={}".format(units)
        aid = "&APPID={}".format(self.api_key)
        api_end_point = self.five_day_three_hour_forecast_api_end_point + \
                        c + u + aid
        try:
            json = ujson.loads(requests.get(api_end_point).text)
            if int(json["cod"]) == 404:
                sys.exit("City not found")
            return {"json": json, "units": units}
        except requests.exceptions.ConnectionError:
            sys.exit("Network Error")
        except ValueError:
            sys.exit("Invalid API Key")

    def get_daily_forecast(self, city, days, units):
        c = "?q={}".format(city)
        d = "&cnt={}".format(days)
        u = "&units={}".format(units)
        aid = "&APPID={}".format(self.api_key)
        api_end_point = self.daily_forecast_api_end_point + c + d + u + aid
        try:
            json = ujson.loads(requests.get(api_end_point).text)
            if int(json["cod"]) == 404:
                sys.exit("City not found")
            return {"json": json, "units": units, "days": days}
        except requests.exceptions.ConnectionError:
            sys.exit("Network Error")
        except ValueError:
            sys.exit("Invalid API Key")

    def print_json(self, json):
        print jjson.dumps(json, indent=4, sort_keys=True)
