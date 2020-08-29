"""
Core functionality of steel toes.

This module does all of the real work to get the current branch and inject it
into fielpaths.
"""
import copy
import logging
import os
import subprocess
from pathlib import Path
from typing import Any, List, Optional, Union

from colorama import Fore
from kedro.framework.context import KedroContext, load_context
from kedro.io.data_catalog import DataCatalog


def get_current_branch(proj_dir: Union[str, Path, None] = None) -> Optional[str]:
    """Get the current branch to use.

    First checks for an environment variable `STEEL_TOES_BRANCH` if none is found, the
    current git branch will be preferred.
    """
    branch = os.getenv("STEEL_TOES_BRANCH")
    if branch is None:
        return get_current_git_branch(proj_dir)
    return branch


def get_current_git_branch(proj_dir: Union[str, Path, None] = None) -> Optional[str]:
    """Git branch of working tree.

    Returns: Git branch or None.
    """
    proj_dir = str(proj_dir or Path.cwd())
    try:
        res = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=proj_dir
        )
        return str(res.decode()).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        logging.getLogger(__name__).warning(f"Unable to git describe {proj_dir}")
    return None


def branched_dataset_exists(dataset: Any, branched_filepath: str) -> bool:
    """Check if branched filepath exists.

    Filepath swapping ensures that we utilize the datasets existing _exists() method.

    Returns: bools - whether branched_filepath exists or not
    """
    copied_dataset = copy.copy(dataset)
    copied_dataset._filepath = branched_filepath
    # needs type conversion kedro implemnets ANY
    return True if copied_dataset._exists() else False


def inject_branch(
    branch: Optional[str],
    catalog: DataCatalog,
    dataset: str,
    save_mode: bool = False,
    reset: bool = False,
) -> None:
    """Inject branch into _filepath attribute of dataset.

    Branch name may be passed in or automatically picked up by the git branch.
    Then will be injected in between stem and suffix of the _filepath

    Example:
    "data/02_intermediate/iris.csv" -> "data/02_intermediate/iris_main.csv"

    """
    if branch is None:  # pragma: no cover
        # branch is not mocked
        branch = ""
    try:
        d = getattr(catalog.datasets, dataset)
        filepath = d._filepath
    except AttributeError:
        return

    if hasattr(d, "_filepath_swapped") and not reset:
        return

    if not reset:
        branchstr = branch if branch == "" else f"_{branch}"
        branched_filepath = (
            filepath.parent / f"{filepath.stem}{branchstr}{filepath.suffix}"
        )
    # elif branch is not None and filepath.stem[-len(branch) - 1 :] == f"_{branch}":
    #     branched_filepath = (
    #         filepath.parent / f"{filepath.stem[:-len(branch) - 1]}{filepath.suffix}"
    #     )
    else:
        return

    if branched_dataset_exists(d, branched_filepath) or save_mode or reset:
        d._filepath = branched_filepath
        d._filepath_swapped = True

    if reset:  # pragma: nocover
        # needed for cli, without mocking a full project `steel-toes clean-branch`
        # cannot be tested, but the clean_branch function itself will still be
        # tested.
        delattr(d, "_filepath_swapped")


def rm_dataset(catalog: DataCatalog, dataset: str, dryrun: bool = False) -> None:
    """Delete a single datasets if branched.

    If the dataset was saved under the currently set branch it will have a
    _filepath_swapped attribute attached to it and can be safely deleted when
    running this function.  When dryrun=True the datasets that would be removed
    will simply be printed out.
    """
    try:
        d = getattr(catalog.datasets, dataset)
    except AttributeError:
        return
    try:
        filepath = d._filepath
    except AttributeError:
        return

    if not hasattr(d, "_filepath_swapped"):  # pragma: nocover
        # extra protection against deleting files
        return

    if dryrun:
        print("dryrun remove |", filepath)
    else:
        print("deleting | ", filepath)
        d._fs.delete(filepath, recursive=True)


def switch_branch(
    directory: Union[str, Path], catalog: DataCatalog, branch: str
) -> None:
    """Switch branch being used.

    This is particularly useful for the cleanup command as it
    allows for the user to cleanup when they no longer have the branch active.
    """
    current_branch = get_current_git_branch(directory)
    # breakpoint()
    if current_branch is None:  # pragma: no cover
        # branch is not mocked
        return
    for dataset in set(catalog.list()):
        inject_branch(current_branch, catalog, dataset, reset=True)
    for dataset in set(catalog.list()):
        inject_branch(branch, catalog, dataset)


def clean_branch(
    directory: Union[str, Path] = ".",
    branch: str = None,
    dryrun: bool = False,
    context: KedroContext = None,
) -> None:
    """Iterate over the catalog to remove branched datasets.

    Arguments:
        directory (Path): directory of kedro project. Defaults to '.'
        branch (str): git branch to clean files from. Defaults to current branch.
        dryrun (bool): Displays the files that would be deleted using the
            specified command without actually deleting them.

    """
    if context is None:
        # tests do not create a full project structure an need to pass context
        context = load_context(directory)  # pragma: nocover
    catalog = context.catalog
    if branch is not None:
        switch_branch(directory=directory, catalog=catalog, branch=branch)
    for dataset in catalog.list():
        rm_dataset(catalog=catalog, dataset=dataset, dryrun=dryrun)


def whos_protected(catalog: DataCatalog = None) -> List[str]:
    """List datasets protected by steel_toes.

    Only lists datasets that are currently branched off, not potentially
    branched datasets.
    """
    if catalog is None:
        catalog = load_context(".").catalog  # pragma: no cover
    protected = []
    for dataset in catalog.list():
        try:
            d = getattr(catalog.datasets, dataset)
            if hasattr(d, "_filepath_swapped"):
                protected.append(dataset)
        except AttributeError:
            pass
    return protected


def announce_protection(catalog: DataCatalog) -> None:
    """Pretty print datasets that are protected."""
    protected = whos_protected(catalog)
    if len(protected) == 0:
        print(
            f"{Fore.LIGHTBLACK_EX}STEEL-TOES |{Fore.RED} NO DATASETS PROETECTED{Fore.RESET}"
        )
        return
    print(
        f"{Fore.LIGHTBLACK_EX}STEEL-TOES |{Fore.YELLOW}{len(protected)}{Fore.GREEN} DATASETS PROETECTED{Fore.RESET}"
    )

    for dataset in protected:
        try:
            d = getattr(catalog.datasets, dataset)
            print(
                f"{Fore.LIGHTBLACK_EX}{dataset}: {Fore.LIGHTMAGENTA_EX}{d._filepath}{Fore.RESET}"
            )
        except AttributeError:  # pragma: no cover
            pass
