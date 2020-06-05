"""Configuration for cli tests."""
from os import makedirs
from typing import Iterator

from click.testing import CliRunner
from pytest import fixture

MOCKED_HOME = "user/path/"


@fixture(name="cli_runner")
def cli_runner_fixture() -> Iterator[CliRunner]:
    """Create cli_runner_fixture."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        makedirs(MOCKED_HOME)
        yield runner
