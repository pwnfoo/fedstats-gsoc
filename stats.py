import argparse
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
        self.values['rows_per_page'] = 100
        self.values['not_category'] = 'meetbot'
        self.baseurl = "https://apps.fedoraproject.org/datagrepper/raw"

    def return_url(self):
        data = urllib.urlencode(self.values)
        full_url = self.baseurl + '?' + data
        return full_url


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


def main():
    # fedmsg config
    config = fedmsg.config.load_config()
    fedmsg.meta.make_processors(**config)

    # Argument Parser initialization
    parser = argparse.ArgumentParser(description='Fedora GSoC stats gatherer')
    parser.add_argument('--user', '-u', help='FAS username', required=True)
    parser.add_argument('--weeks', '-w', help='Time in weeks', default=1)
    args = parser.parse_args()

    userstats = stats()
    userstats.values['user'] = args.user
    userstats.values['delta'] = int(args.weeks) * 604800

    full_url = userstats.return_url()
    response = urllib.urlopen(full_url)
    raw_json = response.read()
    unicode_json = json.loads(raw_json)

    for activity in unicode_json['raw_messages']:
        print fedmsg.meta.msg2repr(activity)


if __name__ == '__main__':
    if(dependency_check()):
        main()
