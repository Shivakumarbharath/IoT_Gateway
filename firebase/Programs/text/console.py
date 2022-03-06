#https://rich.readthedocs.io/en/stable/console.html

from rich.console import Console
console = Console()


console.print([1, 2, 3])
console.print("[blue underline]https://rich.readthedocs.io/en/stable/console.html[/blue underline] - Link for documentation")
console.print(locals())
console.print("FOO", style="white on blue")


#rules
console.rule("[bold red]Chapter 2")
