---
date: 2022-09-03 1:00:00
title: Jinja Variables
published: True
tags:
  - home
  - meta

config_overrides:
  head:
    text:
    - value: |
        <style>
            ul {
                list-style-type: None;
            }
            li a {
                background: rgba(255,255,255,.1);
                margin: .2rem;
            }
        </style>

---

Markata uses python's powerful jinja2 templating library for its templates as well as giving authors the ability to inject variables right into their markdown posts. This post contains quite a few examples of using jinja variables, compare it's output in the browser to the raw markdown file in `{{ path }}`.

### `__version__`

The veresion of markata used to build the site. ({{ __version__ }})

### date

A python datetime object. ({{date.today()}}) 

### Frontmatter

All variables from your post frontmatter like `title` ({{ title|e }}) and `tags` ({{
tags }}). If you are not familiar with frontmatter it's the content at the top
of a markdown file between `---`.  Markata uses the most common type of
frontmatter, `yaml`.

```md
---
# this is the frontmatter
date: 2022-09-29 13:26:33
title: Home Page

---

## the post

markdown gets written after the frontmatter

```

##  markata

The last variable exposed is an instance of `markata.Markata` called `markata`.
This allows you to reference all of your other posts in very interesting ways.
such as getting the latest post -> [{{ markata.map('title', sort='date', filter='published==True and date<=today')[0] }}](/{{ markata.map('slug', sort='date', filter='published==True and date<=today')[0] }})

You can also map over posts to get more.

## Last Three Posts

{% for post in markata.map('post', sort='date', filter='post.get("published", False)==True and date<=today')[:3] %}
*  [{{ post['title'] }}]({{ post['slug'] }}){% endfor %}

## Last Three Python posts

{% for post in markata.map('post', sort='date', filter='post.get("published", False)==True and date<=today and "meta" in post.get("tags", [])')[:3] %}
*  [{{ post['title'] }}]({{ post['slug'] }}){% endfor %}
