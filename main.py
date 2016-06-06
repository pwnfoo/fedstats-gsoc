from __future__ import print_function
from __future__ import absolute_import
from six.moves import input

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
    parser = argparse.ArgumentParser(description='Summer Coding stats gatherer')
    parser.add_argument('--user', '-u', help='FAS username')
    parser.add_argument('--weeks','-w', help='Time in weeks', default=1)
    parser.add_argument('--mode', '-m', help="Type of Output", default='text')
    parser.add_argument('--output', '-o', help="Output name", default='stats')
    parser.add_argument('--category', '-c', help="Category for graphs", default=None)
    parser.add_argument('--interactive', '-i', help="Enable interactive mode", action='store_true')
    args = parser.parse_args()
    args.output = args.user

    # Object inits and argument processing
    if args.interactive:
        stats.values['user'] = str(input("Enter FAS Username : "))
        stats.weeks = args.weeks
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
        stats.weeks = args.weeks
        output.mode = args.mode
        output.filename = args.output

    # For json and text output, we need the JSON rather than the categories
    if output.mode.lower() in ['png', 'svg', 'csv']:
        draw_obj = stats.return_categories()

        # To handle user with no activity
        if len(draw_obj) == 0:
            print (colored("[!] ", 'red') + 'No activity found for user ' + str(args.user))
            return 1

        # Generate the output graph objects required for calling generate_graph
        output.generate_graph(draw_obj, "Topic distribution of " + str(stats.values['user']), stats.category, 'pie')
        draw_obj2 = stats.return_subcategories(stats.category)
        interactions = stats.return_interactions(draw_obj2)

        # Check if a category input was given and generate category graph
        if not stats.category is None :
            output.generate_graph(draw_obj2, "Category: " + stats.category.capitalize()\
            + "\nUser: " + stats.values['user'], stats.category+"0", 'bar')

        i_count = 0
        # Check if the sub-sub-category exists
        if not None in list(interactions.keys()):
            for keys in interactions:
                i_count += 1
                output.generate_graph(interactions[keys], "Interaction with "+str(keys)+"\nCategory:  "\
                + str(stats.category).capitalize(), stats.category+str(i_count), 'pie')

    elif output.mode.lower() in ['json','text','markdown']:
        draw_obj = stats.return_json()
        # To handle user with no activity
        if draw_obj['total'] == 0:
            print (colored("[!] ", 'red') + 'No activity found for user ' + str(args.user))
            return 1
        output.generate_graph(draw_obj, str(stats.values['user']))



if __name__ == '__main__':
    main()
