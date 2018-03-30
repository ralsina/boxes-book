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
names.

```python
# boxes.py
"""
Usage:
    boxes <input> <output>
    boxes --version
"""

from fonts import adjust_widths_by_letter
from hyphen import insert_soft_hyphens

import svgwrite
from docopt import docopt


class Box():

    def __init__(self, x=0, y=0, w=1, h=1, stretchy=False, letter='x'):
        """Accept arguments to define our box, and store them."""
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.stretchy = stretchy
        self.letter = letter

    def __repr__(self):
        return 'Box(%s, %s, %s, %s, "%s")' % (
            self.x, self.y, self.w, self.y, self.letter
        )


def hyphenbox():
    b = Box(letter='-')
    adjust_widths_by_letter([b])
    return b


def badness(page_width, row):
    """Calculate how 'bad' a position to break is.
    
    bigger is worse.
    """
    # Yes, this is suboptimal. It's easier to optimize working code
    # than fixing fast code.
    row_width = (row[-1].x + row[-1].w) - row[0].x
    slack = page_width - row_width
    stretchies = [b for b in row if b.stretchy]
    if len(stretchies) > 0:
        stretchies_width = sum(s.w for s in stretchies)
        # More stetchy space is good. More slack is bad.
        badness = slack / stretchies_width
    else:  # Nothing to stretch. Not good.
        badness = 1000
    if slack < 0:
        # Arbitrary fudge factor, negative slack is THIS much worse
        badness *= 2
    return badness


# We add a "separation" constant so you can see the boxes individually
separation = .05


def layout(_boxes, pages):
    """Layout boxes along pages.

    Keep in mind that this function modifies the boxes themselves, so
    you should be very careful about trying to call layout() more than once
    on the same boxes.

    Specifically, some spaces will become 0-width and not stretchy.
    """

    # Because we modify the box list, we will work on a copy
    boxes = _boxes[:]
    # We start at page 0
    page = 0
    # The 1st box should be placed in the correct page
    previous = boxes.pop(0)
    previous.x = pages[page].x
    previous.y = pages[page].y
    row = []
    while boxes:
        # We take the new 1st box
        box = boxes.pop(0)
        # And put it next to the other
        box.x = previous.x + previous.w + separation
        # At the same vertical location
        box.y = previous.y

        # Handle breaking on newlines
        break_line = False
        # But if it's a newline
        if (box.letter == '\n'):
            break_line = True
            # Newlines take no horizontal space ever
            box.w = 0
            box.stretchy = False

        # Or if it's too far to the right, and is a
        # good place to break the line...
        elif (box.x + box.w) > (
            pages[page].x + pages[page].w
        ) and box.letter in (
            ' ', '\xad'
        ):
            if box.letter == '\xad':
                # Add a visible hyphen in the row
                h_b = hyphenbox()
                h_b.x = previous.x + previous.w + separation
                h_b.y = previous.y
                _boxes.append(h_b)  # So it's drawn
                row.append(h_b)  # So it's justified
            break_line = True
            # We adjust the row
            # Remove all right-margin spaces
            while row[-1].letter == ' ':
                row.pop()
            slack = (pages[page].x + pages[page].w) - (
                row[-1].x + row[-1].w
            )
            # Get a list of all the ones that are stretchy
            stretchies = [b for b in row if b.stretchy]
            if not stretchies:  # Nothing stretches do as before.
                bump = slack / len(row)
                # The 1st box gets 0 bumps, the 2nd gets 1 and so on
                for i, b in enumerate(row):
                    b.x += bump * i
            else:
                bump = slack / len(stretchies)
                # Each stretchy gets wider
                for b in stretchies:
                    b.w += bump
                # And we put each thing next to the previous one
                for j, b in enumerate(row[1:], 1):
                    b.x = row[j - 1].x + row[j - 1].w + separation


        if break_line:
            # We start a new row
            row = []
            # We go all the way left and a little down
            box.x = pages[page].x
            box.y = previous.y + previous.h + separation

        # But if we go too far down
        if box.y + box.h > pages[page].y + pages[page].h:
            # We go to the next page
            page += 1
            # And put the box at the top-left
            box.x = pages[page].x
            box.y = pages[page].y

        # Put the box in the row
        row.append(box)

        # Collapse all left-margin space
        if all(b.letter == ' ' for b in row):
            box.w = 0
            box.stretchy = False
            box.x = pages[page].x

        previous = box


def draw_boxes(boxes, pages, fname, size, hide_boxes=False):
    dwg = svgwrite.Drawing(fname, profile='full', size=size)
    # Draw the pages
    for page in pages:
        dwg.add(
            dwg.rect(
                insert=(page.x, page.y),
                size=(page.w, page.h),
                fill='lightblue',
            )
        )
    # Draw all the boxes
    for box in boxes:
        # The box color depends on its features
        color = 'green' if box.stretchy else 'red'
        # Make the colored boxes optional
        if not hide_boxes:
            dwg.add(
                dwg.rect(
                    insert=(box.x, box.y),
                    size=(box.w, box.h),
                    fill=color,
                )
            )
        # Display the letter in the box
        if box.letter:
            dwg.add(
                dwg.text(
                    box.letter,
                    insert=(box.x, box.y + box.h),
                    font_size=box.h,
                    font_family='Arial',
                )
            )
    dwg.save()


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


def convert(input, output):
    pages = create_pages()
    text_boxes = create_text_boxes(input)
    layout(text_boxes, pages)
    draw_boxes(text_boxes, pages, output, (90, 50), True)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Boxes 0')
    convert(input=arguments['<input>'], output=arguments['<output>'])

```

And if we run it like this:

```sh
$ python boxes.py pride-and-prejudice.txt lesson1.svg
```

![lesson1.svg](part2/lesson1.svg)