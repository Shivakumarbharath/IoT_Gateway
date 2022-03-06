#https://rich.readthedocs.io/en/stable/console.html
from time import sleep
from rich.console import Console
console = Console()

def simple():
	console.print([1, 2, 3])
	sleep(15)
	console.print("[blue underline]https://rich.readthedocs.io/en/stable/console.html[/blue underline] - Link for documentation")
	console.print(locals())
	console.print("FOO", style="white on blue")



with console.status("Working...",spinner="aesthetic"):
    simple()
