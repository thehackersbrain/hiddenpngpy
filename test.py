from rich.panel import Panel
from rich.layout import Layout
from rich import print
from rich import box
from rich.align import Align
from time import sleep
from rich.live import Live


def make_layout() -> Layout:
    layout = Layout(name="root")

    layout.split(
        Layout(name="main"),
        Layout(name="footer", size=5),
    )

    return layout


def main():
    data = "this is secret data"
    pdata = Panel(
                Align.center("[green]{}[/]".format(data), vertical="middle"),
                box=box.ROUNDED,
                padding=(1, 2),
                title="[bold cyan]Extracted Data from the File[/]",
                border_style="blue"
            )
    authorc = Panel(
            Align.center("Created by: [bold cyan]Gaurav Raj[/] [[italic green link='https://github.com/thehackersbrain/']@thehackersbrain[/]]"),
            box=box.ROUNDED,
            padding=(1, 2),
            title="[bold cyan]Author[/]",
            border_style="blue"
            )
    layout = make_layout()
    layout['main'].update(pdata)
    layout['footer'].update(authorc)
    with Live(layout, screen=True):
        print(layout)
        sleep(10)


if __name__ == "__main__":
    main()
