from datetime import datetime
from math import floor

reset   = "\033[0m"
bold    = "\033[1m"
    
def log(color, level, *messages, end="\n"):
    time = datetime.now().strftime("%H:%M:%S")
    print(
        f" \033[90m{bold}{time}{reset}", f"{color}{bold}{level}{reset}", 
        *messages, end=end)

def erro(*messages): log("\033[31m", "erro", *messages)
def vuln(*messages): log("\033[31m", "vuln", *messages)
def safe(*messages): log("\033[32m", "safe", *messages)
def warn(*messages): log("\033[33m", "warn", *messages)
def info(*messages): log("\033[34m", "info", *messages)

class Bar:
    def __init__(self, total, percent):
        self.total = total
        self.percent = percent
        self.update(0)
        
    def update(self, iteration):
        if self.percent:
            iteration = floor(iteration * 100 / self.total)
            total = 100
            progress = f"{iteration}%"
        else:
            total = self.total
            progress = f"{iteration}/{total} it."
        
        spaces = " "  * (len(str(total)) - len(str(iteration)))
        log("\033[34m", "info", f"Progress: {spaces}{progress}", end="\r")

class progress:
    def __init__(self, total, percent=False):
        self.total = total
        self.percent = percent

    def __enter__(self):
        return Bar(self.total, percent=self.percent)

    def __exit__(self, *args):
        print()
