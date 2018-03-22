# BOXES v6

In our [previous lesson](lesson5.run.html) we created a fully justified layout of varying-width boxes spread across multiple pages. But we cheated.

To achieve full justification, we spread the "slack" evenly in the space between all boxes in the row. If we were trying to layout text, that is not the proper way.

You see, text comes separated in words. And usually, in western languages, the words have characters called spaces between them. So what we do, when laying out text, is to make the special **space** boxes slightly larger and keep the separation between boxes constant (in fact, we also tweak separations between letters, but let's ignore that for now. Or for ever.)

How about we choose some boxes and decide they, and only they, are stretchy?

That way, our strategy to fully justify the text will be: stretch the stretchy bits on each row just enough so that the row is exactly the width we need.

For the first time in a few lessons, we need to change our Box class:

```python
class Box():
    def __init__(self, x=0, y=0, w=1, h=1, stretchy=False):
        """We accept a few arguments to define our box, and we store them."""
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.stretchy = stretchy

    def __repr__(self):
        """This is what is shown if we print a Box. We want it to be useful."""
        return 'Box(%s, %s, %s, %s)' % (self.x, self.y, self.w, self.y)

# Many boxes with varying widths, and about 1 in 10 will be stretchy
from random import randint
many_boxes = [Box(w=1 + randint(-5,5)/10, stretchy=(randint(0,5) == 4)) 
    for i in range(5000)]
# A few pages all the same size
pages = [Box(i * 35, 5, 30, 50) for i in range(10)]
```

The changes in the layout function are not so big.

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
            slack = (pages[page].x + pages[page].w) - (row[-1].x + row[-1].w)
            stretchies = [b for b in row if b.stretchy]
            if stretchies:
                bump = slack / len(stretchies)
                # Each stretchy gets wider
                for b in stretchies:
                    b.w += bump
                # And we put each thing next to the previous one
                for j, b in enumerate(row[1:], 1):
                    b.x = row[j-1].x + row[j-1].w + separation

            else:  # Nothing stretches!!! Do it like before.
                bump = slack / len(row)
                for i, b in enumerate(row):
                    b.x += bump * i

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
import svgwrite

def draw_boxes(boxes, name='lesson6.svg'):
    dwg = svgwrite.Drawing(name, profile='full', size=(100, 60))
    for page in pages:
        dwg.add(dwg.rect(insert=(page.x, page.y), 
                size=(page.w, page.h), fill='yellow'))
    for box in boxes:
        color = 'green' if box.stretchy else 'red'
        dwg.add(dwg.rect(insert=(box.x, box.y), size=(box.w, box.h), fill=color))
    dwg.save()

draw_boxes(many_boxes)
```

<img src="lesson6.svg" width="100%" style='border: 1px solid green; overflow: auto;'>

This layout strategy works:

* With multiple pages of arbitrary sizes and positions
* With many boxes of different widths and stretch capabilities
* Even if nothing can stretch

But the next lesson will start taking things to the next level.
