import sys
import ujson
import requests
import json as jjson
import datetime

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
            data = {"json": json, "units": units}
            parsed_data = self.parse_current_weather(data)
            self.print_json(parsed_data)
            return parsed_data
        except requests.exceptions.ConnectionError:
            sys.exit("Network error")
        except ValueError:
            sys.exit("Invalid API key")

    def parse_current_weather(self, data):
        json = data["json"]
        units = data["units"]
        _dict = {}
        _dict["city_id"] = json["id"]
        _dict["city"] = json["name"]
        _dict["country"] = json["sys"]["country"]
        _dict["units"] = units
        _dict["dt_local"] = \
            self.convert_timestamp_to_local_datetime(json["dt"])
        _dict["dt_utc"] = \
            self.convert_timestamp_to_utc_datetime(json["dt"])
        _dict["sunrise"] = json["sys"]["sunrise"]
        _dict["sunset"] = json["sys"]["sunset"]
        _dict["coord_lon"] = json["coord"]["lon"]
        _dict["coord_lat"] = json["coord"]["lat"]
        _dict["humidity"] = json["main"]["humidity"]
        _dict["pressure"] = json["main"]["pressure"]
        _dict["temp"] = json["main"]["temp"]
        _dict["temp_min"] = json["main"]["temp_min"]
        _dict["temp_max"] = json["main"]["temp_max"]
        _dict["weather_id"] = json["weather"][0]["id"]
        _dict["weather_icon"] = json["weather"][0]["icon"]
        _dict["weather_main"] = json["weather"][0]["main"]
        _dict["weather_desc"] = json["weather"][0]["description"]
        _dict["wind_deg"] = json["wind"]["deg"]
        _dict["wind_speed"] = json["wind"]["speed"]
        _dict["clouds_perc"] = json["clouds"]["all"]
        if "sea_level" in json["main"]:
            _dict["sea_level"] = json["main"]["sea_level"]
        if "grnd_level" in json["main"]:
            _dict["grnd_level"] = json["main"]["grnd_level"]
        if "rain" in json:
            _dict["rain_volume"] = json["rain"]["3h"]
        if "snow" in json:
            _dict["snow_volume"] = json["snow"]["3h"]
        return _dict

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

    def parse_five_day_three_hour_forecast(self, data):
        json = data["json"]
        units = data["units"]
        _dict = {}
        _dict["city_id"] = json["city"]["id"]
        _dict["city"] = json["city"]["name"]
        _dict["country"] = json["city"]["country"]
        _dict["units"] = units
        _dict["coord_lon"] = json["city"]["coord"]["lon"]
        _dict["coord_lat"] = json["city"]["coord"]["lat"]
        _dict["cnt"] = json["cnt"]
        _list = []
        for obj in json["list"]:
            weather = {}
            weather["dt_forcasted_local"] = \
                self.convert_timestamp_to_local_datetime(obj["dt"])
            weather["dt_forcasted_utc"] = \
                self.convert_timestamp_to_utc_datetime(obj["dt"])
            weather["dt_txt"] = obj["dt_txt"]
            weather["humidity"] = obj["main"]["humidity"]
            weather["pressure"] = obj["main"]["pressure"]
            weather["temp"] = obj["main"]["temp"]
            weather["weather_main"] = obj["weather"][0]["main"]
            weather["weather_desc"] = obj["weather"][0]["description"]
            weather["wind_deg"] = obj["wind"]["deg"]
            weather["wind_speed"] = obj["wind"]["speed"]
            weather["clouds_perc"] = obj["clouds"]["all"]
            if "rain" in obj:
                weather["rain_volume"] = obj["rain"].get("3h")
            if "snow" in obj:
                weather["snow_volume"] = obj["snow"].get("3h")
            _list.append(weather)
        _dict["list"] = _list
        return _dict

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

    def convert_timestamp_to_local_datetime(self, utc_time):
        return datetime.datetime.fromtimestamp(int(utc_time)).strftime(
            "%Y-%m-%d %H:%M:%S")

    def convert_timestamp_to_utc_datetime(self, utc_time):
        return datetime.datetime.utcfromtimestamp(int(utc_time)).strftime(
            "%Y-%m-%d %H:%M:%S")
