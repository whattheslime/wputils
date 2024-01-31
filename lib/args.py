from argparse import ArgumentParser, Namespace
from datetime import datetime
from packaging.version import InvalidVersion, Version as v
from pathlib import Path

from .logger import warn


def add_plugins_arg(parser):
    parser.add_argument(
        "-p", "--plugins", type=str, nargs="+", required=True,
        help="plugin slug and version string (e.g. contact-form-7:5.3.2) "
        " or file path containing plugins separated by newlines")

def add_output_args(parser, default_path):
    parser.add_argument(
        "-o", "--output", type=Path, default=default_path, 
        help="output directory path")
    
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="enable verbose mode")

def add_session_args(parser):
    parser.add_argument(
        "-x", "--proxy", type=str, default="",
        help="proxy url (e.g. http://127.0.0.1:8080)")
     
    parser.add_argument(
        "-H", "--headers", type=str, nargs="+", metavar="NAME:VALUE", 
        default="", help="add HTTP headers")


def parse_output(output: Path) -> Path:
    """Parse output argument to create and return log file path."""
    if not output.is_dir():
        warn(f"Invalid directory path: {output}")
        exit()

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S%f")[:-4]
    filename = f"wpcheck-{timestamp}.out"

    return output / filename

def load_plugins(objs: str | Path) -> list[str, v]:
    """Parse plugins user arguments and return a list of slug and the version.
    """
    plugins = []
    
    for string in load_lists(objs):
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

        plugins.append((plugin, version))

    return plugins

def load_lists(objs: str | Path) -> list[str]:
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

