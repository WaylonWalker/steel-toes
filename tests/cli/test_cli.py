"""Module to test the command line interface of steel_toes."""

from steel_toes import __version__, cli


def test_cli(cli_runner):
    """Run `steel-toes` without arguments."""
    result = cli_runner.invoke(cli, [])

    assert result.exit_code == 0
    assert "steel-toes" in result.output


def test_print_version(cli_runner):
    """Check that `kedro --version` and `kedro -V` outputs contain.

    the current package version.

    """
    result = cli_runner.invoke(cli, ["--version"])

    assert result.exit_code == 0
    assert __version__ in result.output

    result_abr = cli_runner.invoke(cli, ["-V"])
    assert result_abr.exit_code == 0
    assert __version__ in result_abr.output


def test_help(cli_runner):
    """Check that `kedro --help` returns a valid help message."""
    result = cli_runner.invoke(cli, ["--help"])

    assert result.exit_code == 0
    assert "steel-toes" in result.output
