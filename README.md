<h1 align='center'><span aria-role='img' aria-label='boot'>🥾</span> Steel Toes</h1>

_a kedro hook to protect against breaking changes to data_

![Python Test and Package](https://github.com/WaylonWalker/steel-toes/workflows/Python%20Test%20and%20Package/badge.svg)
[![PyPI version](https://badge.fury.io/py/steel-toes.svg)](https://pypi.org/project/steel-toes/)
[![Code Style: Typed-Black](https://img.shields.io/badge/code%20style-mypy|black-black.svg)](https://github.com/ambv/black)

`steel-toes` is a kedro hook designed to prevent stepping on your teammates toes.  It will branch your data automatically based on your git branch, or manually by passing the branch name into the hook.


## Motivation

`kedro` is a ✨ fantastic project that allows for super-fast prototyping of data pipelines, while yielding production-ready pipelines. `kedro` promotes collaborative projects by giving each team member access to the exact same data.  Team members will often make their own branch of the project and begin work.  Sometimes these changes will break existing functionality. Sometimes we make mistakes as we develop, and fix them before merging in.  Either case can be detrimental to a teammate working downstream of your changes if not careful.

### 🥼 Wear the proper PPE during feature development

`steel-toes` hooks into your catalog to prevent changing downstream data on your teammates while developing in parallel.

### on_catalog_created and before_pipeline_run

When your project creates a catalog `steel-toes` will look to see if branched data exists, if it does it will swap the filepath to the branched path.  So you will be able to load the latest data from the perspective of any branch simulaneusly.

### after_node_run

After your node is ran, before saving, `steel-toes` will check if your `filepath` was swapped, if not it will swap it to the branched `filepath` before saving.

## Installation

`steel-toes` is deployed to pypi and can easily be `pip` installed.

``` console
pip install steel-toes
```

## Python Usage

since `steel-toes` requires access to the project_context to work you will
need to use a bit of an unconventional method to initialize your hooks.

## Override with environment variable

In certain situations such as using `kedro docker` in production, there is no git branch to pull from.  Setting an environment variable before `steel-toes` initializes will set the branch.

### set environment variable in the shell

``` bash
STEEL_TOES_BRANCH='PROD'
```

### set environment variable with python

```bash
import os

os.environ["STEEL_TOES_BRANCH"] = "PROD"
```

### Example Setup

``` python
from steel_toes import SteelToes

class ProjectContext(KedroContext):
   project_name = "kedro0160"
   project_version = "0.16.1"
   package_name = "kedro0160"
@property
def hooks(self):
   self._hooks = [ SteelToes(self), ]
   return self._hooks
```


### CLI Usage

The CLI provides a handy interface to clean up your branched datasets.

``` bash
$ steel-toes --help
Usage: steel-toes [OPTIONS] COMMAND [ARGS]...

  help

Options:
  -V, --version  Prints version and exits
  --help         Show this message and exit.

Commands:
  clean-branch  finds branch datasets and removes them
```

`steel-toes` also registers itself as a `kedro` global cli plugin.  You can run `kedro clean-branch` to clean your branched data.

``` bash
$ kedro clean-branch --help
Usage: kedro clean-branch [OPTIONS]

  finds branch datasets and removes them

Options:
  --dryrun                   Displays the files that would be deleted using
                             the specified command without actually deleting
                             them.

  -b, --branch TEXT          git branch to clean files from
  -d, --directory DIRECTORY  Path to save the static site to
  -h, --help                 Show this message and exit.
```

## Contributing

**You're Awesome** for considering a contribution!  Contributions are welcome, please check out the [Contributing Guide](https://github.com/WaylonWalker/steel-toes/blob/main/contributing.md) for more information.  Please be a positive member of the community and embrace feedback

## Versioning

We use [SemVer](https://semver.org/) for versioning. For the versions available, see the [tags on this repository](./tags).


## Author

[![Waylon Walker](https://avatars1.githubusercontent.com/u/22648375?s=120&v=4)](https://github.com/WaylonWalker) - Waylon Walker - _Original Author_

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE). file for details
