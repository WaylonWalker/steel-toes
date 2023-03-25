---
date: 2022-09-05 1:00:00
title: Your Own Style
published: True
tags:
  - home
  - meta

---

Once you have the site up and running it's important to make it your own.  You
are free to keep the default style if you really like.  Markata is completely
customizable, you can specify some theme colors to your liking or complely
eject out of markata's built in template and completely use your own.


## Picking your own colors

The easiest way to make the site your own is to define custom colors in the
`markata.toml` configuration file.  There is more information about theming
this way in the [docs/colortheme](https://markata.dev/color-theme/)

```toml
[markata]
color_bg = '#1f2022'
color_bg_code = '#1f2022'
color_text = '#eefbfe'
color_link = '#47cbff' 
color_accent = '#e1bd00c9'
overlay_brightness = '.85'

color_bg_light = '#eefbfe'
color_bg_code_light = '#eefbfe'
color_text_light = '#1f2022'
color_link_light = '#47cbff' 
color_accent_light = '#ffeb00'
overlay_brightness_light = '.95'
```

## Adding your own css/overriding css - site wide

You can override the existing css to tweak how the site looks.  Again this is
done in the `markata.toml` configuration.  To add any sort of plain text
entries in the `<head>` of your site, you can specify a `[[markata.head.text]]`
block with an entry for `value` with the text you want to appear in the head.

``` toml
[[markata.head.text]]
value = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">

<style>html{font-family: 'Roboto', sans-serif;}</style>
"""
```

!!! danger
    You can end up with a blank page if you do not close any tags here.

## Using your own template

If you want complete customizability of both the style and structure of the
site, you can use your own template.  To get started copy the default template
from markata into your project.

``` bash
curl https://raw.githubusercontent.com/WaylonWalker/markata/main/markata/plugins/default_post_template.html > pages/templates/post_template.html
```

Then update your post_template in `markata.toml` to point to your template.

``` toml
[markata]
post_template = "pages/templates/post_template.html"
```

Now you can make structural changes to your template and see the results in your build.

## Changing your favicon

Your favicon should be kept in your `assets` directory, which is `./static` by
default.  You can name the icon what you want, `icon.png` is the default, but
you will have to change your icon config in your `markata.toml` to use a
different value.

``` toml
[markata]
assets_dir = "static"
icon = "icon.png"
```

