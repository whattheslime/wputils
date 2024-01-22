from requests import Session
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning


def http_session(headers=[], proxy=""):
    """Create HTTP session
    """
    # Create HTTP session.
    disable_warnings(InsecureRequestWarning)
    session = Session()

    # Disable SSL certificate verification.
    session.verify = False

    # Set HTTP proxy.
    session.proxies["all"] = proxy

    # Set HTTP timeout.
    session.timeout = 20

    # Set HTTP headers.
    session.headers["User-Agent"] = (
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 "
        "Firefox/120.0")
    
    for header in headers:
        name, value = header.split(":", 1)
        session[name.strip()] = value.strip()

    return session
