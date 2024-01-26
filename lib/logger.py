from datetime import datetime
from math import floor


reset   = "\033[0m"
bold    = "\033[1m"

def log(color: str, level: str, *messages: str, end="\n"):
    """Display log on stdout."""
    time = datetime.now().strftime("%H:%M:%S")

    print(
        f"\033[K\r {color}\033[2m{bold}{time}{reset}",  
        f"{color}{bold}{level}{reset}", *messages, end=end, flush=True)

def vuln(*messages: str): log("\033[31m", "Vuln", *messages)
def safe(*messages: str): log("\033[32m", "Safe", *messages)
def warn(*messages: str): log("\033[33m", "Warn", *messages)
def info(*messages: str): log("\033[34m", "Info", *messages)


class Progress:
    """Display iterrations progress."""
    def __init__(self, total: int):
        #: Total number of iterration to process.
        self.total = total
        #: Current iteration index.
        self.index = 0
        # Update the progression at intialization.
        self.update()
    
    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def update(self):
        """Update progres values."""
        # Calculate prgress percentage and iterations.
        percent = f"{floor(self.index * 100 / self.total)}%"
        pt_nb_spaces = 3 - len(str(percent))

        iterations = f"{self.index}/{self.total} it."
        it_nb_spaces = len(str(self.total)) - len(str(self.index))
        
        # Display progress on stdout.
        log("\033[34m", "Info", "Progress", 
            " " * it_nb_spaces + iterations, " " * pt_nb_spaces + percent, 
            end="\r")
        
        self.index += 1
