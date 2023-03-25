---
date: 2022-09-04 1:00:00
title: Loading Markata into Ipython
published: True
tags:
  - home
  - meta

---


## Ipython extension

Setting up the ipython extension is completely optional, and not
required, but there for pure convenience.

You can add markata to your
`~/.ipython/profile_default/ipython_config.py` as reccomended by
ipython with the snippet below.

``` python
c.InteractiveShellApp.extensions.append('markata')
```

I don't prefer this because I also have ipython installed in
environments without markata installed, so I do the following in
my personal config so that it does not error when missing markata.

``` python
import importlib


def activate_extension(extension):
    try:
        mod = importlib.import_module(extension)
        getattr(mod, "load_ipython_extension")
        c.InteractiveShellApp.extensions.append(extension)
    except ModuleNotFoundError:
        "extension is not installed"
    except AttributeError:
        "extension does not have a 'load_ipython_extension' function"


extensions = ["markata", ]
for extension in extensions:
    activate_extension(extension)
```

## Loading a markata instance

If you have the extension active an instance will automatically be created and
available as `m` as well as `markata`.

``` python
m
# or
markata
```

If you opt out of setting up the extension or use something other than ipython
you can make an instance yourself.

``` python
from markata import Markata

m = Markata()
```

## Looking through articles

Once you have an instance of `markata` in memory you can look through your
articles using the list of articles, or the map function.


``` python
# get a list of frontmatter.Post objects
m.articles

# leverage the map function to filter
m.map('post', filter='"python" in tags')
m.map('post', filter='date>today')
```

## Map

The map function 

`func`: What to return as the item in the list. This can ve a single attribute
like `title`, or `tags`, or the full post `post`.  It can also be any string of
python like `'date>today'` or something more complicated like
`f'''"{markata.config['url']}/" + slug'''`

``` python
m.map('post')
m.map('title')
m.map('slug')

m.map('"python" in tags')
m.map(f'''"{markata.config['url']}/" + slug''')
```

`filter`: Filter is also just a string of python similar to the `func`
argument, but it filters based on the boolean value of the result.  You can do
things like look for published posts `published`, check for posts posted before
today `date<today`, or articles with certain tags `"python" in tags`.

``` python
m.map(filter='published')
m.map(filter='date<today')
m.map(filter='"python" in tags')
```

`sort`: Sort will try to sort your articles based on the value returned.

``` python
m.map(sort='title')
m.map(sort='date')
m.map(sort='order')
```

`reverse`: Reverse the results returned by map with the `reverse` flag.

``` python
m.map(reverse=False)
m.map(reverse=True)
```
