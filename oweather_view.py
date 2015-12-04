# import json
from oweather_api_parser import OpenWeatherMapController
from prettytable import PrettyTable
import datetime
import ipdb

class OpenWeatherMapView:
    def print_current_weather(self, data):
        print "Current Weather"
        print "Location:\t\t%s, %s" % (data["city"], data["country"])
        print "Condition:\t\t%s, %s" % (data["weather_main"],
            data["weather_desc"])
        print "Last Updated (Local):\t%s" % \
            self.convert_utc_to_datetime(data["dt"])
        table = PrettyTable(["Variable", "Measurement"])
        table.align["Variable"] = "l"
        if data["units"] == "metric":
            table.add_row(["Temperature", str(data["temp"]) + u"\xB0" + "C"])
            table.add_row(["Humidity", str(data["humidity"]) + "%"])
            table.add_row(["Pressure", str(data["pressure"]) + " hPa"])
            table.add_row(["Wind Speed", str(data["wind_speed"]) +
                                                     " meter/sec"])
            table.add_row(["Wind Direction", str(data["wind_deg"]) +
                                                         u"\xB0"])
            table.add_row(["Clouds", str(data["clouds_perc"]) + "%"])
            if data["rain_volume"] is None:
                table.add_row(["Rain Volume", "0 mm"])
            else:
                table.add_row(["Rain Volume", str(data["rain_volume"]) +
                                                          " mm"])
            if data["snow_volume"] is None:
                table.add_row(["Snow Volume", "0 mm"])
            else:
                table.add_row(["Snow Volume", str(data["snow_volume"]) +
                                                          " mm"])
        elif data["units"] == "imperial":
            table.add_row(["Temperature", str(data["temp"]) + u"\xB0" + "F"])
            table.add_row(["Humidity", str(data["humidity"]) + "%"])
            table.add_row(["Pressure", str(data["pressure"]) + " hPa"])
            table.add_row(["Wind Speed", str(data["wind_speed"]) +
                                                     " mile/hour"])
            table.add_row(["Wind Direction", str(data["wind_deg"]) +
                                                         u"\xB0"])
            table.add_row(["Clouds", str(data["clouds_perc"]) + "%"])
            if data["rain_volume"] is None:
                table.add_row(["Rain Volume", "0 mm"])
            else:
                table.add_row(["Rain Volume", str(data["rain_volume"]) +
                                                          " mm"])
            if data["snow_volume"] is None:
                table.add_row(["Snow Volume", "0 mm"])
            else:
                table.add_row(["Snow Volume", str(data["snow_volume"]) +
                                                          " mm"])
        print table
        print

    def print_five_day_three_hour_forecast(self, data):
        print "Five Day (Three Hour Interval) Forecast"
        city, country, units, _list = data["city"], data["country"], \
            data["units"], data["list"]
        for json in _list:
            print "Location:\t\t{}, {}".format(city, country)
            print "Condition:\t\t{}, {}".format(json["weather_main"],
                json["weather_desc"])
            print "Local Forecast Datetime:%s" % \
                self.convert_utc_to_datetime(json["dt"])
            print "UTC Forecast Datetime:\t%s" % json["dt_txt"]
            table = PrettyTable(["Variable", "Measurement"])
            table.align["Variable"] = "l"
            if units == "metric":
                table.add_row(["Temperature", str(json["temp"]) + u"\xB0" +
                                                                       "C"])
                table.add_row(["Humidity", str(json["humidity"]) + "%"])
                table.add_row(["Pressure", str(json["pressure"]) + " hPa"])
                table.add_row(["Wind Speed", str(json["wind_speed"]) +
                                                          " meter/sec"])
                table.add_row(["Wind Direction", str(json["wind_deg"]) +
                                                              u"\xB0"])
                table.add_row(["Clouds", str(json["clouds_perc"]) + "%"])
                if json["rain_volume"] is None:
                    table.add_row(["Rain Volume", "0 mm"])
                else:
                    table.add_row(["Rain Volume", str(json["rain_volume"]) +
                                                               " mm"])
                if json["snow_volume"] is None:
                    table.add_row(["Snow Volume", "0 mm"])
                else:
                    table.add_row(["Snow Volume", str(json["snow_volume"]) +
                                                               " mm"])
            elif units == "imperial":
                table.add_row(["Temperature", str(json["temp"]) + u"\xB0" +
                                                                       "F"])
                table.add_row(["Humidity", str(json["humidity"]) + "%"])
                table.add_row(["Pressure", str(json["pressure"]) + " hPa"])
                table.add_row(["Wind Speed", str(json["wind_speed"]) +
                                                          " mile/hour"])
                table.add_row(["Wind Direction", str(json["wind_deg"]) +
                                                              u"\xB0"])
                table.add_row(["Clouds", str(json["clouds_perc"]) + "%"])
                if json["rain_volume"] is None:
                    table.add_row(["Rain Volume", "0 mm"])
                else:
                    table.add_row(["Rain Volume", str(json["rain_volume"]) +
                                                               " mm"])
                if json["snow_volume"] is None:
                    table.add_row(["Snow Volume", "0 mm"])
                else:
                    table.add_row(["Snow Volume", str(json["snow_volume"]) +
                                                               " mm"])
            print table
            print

    def print_daily_forcast(self, data):
        city, country, days, units, _list = data["city"], data["country"], \
            data["days"], data["units"], data["list"]
        print "{} Day(s) Forecast".format(days)
        for json in _list:
            print "Location:\t\t{}, {}".format(city, country)
            print "Condition:\t\t{}, {}".format(json["weather_main"],
                json["weather_desc"])
            print "Local Forecast Datetime:{}".format(
                self.convert_utc_to_datetime(json["dt"]))
            table = PrettyTable(["Variable", "Measurement"])
            table.align["Variable"] = "l"
            if units == "metric":
                table.add_row(["Temperature (Morning)",
                    str(json["temp_morn"]) + u"\xB0" + "C"])
                table.add_row(["Temperature (Day)",
                    str(json["temp_day"]) + u"\xB0" + "C"])
                table.add_row(["Temperature (Evening)",
                    str(json["temp_eve"]) + u"\xB0" + "C"])
                table.add_row(["Temperature (Night)",
                    str(json["temp_night"]) + u"\xB0" + "C"])
                table.add_row(["Temperature (Min)",
                    str(json["temp_min"]) + u"\xB0" + "C"])
                table.add_row(["Temperature (Max)",
                    str(json["temp_max"]) + u"\xB0" + "C"])
                table.add_row(["Humidity", str(json["humidity"]) + "%"])
                table.add_row(["Pressure", str(json["pressure"]) + " hPa"])
                table.add_row(["Wind Speed",
                    str(json["wind_speed"]) + " meter/sec"])
                table.add_row(["Wind Direction",
                    str(json["wind_deg"]) + u"\xB0"])
                table.add_row(["Clouds", str(json["clouds_perc"]) + "%"])
                if json["rain_volume"] is None:
                    table.add_row(["Rain Volume", "0 mm"])
                else:
                    table.add_row(["Rain Volume",
                        str(json["rain_volume"]) + " mm"])
                if json["snow_volume"] is None:
                    table.add_row(["Snow Volume", "0 mm"])
                else:
                    table.add_row(["Snow Volume",
                        str(json["snow_volume"]) + " mm"])
            elif units == "imperial":
                table.add_row(["Temperature (Morning)",
                    str(json["temp_morn"]) + u"\xB0" + "F"])
                table.add_row(["Temperature (Day)",
                    str(json["temp_day"]) + u"\xB0" + "F"])
                table.add_row(["Temperature (Evening)",
                    str(json["temp_eve"]) + u"\xB0" + "F"])
                table.add_row(["Temperature (Night)",
                    str(json["temp_night"]) + u"\xB0" + "F"])
                table.add_row(["Temperature (Min)",
                    str(json["temp_min"]) + u"\xB0" + "F"])
                table.add_row(["Temperature (Max)",
                    str(json["temp_max"]) + u"\xB0" + "F"])
                table.add_row(["Humidity", str(json["humidity"]) + "%"])
                table.add_row(["Pressure", str(json["pressure"]) + " hPa"])
                table.add_row(["Wind Speed",
                    str(json["wind_speed"]) + " miles/hour"])
                table.add_row(["Wind Direction",
                    str(json["wind_deg"]) + u"\xB0"])
                table.add_row(["Clouds", str(json["clouds_perc"]) + "%"])
                if json["rain_volume"] is None:
                    table.add_row(["Rain Volume", "0 mm"])
                else:
                    table.add_row(["Rain Volume",
                        str(json["rain_volume"]) + " mm"])
                if json["snow_volume"] is None:
                    table.add_row(["Snow Volume", "0 mm"])
                else:
                    table.add_row(["Snow Volume",
                        str(json["snow_volume"]) + " mm"])
            print table
            print

    # def print_json(self, json_dict):
    #     print json.dumps(json_dict, sort_keys=True, indent=4,
    #                      separators=(",", ": "))


