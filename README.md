# WordPress Plugin Checker

A simple program allowing to find the version of a wordpress plugin on one or more urls.
This tool allows you to quickly check if sites using wordpress have plugins with vulnerabilities.

## Install
1. Clone th repo
```bash
$ git clone git@github.com:WhatTheSlime/wpcheck.git
$ cd wpcheck
```

2. Create a virtual environment (Optional)
```bash
$ python -m venv env
$ . env/bin/activate
```

3. Install requirements
```bash
$ python -m pip install requirements.txt
```

## Usage
Check a plugin on a single url:
```bash
$ ./wpcheck.py -u <URL> <PLUGIN SLUG> <PATCHED VERSION>
# Exemple
$ ./wpcheck.py -u http://target.pwn contact-form-7 5.3.2
```

Check version of a plugin on a list of urls:
```bash
$ ./wpcheck.py -ul <FILE PATH> <PLUGIN SLUG> <PATCHED VERSION>
# Exemple
$ ./wpcheck.py -ul target.lst contact-form-7 5.3.2
```
