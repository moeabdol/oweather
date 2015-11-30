import json
from oweather_api_parser import OpenWeatherMapAPIParser
from prettytable import PrettyTable
import datetime
import ipdb

class OpenWeatherMapPrinter:
    def print_current_weather(self, weather):
        print "Location:\t%s, %s" % (weather["city"], weather["country"])
        print "Condition:\t%s, %s" % (weather["weather_main"],
            weather["weather_desc"])
        table = PrettyTable(["Variable", "Measurement", "Unit"])
        table.align["Variable"] = "l"
        table.add_row(["Temperature", weather["temp"], "Kelvin"])
        table.add_row(["Humidity", weather["humidity"], "%"])
        table.add_row(["Pressure", weather["pressure"], "hPa"])
        table.add_row(["Wind Speed", weather["wind_speed"], "meter/sec"])
        table.add_row(["Wind Direction", weather["wind_deg"], ""])
        table.add_row(["Clouds", weather["clouds_perc"], "%"])
        if weather["rain_volume"] is None:
            table.add_row(["Rain Volume", 0, "mm"])
        else:
            table.add_row(["Rain Volume", weather["rain_volume"], "mm"])
        if weather["snow_volume"] is None:
            table.add_row(["Snow Volume", 0, "mm"])
        else:
            table.add_row(["Snow Volume", weather["snow_volume"], "mm"])
        print table
        print "Last Updated (Local):\t%s" % \
            self.convert_utc_to_datetime(weather["dt"])
        print

    def print_five_day_three_hour_forecast(self, forecast_list):
        city, country = forecast_list[0]["city"], forecast_list[0]["country"]
        for forecast in forecast_list[1:]:
            print "Location:\t%s, %s" % (city, country)
            print "Condition:\t%s, %s" % (forecast["weather_main"],
                forecast["weather_desc"])
            table = PrettyTable(["Variable", "Measurement", "Unit"])
            table.align["Variable"] = "l"
            table.add_row(["Temperature", forecast["temp"], "Kelvin"])
            table.add_row(["Humidity", forecast["humidity"], "%"])
            table.add_row(["Pressure", forecast["pressure"], "hPa"])
            table.add_row(["Wind Speed", forecast["wind_speed"], "meter/sec"])
            table.add_row(["Wind Direction", forecast["wind_deg"], ""])
            table.add_row(["Clouds", forecast["clouds_perc"], "%"])
            if forecast["rain_volume"] is None:
                table.add_row(["Rain Volume", 0, "mm"])
            else:
                table.add_row(["Rain Volume", forecast["rain_volume"], "mm"])
            if forecast["snow_volume"] is None:
                table.add_row(["Snow Volume", 0, "mm"])
            else:
                table.add_row(["Snow Volume", forecast["snow_volume"], "mm"])
            print table
            print "Last Updated (Local)\t%s" % \
                self.convert_utc_to_datetime(forecast["dt"])
            print "Last Updated (UTC):\t%s" % forecast["dt_txt"]
            print

    def print_daily_forcast(self, forecast_list):
        city, country = forecast_list[0]["city"], forecast_list[0]["country"]
        for forecast in forecast_list[1:]:
            print "Location:\t%s, %s" % (city, country)
            print "Condition:\t%s, %s" % (forecast["weather_main"],
                forecast["weather_desc"])
            table = PrettyTable(["Variable", "Measurement", "Unit"])
            table.align["Variable"] = "l"
            table.add_row(["Temperature (Morning)", forecast["temp_morn"], "Kelvin"])
            table.add_row(["Temperature (Day)", forecast["temp_day"], "Kelvin"])
            table.add_row(["Temperature (Evening)", forecast["temp_eve"], "Kelvin"])
            table.add_row(["Temperature (Night)", forecast["temp_night"], "Kelvin"])
            table.add_row(["Temperature (Min)", forecast["temp_min"], "Kelvin"])
            table.add_row(["Temperature (Max)", forecast["temp_max"], "Kelvin"])
            table.add_row(["Humidity", forecast["humidity"], "%"])
            table.add_row(["Pressure", forecast["pressure"], "hPa"])
            table.add_row(["Wind Speed", forecast["wind_speed"], "meter/sec"])
            table.add_row(["Wind Direction", forecast["wind_deg"], ""])
            table.add_row(["Clouds", forecast["clouds_perc"], "%"])
            if forecast["rain_volume"] is None:
                table.add_row(["Rain Volume", 0, "mm"])
            else:
                table.add_row(["Rain Volume", forecast["rain_volume"], "mm"])
            if forecast["snow_volume"] is None:
                table.add_row(["Snow Volume", 0, "mm"])
            else:
                table.add_row(["Snow Volume", forecast["snow_volume"], "mm"])
            print table
            print "Last Updated (Local):\t%s" % \
                self.convert_utc_to_datetime(forecast["dt"])
            print

    def print_json(self, json_dict):
        print json.dumps(json_dict, sort_keys=True, indent=4,
                         separators=(",", ": "))

    def convert_utc_to_datetime(self, utc_time):
        return datetime.datetime.fromtimestamp(int(utc_time)).strftime(
            "%Y-%m-%d %H:%M:%S")
