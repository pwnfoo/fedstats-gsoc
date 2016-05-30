from __future__ import absolute_import
from __future__ import print_function
import argparse
import fedmsg
import fedmsg.meta
from stats import stats
from output import draw
import os


def dependency_check():
    # Without fedmsg-meta, the program will not display the human readable log
    return_val = os.system('rpm -q python2-fedmsg-meta-fedora-infrastructure >> \
    /dev/null')
    if(return_val != 0):
        print("[!] Please install \'python2-fedmsg-meta-fedora-infrastructure\' \
        package to continue.")
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
    parser.add_argument('--mode', '-m', help="Type of Output", default='text')
    parser.add_argument('--output', '-o', help="Output name", default='stats')
    args = parser.parse_args()

    # Check if the user has fedmsg-meta package installed
    dependency_check()

    # Object inits and argument processing
    userstats = stats()
    output = draw()
    userstats.values['user'] = args.user
    userstats.values['delta'] = int(args.weeks) * 604800
    output.mode = args.mode
    output.filename = args.output

    # For json and text output, we need the JSON rather than the categories
    if args.mode.lower() == 'svg' or args.mode.lower() == 'png':
        out_obj = userstats.return_categories()
    elif args.mode.lower() == 'json' or args.mode.lower() == 'text':
        out_obj = userstats.return_json()

    title = "Category distribution for user " + str(args.user)
    output.show_output(out_obj, title)


if __name__ == '__main__':
        main()
        print("[*] All done :)")
