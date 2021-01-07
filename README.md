# Wordpress Plugin Checker

A simple program allowing to find the version of a wordpress plugin on one or more urls.
This tool allows you to quickly check if sites using wordpress have plugins with vulnerabilities.

## Usage
Check a plugin on a single url
```bash
$ python3 wpcheck.py -u <URL> <PLUGIN SLUG> <PATCHED VERSION>
```

Exemple:
```bash
$ python3 wpcheck.py -u http://target.pwn contact-form-7 5.3.2
```

Check version of a plugin on a list of urls
```bash
$ python3 wpcheck.py -ul <FILE PATH> <PLUGIN SLUG> <PATCHED VERSION>
```

Exemple:
```bash
$ python3 wpcheck.py -ul target.lst contact-form-7 5.3.2
```
