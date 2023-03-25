# markata-blog-starter

This is a blog starter for the python static site generator `markata`.

## New blog from template

The markata cli includes a `new` command that will present you with questions
to fill in the jinja variables in this repo.

``` bash
pipx install markata
markata new blog [directory]
```

Alternatively using copier directly

``` bash
pipx install copier
pip install copier

copier git+https://github.com/WaylonWalker/markata-blog-starter [directory]
```

> Note: make sure you specify the [directory] that youu want your site to be
> created into, not [directory]

## Installation

This site comes with a `pyproject.toml` that can be used by hatch to
automatically take care of your virtual environments for you.

``` bash
pip install hatch
```

## Building the site, Leveraging Hatch

Hatch comes with a nice system for creating scirpts that you can run in your
managed virtual environment with less effort of managing.  You can create any
that you want in your own `pyproject.toml`, but these come with the template
out of the box.

``` bash
# builds the site
hatch run build

# clean's cache and output directory
hatch run clean

# clean's cache and output directory, and builds
hatch run clean-build

# runs a development server, watches for changes and rebuilds.
hatch run tui

# run's clean then start's the tui
hatch run clean-tui
```

> Hatch takes care of the venv for you

## Building the site, vanilla

You will want to install everything in a virtual environment to prevent
yourself from clogging up your system python, or trying to run two versions of
`markata` for different projects.

``` bash
# using hatch for the virtual environment
hatch shell

# using venv
python -m venv .venv
. ./.venv/bin/activate
pip install -e .
```

Once you have your virtual environment created and activated you can use the
markata cli plugin to build your site.

``` bash
# builds the site
markata build

# clean's cache and output directory
markata clean

# runs a development server, watches for changes and rebuilds.
markata tui
```

## repl or script

It's also possible to run the build from a repl like ipython or a python
script.

``` python
from markata import Markata

m = Markata()
m.run()
```

## License

`markata-blog-starter` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
