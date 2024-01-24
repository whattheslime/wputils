from argparse import ArgumentParser
from packaging.version import InvalidVersion, Version as v
from pathlib import Path

from .logger import warn

default_workers = 20


def parse_args():
    """Function to parse user arguments"""
    parser = ArgumentParser(description="WordPress plugins version checker")
    
    # Global.
    parser.add_argument(
        "-t", "--targets", type=str, nargs="+", required=True,
        help="target url (e.g. http://target.com) or file path containing urls"
        " separated by newlines.")
    
    parser.add_argument(
        "-p", "--plugins", type=str, nargs="+", required=True,
        help="vulnerable plugin slug and version (e.g. contact-form-7:5.3.2) "
        " or file path containing plugins separated by newlines.")

    parser.add_argument(
        "-w", "--workers", type=int, default=default_workers,
        help=f"Number of max concurrent workers (default {default_workers}).")

    # HTTP session
    parser.add_argument(
        "-H", "--headers", type=str, nargs="+", metavar="NAME:VALUE", 
        default="", help="add HTTP headers.")

    parser.add_argument(
        "-x", "--proxy", type=str, default="",
        help="Proxy url (e.g. http://127.0.0.1:8080).")
    
    # Output
    parser.add_argument(
        "-o", "--output", default="", type=Path, 
        help="File path to output logs.")
    
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose mode")

    return parser.parse_args()


def parse_plugin(string):
    """Parse plugin user argument."""
    if ":" not in string:
        warn(
            "Malformed plugin! plugin must be like \"slug:version\" "
            "(e.g. contact-form-7:5.3.2).")
        exit()

    plugin, version = string.split(":", 1)

    try:
        version = v(version)
    except InvalidVersion as error:
        warn(error, "for", plugin, "plugin.")
        exit()
    
    return plugin, version

def parse_output(output):
    if output.is_dir():
        output = None
    elif output.exists():
        warn(f"\"{output}\" file exists!")
        exit()
    return output

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

