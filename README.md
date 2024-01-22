# WordPress Plugin Checker

A simple program allowing to find the version of a wordpress plugin on one or more urls asynchronously.

This tool allows you to quickly check if sites using wordpress have plugins with vulnerabilities.

## Install

```bash
git clone git@github.com:WhatTheSlime/wpcheck.git
cd wpcheck
python3 -m pip install packaging
./wpcheck.py -h
```

## Usage

```bash
# One target, one plugin.
./wpcheck.py -t http://target.url -p contact-form-7:5.3.2

# Many targets, many plugins.
./wpcheck.py -t http://target1.url http://target2.url -p contact-form-7:5.3.2 wordpress-seo:17.2

# Targets files, plugins files.
./wpcheck.py -t path/to/targets1.lst path/to/targets2.lst -p path/to/plugins1.lst path/to/plugins2.lst
```

