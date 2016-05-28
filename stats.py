import fedmsg
import fedmsg.meta
import json
import urllib


class stats:
    def __init__(self):
        self.values = dict()
        self.values['user'] = None
        self.values['delta'] = 604800
        self.values['rows_per_page'] = 10
        self.values['not_category'] = 'meetbot'
        self.baseurl = "https://apps.fedoraproject.org/datagrepper/raw"
        self.full_url = ''

    def return_url(self):
        data = urllib.urlencode(self.values)
        self.full_url = self.baseurl + '?' + data
        return self.full_url

    def return_json(self):
        self.full_url = self.return_url()
        response = urllib.urlopen(self.full_url)
        raw_json = response.read()
        unicode_json = json.loads(raw_json)
        return unicode_json

    def return_categories(self):
        categories = dict()
        unicode_json = self.return_json()
        for activity in unicode_json['raw_messages']:
            category = activity['topic'].split('.')[3]
            if category in categories.keys():
                categories[category] += 1
            else:
                categories[category] = 1
        return categories
