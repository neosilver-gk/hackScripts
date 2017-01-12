#!/usr/bin/env python3
"""
SYNOPSIS

    TODO helloworld [-h, --help] [-v, --verbose] [--version]

DESCRIPTION

    TODO This describes how to use this script. This docstring
    will be printed by the script if there is an error or
    if the user requests help (-h or --help).

EXAMPLES

    TODO: Show some examples of how to use this script.

EXIT STATUS

    TODO: List exit codes

AUTHOR

    TODO: Name <name@examples.org>

LICENSE

    This script is in the public domain, free from copyrights or
    restrictions.

VERSION

        $Id$
"""

import sys
import os
import argparse
import traceback
import re
import requests
# from pexpect import run, spawn


def crawl_web(initial_url, depth, not_crawl='no'):

    crawled, ato_crawl, to_crawl = set(), set(), set()
    cur_depth = 0
    to_crawl.add(initial_url)

    emails = set()

    while cur_depth <= depth:

        print("______________" + str(cur_depth) + "____________")

        while to_crawl:

            current_url = to_crawl.pop()

            # get url's content
            try:
                r = requests.get(current_url)
                print("Processing %s" % current_url)
            except (requests.exceptions.MissingSchema,
                    requests.exceptions.ConnectionError):
                # ignore pages with errors
                print("exception raised")
                continue

            crawled.add(current_url)

            # extract all email addresses and add them into the resulting set
            new_emails = set()

            for emailadd in re.findall('[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+',
                                       str(r.content), re.I):
                new_emails.add(emailadd)

            emails.update(new_emails)

            for url in re.findall('a href="?\'?([^"\'>]*)', str(r.content)):

                if url[:4] != 'http':
                    if current_url[-1:] != '/':
                        if url[0] != '/':
                            url = current_url + '/' + url
                        else:
                            url = current_url + url
                    else:
                        if url[0] != '/':
                            url = current_url + '/' + url
                        else:
                            url = current_url + url

                pattern = re.compile('http?')

                if url != not_crawl:
                    if pattern.match(url):
                        ato_crawl.add(url)

        cur_depth += 1
        to_crawl.update(ato_crawl)
        ato_crawl.clear()

    return(emails, crawled)


def main(args):

    # TODO: Do something more interesting here...
    emails, crawled = crawl_web(args.url, args.depth, args.exc)

    efile = open(args.file, 'w')

    for email in emails:
        efile.write(email + '\n')

    efile.close()


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-f', '--file', help="output file")
        parser.add_argument('-u', '--url', help="target url")
        parser.add_argument('-d', '--depth', type=int,
                            help="depth to crawl the web")
        parser.add_argument('-e', '--exc', help="address not to folow")
        args = parser.parse_args()

        main(args)
        # TODO: Do add parse funktion
        sys.exit(0)
    except KeyboardInterrupt as e:  # Ctrl-C
        raise e
    except SystemExit as e:  # sys.exit()
        raise e
    except Exception as e:
        print("ERROR, UNEXPECTED EXCEPTION")
        print(str(e))
        traceback.print_exc()
        os._exit(1)
