from __future__ import print_function
from __future__ import absolute_import

import os
import fedmsg
import argparse
import fedmsg.meta
import stats
import output
from termcolor import colored
from six.moves import input


def main():
    # fedmsg config
    config = fedmsg.config.load_config()
    fedmsg.meta.make_processors(**config)

    # Argument Parser initialization
    parser = argparse.ArgumentParser(description='Fedora GSoC stats gatherer')
    parser.add_argument('--user', '-u', help='FAS username')
    parser.add_argument('--weeks','-w', help='Time in weeks', default=1)
    parser.add_argument('--mode', '-m', help="Type of Output", default='text')
    parser.add_argument('--output', '-o', help="Output name", default='stats')
    parser.add_argument('--category', '-c', help="Category for graphs", default=None)
    parser.add_argument('--interactive', '-i', help="Enable interactive mode", action='store_true')
    args = parser.parse_args()

    # Object inits and argument processing
    if args.interactive:
        stats.values['user'] = str(input("Enter FAS Username : "))
        stats.values['delta'] = 604800 * int(input("Number of weeks stats required for : "))
        stats.category = str(input("Enter category : "))
        output.mode = str(input("Type of output : "))
        output.filename = str(input("Output file : "))

    # Check if the user argument exists
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
        # Generate the output graphs
        output.generate_graph(draw_obj, "Topic distribution of " + str(stats.values['user']), 'pie')
        draw_obj2 = stats.return_subcategories(stats.category)
        interactions = stats.return_interactions(draw_obj2)
        # Check if a category input was given
        if not stats.category is None :
            output.generate_graph(draw_obj2, "Category: " + str(stats.category).capitalize()\
            + "\nUser: " + str(stats.values['user']), 'bar')

        # Check if the sub-sub-category exists
        if not None in list(interactions.keys()):
            for keys in interactions:
                output.generate_graph(interactions[keys], "Interaction with "+str(keys)+"\nCategory:  "\
                + str(stats.category).capitalize(), 'pie')


    elif output.mode.lower() == 'json' or output.mode.lower() == 'text':
        draw_obj = stats.return_json()
        # To handle user with no activity
        if draw_obj['total'] == 0:
            print ('[!] No activity found for user ' + str(args.user))
            return 1
        output.generate_graph(draw_obj, str(stats.values['user']))



if __name__ == '__main__':
    main()
