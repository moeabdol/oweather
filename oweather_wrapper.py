# -*- coding: utf-8 -*-

import sys
import ujson
import requests

class OpenWeatherWrapper(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url              = "http://api.openweathermap.org/data/2.5/"
        self.current_weather_url   = "weather?q={}&units={}&APPID={}"
        self.five_day_forecast_url = "forecast?q={}&units={}&APPID={}"
        self.daily_forecast_url = "forecast/daily?q={}&cnt={}&units={}&APPID={}"

    def get_current_weather(self, city, units):
        url = self.base_url + self.current_weather_url.format(
            city, units, self.api_key)
        json = self.call_api(url)
        data = {"json": json, "units": units}
        return data

    def get_five_day_forecast(self, city, units):
        url = self.base_url + self.five_day_forecast_url.format(
            city, units, self.api_key)
        json = self.call_api(url)
        data = {"json": json, "units": units}
        return data

    def get_daily_forecast(self, city, days, units):
        url = self.base_url + self.daily_forecast_url.format(
            city, days, units, self.api_key)
        json = self.call_api(url)
        data = {"json": json, "days": days, "units": units}
        return data

    def call_api(self, url):
        try:
            json = ujson.loads(requests.get(url).text)
            if int(json["cod"]) != 200:
                sys.exit("City not found")
            return json
        except requests.exceptions.ConnectionError:
            sys.exit("Network Error")
        except ValueError:
            sys.exit("Invalid API Key")
