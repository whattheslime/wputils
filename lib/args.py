from argparse import ArgumentParser, Namespace
from datetime import datetime
from packaging.version import InvalidVersion, Version as v
from pathlib import Path

from .logger import warn


default_workers = 20
default_output = Path(__file__).parent.parent / "results"


def parse_args() -> Namespace:
    """Function to parse user arguments."""
    parser = ArgumentParser()
    
    # Global arguments.
    parser.add_argument(
        "-t", "--targets", type=str, nargs="+", required=True,
        help="target url (e.g. http://target.com) or file path containing urls"
        " separated by newlines")
    
    parser.add_argument(
        "-p", "--plugins", type=str, nargs="+", required=True,
        help="vulnerable plugin slug and version (e.g. contact-form-7:5.3.2) "
        " or file path containing plugins separated by newlines")

    parser.add_argument(
        "-w", "--workers", type=int, default=default_workers,
        help=f"number of max concurrent workers (default {default_workers})")

    # HTTP session arguments.
    parser.add_argument(
        "-H", "--headers", type=str, nargs="+", metavar="NAME:VALUE", 
        default="", help="add HTTP headers")

    parser.add_argument(
        "-x", "--proxy", type=str, default="",
        help="proxy url (e.g. http://127.0.0.1:8080)")
    
    # Output arguments.
    parser.add_argument(
        "-o", "--output", type=Path, default=default_output, 
        help="output directory path")
    
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="enable verbose mode")

    return parser.parse_args()


def parse_plugin(string: str) -> (str, v):
    """Parse plugin string and return the slug and the version."""
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


def parse_output(output: Path) -> Path:
    """Parse output argument to create and return log file path."""
    if not output.is_dir():
        warn(f"Invalid directory path: {output}")
        exit()

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S%f")[:-4]
    filename = f"wpcheck-{timestamp}.out"

    return output / filename


def loadlist(objs: str | Path) -> list[str]:
    """Parse argument with `type=str` and `nargs='+' and return a  list of 
    strings."""
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

