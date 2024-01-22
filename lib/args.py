from argparse import ArgumentParser
from pathlib import Path


default_workers = 20


def parse_args():
    """Function to parse user arguments"""
    parser = ArgumentParser(description="WordPress plugins version checker")
    
    parser.add_argument(
        "-t", "--targets", type=str, nargs="+", required=True,
        help="target url (e.g. http://target.com) or file path containing urls"
        " separated by newlines.")
    
    parser.add_argument(
        "-p", "--plugins", type=str, nargs="+", required=True,
        help="vulnerable plugin slug and version (e.g. contact-form-7:5.3.2) "
        " or file path containing plugins separated by newlines.")

    parser.add_argument(
        "-H", "--headers", type=str, nargs="+", metavar="NAME:VALUE", 
        default="", help="add HTTP headers.")

    parser.add_argument(
        "-x", "--proxy", type=str, default="",
        help="Proxy url (e.g. http://127.0.0.1:8080).")
    
    parser.add_argument(
        "-w", "--workers", type=int, default=default_workers,
        help=f"Number of max concurrent workers (default {default_workers}).")
    
    parser.add_argument(
        "-u", "--users", type=str, nargs="+", default=[],
        help="username or file path containing usernames separated by "
             "newlines.")
    
    parser.add_argument(
        "-o", "--output", type=Path, help="File path to output logs.")
    
    return parser.parse_args()


def loadlist(objs):
    """Process ArgParse argument with `type=str` and `nargs='+' and return a 
    list of unique strings."""
    result = []
    
    for obj in objs:
        # Process argument as a wordlist path.
        if Path(obj).is_file():
            with open(obj, "r") as file:
                result += [
                    line.strip() for line in file 
                    if not line.strip().startswith("#")]
        # Process argument as a single element.
        else:
            result += [obj]

    return result

