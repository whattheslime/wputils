from requests import Session
from requests.adapters import HTTPAdapter, Retry
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning


def http_session(headers: list, proxy: str) -> Session:
    """Create HTTP session with custom configuration."""
    disable_warnings(InsecureRequestWarning)

    # Create HTTP session.
    session = Session()

    # Sent requests counter.
    session.nb_requests = 0

    # Set of targets that return a HTTP requests exception.
    session.errors = set()

    # Set maximum retries to 3.
    adapter = HTTPAdapter(max_retries=Retry(connect=3, backoff_factor=0.5))
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    # Disable SSL certificate verification.
    session.verify = False

    # Set HTTP proxy.
    session.proxies["all"] = proxy

    # Set User-Agent header.
    session.headers["User-Agent"] = (
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 "
        "Firefox/120.0")
    
    # Parse and set HTTP headers ("User-Agent" may be overwrited).
    for header in headers:
        name, value = header.split(":", 1)
        session[name.strip()] = value.strip()

    return session
