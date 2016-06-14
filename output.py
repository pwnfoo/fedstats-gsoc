from __future__ import absolute_import
from __future__ import print_function
from datetime import date, timedelta
import fedmsg.meta
import fedmsg
import stats
import pygal
import json
import grip
import csv
import os

# Default global variables
subcategory_json = None
category_json = None
filename = 'stats'
csv_init = False
mode = 'text'
cat = None


# Gets a drawable object argument and renders an SVG Image of it.
def draw_svg(graph_obj):
    if cat is None:
        fname = filename + '_main' + '.svg'
    else:
        fname = filename + "_" + cat + '.svg'
    graph_obj.render_to_file(fname)
    os.system("firefox " + fname)


# Gets a drawable object argument and renders a PNG image of it.
def draw_png(graph_obj):
    if cat is None:
        fname = filename + '_main' + '.png'
    else:
        fname = filename + "_" + cat + '.png'
        graph_obj.render_to_png(fname)


# Generates a drawable pie chart object from a dictionary passed.
def draw_pie(output_json, title):
    pie_chart = pygal.Pie(inner_radius=0.4, width=500, height=500)
    pie_chart.title = str(title)
    for key in output_json:
        percent = output_json[key] / float(sum(output_json.values())) * 100
        pie_chart.add(str(key), round(percent, 2))
    return pie_chart


# Generates a drawable pie chart object from a dictionary passed.
def draw_bar(output_json, title):
    bar_chart = pygal.Bar(width=500, height=500)
    bar_chart.title = str(title)
    for key in output_json:
        bar_chart.add(str(key), output_json[key])
    return bar_chart


# Generates CSV report for the user from the dictionary passed
def save_csv(output_json):
    global csv_init, cat
    fname = filename + '_main.csv'
    fout = open(fname, 'a')
    csvw = csv.writer(fout)

    # Write the dates into CSV
    if not csv_init:
        csvw.writerows(
            [['Start Date : ', stats.start],
                ['End Date  : ', stats.end],
                ['']])
        csv_init = True

    # Initial heading row
    data = [['Username', 'Category', 'Activity Count', 'Percentage'], []]
    for key in output_json:
        percent = round(output_json[key] / float(sum(output_json.values())) *
                        100, 2)
        if cat is not None and cat.capitalize() != key.capitalize():
            data.append([stats.values['user'], cat.capitalize() + "." +
                        key.capitalize(), output_json[key], str(percent)+'%'])
        else:
            data.append([stats.values['user'], key.capitalize(),
                        output_json[key], str(percent)+'%'])

    # Insert blank lines and total
    data.append([''])
    data.append(['', 'Total : ', sum(output_json.values())])
    data.append([''])
    csvw.writerows(data)
    fout.close()


# Saves category-wise text report of a user.
def save_text(unicode_json):
    fname = filename + '_main.txt'
    fout = open(fname, 'w')

    # Category-wise Log
    fout.write("\n\n*** Category-wise activities ***\n\n")
    for category in stats.return_categories():
        flag = True
        actcount = 0
        for activity in unicode_json['raw_messages']:
            if category == activity['topic'].split('.')[3]:
                actcount += 1
                # Print the category once
                if flag is True:
                    fout.write("\n\n** Category : "+category.capitalize() + " **\n")
                    flag = False
                fout.write("* "+fedmsg.meta.msg2subtitle(activity)+"\n")
        fout.write("\nTotal Entries in category : " + str(actcount) + "\n")
        fout.write("\nPercentage participation in category : " +
                    str(round(100*actcount/float(unicode_json['total']),2)) + "\n")
    fout.close()


# Saves the markdown version of the text log
def save_markdown(unicode_json):
    fname = filename + '_main.md'
    fout = open(fname, 'w')
    # Category-wise Log, markdown ready
    fout.write("\n\n### Category-wise activities\n\n")
    for category in stats.return_categories():
        flag = True
        actcount = 0
        for activity in unicode_json['raw_messages']:
            if category == activity['topic'].split('.')[3]:
                actcount += 1
                # Print the category once
                if flag is True:
                    fout.write("\n\n#### Category : "+category.capitalize()+"\n")
                    flag = False
                fout.write("* "+fedmsg.meta.msg2subtitle(activity)+"\n")
        fout.write("\n* **Total Entries in category :** " + str(actcount) + "\n")
        fout.write("\n* **Percentage participation in category :** " +
                    str(round(100*actcount/float(unicode_json['total']), 2)) + "\n")
    fout.close()
    render_report(fname)


# WIP - Renders HTML from markdown, invoked my markdown function atm.
def render_report(fname):
    grip.export(fname, title="Summer Coding Statistics")


# Saves the JSON as a file.
def save_json(unicode_json):
    fname = filename + '_main.json'
    try:
        with open(fname, 'w') as outfile:
            json.dump(unicode_json, outfile)
    except IOError:
        print("[!] Could not write into directory. Check Permissions")


# Identifies categories & generates drawable objects for the above functions.
def generate_graph(output_json, title, category=None, gtype=None):
    global cat
    cat = category
    graph_obj = None
    print('[*] Readying Output..')
    if mode.lower() == 'svg':
        if gtype == 'pie':
            graph_obj = draw_pie(output_json, title)
        elif gtype == 'bar':
            graph_obj = draw_bar(output_json, title)
        draw_svg(graph_obj)
    elif mode.lower() == 'png':
        if gtype == 'pie':
            graph_obj = draw_pie(output_json, title)
        elif gtype == 'bar':
            graph_obj = draw_bar(output_json, title)
        draw_png(graph_obj)
    elif mode.lower() == 'json':
        save_json(output_json)
    elif mode.lower() == 'text':
        save_text(output_json)
    elif mode.lower() == 'csv':
        save_csv(output_json)
    elif mode.lower() == 'markdown':
        save_markdown(output_json)
    else:
        print("[!] That output mode is not supported! Check README for help.")
