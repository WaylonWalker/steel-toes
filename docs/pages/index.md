---
date: 2022-09-01 1:00:00
title: steel-toes
published: True
tags:
  - home
  - meta
---

<img src="/steel-toes.png" alt="steel-toes" width="250" align=right>


_a kedro hook to protect against breaking changes to data_

`steel-toes` is a plugin for the python data pipelining framework **kedro**.
It modifies each datasets filepath when you are developing a new feature to the
pipeline, but do not want to wreck pipelines running on other branches.

* [installation](#installation)
* [setup](#setup)
* [overrides](#override-with-environment-variable)

## Motivation

`kedro` is a ✨ fantastic project that allows for super-fast prototyping of
data pipelines, while yielding production-ready pipelines. `kedro` promotes
collaborative projects by giving each team member access to the exact same
data. Team members will often make their own branch of the project and begin
work. Sometimes these changes will break existing functionality. Sometimes we
make mistakes as we develop, and fix them before merging in. Either case can be
detrimental to a teammate working downstream of your changes if not careful.

### 🥼 Wear the proper PPE during feature development

`steel-toes` hooks into your catalog to prevent changing downstream data on
your teammates while developing in parallel.

### on_catalog_created and before_pipeline_run

When your project creates a catalog `steel-toes` will look to see if branched
data exists, if it does it will swap the filepath to the branched path. So you
will be able to load the latest data from the perspective of any branch
simulaneusly.

### after_node_run

After your node is ran, before saving, `steel-toes` will check if your
`filepath` was swapped, if not it will swap it to the branched `filepath`
before saving.

## Installation

`steel-toes` is deployed to pypi and can be `pip` installed.

```console
pip install steel-toes
```

For a real kedro project you should add to your requirements.

## Setup

To add `SteelToes` to your kedro>0.18.0 project add an instance of the
`SteelToes` hook to your tuple of hooks in src/<project_name>/settings.py.

``` python title=settings.py
from steel_toes import SteelToes

HOOKS = (SteelToes(),)
```

!!! Note settings<span/>.py location
    `settings.py` is typically located in `src/<python_package>/settings.py`.

### ignore_types

Some datasets have a `_filepath` attribute that is not meant for saving
datasets to and is not needed to be "branched", and should be ignored from
steel_toes, for example `SQLQueryDataSet`.

``` python title=settings.py
from kedro.extras.datasets.pandas.sql_dataset import SQLQueryDataSet, SQLTableDataSet
from steel_toes import SteelToes

HOOKS = (SteelToes(ignore_types=[SQLQueryDataSet, SQLTableDataSet]),)
```

## Automatic branch naming

`steel_toes` will automatically get the branch name from your git branch.  All
you need to do is create a new branch, and steel-toes will make sure that all
the data you write will go to a specific place for that branch.  It will not
change the filepaths until the dataset exists or just before its written, this
way your catalog will still load existing datasets from the dataset specified
in the catalog.

``` bash
git checkout -b my-new-feature origin/main
```

## Override with environment variable

In certain situations such as using `kedro docker` in production, there is no
git branch to pull from. Setting an environment variable before `steel-toes`
initializes will set the branch.

### set environment variable in the shell

``` bash title=run.sh
STEEL_TOES_BRANCH='PROD'

# run kedro here
```

### set environment variable with python

``` python title=run.py
import os

os.environ["STEEL_TOES_BRANCH"] = "PROD"

# run kedro here
```

## Example filenames

Here is an example of what filepaths look like when I add parquet catalog
entries to the spaceflights project, `steel_toes` will add the branch name
automatically just before the file extension.

``` yaml
X_test: data/X_test_main.pq
X_train: data/X_train_main.pq
preprocessed_companies: data/02_intermediate/preprocessed_companies_main.pq
preprocessed_shuttles: data/02_intermediate/preprocessed_shuttles_main.pq
model_input_table: data/03_primary/model_input_table_main.pq
regressor: data/06_models/regressor_main.pickle
```

## Logs on first run

When first running your pipeline with `steel-toes` it will start the
`_filepath` swap **after_node_run**, since the swapped file does not yet exist.

!!! Note 
    At this point catalog.load('preprocessed_shuttles') will **not** load the
    branched dataset.

``` bash
❯ kedro run
INFO     Kedro project spaceflights                                                               session.py:340
...
INFO     STEEL_TOES:after_node_run 'preprocessed_shuttles.pq' -> 'preprocessed_shuttles_main.pq'  steel_toes.py:102
...
INFO     Completed 6 out of 6 tasks                                                               sequential_runner.py:85
INFO     Pipeline execution completed successfully.                                               runner.py:90
```

## Logs after dataset exists

Subsequent runs of kedro will swap the dataset to the branched filepath
immediately after the catalog has been created.

!!! Note
    Now catalog.load('preprocessed_shuttles') **will** load the branched dataset.

``` bash
INFO     Kedro project spaceflights                                                                      session.py:340
...
INFO     STEEL_TOES:after_catalog_created 'preprocessed_shuttles.pq' -> 'preprocessed_shuttles_main.pq'  steel_toes.py:102
...
INFO     Completed 6 out of 6 tasks                                                                      sequential_runner.py:85
INFO     Pipeline execution completed successfully.                                                      runner.py:90

```

### CLI Usage

The CLI provides a handy interface to clean up your branched datasets.

```bash title="steel-toes --help"
Usage: steel-toes [OPTIONS] COMMAND [ARGS]...

  help

Options:
  -V, --version  Prints version and exits
  --help         Show this message and exit.

Commands:
  clean-branch  finds branch datasets and removes them
````

`steel-toes` also registers itself as a `kedro` global cli plugin. You can run
`kedro clean-branch` to clean your branched data.

```bash title="steel-toes clean-branch --help"
Usage: kedro clean-branch [OPTIONS]

  finds branch datasets and removes them

Options:
  --dryrun                   Displays the files that would be deleted using
                             the specified command without actually deleting
                             them.

  -b, --branch TEXT          git branch to clean files from
  -h, --help                 Show this message and exit.
```

## Cleaning up old branches

To clean up your current branch, running `kedro clean-branch` will remove all
the datasets that have been swapped to the current branch. Adding `--dryrun`
will only log what `steel-toes` intends to do, and will not delete.

``` bash title="kedro clean-branch --dryrun"
INFO     STEEL_TOES:after_catalog_created 'preprocessed_shuttles.pq' -> 'preprocessed_shuttles_main.pq'                                         steel_toes.py:102
...
INFO     STEEL_TOES:dryrun-remove | '/home/waylon/git/spaceflights/data/02_intermediate/preprocessed_shuttles_main.pq'                          steel_toes.py:141
```

Dropping the `--dryrun` flag will delete all the branched datasets.

``` bash title="kedro clean-branch"
INFO     STEEL_TOES:after_catalog_created 'preprocessed_shuttles.pq' -> 'preprocessed_shuttles_main.pq'                                         steel_toes.py:102
...
INFO     STEEL_TOES:deleting | '/home/waylon/git/spaceflights/data/02_intermediate/preprocessed_shuttles_main.pq'                          steel_toes.py:141
```

## Contributing

**You're Awesome** for considering a contribution! Contributions are welcome,
please check out the [Contributing Guide](https://github.com/WaylonWalker/steel-toes/blob/main/contributing.md)
for more information. Please be a positive member of the community and embrace
feedback

## Versioning

We use [SemVer](https://semver.org/) for versioning. For the versions
available, see the [tags](https://github.com/WaylonWalker/steel-toes/tags), or
[releases](https://github.com/WaylonWalker/steel-toes/releases/)


## Author

<img src="https://avatars1.githubusercontent.com/u/22648375?s=120&v=4" alt="Waylon Walker" width="150">

Waylon Walker - _Original Author_

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE).
file for details
