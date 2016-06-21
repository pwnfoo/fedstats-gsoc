from __future__ import absolute_import
from __future__ import print_function
import fedmsg
import fedmsg.meta
import calendar
import json
import requests
from collections import Counter

# This dictionary will be passed as param to requests later
values = dict()
values['user'] = None
values['delta'] = 604800
values['rows_per_page'] = 100
values['not_category'] = 'meetbot'
values['page'] = 1
values['size'] = 'small'
category = ''
start = ''
end = ''
logs = False
weeks = 0
baseurl = "https://apps.fedoraproject.org/datagrepper/raw"
unicode_json = {}


def return_epoch(time):
    if time == '':
        return ''
    tup = map(int, time.split('/'))
    l = (tup[2], tup[0], tup[1], 0, 0, 0)
    epochs = calendar.timegm(l)
    return (int(epochs))

# Checks if unicode_json is empty, pulls datagrepper values and returns
# the json


def return_json():
    global unicode_json
    total_pages = 1

    # Only pull the values from datagrepper if it's the first run
    if len(unicode_json) == 0:
        print('[*] Grabbing datagrepper values..')

        # If the user is set as all, we filter it using the provided category,
        # if any
        if category != '' and values['user'] == 'all':
            values['category'] = category
        if start != '' and end != '':
            values['start'] = return_epoch(start)
            values['end'] = return_epoch(end)
            del(values['delta'])
        # If the user value is passed as all, remove it from the dict and pass
        # arguments
        if values['user'] == 'all':
            temp_dict = dict(values)
            del(temp_dict['user'])
            response = requests.get(baseurl, params=temp_dict)
        else:
            response = requests.get(baseurl, params=values)
        unicode_json = json.loads(response.text)
        total_pages = unicode_json['pages']
        print ("Total pages found : " + str(total_pages))
        total = total_pages
        # If multiple pages exist, get them all.
        while total_pages > 1:
            print("  [*] Loading Page " + str(values['page']) + "/" + str(total))
            values['page'] += 1
            response = requests.get(baseurl, params=values)
            paginated_json = json.loads(response.text)
            # Pull data from multiple pages and append them to the main JSON
            for activity in paginated_json['raw_messages']:
                unicode_json['raw_messages'].append(activity)
            total_pages -= 1
    return unicode_json

# Analyzes the JSON and return categories present as a list.


def return_categories():
    cat_list = list()
    categories = Counter()
    unicode_json = return_json()
    print("[*] Identifying Categories..")
    for activity in unicode_json['raw_messages']:
        # Split the topic using . param , extract the 4th word and append
        cat_list.append(activity['topic'].split('.')[3])
    for category in cat_list:
        categories[category] += 1
    return categories

# Given a category, looks for subcategories in the category and returns a
# sub-category counter.

def return_subcategories(category):
    subcat_list = list()
    subcategories = Counter()
    print("[*] Identifying sub-categories..")
    for activity in unicode_json['raw_messages']:
        if category == activity['topic'].split('.')[3]:
            subcat_list.append(activity['topic'].split('.')[4])

    # Converts the list into a counter.
    for subcategory in subcat_list:
        subcategories[subcategory] += 1
    return subcategories

# Gets the subcategories as a counter, analyzes it for further activities
# Returns a counter with the found interactions


def return_interactions(subcategories):
    interaction_dict = dict()
    interaction_list = list()

    # Initializing the dictionary
    for object in subcategories:
        interaction_dict[object] = []

    # Gathering sub-sub-categories
    for activity in unicode_json['raw_messages']:
        for object in subcategories:
            try:
                if object == activity['topic'].split('.')[4] and activity[
                        'topic'].split('.')[5]:
                    interaction_dict[object].append(
                        activity['topic'].split('.')[5])
            except IndexError:
                print("[!] That category doesn't have any more interactions!")
                return {None: None}

    # Changing list to a counter
    for key in interaction_dict:
        interaction_dict[key] = Counter(interaction_dict[key])
    return interaction_dict
