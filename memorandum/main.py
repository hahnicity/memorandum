"""
memorandum.main
~~~~~~~~~~~~~~~
"""
#!/usr/bin/env python
from argparse import ArgumentParser

from memorandum.finder import get_yearly_data


def parse_argv():
    """
    Parse argv for a wiki page
    """
    parser = ArgumentParser()
    parser.add_argument(
        "page", help="Wiki page to get yearly views for eg: Apple_Inc."
    )
    return parser.parse_args()


def main():
    """
    Get yearly page views for a given wiki page
    """
    args = parse_argv()    
    return get_yearly_data(args.page)


# For dev purposes
if __name__ == "__main__":
    main()
