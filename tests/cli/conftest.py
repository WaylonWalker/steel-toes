"configuration for cli tests"
from os import makedirs

from click.testing import CliRunner
from pytest import fixture

MOCKED_HOME = "user/path/"


@fixture(name="cli_runner")
def cli_runner_fixture() -> None:
    "creates cli_runner_fixture"
    runner = CliRunner()
    with runner.isolated_filesystem():
        makedirs(MOCKED_HOME)
        yield runner
