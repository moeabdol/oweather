# -*- coding: utf-8 -*-

class OpenWeatherView(object):
    def print_weather(self, data):
        for key, value in sorted(data.items()):
            if key != "list":
                print key, ":", value
            else:
                print
                for item in data["list"]:
                    for ikey, ivalue in sorted(item.items()):
                        print ikey, ":", ivalue
                    print
