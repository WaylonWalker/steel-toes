"""
cli module provides steel-toes command line interface

The main use case for the cli is to cleanup data after branch work is done.
"""
import click

from .core import clean_branch as _clean_branch

__version__ = "0.0.1"


@click.group(name="steel-toes")
@click.version_option(__version__, "-V", "--version", help="Prints version and exits")
def cli() -> None:
    "help"
    pass  # pragma: nocover


@click.option(
    "--directory",
    "-d",
    default=".",
    type=click.Path(exists=False, file_okay=False),
    help="Path to save the static site to",
)
@click.option(
    "--branch", "-b", default=None, type=str, help="git branch to clean files from",
)
@click.option(
    "--dryrun",
    default=False,
    is_flag=True,
    help="Displays the files that would be deleted using the specified command without actually deleting them.",
)
@cli.command()
def clean_branch(
    directory: str = ".", branch: str = None, dryrun: bool = False
) -> None:
    "finds branch datasets and removes them"
    _clean_branch(directory=directory, branch=branch, dryrun=dryrun)  # pragma: nocover
