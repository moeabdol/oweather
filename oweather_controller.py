from oweather_model import OpenWeatherMapModel

class OpenWeatherMapController:
    def parse_current_weather(self, data):
        json = data["json"]
        units = data["units"]
        weather_dict = {}
        weather_dict["city"] = json["name"]
        weather_dict["country"] = json["sys"]["country"]
        weather_dict["units"] = units
        weather_dict["dt"] = json["dt"]
        weather_dict["humidity"] = json["main"]["humidity"]
        weather_dict["pressure"] = json["main"]["pressure"]
        weather_dict["temp"] = json["main"]["temp"]
        weather_dict["weather_main"] = json["weather"][0]["main"]
        weather_dict["weather_desc"] = json["weather"][0]["description"]
        weather_dict["wind_deg"] = json["wind"]["deg"]
        weather_dict["wind_speed"] = json["wind"]["speed"]
        weather_dict["clouds_perc"] = json["clouds"]["all"]
        weather_dict["rain_volume"] = None
        weather_dict["snow_volume"] = None
        if weather_dict["weather_main"] == "Rain":
            weather_dict["rain_volume"] = json["rain"]["3h"]
        elif weather_dict["weather_main"] == "Snow":
            weather_dict["snow_volume"] = json["snow"]["3h"]
        return weather_dict

    def parse_five_day_three_hour_forecast(self, data):
        json = data["json"]
        city = json["city"]["name"]
        country = json["city"]["country"]
        units = data["units"]
        _dict = {"city": city, "country": country, "units": units}
        _list = []
        for j in json["list"]:
            weather = {}
            weather["dt"] = j["dt"]
            weather["dt_txt"] = j["dt_txt"]
            weather["humidity"] = j["main"]["humidity"]
            weather["pressure"] = j["main"]["pressure"]
            weather["temp"] = j["main"]["temp"]
            weather["weather_main"] = j["weather"][0]["main"]
            weather["weather_desc"] = j["weather"][0]["description"]
            weather["wind_deg"] = j["wind"]["deg"]
            weather["wind_speed"] = j["wind"]["speed"]
            weather["clouds_perc"] = j["clouds"]["all"]
            weather["rain_volume"] = None
            weather["snow_volume"] = None
            if "rain" in j.keys():
                weather["rain_volume"] = j["rain"].get("3h")
            if "snow" in j.keys():
                weather["snow_volume"] = j["snow"].get("3h")
            _list.append(weather)
        _dict["list"] = _list
        return _dict

    def parse_daily_forecast(self, data):
        json = data["json"]
        city = json["city"]["name"]
        country = json["city"]["country"]
        days = data["days"]
        units = data["units"]
        _dict = {"city": city, "country": country, "days": days, "units": units}
        _list = []
        for j in json["list"]:
            weather = {}
            weather["dt"] = j["dt"]
            weather["temp_day"] = j["temp"]["day"]
            weather["temp_min"] = j["temp"]["min"]
            weather["temp_max"] = j["temp"]["max"]
            weather["temp_night"] = j["temp"]["night"]
            weather["temp_eve"] = j["temp"]["eve"]
            weather["temp_morn"] = j["temp"]["morn"]
            weather["pressure"] = j["pressure"]
            weather["humidity"] = j["humidity"]
            weather["weather_main"] = j["weather"][0]["main"]
            weather["weather_desc"] = j["weather"][0]["description"]
            weather["wind_speed"] = j["speed"]
            weather["wind_deg"] = j["deg"]
            weather["clouds_perc"] = j["clouds"]
            weather["rain_volume"] = None
            weather["snow_volume"] = None
            if "rain" in j.keys():
                weather["rain_volume"] = j["rain"]
            if "snow" in j.keys():
                weather["snow_volume"] = j["snow"]
            _list.append(weather)
        _dict["list"] = _list
        return _dict
