import json
from oweather_api_parser import OpenWeatherMapAPIParser
from prettytable import PrettyTable
import datetime
import ipdb

class OpenWeatherMapPrinter:
    def print_current_weather(self, weather):
        print "Current Weather"
        print "Location:\t\t%s, %s" % (weather["city"], weather["country"])
        print "Condition:\t\t%s, %s" % (weather["weather_main"],
            weather["weather_desc"])
        print "Last Updated (Local):\t%s" % \
            self.convert_utc_to_datetime(weather["dt"])
        table = PrettyTable(["Variable", "Measurement"])
        table.align["Variable"] = "l"
        if weather["units"] == "metric":
            table.add_row(["Temperature", str(weather["temp"]) + u"\xB0" + "C"])
            table.add_row(["Humidity", str(weather["humidity"]) + "%"])
            table.add_row(["Pressure", str(weather["pressure"]) + " hPa"])
            table.add_row(["Wind Speed", str(weather["wind_speed"]) +
                                                     " meter/sec"])
            table.add_row(["Wind Direction", str(weather["wind_deg"]) +
                                                         u"\xB0"])
            table.add_row(["Clouds", str(weather["clouds_perc"]) + "%"])
            if weather["rain_volume"] is None:
                table.add_row(["Rain Volume", "0 mm"])
            else:
                table.add_row(["Rain Volume", str(weather["rain_volume"]) +
                                                          " mm"])
            if weather["snow_volume"] is None:
                table.add_row(["Snow Volume", "0 mm"])
            else:
                table.add_row(["Snow Volume", str(weather["snow_volume"]) +
                                                          " mm"])
        elif weather["units"] == "imperial":
            table.add_row(["Temperature", str(weather["temp"]) + u"\xB0" + "F"])
            table.add_row(["Humidity", str(weather["humidity"]) + "%"])
            table.add_row(["Pressure", str(weather["pressure"]) + " hPa"])
            table.add_row(["Wind Speed", str(weather["wind_speed"]) +
                                                     " mile/hour"])
            table.add_row(["Wind Direction", str(weather["wind_deg"]) +
                                                         u"\xB0"])
            table.add_row(["Clouds", str(weather["clouds_perc"]) + "%"])
            if weather["rain_volume"] is None:
                table.add_row(["Rain Volume", "0 mm"])
            else:
                table.add_row(["Rain Volume", str(weather["rain_volume"]) +
                                                          " mm"])
            if weather["snow_volume"] is None:
                table.add_row(["Snow Volume", "0 mm"])
            else:
                table.add_row(["Snow Volume", str(weather["snow_volume"]) +
                                                          " mm"])
        print table
        print

    def print_five_day_three_hour_forecast(self, forecast_list):
        print "Five Day (Three Hour Interval) Forecast"
        city, country, units = forecast_list[0]["city"], \
            forecast_list[0]["country"], forecast_list[0]["units"]
        for forecast in forecast_list[1:]:
            print "Location:\t\t%s, %s" % (city, country)
            print "Condition:\t\t%s, %s" % (forecast["weather_main"],
                forecast["weather_desc"])
            print "Local Forecast Datetime:%s" % \
                self.convert_utc_to_datetime(forecast["dt"])
            print "UTC Forecast Datetime:\t%s" % forecast["dt_txt"]
            table = PrettyTable(["Variable", "Measurement"])
            table.align["Variable"] = "l"
            if units == "metric":
                table.add_row(["Temperature", str(forecast["temp"]) + u"\xB0" +
                                                                       "C"])
                table.add_row(["Humidity", str(forecast["humidity"]) + "%"])
                table.add_row(["Pressure", str(forecast["pressure"]) + " hPa"])
                table.add_row(["Wind Speed", str(forecast["wind_speed"]) +
                                                          " meter/sec"])
                table.add_row(["Wind Direction", str(forecast["wind_deg"]) +
                                                              u"\xB0"])
                table.add_row(["Clouds", str(forecast["clouds_perc"]) + "%"])
                if forecast["rain_volume"] is None:
                    table.add_row(["Rain Volume", "0 mm"])
                else:
                    table.add_row(["Rain Volume", str(forecast["rain_volume"]) +
                                                               " mm"])
                if forecast["snow_volume"] is None:
                    table.add_row(["Snow Volume", "0 mm"])
                else:
                    table.add_row(["Snow Volume", str(forecast["snow_volume"]) +
                                                               " mm"])
            elif units == "imperial":
                table.add_row(["Temperature", str(forecast["temp"]) + u"\xB0" +
                                                                       "F"])
                table.add_row(["Humidity", str(forecast["humidity"]) + "%"])
                table.add_row(["Pressure", str(forecast["pressure"]) + " hPa"])
                table.add_row(["Wind Speed", str(forecast["wind_speed"]) +
                                                          " mile/hour"])
                table.add_row(["Wind Direction", str(forecast["wind_deg"]) +
                                                              u"\xB0"])
                table.add_row(["Clouds", str(forecast["clouds_perc"]) + "%"])
                if forecast["rain_volume"] is None:
                    table.add_row(["Rain Volume", "0 mm"])
                else:
                    table.add_row(["Rain Volume", str(forecast["rain_volume"]) +
                                                               " mm"])
                if forecast["snow_volume"] is None:
                    table.add_row(["Snow Volume", "0 mm"])
                else:
                    table.add_row(["Snow Volume", str(forecast["snow_volume"]) +
                                                               " mm"])
            print table
            print

    def print_daily_forcast(self, forecast_list):
        city, country, days, units = forecast_list[0]["city"], \
            forecast_list[0]["country"], forecast_list[0]["days"], \
            forecast_list[0]["units"]
        print "{} Day(s) Forecast".format(days)
        for forecast in forecast_list[1:]:
            print "Location:\t\t%s, %s" % (city, country)
            print "Condition:\t\t%s, %s" % (forecast["weather_main"],
                forecast["weather_desc"])
            print "Local Forecast Datetime:%s" % \
                self.convert_utc_to_datetime(forecast["dt"])
            table = PrettyTable(["Variable", "Measurement"])
            table.align["Variable"] = "l"
            if units == "metric":
                table.add_row(["Temperature (Morning)",
                    str(forecast["temp_morn"]) + u"\xB0" + "C"])
                table.add_row(["Temperature (Day)",
                    str(forecast["temp_day"]) + u"\xB0" + "C"])
                table.add_row(["Temperature (Evening)",
                    str(forecast["temp_eve"]) + u"\xB0" + "C"])
                table.add_row(["Temperature (Night)",
                    str(forecast["temp_night"]) + u"\xB0" + "C"])
                table.add_row(["Temperature (Min)",
                    str(forecast["temp_min"]) + u"\xB0" + "C"])
                table.add_row(["Temperature (Max)",
                    str(forecast["temp_max"]) + u"\xB0" + "C"])
                table.add_row(["Humidity", str(forecast["humidity"]) + "%"])
                table.add_row(["Pressure", str(forecast["pressure"]) + " hPa"])
                table.add_row(["Wind Speed",
                    str(forecast["wind_speed"]) + " meter/sec"])
                table.add_row(["Wind Direction",
                    str(forecast["wind_deg"]) + u"\xB0"])
                table.add_row(["Clouds", str(forecast["clouds_perc"]) + "%"])
                if forecast["rain_volume"] is None:
                    table.add_row(["Rain Volume", "0 mm"])
                else:
                    table.add_row(["Rain Volume",
                        str(forecast["rain_volume"]) + " mm"])
                if forecast["snow_volume"] is None:
                    table.add_row(["Snow Volume", "0 mm"])
                else:
                    table.add_row(["Snow Volume",
                        str(forecast["snow_volume"]) + " mm"])
            elif units == "imperial":
                table.add_row(["Temperature (Morning)",
                    str(forecast["temp_morn"]) + u"\xB0" + "F"])
                table.add_row(["Temperature (Day)",
                    str(forecast["temp_day"]) + u"\xB0" + "F"])
                table.add_row(["Temperature (Evening)",
                    str(forecast["temp_eve"]) + u"\xB0" + "F"])
                table.add_row(["Temperature (Night)",
                    str(forecast["temp_night"]) + u"\xB0" + "F"])
                table.add_row(["Temperature (Min)",
                    str(forecast["temp_min"]) + u"\xB0" + "F"])
                table.add_row(["Temperature (Max)",
                    str(forecast["temp_max"]) + u"\xB0" + "F"])
                table.add_row(["Humidity", str(forecast["humidity"]) + "%"])
                table.add_row(["Pressure", str(forecast["pressure"]) + " hPa"])
                table.add_row(["Wind Speed",
                    str(forecast["wind_speed"]) + " miles/hour"])
                table.add_row(["Wind Direction",
                    str(forecast["wind_deg"]) + u"\xB0"])
                table.add_row(["Clouds", str(forecast["clouds_perc"]) + "%"])
                if forecast["rain_volume"] is None:
                    table.add_row(["Rain Volume", "0 mm"])
                else:
                    table.add_row(["Rain Volume",
                        str(forecast["rain_volume"]) + " mm"])
                if forecast["snow_volume"] is None:
                    table.add_row(["Snow Volume", "0 mm"])
                else:
                    table.add_row(["Snow Volume",
                        str(forecast["snow_volume"]) + " mm"])
            print table
            print

    def print_json(self, json_dict):
        print json.dumps(json_dict, sort_keys=True, indent=4,
                         separators=(",", ": "))

    def convert_utc_to_datetime(self, utc_time):
        return datetime.datetime.fromtimestamp(int(utc_time)).strftime(
            "%Y-%m-%d %H:%M:%S")
