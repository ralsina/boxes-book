# BOXES v4

In the [previous lesson](lesson3.run.html) we totally nailed drawing between the lines ... horizontally. Let's improve on that by being bidimensional.

This code is just like before:

```python
# lesson4.py
class Box():

    def __init__(self, x=0, y=0, w=1, h=1):
        """Accept arguments to define our box, and store them."""
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __repr__(self):
        return 'Box(%s, %s, %s, %s)' % (self.x, self.y, self.w, self.y)


many_boxes = [Box() for i in range(5000)]

```

But now, instead of a big box, let's have a list of, say, 10 pages (or large boxes), one below the other, slighty separated.

```python
# lesson4.py
pages = [Box(0, i * 55, 30, 50) for i in range(10)]

```

Of course our layout routine needs improvements to handle overflowing a
page vertically.

```python
# lesson4.py
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
    while boxes:
        # We take the new 1st box
        box = boxes.pop(0)
        # And put it next to the other
        box.x = previous.x + previous.w + separation
        # At the same vertical location
        box.y = previous.y
        # But if it's too far to the right...
        if (box.x + box.w) > (pages[page].x + pages[page].w):
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

        previous = box


layout(many_boxes)

```

We need to change our drawing code to draw more than one page.

```python
# lesson4.py
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
        dwg.add(
            dwg.rect(
                insert=(box.x, box.y), size=(box.w, box.h), fill='red'
            )
        )
    dwg.save()


draw_boxes(many_boxes, 'lesson4.svg', (100, 60))

```

And here is the output:

![lesson4.svg](lesson4.svg)

Would this work if the pages are arranged differently? Let's put the pages
side by side instead.

```python
# lesson4.py
pages = [Box(i * 35, 0, 30, 50) for i in range(10)]
layout(many_boxes)
draw_boxes(many_boxes, 'lesson4_side_by_side.svg', (100, 60))

```

![lesson4_side_by_side.svg](lesson4_side_by_side.svg)

And how about pages of different sizes?

```python
# lesson4.py
from random import randint

pages = [
    Box(i * 35, 0, 30 + randint(-3, 3), 50 + randint(-10, 10))
    for i in range(10)
]
layout(many_boxes)
draw_boxes(many_boxes, 'lesson4_random_sizes.svg', (100, 60))

```

![lesson4_random_sizes.svg](lesson4_random_sizes.svg)

So, we can fill pages and pages with little red squares now. Nice!

How about we make the squares not be all the same width?

```python
# lesson4.py
many_boxes = [Box(w=1 + randint(-5, 5) / 10) for i in range(5000)]
layout(many_boxes)
draw_boxes(many_boxes, 'lesson4_random_box_sizes.svg', (100, 60))

```

This adds "noise" to the width of the boxes, so they are now anything between 0.5 and 1.5 units wide.

![lesson4_random_box_sizes.svg](lesson4_random_box_sizes.svg)

That looks interesting...

----------

Further references:

* Full source code for this lesson [lesson4.py](code/lesson4.py)
* [Difference with code from last lesson](diffs/lesson3_lesson4.html)