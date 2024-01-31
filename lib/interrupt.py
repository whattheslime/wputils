from .logger import warn
from signal import signal, SIGINT


def sigint_handler():
    signal(SIGINT, interrupt_handler)

def interrupt_handler(signum, frame):
    """CTRL+C handler."""
    warn("Quitting... Bye!")
    exit()