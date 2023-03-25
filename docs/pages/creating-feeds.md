---
date: 2022-09-05 1:00:00
title: Creating Your Feeds
published: True
tags:
  - home
  - meta

---

Feeds are a powerful feature of `markata` that allow you to build feeds of
posts from the same arguments that get passed into `Markata.map`, all within
`markata.toml`.  You can create feeds for things like your published articles,
articles that contain a certain tag, articles that are stored in a certain
folder, articles posted before or after a certain date (likely today).

## Load up ipython

_or python or a script that you run, whatever your fancy_

Now create an instance of markata.

``` python
from markata import Markta
m = Markata()
```

## Let's poke through our articles

Now you should be able to list out the articles, for this site it will be something like.

``` python
m.articles
# [
#     <frontmatter.Post object at 0x7f609831b0a0>,
#     <frontmatter.Post object at 0x7f6098318b80>,
#     <frontmatter.Post object at 0x7f609831a890>,
#     <frontmatter.Post object at 0x7f609831ab30>,
#     <frontmatter.Post object at 0x7f609831aa70>,
#     <frontmatter.Post object at 0x7f609831b760>
# ]
```

Now let's say you want the title for all the articles, you could do this with a list comp.

``` python
[post['title'] for post in markata.articles]
# ['Building the Site', 'Home Page', 'Loading Markata into Ipython', 'Jinja Variables', 'Your Own Style', '404']
```

Now if you wanted to filter for only published posts, you can filter by the boolean variable `published`.

``` python
[post['title'] for post in markata.articles if published]
# ['Building the Site', 'Home Page', 'Loading Markata into Ipython', 'Jinja Variables', 'Your Own Style']
```

And a little more arbitrary, and slightly more complex filter.

``` python
[post['title'] for post in markata.articles if "y" in post['path']]
# ['Loading Markata into Ipython', 'Your Own Style']
```

## Using map

The same results can be achieved with the `Markata.map` function.  Again let's
start by getting the title.

``` python
[post['title'] for post in markata.articles if published]
markata.map('title')
# ['Building the Site', 'Home Page', 'Loading Markata into Ipython', 'Jinja Variables', 'Your Own Style', '404']
```

Then we can add the filter for `published` posts back in.

``` python
markata.map('title', filter='published')
# ['Building the Site', 'Home Page', 'Loading Markata into Ipython', 'Jinja Variables', 'Your Own Style', '404']
```

And the more arbitrary filter looking for "y" in the article's path.

``` python
markata.map('title', filter='"y" in post["path"]')
# ['Loading Markata into Ipython', 'Your Own Style']
```

Since each article is unpacked into the map function, path is also directly
available to the filter, so we don't necessarily need to reach for the `post`.

``` python
markata.map('title', filter='"y" in path')
# ['Loading Markata into Ipython', 'Your Own Style']
```

Lastely we can also **sort on date**, by adding a sort argument.

``` python
markata.map('title', filter='published', sort='date')
# ['Building the Site', 'Home Page', 'Loading Markata into Ipython', 'Jinja Variables', 'Your Own Style', '404']
```

## What does this have to do with feeds.

Markata can make a feed page, displaying each post in the returned list inside
of an html feed.  It does this by unpacking the arguments from the feeds config
into the map function.

``` python
[markata.feeds.published]
# creates a feed at /published
filter="date<=today and post.get('published', False)"
sort="date"
```

