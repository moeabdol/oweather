# -*- coding: utf-8 -*-
from prettytable import PrettyTable

class OpenWeatherView(object):
    def __init__(self, plain=False):
        self.plain = plain

    def print_weather(self, data):
        if self.plain:
            self.plain_print(data)
        else:
            self.pretty_print(data)

    def plain_print(self, data):
        for key, value in sorted(data.items()):
            if key != "list":
                print key, ":", value
            else:
                print
                for item in data["list"]:
                    for ikey, ivalue in sorted(item.items()):
                        print ikey, ":", ivalue
                    print

    def pretty_print(self, data):
        for key, value in sorted(data.items()):
            if key != "list":
                print key, ":", value
            else:
                print
                for item in data["list"]:
                    table = PrettyTable(["Variable", "Measurement"])
                    table.align["Variable"] = "l"
                    table.align["Measurement"] = "r"
                    for ikey, ivalue in sorted(item.items()):
                        table.add_row([ikey, ivalue])
                    print table
                    print
