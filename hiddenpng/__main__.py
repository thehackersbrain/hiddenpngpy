from rich import print
from rich.panel import Panel
from rich.align import Align
from rich import box
import argparse
from sys import exit
from hiddenpng.functions import generate_key, hide_data, extract_data, make_layout # noqa
from rich.live import Live
from time import sleep


def parse_arguments():
    parser = argparse.ArgumentParser(description="Hide any data inside an Image file.") # noqa
    parser.add_argument(
        "-e",
        "--extract",
        help="Calls the tool to extract data from image.",
        action="store_true"
    )
    parser.add_argument(
        "-i",
        "--input",
        help="Specify the input file for hiding data",
        required=True
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Specify the output file or else the default will be used.",
    )
    parser.add_argument(
        "-k",
        "--key",
        help="Specify the secret key.",
        required=True
    )
    parser.add_argument(
        "-d",
        "--data",
        help="Specify the data to be hidden."
    )
    return parser.parse_args()


def main():
    args = parse_arguments()

    if (args.input.split('.')[1].lower() != 'png'):
        print("[[bold red]!![/]] This Program only works with 'png' filetypes.") # noqa
        exit(1)
    input_file = args.input
    key = generate_key(args.key)

    if (not args.extract):
        output_file = "default.png"
        if (args.output):
            output_file = args.output
        if (args.data):
            hide_data(input_file, output_file, args.data, key)
            print("[[bold green]s[/]] Data hidden successfully...")
        else:
            print("[[bold red]-[/]] Data is not specified...")
            exit(1)
    else:
        data = extract_data(input_file, key)
        pdata = Panel(
                    Align.center("[green]{}[/]".format(data.decode('utf-8')), vertical="middle"), # noqa
                    box=box.ROUNDED,
                    padding=(1, 2),
                    title="[bold cyan]Extracted Data from the File[/]",
                    border_style="blue"
                )
        authorc = Panel(
                Align.center("Created by: [bold cyan]Gaurav Raj[/] [[italic green link='https://github.com/thehackersbrain/']@thehackersbrain[/]]"), # noqa
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


if __name__ == '__main__':
    main()
