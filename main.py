from __future__ import print_function
from __future__ import absolute_import

import os
import fedmsg
import argparse
import fedmsg.meta
from stats import stats
from output import draw
from termcolor import colored


def main():
    # fedmsg config
    config = fedmsg.config.load_config()
    fedmsg.meta.make_processors(**config)

    # Argument Parser initialization
    parser = argparse.ArgumentParser(description='Fedora GSoC stats gatherer')
    parser.add_argument('--user', '-u', help='FAS username')
    parser.add_argument('--weeks', '-w', help='Time in weeks', default=1)
    parser.add_argument('--mode', '-m', help="Type of Output", default='text')
    parser.add_argument('--output', '-o', help="Output name", default='stats')
    parser.add_argument('--interactive', '-i', help="Enable interactive mode",
                                                    action='store_true')
    args = parser.parse_args()

    # Object inits and argument processing
    userstats = stats()
    output = draw()

    if args.interactive:
        userstats.values['user'] = str(raw_input("Enter FAS Username : "))
        userstats.values['delta'] = 604800 * int(raw_input("Number of weeks stats \
required for : "))
        output.mode = str(raw_input("Type of output : "))
        output.filename = str(raw_input("Output file : "))
    elif args.user is None:
        print(colored("[!] ", 'red') + "FAS Username is required.")
        return 1
    else:
        userstats.values['user'] = str(args.user)
        userstats.values['delta'] = int(args.weeks) * 604800
        output.mode = args.mode
        output.filename = args.output

    # For json and text output, we need the JSON rather than the categories
    if output.mode == 'svg' or output.mode == 'png':
        out_obj = userstats.return_categories()
        # To handle user with no activity
        if len(out_obj) == 0:
            print ('[!] No activity found for user ' + str(args.user))
            return 1
    elif args.mode.lower() == 'json' or args.mode.lower() == 'text':
        out_obj = userstats.return_json()
        if out_obj['total'] == 0:
            print ('[!] No activity found for user ' + str(args.user))
            return 1

    title = "Category distribution for user " + str(args.user)
    output.show_output(out_obj, title)


if __name__ == '__main__':
        main()
