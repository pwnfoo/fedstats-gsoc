from __future__ import absolute_import
from __future__ import print_function
import pygal
import json
import os
from stats import *


class draw:

    def __init__(self):
        self.mode = 'text'
        self.filename = 'stats'

    def draw_svg(self, graph_obj):
        filename = self.filename + '.svg'
        graph_obj.render_to_file(filename)
        os.system('firefox '+filename)

    def draw_png(self, graph_obj):
        fname = self.filename + '.png'
        graph_obj.render_to_png(filename=fname)

    def draw_pie(self, input_json, title):
        pie_chart = pygal.Pie(inner_radius=0.4)
        pie_chart.title = str(title)
        for key in input_json:
            percent = input_json[key] / float(sum(input_json.values())) * 100
            pie_chart.add(str(key), round(percent, 2))
        return pie_chart

    def show_logs(self, unicode_json):
        for activity in unicode_json['raw_messages']:
            print(fedmsg.meta.msg2subtitle(activity))

    def save_json(self, unicode_json):
        filename = self.filename + '.json'
        try:
            with open(filename, 'w') as outfile:
                json.dump(unicode_json, outfile)
        except IOError:
            print("[!] Could not write into directory. Check Permissions")

    def show_output(self, input_json, title):
        print('[*] Readying Output..')
        if self.mode.lower() == 'svg':
            temp_obj = self.draw_pie(input_json, title)
            self.draw_svg(temp_obj)
        elif self.mode.lower() == 'png':
            temp_obj = self.draw_pie(input_json, title)
            self.draw_png(temp_obj)
        elif self.mode.lower() == 'json':
            self.save_json(input_json)
        elif self.mode.lower() == 'text':
            self.show_logs(input_json)
