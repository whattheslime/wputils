#!/usr/bin/env python3
# author: @whattheslime
from asyncio import run
from datetime import datetime
from packaging.version import Version as v
from re import search
from signal import signal, SIGINT
from urllib.parse import urljoin, urlparse

from lib.args import loadlist, parse_args, parse_plugin, parse_output
from lib.asyncqueue import AsyncQueue
from lib.logger import bold, reset, info, progress, safe, vuln, warn
from lib.session import http_session


LOGO = """\033[34;1m
 \033[34;1m__      __\033[94m     ___ _           _   
 \033[34;1m\ \    / / __\033[94m / __| |_  ___ __| |__
  \033[34;1m\ \/\/ / '_ \\\033[94m (__| ' \/ -_) _| / /
   \033[34;1m\_/\_/| .__/\033[94m\___|_||_\___\__|_\_\\
         \033[34m|_|\033[0m
"""

version_regex = r"((?:\d+\.)+\d+)"
readme_regex = f"Stable tag:\s+{version_regex}"

versions_files = {        
    "readme.txt":       readme_regex,
    "README.txt":       readme_regex,
    "README.md":        readme_regex,
    "changelog.txt":    version_regex,
    "readme.md":        readme_regex,
    "CHANGELOG.md":     version_regex,
    "Readme.txt":       readme_regex,
}


def interrupt_handler(signum, frame):
    """CTRL+C handler."""
    warn("Quitting... Bye!")
    exit()


def check_version(session, target, slug, max_version, output, verbose):
    host = bold + target + reset

    # Check version files.
    for file, regex in versions_files.items():
        url = urljoin(target, f"wp-content/plugins/{slug}/{file}")
        try:
            response = session.get(url, allow_redirects=False)
        except Exception as exception:
            warn(exception)
            return
        
        # Search version in file.
        title = search(r"<title>(.*)</title>", response.text)
        if response.status_code == 200 and not title:
            match = search(regex, response.text)
            if match:
                # Check if version is vulnerable.
                log = ""
                version = v(match.group(1))
                message = f"{host} {slug} {version}"
                
                # Version should be vulnerable.
                if version <= max_version:
                    vuln(message, out=output)

                # Version should be safe.
                else:
                    safe(message)
                
                if verbose:
                    info(slug, "version found on", response.url)
                
                return log



async def main():
    """Program entry point."""
    start_time = datetime.now()

    signal(SIGINT, interrupt_handler)

    args = parse_args()

    output = parse_output(args.output)
    plugins = [parse_plugin(plugin) for plugin in loadlist(args.plugins)]
    targets = loadlist(args.targets)
    verbose = args.verbose

    with http_session(headers=args.headers, proxy=args.proxy) as session:
        asyncqueue = AsyncQueue(args.workers)

        info("Loading targets...")

        for target in targets:
            for slug, version in plugins:                
                asyncqueue.enqueue(
                    check_version, 
                    session, target, slug, version, output, verbose)
        
        total = len(targets) * len(plugins)

        info(f"{len(targets)} target(s) and {len(plugins)} plugin(s) loaded!")
        info("Starting scan...")
        
        founded = set()
        with progress(total) as bar:
            async for host in asyncqueue.dequeue():
                bar.update()
                if host:
                    founded.add(host)

    info(len(founded), "hosts have vulnerable plugins.")
    info(f"Eleapsed Time: {datetime.now() - start_time}")
    

if __name__ == "__main__":
    print(LOGO)
    run(main())
