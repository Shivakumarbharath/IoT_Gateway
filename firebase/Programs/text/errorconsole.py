from rich.console import Console
from rich import print
error_console=Console(stderr=True,style="bold red")
error_console.print("Error console")
