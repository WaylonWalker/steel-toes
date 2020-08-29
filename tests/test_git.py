"""Module to test how steel-toes interprets your git branch automatically."""
import os

import pytest
from git import Repo

from steel_toes.core import get_current_branch, get_current_git_branch


def git_repo(tmpdir, branch="main"):
    """Make and branch a git repo in tmpdir."""
    p = tmpdir.join("README.md")
    p.write("content")
    repo = Repo.init(tmpdir)
    repo.index.add(str(tmpdir))
    repo.index.commit("init")
    new_branch = repo.create_head(branch)
    repo.head.reference = new_branch
    return tmpdir


BRANCHES = ["steel", "main", "master", "one-two", "1", "one&two"]


@pytest.mark.parametrize("branch", BRANCHES)
def test_git_branch(tmpdir, branch):
    """Check that environment variable sets branch."""
    git_repo(tmpdir, branch)
    assert get_current_branch(tmpdir) == branch


def test_git_sha_not_git(tmp_path):
    """Check that get_current_git_branch returns None when not in a git directory."""
    result = get_current_git_branch(tmp_path)
    assert result is None


@pytest.mark.parametrize("branch", BRANCHES)
def test_environment_variables_no_git(tmpdir, branch):
    """Check that environment variable sets branch."""
    os.environ["STEEL_TOES_BRANCH"] = branch
    assert get_current_branch() == branch


@pytest.mark.parametrize("branch", BRANCHES)
def test_environment_variables_with_git(tmpdir, branch):
    """Check that environment variable sets branch when git branch matches."""
    os.environ["STEEL_TOES_BRANCH"] = branch
    git_repo(tmpdir, branch)
    assert get_current_branch() == branch


@pytest.mark.parametrize("branch", BRANCHES)
def test_prefers_environment_variables(tmpdir, branch):
    """Check that environment variable sets branch when git branch is main."""
    os.environ["STEEL_TOES_BRANCH"] = branch
    git_repo(tmpdir, "main")
    assert get_current_branch() == branch


@pytest.mark.parametrize("branch", BRANCHES)
def test_prefers_environment_variables_change_git(tmpdir, branch):
    """Check that environment variable sets branch when env git branch is different."""
    os.environ["STEEL_TOES_BRANCH"] = "main"
    git_repo(tmpdir, branch)
    assert get_current_branch() == "main"
