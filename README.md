# WordPress Plugins Checker

A simple program allowing to find the version of [WordPress plugins](https://wordpress.org/plugins/) on one or more urls asynchronously.

This tool allows you to quickly check if sites using WordPress have deprecated plugins with known vulnerabilities.

## Install

```bash
git clone git@github.com:WhatTheSlime/wpcheck.git
cd wpcheck
python3 -m pip install packaging
./wpcheck.py -h
```

## Usage

One target, one plugin:

```bash
./wpcheck -t http://target.url -p contact-form-7:5.3.2
```

Many targets, many plugins:

```bash
./wpcheck -t http://target1.url http://target2.url -p contact-form-7:5.3.2 wordpress-seo:17.2
```

Targets files, plugins files:

```bash
./wpcheck -t path/to/targets.lst http://target.url -p contact-form-7:5.3.2 path/to/plugins.lst
```

