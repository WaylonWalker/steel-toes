"""Steel Toes is designed to protect datasets from feature development.

Steel Toes provides protection against stepping on teammates toes inside of a
kedro project.  It does this by appending current git branch to the `_filepath`
of datasets on save, and loads the branch version if it exists.

HomePage and documentation: https://steeltoes.waylonwalker.com/

Copyright (c) 2020, Waylon Walker.
License: MIT (see LICENSE for details)
"""

__version__ = "0.4.0"
__author__ = ("Waylon Walker",)
__author_email__ = ("waylon@waylonwalker.com",)
__license__ = "MIT"

__all__ = ["cli", "SteelToes", "whos_protected", "clean_branch"]

from steel_toes.cli import cli
from steel_toes.hook import SteelToes
from steel_toes.steel_toes import clean_branch, whos_protected
