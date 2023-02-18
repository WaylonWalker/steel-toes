"""Configuration for context testing module.

pytest automatically loads conftest in all tests in this module
"""

import configparser
import itertools
import json
import logging
from pathlib import Path
from typing import Any, Dict, Union  # ,  Mapping,

import pandas as pd
import pytest
import yaml
from kedro import __version__ as kedro_version
from kedro.framework.context import KedroContext
from kedro.pipeline import Pipeline, node

from steel_toes import SteelToes, clean_branch


def _get_local_logging_config() -> Dict:
    """Create local logging config for running the dummy projects."""
    return {
        "version": 1,
        "formatters": {
            "simple": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}
        },
        "root": {"level": "ERROR", "handlers": ["console"]},
        "loggers": {
            "kedro": {"level": "ERROR", "handlers": ["console"], "propagate": False}
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "ERROR",
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            }
        },
        "info_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "simple",
            "filename": "logs/info.log",
        },
    }


def _write_yaml(filepath: Path, config: Dict) -> None:
    """YAML writer."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    yaml_str = yaml.dump(config)
    filepath.write_text(yaml_str)


def _write_json(filepath: Path, config: Dict) -> None:
    """JSON writer."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    json_str = json.dumps(config)
    filepath.write_text(json_str)


def _write_dummy_ini(filepath: Path) -> None:
    """INI writer."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    config = configparser.ConfigParser()
    config["prod"] = {"url": "postgresql://user:pass@url_prod/db"}
    config["staging"] = {"url": "postgresql://user:pass@url_staging/db"}
    with filepath.open("wt") as configfile:  # save
        config.write(configfile)


@pytest.fixture
def base_config(tmp_path: Path) -> Dict:
    """Create base config file containing all tested datasets.

    Note we are using bob as our test git branch, so that is used in the layers
    and datasets as well to ensure we are not clobbering anything up when we
    use the branch name as a dataset or directory name.
    """
    generic_config = {
        "type": "pandas.CSVDataSet",
        "save_args": {"index": False},
        "layer": "raw",
    }

    layers = ["raw", "int", "pri", "bob"]
    datasets = ["cars", "boats", "horses", "bob"]
    relative_datasets = ["horses"]

    data = {}

    for layer, dataset in itertools.product(layers, datasets):
        if dataset in relative_datasets:
            data[f"{layer}_{dataset}"] = {
                "filepath": f"{layer}_{dataset}.csv",
                **generic_config,
            }
        else:
            data[f"{layer}_{dataset}"] = {
                "filepath": str(tmp_path / layer / f"{dataset}.csv"),
                **generic_config,
            }
    return data


@pytest.fixture
def local_config(tmp_path: Path) -> Dict:
    """No need to test local config."""
    return {}


@pytest.fixture(params=[None])
def env(request) -> str:
    """Create env."""
    return request.param


@pytest.fixture
def config_dir(
    tmp_path: Path, base_config: Dict, local_config: Dict, env: Union[str, None]
) -> None:
    """Create config files in temp_path.

    Combine everything to create the config files.

    """
    env = "local" if env is None else env
    proj_catalog = tmp_path / "conf" / "base" / "catalog.yml"
    env_catalog = tmp_path / "conf" / str(env) / "catalog.yml"
    env_credentials = tmp_path / "conf" / str(env) / "credentials.yml"
    env_logging = tmp_path / "conf" / str(env) / "logging.yml"
    logging = tmp_path / "conf" / "logging.yml"
    parameters = tmp_path / "conf" / "base" / "parameters.json"
    db_config_path = tmp_path / "conf" / "base" / "db.ini"
    project_parameters = {"param1": 1, "param2": 2, "param3": {"param4": 3}}
    _write_yaml(proj_catalog, base_config)
    _write_yaml(env_catalog, local_config)
    _write_yaml(env_credentials, local_config)
    _write_yaml(env_logging, _get_local_logging_config())
    _write_yaml(logging, _get_local_logging_config())
    _write_json(parameters, project_parameters)
    _write_dummy_ini(db_config_path)


@pytest.fixture
def dummy_dataframe() -> pd.DataFrame:
    """Create dummy data for testing."""
    return pd.DataFrame({"col1": [1, 2], "col2": [4, 5], "col3": [5, 6]})


def identity(input1: Any) -> Any:
    """Use to pass dummy data without any operations."""
    return input1  # pragma: no cover


class DummyContext(KedroContext):
    """Dummy Context for testing.

    Note there is a init with extra arguments than may normally be there.  This
    was done to make the DummyContext More flexible.  I was hoping to be able to
    parameterize some of the data.

    """

    project_name = "bob"
    project_version = kedro_version
    package_name = "bob"

    def __init__(
        self, project_path, env, extra_params, layers, datasets, branch, announce=False
    ):
        """Initialize dummy context."""
        self.layers = layers
        self.datasets = datasets
        self.branch = branch
        self.announce = announce
        super().__init__(project_path, env, extra_params)

    def _get_pipelines(self) -> Dict[str, Pipeline]:
        """Create a default pipleine based on layers and datasets.

        Standard _get_pipelines, nothing special.

        uses itertools to create a list of every combination of layer and dataset
        uses zip to run identity on every layer_dataset combination

        """
        nodes = [
            "_".join(i) for i in list(itertools.product(self.layers, self.datasets))
        ]
        pipeline = Pipeline(
            [
                node(identity, a, b, name=f"create_{b}")
                for a, b in zip(nodes[:-1], nodes[1:])
            ],
            tags="pipeline",
        )
        return {"__default__": pipeline}

    def _setup_logging(self) -> None:
        """Disable logging during test.

        Logging was clogging up the failed test results unnecessarily.

        """
        logging.disable(50)

    @property
    def hooks(self):
        """Contains kedro hooks."""
        print(f"\n\nSTEELTOES BRANCH {self.branch}\n\n")
        self._hooks = [SteelToes(self, branch=self.branch, announce=self.announce)]
        return self._hooks


@pytest.fixture(params=[None])
def extra_params(request):
    """Extra params fixure, not really used in this project."""
    return request.param


@pytest.fixture
def dummy_context(tmp_path, mocker, env, extra_params):
    """Set up dummy_context with empty branch."""
    # Disable logging.config.dictConfig in KedroContext._setup_logging as
    # it changes logging.config and affects other unit tests
    mocker.patch("logging.config.dictConfig")
    layers = ["raw", "int", "pri", "bob"]
    datasets = ["cars", "boats", "horses", "bob"]
    return DummyContext(
        str(tmp_path),
        layers=layers,
        datasets=datasets,
        env=env,
        extra_params=extra_params,
        branch="",
    )


@pytest.fixture
def branched_dummy_context(tmp_path, mocker, env, extra_params):
    """Set up dummy_context with 'bob' branch."""
    # Disable logging.config.dictConfig in KedroContext._setup_logging as
    # it changes logging.config and affects other unit tests
    mocker.patch("logging.config.dictConfig")
    layers = ["raw", "int", "pri", "bob"]
    datasets = ["cars", "boats", "horses", "bob"]
    return DummyContext(
        str(tmp_path),
        layers=layers,
        datasets=datasets,
        env=env,
        extra_params=extra_params,
        branch="bob",
    )


@pytest.fixture
def branched_announce_dummy_context(tmp_path, mocker, env, extra_params):
    """Set up dummy_contet with 'bob' branch and announces protected datasets."""
    # Disable logging.config.dictConfig in KedroContext._setup_logging as
    # it changes logging.config and affects other unit tests
    mocker.patch("logging.config.dictConfig")
    layers = ["raw", "int", "pri", "bob"]
    datasets = ["cars", "boats", "horses", "bob"]
    return DummyContext(
        str(tmp_path),
        layers=layers,
        datasets=datasets,
        env=env,
        extra_params=extra_params,
        branch="bob",
        announce=True,
    )


@pytest.fixture
def ready_dummy_context(dummy_context, dummy_dataframe):
    """Get dummy ready by placing a dummy dataframe at every input edge node."""
    for dataset in dummy_context.pipeline.inputs():
        d = getattr(dummy_context.catalog.datasets, dataset)
        d.save(dummy_dataframe)
    return dummy_context


@pytest.fixture
def ready_branched_dummy_context(branched_dummy_context, dummy_dataframe):
    """Get dummy ready by placing a dummy dataframe at every input edge node."""
    print("ready branched")
    for dataset in branched_dummy_context.pipeline.inputs():
        d = getattr(branched_dummy_context.catalog.datasets, dataset)
        d.save(dummy_dataframe)
    return branched_dummy_context


@pytest.fixture
def ready_branched_announce_dummy_context(
    branched_announce_dummy_context, dummy_dataframe
):
    """Get dummy ready by placing a dummy dataframe at every input edge node."""
    print("ready branched")
    for dataset in branched_announce_dummy_context.pipeline.inputs():
        d = getattr(branched_announce_dummy_context.catalog.datasets, dataset)
        d.save(dummy_dataframe)
    return branched_announce_dummy_context


@pytest.fixture
def ran_dummy_context(ready_dummy_context):
    """Run dummy_context."""
    ready_dummy_context.run()
    return ready_dummy_context


@pytest.fixture
def ran_branched_dummy_context(ready_branched_dummy_context):
    """Run dummy_context."""
    ready_branched_dummy_context.run()
    return ready_branched_dummy_context


@pytest.fixture
def dry_cleaned_dummy_context(ran_branched_dummy_context):
    """Run clean_branch with --dryrun."""
    print(f"self.branch: {ran_branched_dummy_context.branch}")
    clean_branch(
        directory=".", branch="bob", dryrun=True, context=ran_branched_dummy_context
    )
    return ran_branched_dummy_context


@pytest.fixture
def cleaned_dummy_context(dry_cleaned_dummy_context):
    """Run clean_branch."""
    clean_branch(
        directory=".", branch="bob", dryrun=False, context=dry_cleaned_dummy_context
    )
    return dry_cleaned_dummy_context
