from datetime import datetime

class OpenWeatherParser(object):
    def parse_current_weather(self, data):
        json    = data["json"]
        units   = data["units"].capitalize()
        no_info = "No information available!"
        _dict = {}
        _dict["City ID"] = str(json.get("id",  no_info))
        _dict["City"]    = json.get("name",    no_info)
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
            _dict["Longtitude"] = str(json["coord"].get("lon", no_info))
            _dict["Latitude"]   = str(json["coord"].get("lat", no_info))
        if "main" in json:
            main = json["main"]
            _dict["Humidity"]          = str(main.get("humidity"   , no_info))
            _dict["Pressure"]          = str(main.get("pressure"   , no_info))
            _dict["Temperature"]       = str(main.get("temp"       , no_info))
            _dict["Temperature (Min)"] = str(main.get("temp_min"   , no_info))
            _dict["Temperature (Max)"] = str(main.get("temp_max"   , no_info))
            _dict["Sea Level"]         = str(main.get("sea_level"  , no_info))
            _dict["Ground Level"]      = str(main.get("grnd_level" , no_info))
        if "weather" in json and json["weather"][0]:
            weather = json["weather"][0]
            _dict["Weather ID"]          = str(weather.get("id", no_info))
            _dict["Weather Icon"]        = str(weather.get("icon", no_info))
            _dict["Weather Main"]        = str(weather.get("main", no_info))
            _dict["Weather Description"] = str(weather.get("description",
                no_info))
        if "wind" in json:
            wind = json["wind"]
            _dict["Wind Direction"] = str(wind.get("deg",    no_info))
            _dict["Wind Speed"]     = str(wind.get("speed",  no_info))
            _dict["Wind Gust"]      = str(wind.get("gust",   no_info))
        if "clouds" in json:
            _dict["Clouds"] = str(json["clouds"].get("all", no_info))
        if "rain" in json:
            _dict["Rain Volume"] = str(json["rain"].get("3h", no_info))
        if "snow" in json:
            _dict["Snow Volume"] = str(json["snow"].get("3h", no_info))
        return _dict

    def parse_five_day_forecast(self, data):
        json    = data["json"]
        units   = data["units"].capitalize()
        no_info = "No information available!"
        _dict = {}
        _dict["Units"] = units
        if "city" in json:
            city = json["city"]
            _dict["City ID"] = str(city.get("id",   no_info))
            _dict["City"]    = city.get("name",     no_info)
            _dict["Country"] = city.get("country",  no_info)
            if "coord" in city:
                coord = city["coord"]
                _dict["Longtitude"] = str(coord.get("lon", no_info))
                _dict["Latitude"]   = str(coord.get("lat", no_info))
        _list = []
        for obj in json["list"]:
            weather = {}
            weather["Forecasted Datetime (Local)"] = \
                self.convert_timestamp_to_local_datetime(obj.get("dt", no_info))
            weather["Forecasted Datetime (UTC)"] = \
                self.convert_timestamp_to_utc_datetime(obj.get("dt", no_info))
            weather["Datetime Text (UTC)"] = obj["dt_txt"]
            if "main" in obj:
                main = obj["main"]
                weather["Humidity"]         = str(main.get("humidity", no_info))
                weather["Pressure"]         = str(main.get("pressure", no_info))
                weather["Sea Level"]       = str(main.get("sea_level", no_info))
                weather["Ground Level"]   = str(main.get("grnd_level", no_info))
                weather["Temperature"]       =    str(main.get("temp", no_info))
                weather["Temperature (Min)"] = str(main.get("temp_min",no_info))
                weather["Temperature (Max)"] = str(main.get("temp_max",no_info))
            if "weather" in obj and obj["weather"][0]:
                wthr = obj["weather"][0]
                weather["Weather ID"]          = str(wthr.get("id",    no_info))
                weather["Weather Icon"]        = str(wthr.get("icon",  no_info))
                weather["Weather Main"]        = str(wthr.get("main",  no_info))
                weather["Weather Description"] = str(wthr.get("description",
                    no_info))
            if "wind" in obj:
                wind = obj["wind"]
                weather["Wind Direction"] = str(wind.get("deg",    no_info))
                weather["Wind Speed"]     = str(wind.get("speed",  no_info))
                weather["Wind Gust"]      = str(wind.get("gust",   no_info))
            if "clouds" in obj:
                weather["Clouds"] = str(obj["clouds"].get("all", no_info))
            if "rain" in obj:
                weather["Rain Volume"] = str(obj["rain"].get("3h", no_info))
            if "snow" in obj:
                weather["Snow Volume"] = str(obj["snow"].get("3h", no_info))
            _list.append(weather)
        _dict["list"] = _list
        return _dict

    def parse_daily_forecast(self, data):
        json  = data["json"]
        units = data["units"].capitalize()
        no_info = "No information available!"
        _dict = {}
        _dict["Units"]     = units
        _dict["Days"]      = str(data["days"])
        if "city" in json:
            city = json["city"]
            _dict["City ID"]   = str(city.get("id"  , no_info))
            _dict["City"]      = city.get("name"    , no_info)
            _dict["Country"]   = city.get("country" , no_info)
            if "coord" in city:
                coord = city["coord"]
                _dict["Longtitude"] = str(coord.get("lon", no_info))
                _dict["Latitude"]   = str(coord.get("lat", no_info))
        _list = []
        for obj in json["list"]:
            weather = {}
            weather["Forecast Datetime (Local)"] = \
                self.convert_timestamp_to_local_datetime(obj.get("dt", no_info))
            weather["Forecasted Datetime (UTC)"] = \
                self.convert_timestamp_to_utc_datetime(obj.get("dt", no_info))
            weather["Pressure"] = str(obj.get("pressure", no_info))
            weather["Humidity"] = str(obj.get("humidity", no_info))
            if "temp" in obj:
                temp = obj["temp"]
                weather["Temperature (day)"]   = str(temp.get("day",   no_info))
                weather["Temperature (min)"]   = str(temp.get("min",   no_info))
                weather["Temperature (max)"]   = str(temp.get("max",   no_info))
                weather["Temperature (night)"] = str(temp.get("night", no_info))
                weather["Temperature (eve)"]   = str(temp.get("eve",   no_info))
                weather["Temperature (morn)"]  = str(temp.get("morn",  no_info))
            if "weather" in obj and obj["weather"][0]:
                wthr = obj["weather"][0]
                weather["Weather ID"]          = str(wthr.get("id",no_info))
                weather["Weather Icon"]        = str(wthr.get("icon",no_info))
                weather["Weather Main"]        = str(wthr.get("main",no_info))
                weather["Weather Description"] = str(wthr.get("description",
                    no_info))
            if "wind" in obj:
                wind = obj["wind"]
                weather["Wind Direction"] = str(wind.get("deg",    no_info))
                weather["Wind Speed"]     = str(wind.get("speed",  no_info))
                weather["Wind Gust"]      = str(wind.get("gust",   no_info))
            weather["Clouds"]      = str(obj.get("clouds", no_info))
            weather["Rain Volume"] = str(obj.get("rain", no_info))
            weather["Snow Volume"] = str(obj.get("snow", no_info))
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
    # from oweather_wrapper import OpenWeatherWrapper
    # key = "d0fc78d57e3d1d08f2a3241f8bc47d3c"
    # wrpr = OpenWeatherWrapper(key)
    # prsr = OpenWeatherParser()
    # json = wrpr.get_current_weather("tokyo", "imperial")
    # data = prsr.parse_current_weather(json)
    # json = wrpr.get_five_day_forecast("tokyo", "metric")
    # data = prsr.parse_five_day_forecast(json)
    # json = wrpr.get_daily_forecast("tokyo", 4, "metric")
    # data = prsr.parse_daily_forecast(json)
    # import json as jjson
    # print jjson.dumps(data, indent=4, sort_keys=True)
