import argparse
import sys

from goofile.goofile import GooSearch


def main():
    """
    
    :return: A Python List object containing all of the links found
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", help="the domain to search - optional (ie. kali.org")
    parser.add_argument("-f", "--filetype", help="the filetype to search for - required (ie. pdf)")
    parser.add_argument("-k", "--key", help="Google Custom Search Engine API key - optional")
    parser.add_argument("-e", "--engine", help="Google Custom Search Engine ID - optional")
    parser.add_argument("-q", "--query", help="Only search for files with keyword - optional")
    parser.add_argument("--logging", help="Set the logging verbosity to something other than \"INFO\" - optional")
    args = parser.parse_args()
    if args.filetype:
        filetype = args.filetype
        domain = None
        key = None
        engine = None
        query = None
        logging = "INFO"
        if args.domain:
            domain = args.domain
        if args.key:
            key = args.key
        if args.engine:
            engine = args.engine
        if args.query:
            query = args.query
        if args.logging:
            logging = args.logging
    else:
        args.print_help()
        sys.exit(1)

    goo = GooSearch(domain=domain, filetype=filetype, key=key, engine=engine, query=query, log=logging)
    result = []

    print("Searching in {0} for {1}".format(domain, filetype))
    print("========================================")
    cant = 0

    while cant < goo.limit:
        if getattr(goo, 'key', None) and getattr(goo, 'engine', None):
            r = goo.run_api(goo)
        else:
            r = goo.run_basic()
        for x in r:
            if result.count(x) == 0:
                result.append(x)
        cant += 100

    print("\nFiles found:")
    print("====================\n")
    if result:
        for x in result:
            print(x)
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