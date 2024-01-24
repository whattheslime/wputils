from asyncio.exceptions import CancelledError
from datetime import datetime
from math import floor


reset   = "\033[0m"
bold    = "\033[1m"
    
def log(color, level, *messages, end="\n", out=None):
    time = datetime.now().strftime("%H:%M:%S")

    # Write log.
    if out:
        with open(out, "a") as file:
            file.write(" ".join(messages) + end)
    
    print(
        f"\r \033[90m{bold}{time}{reset}", f"{color}{bold}{level}{reset}", 
        *messages, end=end)

def vuln(*messages, out=""): log("\033[31m", "Vuln", *messages, out=out)
def safe(*messages, out=""): log("\033[32m", "Safe", *messages, out=out)
def warn(*messages, out=""): log("\033[33m", "Warn", *messages, out=out)
def info(*messages, out=""): log("\033[34m", "Info", *messages, out=out)

class Bar:
    def __init__(self, total, percent):
        self.total = total
        self.percent = percent
        self.index = 0
        self.update()
        
    def update(self):
        iteration = self.index

        percent = f"{floor(iteration * 100 / self.total)}%"
        p_spaces = " " * (3 - len(str(percent)))

        progress = f"{iteration}/{self.total} it."
        spaces = " "  * (len(str(self.total)) - len(str(iteration)))
        
        log(
            "\033[34m", "Info", "Progress", 
            spaces + progress, " ", p_spaces + percent, end="\r")
        
        self.index += 1

class progress:
    def __init__(self, total, percent=False):
        self.total = total
        self.percent = percent

    def __enter__(self):
        return Bar(self.total, percent=self.percent)

    def __exit__(self, etype, value, traceback):
        if etype != CancelledError:
            print()
        
