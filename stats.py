from __future__ import absolute_import
from __future__ import print_function
import fedmsg
import fedmsg.meta
import json
import requests
from collections import Counter


class stats:
    def __init__(self):
        self.values = dict()
        self.values['user'] = None
        self.values['delta'] = 604800
        self.values['rows_per_page'] = 100
        self.values['not_category'] = 'meetbot'
        self.baseurl = "https://apps.fedoraproject.org/datagrepper/raw"

    def return_json(self):
        print('[*] Grabbing datagrepper values..')
        response = requests.get(self.baseurl, params=self.values)
        unicode_json = json.loads(response.text)
        return unicode_json

    def return_categories(self):
        cat_list = list()
        categories = Counter()
        unicode_json = self.return_json()
        print("[*] Identifying Categories..")
        for activity in unicode_json['raw_messages']:
            # Split the topic using . param , extract the 4th word and append
            cat_list.append(activity['topic'].split('.')[3])
            for category in cat_list:
                categories[category] += 1
        return categories
