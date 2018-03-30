# BOXES v0.6

In our [previous lesson](lesson5.run.html) we created a fully justified layout of varying-width boxes spread across multiple pages. But we cheated.

To achieve full justification, we spread the "slack" evenly in the space between all boxes in the row. If we were trying to layout text, that is not the proper way.

You see, text comes separated in words. And usually, in western languages, the words have characters called spaces between them. So what we do, when laying out text, is to make the special **space** boxes slightly larger and keep the separation between boxes constant (in fact, we also tweak separations between letters, but let's ignore that for now. Or for ever.

How about we choose some boxes and decide they, and only they, are stretchy?

That way, our strategy to fully justify the text will be: stretch the stretchy bits on each row just enough so that the row is exactly the width we need.

For the first time in a few lessons, we need to change our Box class:

```python
# lesson6.py
class Box():

    def __init__(self, x=0, y=0, w=1, h=1, stretchy=False):
        """Accept arguments to define our box, and store them."""
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.stretchy = stretchy

    def __repr__(self):
        return 'Box(%s, %s, %s, %s)' % (self.x, self.y, self.w, self.y)


# Many boxes with varying widths, and about 1 in 10 will be stretchy
from random import randint

many_boxes = [
    Box(w=1 + randint(-5, 5) / 10, stretchy=(randint(0, 5) == 4))
    for i in range(5000)
]
# A few pages all the same size
pages = [Box(i * 35, 0, 30, 50) for i in range(10)]

```

The changes in the layout function are not so big.

```python
# lesson6.py
# We add a "separation" constant so you can see the boxes individually
separation = .2


def layout(_boxes):
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
        # But if it's too far to the right...
        if (box.x + box.w) > (pages[page].x + pages[page].w):
            # We adjust the row
            slack = (pages[page].x + pages[page].w) - (
                row[-1].x + row[-1].w
            )

```

When finishing a row, see if it has stretchy boxes in it.

If it doesn't, bump each box a little to the right like we did before.

```python
# lesson6.py
            # Get a list of all the ones that are stretchy
            stretchies = [b for b in row if b.stretchy]
            if not stretchies:  # Nothing stretches do as before.
                bump = slack / len(row)
                # The 1st box gets 0 bumps, the 2nd gets 1 and so on
                for i, b in enumerate(row):
                    b.x += bump * i

```

If we do have stretchy boxes in the row, make each one wider.


```python
# lesson6.py
            else:
                bump = slack / len(stretchies)
                # Each stretchy gets wider
                for b in stretchies:
                    b.w += bump
                # And we put each thing next to the previous one
                for j, b in enumerate(row[1:], 1):
                    b.x = row[j - 1].x + row[j - 1].w + separation

```

And continue like we did before.

```python
# lesson6.py
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
        previous = box


layout(many_boxes)

```

The drawing code needs a change so we can see the "stretchy" boxes in a different color.

```python
# lesson6.py
import svgwrite


def draw_boxes(boxes, fname, size):
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
        dwg.add(
            dwg.rect(
                insert=(box.x, box.y), size=(box.w, box.h), fill=color
            )
        )
    dwg.save()


draw_boxes(many_boxes, 'lesson6.svg', (100, 50))

```

![lesson6.svg](part1/lesson6.svg)

This layout strategy works:

* With multiple pages of arbitrary sizes and positions
* With many boxes of different widths and stretch capabilities
* Even if nothing can stretch

But the next lesson will start taking things to the next level.

----------

Further references:

* Full source code for this lesson [lesson6.py](lesson6.py.run.html)
* [Difference with code from last lesson](part1/code/diffs/lesson5_lesson6.html)
