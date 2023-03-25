---
date: 2022-09-02 1:00:00
title: Building the Site
published: True
tags:
  - home
  - meta

---

The first thing you will want to do is make sure that you can build your site and see it in the browser.  Markata builds static websites using a python based cli that can be setup with very few steps once you have python 3.7+ installed.  You will have to become at least a little bit comfortable running some commands from the command line to run the build.


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

# just serve markout at localhost:8000
hatch run serve
```

Once you have the site up and running, open your browser to
[http://localhost:8000](http://localhost:8000).

> Note,if you already have something running on port `8000` hatch run serve will give
> you an error, but hatch run tui will automatically choose the next available port.
> Make sure you open the right link in your browser.

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



