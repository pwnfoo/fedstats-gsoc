from __future__ import absolute_import
from __future__ import print_function
import fedmsg
import fedmsg.meta
import json
import requests
from collections import Counter


values = dict()
values['user'] = None
values['delta'] = 604800
values['rows_per_page'] = 100
values['not_category'] = 'meetbot'
category = None
baseurl = "https://apps.fedoraproject.org/datagrepper/raw"

def return_user():
    return values['user']

def return_json():
    print('[*] Grabbing datagrepper values..')
    response = requests.get(baseurl, params=values)
    unicode_json = json.loads(response.text)
    return unicode_json

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

def return_subcategories(category):
    unicode_json = return_json()
    subcat_list = list()
    subcategories = Counter()
    print("[*] Identifying sub-categories..")
    for activity in unicode_json['raw_messages']:
        if category == activity['topic'].split('.')[3]:
            subcat_list.append(activity['topic'].split('.')[4])

    for subcategory in subcat_list:
            subcategories[subcategory] += 1
    return subcategories


def return_interactions(subcategories):
    unicode_json = return_json()
    interaction_dict = dict()
    interaction_list = list()

    # Initializing the dictionary
    for object in subcategories:
        interaction_dict[object] = []

    # Gathering sub-sub-categories
    for activity in unicode_json['raw_messages']:
        for object in subcategories:
            if object == activity['topic'].split('.')[4] and activity['topic'].split('.')[5]:
                interaction_dict[object].append(activity['topic'].split('.')[5])

    # Changing list to a counter
    for key in interaction_dict:
        interaction_dict[key] = Counter(interaction_dict[key])
    return interaction_dict
