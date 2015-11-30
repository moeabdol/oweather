import ujson
import requests

class OpenWeatherMapAPIWrapper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.current_weather_end_point = \
            "http://api.openweathermap.org/data/2.5/weather"
        self.five_day_three_hour_forecast_end_point = \
            "http://api.openweathermap.org/data/2.5/forecast"
        self.daily_forecast_end_point = \
            "http://api.openweathermap.org/data/2.5/forecast/daily"

    def get_current_weather_by_city_name(self, city, units):
        city_query = "?q={}".format(city)
        units_query = "&units={}".format(units)
        appid_query = "&APPID={}".format(self.api_key)
        end_point = self.current_weather_end_point + city_query + \
                    units_query + appid_query
        return ujson.loads(requests.get(end_point).text)

    def get_five_day_three_hour_forecast_by_city_name(self, city, units):
        city_query = "?q={}".format(city)
        units_query = "&units={}".format(units)
        appid_query = "&APPID={}".format(self.api_key)
        end_point = self.five_day_three_hour_forecast_end_point + city_query + \
                    units_query + appid_query
        return ujson.loads(requests.get(end_point).text)

    def get_daily_forecast_by_city_name(self, city, days, units):
        city_query = "?q={}".format(city)
        days_query = "&cnt={}".format(days)
        units_query = "&units={}".format(units)
        appid_query = "&APPID={}".format(self.api_key)
        end_point = self.daily_forecast_end_point + city_query + days_query + \
                    units_query + appid_query
        return ujson.loads(requests.get(end_point).text)
