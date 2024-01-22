#!/usr/bin/env python3
from asyncio import run
from datetime import datetime
from packaging.version import InvalidVersion, Version as v
from pathlib import Path
from re import search
from urllib.parse import urljoin, urlparse

from lib.args import parse_args, loadlist
from lib.asyncqueue import AsyncQueue
from lib.logger import info, progress, safe, vuln, warn
from lib.session import http_session


LOGO = """
  __      _____  ___ _           _    
  \ \    / / _ \/ __| |_  ___ __| |__ 
   \ \/\/ /|  _/ (__| ' \/ -_) _| / / 
    \_/\_/ |_|  \___|_||_\___\__|_\_\ 
"""
version_regex = r"((?:\d+\.)+\d+)"
readme_regex = f"Stable tag:\s+{version_regex}"

versions_files = {        
    "readme.txt":       readme_regex,
    "README.txt":       readme_regex,
    "README.md":        readme_regex,
    "readme.md":        readme_regex,
    "Readme.txt":       readme_regex,
    "changelog.txt":    version_regex,
    "CHANGELOG.md":     version_regex,
}


def check_version(session, target, slug, max_version, output):
    host = urlparse(target).netloc

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
                version = v(match.group(1))
                message = f"{host} {slug} {version} {response.url}"
                if version <= max_version:
                    vuln(message)
                    log = message.replace(" ", ",")
                    # Write log.
                    if output:
                        with open(output, "a") as file:
                            file.write(log)
                    return log
                else:
                    safe(message)
                    return


async def main():
    """Program entry point."""
    start_time = datetime.now()
    args = parse_args()

    output = Path(args.output)
    plugins = [plugin.split(":", 1) for plugin in loadlist(args.plugins)]
    targets = loadlist(args.targets)

    with http_session(headers=args.headers, proxy=args.proxy) as session:
        asyncqueue = AsyncQueue(args.workers)

        info("Loading targets...")
        for target in targets:
            for slug, version in plugins:
                try:
                    version = v(version)
                except InvalidVersion as error:
                    error(error, "for", slug)
                    return
                
                asyncqueue.enqueue(
                    check_version, session, target, slug, version, output)
        
        total = len(targets) * len(plugins)

        info(
            "Starting scan...", 
            f"{len(targets)} target(s) and {len(plugins)} plugin(s) loaded!)")
        try:
            i = 0
            founded = set()
            with progress(total) as bar:
                
                async for host in asyncqueue.dequeue():
                    i += 1
                    bar.update(i)   
                    if host:
                        founded.add(host) 

        except KeyboardInterrupt:
            warn("Pausing threads...")

    info(len(founded), "hosts have vulnerable plugins")
    info(f"Eleapsed Time: {datetime.now() - start_time}")
    

if __name__ == "__main__":
    print(LOGO)
    run(main())
