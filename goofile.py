#!/usr/bin/env python
# Goofile v1.6
# My Website:
# Project Page: github.com/sosukeinu/goofile
#
# TheHarvester used for inspiration
# A many thanks to the Edge-Security team!
# Thanks to Thomas (G13) Richards for such a cool tool
#

import getopt
import re
import sys
import http.client

import requests

print("\n----------------------------------------")
print("|Goofile v1.6	                        |")
print("|Coded by Thomas (G13) Richards          |")
print("|Updated by Jonathan (sosukeinu) Batteas |")
print("|                                        |")
print("|github.com/sosukeinu/goofile            |")
print("------------------------------------------\n\n")

global result
result = []


def usage():
    print("Goofile 1.6\n")
    print("usage: goofile options \n")
    print("       -d: domain to search\n")
    print("       -f: filetype (ex. pdf)\n")
    print("example:./goofile.py -d test.com -f txt\n")
    sys.exit()


def run_basic(dmn, file):
    h = http.client.HTTPSConnection('www.google.com')
    headers = {'Host': 'www.google.com', 'User-agent': 'Internet Explorer 6.0 ', 'Referrer': 'www.g13net.com'}
    h.request('GET', "/search?num=500&q=site:" + dmn + "+filetype:" + file, headers=headers)
    response = h.getresponse()
    status = response.status
    reason = response.reason
    if status == 200:
        data = response.read()
        try:
            data = data.decode('utf-8')
        except UnicodeDecodeError:
            data = data.decode('latin-1')
        data = re.sub('<b>', '', data)
        for e in ('>', '=', '<', '\\', '(', ')', '"', 'http', ':', '//'):
            data = data.replace(e, ' ')
        r1 = re.compile('[-_.a-zA-Z0-9.-_]*' + '\.' + file)
        res = r1.findall(data)
    elif status == 302:
        print('Your request returned a {0} status. Reason: {1}'.format(status, reason))
        print('This usually happens because Google flagged your network for suspicious activity.')
        sys.exit()
    else:
        print('Your request returned a {0} status. Reason: {1}'.format(status, reason))
        sys.exit()
    return res

def run_api(dmn, file, key, engine, **kwargs):
    start_index = kwargs.get('startIndex', 1)
    r = requests.get("https://www.googleapis.com/customsearch/v1?key={0}&siteSearch={1}&fileType={2}&cx={3}&startIndex={4}&q=''".format(key, dmn, file, engine, start_index))
    res = r.json()['items']
    return res

def main(args=None):
    if args is None:
        args = sys.argv[1:]
    global limit
    limit = 100
    if len(sys.argv) < 3:
        usage()
    try:
        opts, args = getopt.getopt(args, "d:f:k:e:")

    except getopt.GetoptError:
        usage()
        sys.exit()
    key = None
    engine = None
    for opt, arg in opts:
        if opt == '-f':
            file = arg
        elif opt == '-d':
            dmn = arg
        elif opt == '-k':
            key = arg
        elif opt == '-e':
            engine = arg

    print("Searching in {0} for {1}".format(dmn, file))
    print("========================================")
    cant = 0

    while cant < limit:
        if key and engine:
            res = run_api(dmn, file, key, engine)
        else:
            res = run_basic(dmn, file)
        for x in res:
            if result.count(x) == 0:
                if key and engine:
                    result.append(x['link'])
                else:
                    result.append(x)
        cant += 100

    print("\nFiles found:")
    print("====================\n")
    t = 0
    if result:
        if key and engine:
            for x in result:
                print(x)
                t += 1
        else:
            for x in result:
                x = re.sub('<li class="first">', '', x)
            x = re.sub('</li>', '', x)
        print(x)
        t += 1
        print("====================\n")
    else:
        print("No results were found")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Search interrupted by user..")
    except:
        sys.exit()