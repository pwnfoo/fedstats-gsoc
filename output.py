import pygal
from stats import *


class draw:

    def __init__(self):
        self.mode = 'text'
        self.filename = 'chart'

    def draw_svg(self, graph_obj):
        filename = self.filename + '.svg'
        graph_obj.render_to_file(filename)

    def draw_png(self, graph_obj):
        fname = self.filename + '.png'
        graph_obj.render_to_png(filename=fname)

    def draw_pie(self, input_json, title):
        pie_chart = pygal.Pie(inner_radius=0.4)
        pie_chart.title = str(title)
        for key in input_json:
            percent = input_json[key] / float(sum(input_json.values())) * 100
            pie_chart.add(str(key), percent)
        return pie_chart

    def show_output(self, input_json, title):
        temp_obj = self.draw_pie(input_json, title)
        if self.mode.lower() == 'svg':
            self.draw_svg(temp_obj)
        elif self.mode.lower() == 'png':
            self.draw_png(temp_obj)
