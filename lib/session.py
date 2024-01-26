from requests import Session
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning


def http_session(headers: list = [], proxy: str = "") -> Session:
    """Create HTTP session with custom configuration."""
    disable_warnings(InsecureRequestWarning)
    
    # Create HTTP session.
    session = Session()

    # Sent requests counter.
    session.nb_requests = 0

    # Disable SSL certificate verification.
    session.verify = False

    # Set HTTP proxy.
    session.proxies["all"] = proxy

    # Set HTTP timeout.
    session.timeout = 20

    # Set User-Agent header.
    session.headers["User-Agent"] = (
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 "
        "Firefox/120.0")
    
    # Parse and set HTTP headers ("User-Agent" may be overwrited).
    for header in headers:
        name, value = header.split(":", 1)
        session[name.strip()] = value.strip()

    return session
