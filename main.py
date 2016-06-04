from __future__ import print_function
from __future__ import absolute_import

import os
import fedmsg
import argparse
import fedmsg.meta
import stats
import output
from termcolor import colored


def main():
    # fedmsg config
    config = fedmsg.config.load_config()
    fedmsg.meta.make_processors(**config)

    # Argument Parser initialization
    parser = argparse.ArgumentParser(description='Fedora GSoC stats gatherer')
    parser.add_argument('--user', help='FAS username')
    parser.add_argument('--weeks', help='Time in weeks', default=1)
    parser.add_argument('--mode', help="Type of Output", default='text')
    parser.add_argument('--output', help="Output name", default='stats')
    parser.add_argument('--category', help="Category for graphs", default=None)
    parser.add_argument('--interactive', '-i', help="Enable interactive mode", action='store_true')
    args = parser.parse_args()

    # Object inits and argument processing

    if args.interactive:
        stats.values['user'] = str(raw_input("Enter FAS Username : "))
        stats.values['delta'] = 604800 * int(raw_input("Number of weeks stats required for : "))
        output.mode = str(raw_input("Type of output : "))
        output.filename = str(raw_input("Output file : "))
    elif args.user is None:
        print(colored("[!] ", 'red') + "Username is required. Use -h for help")
        return 1
    else:
        stats.values['user'] = str(args.user)
        stats.values['delta'] = int(args.weeks) * 604800
        stats.category = args.category
        output.mode = args.mode
        output.filename = args.output

    # For json and text output, we need the JSON rather than the categories
    if output.mode == 'svg' or output.mode == 'png':
        draw_obj = stats.return_categories()
        # To handle user with no activity
        if len(draw_obj) == 0:
            print ('[!] No activity found for user ' + str(args.user))
            return 1

    elif args.mode.lower() == 'json' or args.mode.lower() == 'text':
        draw_obj = stats.return_json()
        if draw_obj['total'] == 0:
            print ('[!] No activity found for user ' + str(args.user))
            return 1

    # output.show_category_output(draw_obj, str(stats.values['user']), 'bar')
    stats.return_interactions(['issue','pull-request'])


if __name__ == '__main__':
    main()
