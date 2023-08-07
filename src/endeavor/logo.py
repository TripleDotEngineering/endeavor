import rich
from .__metadata__ import __version__, __copyright__

__logo__ = """
             ____
  ___ _   __/ __ \____  _____
 / _ \ | / / / / / __ \/ ___/
/  __/ |/ / /_/ / /_/ / /__     {version}
\___/|___/_____/\____/\___/     {copyright}
"""


def print_header():
    options = {
        'version'  : f'[bold white]Version [/bold white][bold cyan]{__version__}[/bold cyan]',
        'copyright': f'[bold white]Copyright (c) 2023 [/bold white][bold cyan]{__copyright__}[/bold cyan]'
    }
    fmt = __logo__.format(**options)
    rich.print(f'[bold yellow]{fmt}[/bold yellow]')
