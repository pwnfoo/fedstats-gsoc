import fedmsg
import fedmsg.meta
import json
import os
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

    def show_logs(self):
        unicode_json = self.return_json()
        for activity in unicode_json['raw_messages']:
            print activity

    def save_json(self, filename):
        unicode_json = self.return_json()
        filename = str(filename) + '.json'
        try:
            fp = open(filename, 'w')
        except IOError:
            print "[!] Could not write into directory. Check Permissions"
        fp.write(unicode_json)

    def show_json(self):
        print self.return_json()

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

def dependency_check():
    # Without fedmsg-meta, the program will not display the human readable log
    return_val = os.system('rpm -q python2-fedmsg-meta-fedora-infrastructure >> \
    /dev/null')
    if(return_val != 0):
        print "[!] Please install \'python2-fedmsg-meta-fedora-infrastructure\' \
        package to continue."
        return False
    else:
        return True
