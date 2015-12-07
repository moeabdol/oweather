from datetime import datetime

class OpenWeatherParser(object):
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

    def parse_five_day_forecast(self, data):
        json    = data["json"]
        units   = data["units"]
        no_info = "No information available!"
        _dict = {}
        _dict["Units"] = units
        if "city" in json:
            city = json["city"]
            _dict["City ID"] = city.get("id", no_info)
            _dict["City"]    = city.get("name", no_info)
            _dict["Country"] = city.get("country", no_info)
            if "coord" in city:
                coord = city["coord"]
                _dict["Longtitude"] = coord.get("lon", no_info)
                _dict["Latitude"]   = coord.get("lat", no_info)
        _list = []
        for obj in json["list"]:
            weather = {}
            weather["Forecasted Timestamp"] = obj.get("dt", no_info)
            weather["Forecasted Datetime (Local)"] = \
                self.convert_timestamp_to_local_datetime(obj.get("dt", no_info))
            weather["Forecasted Datetime (UTC)"] = \
                self.convert_timestamp_to_utc_datetime(obj.get("dt", no_info))
            weather["Datetime Text (UTC)"] = obj["dt_txt"]
            if "main" in obj:
                main = obj["main"]
                weather["Humidity"]          = main.get("humidity",    no_info)
                weather["Pressure"]          = main.get("pressure",    no_info)
                weather["Sea Level"]         = main.get("sea_level",   no_info)
                weather["Ground Level"]      = main.get("grnd_level",  no_info)
                weather["Temperature"]       = main.get("temp",        no_info)
                weather["Temperature (Min)"] = main.get("temp_min",    no_info)
                weather["Temperature (Max)"] = main.get("temp_max",    no_info)
            if "weather" in obj and obj["weather"][0]:
                wthr = obj["weather"][0]
                weather["Weather ID"]          = wthr.get("id"   , no_info)
                weather["Weather Icon"]        = wthr.get("icon" , no_info)
                weather["Weather Main"]        = wthr.get("main" , no_info)
                weather["Weather Description"] = wthr.get("description",no_info)
            if "wind" in obj:
                wind = obj["wind"]
                weather["Wind Direction"] = wind.get("deg"   , no_info)
                weather["Wind Speed"]     = wind.get("speed" , no_info)
                weather["Wind Gust"]      = wind.get("gust"  , no_info)
            if "clouds" in obj:
                weather["Clouds"] = obj["clouds"].get("all", no_info)
            if "rain" in obj:
                weather["Rain Volume"] = obj["rain"].get("3h", no_info)
            if "snow" in obj:
                weather["Snow Volume"] = obj["snow"].get("3h", no_info)
            _list.append(weather)
        _dict["list"] = _list
        return _dict

    def parse_daily_forecast(self, data):
        json = data["json"]
        units = data["units"]
        no_info = "No information available!"
        _dict = {}
        _dict["Units"]     = units
        _dict["Days"]      = data["days"]
        if "city" in json:
            city = json["city"]
            _dict["City ID"]   = city.get("id"      , no_info)
            _dict["City"]      = city.get("name"    , no_info)
            _dict["Country"]   = city.get("country" , no_info)
            if "coord" in city:
                coord = city["coord"]
                _dict["Longtitude"] = coord.get("lon", no_info)
                _dict["Latitude"]   = coord.get("lat", no_info)
        _list = []
        for obj in json["list"]:
            weather = {}
            weather["Forecasted Timestamp"] = obj["dt"]
            weather["Forecast Datetime (Local)"] = \
                self.convert_timestamp_to_local_datetime(obj.get("dt", no_info))
            weather["Forecasted Datetime (UTC)"] = \
                self.convert_timestamp_to_utc_datetime(obj.get("dt", no_info))
            weather["Pressure"] = obj.get("pressure", no_info)
            weather["Humidity"] = obj.get("humidity", no_info)
            if "temp" in obj:
                temp = obj["temp"]
                weather["Temperature (day)"]   = temp.get("day",    no_info)
                weather["Temperature (min)"]   = temp.get("min",    no_info)
                weather["Temperature (max)"]   = temp.get("max",    no_info)
                weather["Temperature (night)"] = temp.get("night",  no_info)
                weather["Temperature (eve)"]   = temp.get("eve",    no_info)
                weather["Temperature (morn)"]  = temp.get("morn",   no_info)
            if "weather" in obj and obj["weather"][0]:
                wthr = obj["weather"][0]
                weather["Weather ID"]          = wthr.get("id",         no_info)
                weather["Weather Icon"]        = wthr.get("icon",       no_info)
                weather["Weather Main"]        = wthr.get("main",       no_info)
                weather["Weather Description"] = wthr.get("description",no_info)
            if "wind" in obj:
                wind = obj["wind"]
                weather["Wind Direction"] = wind.get("deg",    no_info)
                weather["Wind Speed"]     = wind.get("speed",  no_info)
                weather["Wind Gust"]      = wind.get("gust",   no_info)
            weather["Clouds"]      = obj.get("clouds",  no_info)
            weather["Rain Volume"] = obj.get("rain",    no_info)
            weather["Snow Volume"] = obj.get("snow",    no_info)
            _list.append(weather)
        _dict["list"] = _list
        return _dict

    def convert_timestamp_to_local_datetime(self, timestamp):
        return datetime.fromtimestamp(int(timestamp)).strftime(
            "%Y-%m-%d %H:%M:%S")

    def convert_timestamp_to_utc_datetime(self, timestamp):
        return datetime.utcfromtimestamp(int(timestamp)).strftime(
            "%Y-%m-%d %H:%M:%S")

# if __name__ == "__main__":
#     from oweather_wrapper import OpenWeatherWrapper
#     key = "d0fc78d57e3d1d08f2a3241f8bc47d3c"
#     wrpr = OpenWeatherWrapper(key)
#     prsr = OpenWeatherParser()
    # json = wrpr.get_current_weather("tokyo", "imperial")
    # data = prsr.parse_current_weather(json)
    # json = wrpr.get_five_day_forecast("tokyo", "metric")
    # data = prsr.parse_five_day_forecast(json)
    # json = wrpr.get_daily_forecast("tokyo", 4, "metric")
    # data = prsr.parse_daily_forecast(json)
    # import json as jjson
    # print jjson.dumps(data, indent=4, sort_keys=True)
