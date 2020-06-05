"""Module to test how steel-toes iterprets your git branch automatically."""
from steel_toes.core import get_current_git_branch


def test_git_branch(tmp_path, mocker):
    """This is a replicate of kedros test_git_sha."""
    mocker.patch("subprocess.check_output", return_value="mocked_return".encode())
    result = get_current_git_branch(tmp_path)
    assert result == "mocked_return"


def test_git_sha_not_git(tmp_path):
    """Check that get_current_git_branch returns None when not in a git directory."""
    result = get_current_git_branch(tmp_path)
    assert result is None
