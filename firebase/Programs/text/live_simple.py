import random
import time

from rich.live import Live
from rich.table import Table
from rich import print
from rich.panel import Panel
def Print()
    print(Panel("Hello world"))

with Live(print(Panel("Hello world")), refresh_per_second=4) as live:
    for _ in range(40):
        time.sleep(0.4)
        live.update(print(Panel(f"Hello world no : {_}")))
