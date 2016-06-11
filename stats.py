from __future__ import absolute_import
from __future__ import print_function
import fedmsg
import fedmsg.meta
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
category = None
weeks = 0
baseurl = "https://apps.fedoraproject.org/datagrepper/raw"
unicode_json={}

# Checks if unicode_json is empty, pulls datagrepper values and returns the json
def return_json():
    global unicode_json
    total_pages = 1
    if category is not None :
        values['category'] = category
    if len(unicode_json) == 0:
        print('[*] Grabbing datagrepper values..')
        response = requests.get(baseurl, params=values)
        unicode_json = json.loads(response.text)
        total_pages = unicode_json['pages']
        print ("Total pages found : " + str(total_pages))
        while total_pages > 1:
            values['page'] += 1
            print("  [*] Pulling data from page " + str(values['page']))
            response = requests.get(baseurl, params=values)
            paginated_json = json.loads(response.text)
            for activity in paginated_json['raw_messages'] :
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

# Given a category, looks for subcategories in the category and returns a sub-category counter.
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

# Gets the subcategories as a counter, analyzes it for further activities - named interactions.
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
                if object == activity['topic'].split('.')[4] and activity['topic'].split('.')[5]:
                    interaction_dict[object].append(activity['topic'].split('.')[5])
            except IndexError:
                print("[!] That category doesn't have any more interactions!")
                return {None:None}

    # Changing list to a counter
    for key in interaction_dict:
        interaction_dict[key] = Counter(interaction_dict[key])
    return interaction_dict
