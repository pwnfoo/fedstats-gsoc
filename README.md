## fedstats-gsoc


A simple CLI to tool to gather statistics from [datagrepper](https://apps.fedoraproject.org/datagrepper/)

### Description
This tool will help anyone to  pull statistics of any registered Fedora user with an active [FAS](https://fedoraproject.org/wiki/Account_System) account.

### Usage

This tool uses`argparse` to parse arguments. This can be used in two ways, one-liner / interactive method.
The interactive mode can be enabled by using the `--interactive` or `-i` flag. This mode of usage does not require any additional argument. Please not that the arguments passed (if any) will be invalid.

One-liner uses the classic argument parsing method to generate output. This is useful for automating the report generation process. The only mandatory argument is `--user / -u` which takes the FAS username as input.

`python stats.py --user=nobody` or `python stats.py -u nobody` will generate text based statistics of user `nobody` from datagrepper.

####Arguments :

`--interactive / -i`

* Launches the tool in interactive mode. Does not require any further arguments.

`--user / -u`

* Takes any FAS Username as argument. There is no default value and the tool will throw an error if this argument is left blank/not used.

`--weeks / -w`

* Takes an integer value to represent number of weeks. Converts it into timedelta. (1week = 604,800 seconds). Default value is 1.

`--mode / -m`

* Takes a single word string input. Supported input modes are : json, text, csv, markdown, svg and png. The default value is `text`. *(More features will be added soon)*

`--category / -c`

* Take a single word string input. This will define the category for which deeper analytics are required. Some example categories : pagure, irc, mailman, etc.

`--output / -o`

* Takes a single word string input. This will define the output file name. This option is to be combined with the `--mode/-m` argument. Please note that this option **DOES NOT** require an extension type. For instance, if you need an SVG output with the name `nobody.svg`, the --output flag should be set as `nobody` and not `nobody.svg`. the default value is `stats`

####Examples :

* Generate statistics of user nobody for a week and view the text logs :

`python main.py --user=nobody`

* Generate statistics of user foo in `.svg` format :

`python main.py --user=foo --mode=svg`

This will create `stats.svg` in your `$pwd`.

* Generate statistics of user foo in `.png` format with output name as `foo_stats.png`

`python main.py --user=foo --mode=png --output=foo_stats`

#### Basic Troubleshooting :

Please take a look at this [blog-post](https://sachinwrites.xyz/2016/05/28/getting-fedstats-gsoc-production-ready/).
