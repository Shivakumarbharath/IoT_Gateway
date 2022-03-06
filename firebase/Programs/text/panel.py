#https://rich.readthedocs.io/en/stable/reference/panel.html#rich.panel.Panel

from rich import print
from rich.panel import Panel
print(Panel("Hello, [red]World!",title="Title",expand=False))
