# BOXES v4

In the [previous lesson](lesson3.run.html) we totally nailed drawing between the lines ... horizontally. Let's improve on that by being bidimensional.

This code is just like before:

```python
class Box():
    def __init__(self, x=0, y=0, w=1, h=1):
        """We accept a few arguments to define our box, and we store them."""
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __repr__(self):
        """This is what is shown if we print a Box. We want it to be useful."""
        return 'Box(%s, %s, %s, %s)' % (self.x, self.y, self.w, self.y)

many_boxes = [Box() for i in range(5000)]
```

But now, instead of a big box, let's have a list of, say, 10 pages (or large boxes), one below the other, slighty separated.

```python
pages = [Box(0, i * 55, 30, 50) for i in range(10)]
```

Of course our layout routine needs improvements to handle overflowing a
page vertically.

```python
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
        if (box.x + box.w) > pages[page].x + pages[page].w:
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

And we need to change our drawing code to draw more than one page. Also, because we will run it more than once, I added an argument to choose
the name of the output file.

```python
import svgwrite

def draw_boxes(boxes, name='lesson4.svg'):
    dwg = svgwrite.Drawing(name, profile='full', size=(100, 100))
    for page in pages:
        dwg.add(dwg.rect(insert=(page.x, page.y), 
                size=(page.w, page.h), fill='yellow'))
    for box in boxes:
        dwg.add(dwg.rect(insert=(box.x, box.y), size=(box.w, box.h), fill='red'))
    dwg.save()

draw_boxes(many_boxes)
```

And here is the output:

<img src="lesson4.svg" width="100%" style='border: 1px solid green; overflow: auto;'>

Would this work if the pages are arranged differently? Let's put the pages
side by side instead.

```python
pages = [Box(i * 35, 0, 30, 50) for i in range(10)]
layout(many_boxes)
draw_boxes(many_boxes, 'lesson4_side_by_side.svg')
```

<img src="lesson4_side_by_side.svg" width="100%" style='border: 1px solid green; overflow: auto;'>

And how about pages of different sizes?

```python
from random import randint
pages = [Box(i * 35, 0, 30 + randint(-3,3), 50 + randint(-10, 10)) for i in range(10)]
layout(many_boxes)
draw_boxes(many_boxes, 'lesson4_random_sizes.svg')
```

<img src="lesson4_random_sizes.svg" width="100%" style='border: 1px solid green; overflow: auto;'>

So, we can fill pages and pages with little red squares now. Nice!

How about we make the squares not be all the same width?

```python
many_boxes = [Box(w=1 + randint(-5,5)/10) for i in range(5000)]
layout(many_boxes)
draw_boxes(many_boxes, 'lesson4_random_box_sizes.svg')
```

This adds "noise" to the width of the boxes, so they are now anything between 0.5 and 1.5 units wide.

<img src="lesson4_random_box_sizes.svg" width="100%" style='border: 1px solid green; overflow: auto;'>

That looks interesting...