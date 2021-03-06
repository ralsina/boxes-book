# BOXES v0.12

What we have right now is not a real program, it's just a fun script. In order
to turn it into a real program we need to figure out what we **want** it to
be. Then we will take our wish and make it happen. Easy, right?

We have the following things:

* Code to generate text "boxes" representing a given text file.
* Code to generate a series of pages.
* Code to lay the text boxes in the pages.
* Code to draw text boxes and pages in a SVG.

How can we combine those assets into a working, functional piece of software?

Because I am *old* my first idea is to create a command line tool. We can
explore others later, but this one is easy. It takes the name of a text file
as first argument, and the name of a SVG file as second argument and it
creates the second with the contents of the first.

My favorite to do this is using [docopt](https://github.com/docopt/docopt),
where we will describe how the tool works and it turns the documentation into
actual working code. It's serious overkill for what we want now, but we may
grow into it.

We will start with an empty file and then add all the bits of code we have
until it works.

Here's a first draft:

```python
"""
Usage:
    boxes <input> <output>
    boxes --version
"""

from docopt import docopt


# __name__ is the name of the current module. If it's called as a
# script, it will be '__main__'
if __name__ == '__main__':
    # If we are called as a script, call docopt.
    # __doc__ is that big string at the beginning of the file.
    arguments = docopt(__doc__, version='Boxes 0.12')
    # Print whatever docopt gives us
    print(arguments)
```

And here is how that works. If we call it with two arguments, we get the
information in `arguments`:

```sh
$ python boxes.py foo bar

{'--version': False,
 '<input>': 'foo',
 '<output>': 'bar'}
```

If we were missing one, then we are using it wrong, and it will complain and
print the help.

```sh
$ python boxes.py foo

Usage:
    boxes <input> <output>
    boxes --version
```

And if we pass `--version`?

```sh
$ python boxes.py foo

Boxes 0.12
```

So, we have a dictionary with input and output as keys. That is handy. All we
need to do is slap our existing code in this script and make it use those
names. Because I don't want to show you a wall of code, I am going to just
highlight some snippets. You can see the whole change in [our diff page](code/diffs/lesson1_diff.html)

Some of that code needs to be moved into proper functions:

```python
# boxes.py
def create_text_boxes(input_file):
    p_and_p = open(input_file).read()
    p_and_p = insert_soft_hyphens(p_and_p)  # Insert invisible hyphens
    text_boxes = []
    for l in p_and_p:
        text_boxes.append(Box(letter=l, stretchy=l == ' '))
    adjust_widths_by_letter(text_boxes)
    return text_boxes


def create_pages():
    # A few pages all the same size
    pages = [Box(i * 35, 0, 30, 50) for i in range(10)]
    return pages

```

We need to have pages be an argument to some functions instead of being a
global variable:

```python
# boxes.py
def layout(_boxes, pages):

```

```python
# boxes.py
def draw_boxes(boxes, pages, fname, size, hide_boxes=False):

```

And of course, we need to write a new function that calls everything in the
right order with the right arguments:

```python
# boxes.py
def convert(input, output):
    pages = create_pages()
    text_boxes = create_text_boxes(input)
    layout(text_boxes, pages)
    draw_boxes(text_boxes, pages, output, (100, 50), True)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Boxes 0.12')
    convert(input=arguments['<input>'], output=arguments['<output>'])

```

And if we run it like this:

```sh
$ python boxes.py pride-and-prejudice.txt lesson1.svg
```

It will give us this output:

![lesson1.svg](lesson1.svg)

----------

Further references:

* Full source code for this lesson [boxes.py](code/lesson1/boxes.py)
* [Difference with code from last lesson](code/diffs/lesson1_diff.html)
