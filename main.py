import argparse
import fedmsg
import fedmsg.meta
from stats import *

def main():
    # fedmsg config
    config = fedmsg.config.load_config()
    fedmsg.meta.make_processors(**config)

    # Argument Parser initialization
    parser = argparse.ArgumentParser(description='Fedora GSoC stats gatherer')
    parser.add_argument('--user', '-u', help='FAS username', required=True)
    parser.add_argument('--weeks', '-w', help='Time in weeks', default=1)
    parser.add_argument('--mode', '-m', help="Type of Output", default='text')
    parser.add_argument('--output', '-o', help="Output name", default='stats')
    args = parser.parse_args()

    userstats = stats()
    userstats.values['user'] = args.user
    userstats.values['delta'] = int(args.weeks) * 604800
    userstats.return_categories()


if __name__ == '__main__':
    if(dependency_check()):
        main()
