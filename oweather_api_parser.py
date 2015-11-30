from oweather_api_wrapper import OpenWeatherMapAPIWrapper

class OpenWeatherMapAPIParser:
  def parse_current_weather(self, json):
    try:
      weather_dict = {}
      weather_dict["city"] = json["name"]
    except:
      print "Unknown city"
      return
    weather_dict["country"] = json["sys"]["country"]
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

  def parse_five_day_three_hour_forecast(self, json):
    try:
      city = json["city"]["name"]
    except:
      print "Unknown city"
      return
    country = json["city"]["country"]
    weather_list = [{"city": city, "country": country}]
    for weather in json["list"]:
      weather_dict = {}
      weather_dict["dt"] = weather["dt"]
      weather_dict["dt_txt"] = weather["dt_txt"]
      weather_dict["humidity"] = weather["main"]["humidity"]
      weather_dict["pressure"] = weather["main"]["pressure"]
      weather_dict["temp"] = weather["main"]["temp"]
      weather_dict["weather_main"] = weather["weather"][0]["main"]
      weather_dict["weather_desc"] = weather["weather"][0]["description"]
      weather_dict["wind_deg"] = weather["wind"]["deg"]
      weather_dict["wind_speed"] = weather["wind"]["speed"]
      weather_dict["clouds_perc"] = weather["clouds"]["all"]
      weather_dict["rain_volume"] = None
      weather_dict["snow_volume"] = None
      if "rain" in weather.keys():
        weather_dict["rain_volume"] = weather["rain"].get("3h")
      if "snow" in weather.keys():
        weather_dict["snow_volume"] = weather["snow"].get("3h")
      weather_list.append(weather_dict)
    return weather_list

  def parse_daily_forecast(self, json):
    try:
      city = json["city"]["name"]
    except:
      print "Unknown city"
      return
    country = json["city"]["country"]
    weather_list = [{"city": city, "country": country}]
    for weather in json["list"]:
      weather_dict = {}
      weather_dict["dt"] = weather["dt"]
      weather_dict["temp_day"] = weather["temp"]["day"]
      weather_dict["temp_min"] = weather["temp"]["min"]
      weather_dict["temp_max"] = weather["temp"]["max"]
      weather_dict["temp_night"] = weather["temp"]["night"]
      weather_dict["temp_eve"] = weather["temp"]["eve"]
      weather_dict["temp_morn"] = weather["temp"]["morn"]
      weather_dict["pressure"] = weather["pressure"]
      weather_dict["humidity"] = weather["humidity"]
      weather_dict["weather_main"] = weather["weather"][0]["main"]
      weather_dict["weather_desc"] = weather["weather"][0]["description"]
      weather_dict["wind_speed"] = weather["speed"]
      weather_dict["wind_deg"] = weather["deg"]
      weather_dict["clouds_perc"] = weather["clouds"]
      weather_dict["rain_volume"] = None
      weather_dict["snow_volume"] = None
      if "rain" in weather.keys():
        weather_dict["rain_volume"] = weather["rain"]
      if "snow" in weather.keys():
        weather_dict["snow_volume"] = weather["snow"]
      weather_list.append(weather_dict)
    return weather_list
