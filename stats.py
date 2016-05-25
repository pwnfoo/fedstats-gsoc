import argparse
import fedmsg
import fedmsg.meta
import json
import os
import urllib


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
    # Constants
    baseurl = "https://apps.fedoraproject.org/datagrepper/raw"
    week = 604800

    # Initial invokes
    values = dict()

    # fedmsg config
    config = fedmsg.config.load_config()
    fedmsg.meta.make_processors(**config)

    # Argument Parser initialization
    parser = argparse.ArgumentParser(description='Fedora GSoC stats gatherer')
    parser.add_argument('--user', '-u', help='FAS username', required=True)
    parser.add_argument('--time', '-t', help='Time in weeks', default=1)
    args = parser.parse_args()

    values['user'] = args.user
    values['delta'] = int(args.time) * week
    values['rows_per_page'] = 100
    values['not_category'] = 'meetbot'

    '''
    values = {
        'user': 'skamath',
        'delta': '500000',
        'topic': 'org.fedoraproject.prod.wiki.article.edit'
    }
    '''
    data = urllib.urlencode(values)
    full_url = baseurl + '?' + data
    print full_url
    response = urllib.urlopen(full_url)
    raw_json = response.read()
    unicode_json = json.loads(raw_json)

    for activity in unicode_json['raw_messages']:
        print fedmsg.meta.msg2repr(activity)
if __name__ == '__main__':
    if(dependency_check()):
        main()
