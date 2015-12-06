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
            self.print_json(json)
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
        json    = data["json"]
        units   = data["units"]
        no_info = "No information available!"
        _dict = {}
        _dict["City ID"] = json.get("id"   , no_info)
        _dict["City"]    = json.get("name" , no_info)
        _dict["Units"]   = units
        _dict["Last Updated (Local)"] = \
            self.convert_timestamp_to_local_datetime(json.get("dt", no_info))
        _dict["Last Updated (UTC)"] = \
            self.convert_timestamp_to_utc_datetime(json.get("dt", no_info))
        if "sys" in json:
            _dict["Country"] = json["sys"].get("country", no_info)
            _dict["Sunrise (Local)"] = \
                self.convert_timestamp_to_local_datetime(json["sys"].get(
                    "sunrise", no_info))
            _dict["Sunset (Local)"] = \
                self.convert_timestamp_to_local_datetime(json["sys"].get(
                    "sunset", no_info))
            _dict["Sunrise (UTC)"] = \
                self.convert_timestamp_to_utc_datetime(json["sys"].get(
                    "sunrise", no_info))
            _dict["Sunset (UTC)"] = \
                self.convert_timestamp_to_utc_datetime(json["sys"].get(
                    "sunset", no_info))
        if "coord" in json:
            _dict["Longtitude"] = json["coord"].get("lon", no_info)
            _dict["Latitude"]   = json["coord"].get("lat", no_info)
        if "main" in json:
            main = json["main"]
            _dict["Humidity"]          = main.get("humidity"   , no_info)
            _dict["Pressure"]          = main.get("pressure"   , no_info)
            _dict["Temperature"]       = main.get("temp"       , no_info)
            _dict["Temperature (Min)"] = main.get("temp_min"   , no_info)
            _dict["Temperature (Max)"] = main.get("temp_max"   , no_info)
            _dict["Sea Level"]         = main.get("sea_level"  , no_info)
            _dict["Ground Level"]      = main.get("grnd_level" , no_info)
        if "weather" in json and json["weather"][0]:
            weather = json["weather"][0]
            _dict["Weather ID"]          = weather.get("id"          , no_info)
            _dict["Weather Icon"]        = weather.get("icon"        , no_info)
            _dict["Weather Main"]        = weather.get("main"        , no_info)
            _dict["Weather Description"] = weather.get("description" , no_info)
        if "wind" in json:
            wind = json["wind"]
            _dict["Wind Direction"] = wind.get("deg"   , no_info)
            _dict["Wind Speed"]     = wind.get("speed" , no_info)
            _dict["Wind Gust"]      = wind.get("gust"  , no_info)
        if "clouds" in json:
            _dict["Clouds"] = json["clouds"].get("all", no_info)
        if "rain" in json:
            _dict["Rain Volume"] = json["rain"].get("3h", no_info)
        if "snow" in json:
            _dict["Snow Volume"] = json["snow"].get("3h", no_info)
        return _dict

    def get_five_day_three_hour_forecast(self, city, units):
        c =              "?q={}".format(city)
        u =              "&units={}".format(units)
        aid =            "&APPID={}".format(self.api_key)
        api_end_point =  self.five_day_three_hour_forecast_api_end_point + \
            c + u + aid
        try:
            json = ujson.loads(requests.get(api_end_point).text)
            if int(json["cod"]) == 404:
                sys.exit("City not found")
            data = {"json": json, "units": units}
            parsed_data = self.parse_five_day_three_hour_forecast(data)
            self.print_json(parsed_data)
            return parsed_data
        except requests.exceptions.ConnectionError:
            sys.exit("Network Error")
        except ValueError:
            sys.exit("Invalid API Key")

    def parse_five_day_three_hour_forecast(self, data):
        json = data["json"]
        _dict = {}
        _dict["City ID"]    = json["city"]["id"]
        _dict["City"]       = json["city"]["name"]
        _dict["Country"]    = json["city"]["country"]
        _dict["Units"]      = data["units"]
        _dict["Longtitude"] = json["city"]["coord"]["lon"]
        _dict["Latitude"]   = json["city"]["coord"]["lat"]
        _dict["Line Count"] = json["cnt"]
        _list = []
        for obj in json["list"]:
            weather = {}
            weather["Forecasted Timestamp"] = obj["dt"]
            weather["Forecasted Datetime (Local)"] = \
                self.convert_timestamp_to_local_datetime(obj["dt"])
            weather["Forecasted Datetime (UTC)"] = \
                self.convert_timestamp_to_utc_datetime(obj["dt"])
            weather["Datetime Text (UTC)"] = obj["dt_txt"]
            weather["Humidity"]            = obj["main"]["humidity"]
            weather["Pressure"]            = obj["main"]["pressure"]
            weather["Sea Level"]           = obj["main"]["sea_level"]
            weather["Ground Level"]        = obj["main"]["grnd_level"]
            weather["Temperature"]         = obj["main"]["temp"]
            weather["Temperature (Min)"]   = obj["main"]["temp_min"]
            weather["Temperature (Max)"]   = obj["main"]["temp_max"]
            weather["Weather ID"]          = obj["weather"][0]["id"]
            weather["Weather Icon"]        = obj["weather"][0]["icon"]
            weather["Weather Main"]        = obj["weather"][0]["main"]
            weather["Weather Description"] = obj["weather"][0]["description"]
            weather["Wind Direction"]      = obj["wind"]["deg"]
            weather["Wind Speed"]          = obj["wind"]["speed"]
            weather["Clouds"]              = obj["clouds"]["all"]
            if "rain" in obj:
                weather["Rain Volume"] = obj["rain"].get("3h")
            if "snow" in obj:
                weather["Snow Volume"] = obj["snow"].get("3h")
            _list.append(weather)
        _dict["list"] = _list
        return _dict

    def get_daily_forecast(self, city, days, units):
        c =              "?q={}".format(city)
        d =              "&cnt={}".format(days)
        u =              "&units={}".format(units)
        aid =            "&APPID={}".format(self.api_key)
        api_end_point =  self.daily_forecast_api_end_point + c + d + u + aid
        try:
            json = ujson.loads(requests.get(api_end_point).text)
            if int(json["cod"]) == 404:
                sys.exit("City not found")
            data = {"json": json, "units": units, "days": days}
            parsed_data = self.parse_daily_forecast(data)
            # self.print_json(parsed_data)
            return parsed_data
        except requests.exceptions.ConnectionError:
            sys.exit("Network Error")
        except ValueError:
            sys.exit("Invalid API Key")

    def parse_daily_forecast(self, data):
        json = data["json"]
        _dict = {}
        _dict["city_id"]   = json["city"]["id"]
        _dict["city"]      = json["city"]["name"]
        _dict["country"]   = json["city"]["country"]
        _dict["units"]     = data["units"]
        _dict["days"]      = data["days"]
        _dict["coord_lon"] = json["city"]["coord"]["lon"]
        _dict["coord_lat"] = json["city"]["coord"]["lat"]
        _dict["cnt"]       = json["cnt"]
        _list = []
        for obj in json["list"]:
            weather = {}
            weather["dt"] = obj["dt"]
            weather["dt_forecasted_local"] = \
                self.convert_timestamp_to_local_datetime(obj["dt"])
            weather["dt_forecasted_utc"] = \
                self.convert_timestamp_to_utc_datetime(obj["dt"])
            weather["temp_day"]     = obj["temp"]["day"]
            weather["temp_min"]     = obj["temp"]["min"]
            weather["temp_max"]     = obj["temp"]["max"]
            weather["temp_night"]   = obj["temp"]["night"]
            weather["temp_eve"]     = obj["temp"]["eve"]
            weather["temp_morn"]    = obj["temp"]["morn"]
            weather["pressure"]     = obj["pressure"]
            weather["humidity"]     = obj["humidity"]
            weather["weather_id"]   = obj["weather"][0]["id"]
            weather["weather_icon"] = obj["weather"][0]["icon"]
            weather["weather_main"] = obj["weather"][0]["main"]
            weather["weather_desc"] = obj["weather"][0]["description"]
            weather["wind_speed"]   = obj["speed"]
            weather["wind_deg"]     = obj["deg"]
            weather["clouds_perc"]  = obj["clouds"]
            weather["rain_volume"]  = None
            weather["snow_volume"]  = None
            if "rain" in obj:
                weather["rain_volume"] = obj["rain"]
            if "snow" in obj:
                weather["snow_volume"] = obj["snow"]
            if "gust" in obj:
                weather["wind_gust"] = obj["gust"]
            _list.append(weather)
        _dict["list"] = _list
        return _dict

    def print_json(self, json):
        print jjson.dumps(json, indent=4, sort_keys=True)

    def convert_timestamp_to_local_datetime(self, utc_time):
        return datetime.datetime.fromtimestamp(int(utc_time)).strftime(
            "%Y-%m-%d %H:%M:%S")

    def convert_timestamp_to_utc_datetime(self, utc_time):
        return datetime.datetime.utcfromtimestamp(int(utc_time)).strftime(
            "%Y-%m-%d %H:%M:%S")
