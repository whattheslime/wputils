# WordPress Plugins Utils

Collection of simple programs allowing to find the version of [WordPress plugins](https://wordpress.org/plugins/) on one or more urls asynchronously, download them and check known vulnerabilities using [Wordfence Database](https://www.wordfence.com/threat-intel/vulnerabilities/wordpress-plugins/).

## Install

```bash
git clone https://github.com/whattheslime/wputils.git
cd wputils
python3 -m pip install packaging
```

## Update the Database

```bash
wget https://www.wordfence.com/api/intelligence/v2/vulnerabilities/scanner/ -O vulns.json
```

## Usages

### WpCheck - WordPress plugins checker

Check if one or more plugins with specific versions are present on one or many targets:

```bash
# One target, one plugin.
./wpcheck -t http://target.url -p contact-form-7:5.3.2

# Many targets, many plugins.
./wpcheck -t http://target1.url http://target2.url -p contact-form-7:5.3.2 wordpress-seo:17.2

# Targets and plugins files.
./wpcheck -t path/to/targets1.lst path/to/targets2.lst -p path/to/plugins1.lst path/to/plugins2.lst

# Mix of urls, files etc...
./wpcheck -t path/to/targets.lst http://target.url -p contact-form-7:5.3.2 path/to/plugins.lst
```

### WpGet - WordPress plugins getter

Download one or more plugins archives:

```bash
./wpget -p contact-form-7:5.3.2
```

### WpVuln - WordPress plugins vulnerabilities displayer

Display known vulnerabilities found on one or more plugins:

```bash
./wpvuln -p contact-form-7:5.3.2
```
