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

    #Initializing to None to prevent errors while generating multiple reports
    stats.unicode_json = {}
    i_count = 0

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

    # Check if the argument type is interactive
    if args.interactive:
        stats.values['user'] = str(input("Enter FAS Username : ")).lower()
        stats.weeks = int(args.weeks)
        stats.values['delta'] = 604800 * int(input("Number of weeks stats required for : "))
        stats.category = str(input("Enter category : ")).lower()
        output.mode = str(input("Type of output : ")).lower()
        output.filename = str(input("Output file : ")).lower()

    # Check if the user argument exists
    elif args.user is None:
        print(colored("[!] ", 'red') + "Username is required. Use -h for help")
        return 1

    # Else, use the argparse values. No arguments is handled by argparse.
    else:
        stats.values['user'] = str(args.user).lower()
        stats.values['delta'] = int(args.weeks) * 604800
        stats.category = args.category.lower()
        stats.weeks = int(args.weeks)
        output.mode = args.mode.lower()
        output.filename = args.output.lower()
    # For json and text output, we need the JSON rather than the categories
    if output.mode in ['png', 'svg', 'csv']:
        # Draw object for the above mentioned categories.
        draw_obj = stats.return_categories()

        # To handle user with no activity
        if len(draw_obj) ==  0:
            print (colored("[!] ", 'red') + 'No activity found for user ' + args.user)
            return 1

        # Generate the output graph objects required for calling generate_graph
        output.generate_graph(draw_obj, "Topic distribution of " + stats.values['user'], None, 'pie')
        draw_obj2 = stats.return_subcategories(stats.category)
        interactions = stats.return_interactions(draw_obj2)

        # Check if a category input was given and generate the specific category graph
        if not stats.category is None :
            output.generate_graph(draw_obj2, "Category: " + stats.category.capitalize()\
            + "\nUser: " + stats.values['user'], stats.category, 'bar')

        # Check if the sub-sub-category exists and generate it's graph
        if not None in list(interactions.keys()):
            for keys in interactions:
                i_count += 1
                output.generate_graph(interactions[keys], "Interaction with "+str(keys)+"\nCategory:  "\
                + stats.category.capitalize(), stats.category +"_" + keys, 'pie')

    # If not image based outputs, check if the input matches any of the text based inputs
    elif output.mode in ['json','text','markdown']:
        draw_obj = stats.return_json()
        # To handle user with no activity
        if draw_obj['total'] == 0:
            print (colored("[!] ", 'red') + 'No activity found for user ' + str(args.user))
            return 1
        output.generate_graph(draw_obj, stats.values['user'])



if __name__ == '__main__':
    main()
