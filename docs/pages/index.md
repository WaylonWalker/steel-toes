---
date: 2022-09-01 1:00:00
title: Markata Blog Starter
published: True
tags:
  - home
  - meta

---

Welcome to the Markata starter blog, this is your home page to edit and make
your own.  Edit this page in `pages/index.md`.

## Some helpful pages

Here are some pages to help get you started. Feel free to delete them and and
make this site your own.

{% for post in markata.map('post', sort='date', filter='post.get("published", False)==True and date<=today and "meta" in post.get("tags", [])', reverse=False) %}
!!! note "[{{ post['title'] }}]({{ post['slug'] }})"
    {{post['description']}}...
{% endfor %}

