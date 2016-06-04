from __future__ import absolute_import
from __future__ import print_function
from stats import *
import pygal
import stats
import json
import os


mode = 'text'
filename = 'stats'
category_json = None
subcategory_json = None
count = 0

def draw_svg(graph_obj):
    global count
    fname = filename + str(count) + '.svg'
    graph_obj.render_to_file(fname)
    os.system('firefox ' + fname)

def draw_category_png(graph_obj):
    fname = filename + str(count) + '.png'
    graph_obj.render_to_png(filename=fname)

def draw_pie(output_json, title):
    pie_chart = pygal.Pie(inner_radius=0.4, width=500, height=500)
    pie_chart.title = str(title)
    for key in output_json:
        percent = output_json[key] / float(sum(output_json.values())) * 100
        pie_chart.add(str(key), round(percent, 2))
    return pie_chart

def draw_bar(output_json, title):
    bar_chart = pygal.Bar(width=500, height=500)
    bar_chart.title = str(title)
    for key in output_json:
        bar_chart.add(str(key), output_json[key])
    return bar_chart

def save_text(unicode_json, username):
    fname = filename + str(count) + '.txt'
    fout = open(fname, 'w')

    # Entire Log Write
    fout.write("*****Full log for user " + username + "*****\n\n\n")
    for activity in unicode_json['raw_messages']:
        fout.write(fedmsg.meta.msg2subtitle(activity)+"\n")
'''
    # Category-wise Log
    fout.write("\n\n*****Category-wise activities*****\n\n")
    for category in stats.return_categories():
        for activity in unicode_json['raw_messages']:
            if category == activity['topic'].split('.')[3]:
                fout.write()

'''
def save_json(unicode_json):
    filename = filename + str(count) + '.json'
    try:
        with open(filename, 'w') as outfile:
            json.dump(unicode_json, outfile)
    except IOError:
        print("[!] Could not write into directory. Check Permissions")

def generate_graph(output_json, username, gtype):
    global count
    print('[*] Readying Output..')
    count += 1
    if mode.lower() == 'svg':
        if gtype == 'pie':
            graph_obj = draw_pie(output_json, username)
        elif gtype == 'bar':
            graph_obj = draw_bar(output_json, username)
        draw_svg(graph_obj)

    elif mode.lower() == 'png':
        graph_obj = draw_pie(output_json, username)
        draw_category_png(graph_obj)

    elif mode.lower() == 'json':
        save_json(output_json)

    elif mode.lower() == 'text':
        save_text(output_json, username)
