# BOXES v8

In the [previous lesson](lesson7.run.html) we started using our layout engine to display text, and ran into some limitations. Let's get rid of them.

We have no changes in our Box class, or the page setup, or how we load and adjust the boxes' sizes. 

```python
# lesson8.py
from code.fonts import adjust_widths_by_letter


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


p_and_p = open('pride-and-prejudice.txt').read()
text_boxes = []
for l in p_and_p:
    text_boxes.append(Box(letter=l, stretchy=l == ' '))
adjust_widths_by_letter(text_boxes)

# A few pages all the same size
pages = [Box(i * 35, 0, 30, 50) for i in range(10)]

```

Also unchanged is the drawing code.

```python
# lesson8.py

import svgwrite


def draw_boxes(boxes, fname, size, hide_boxes=False):
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

```

But we need to work on our layout engine, a lot. Here is the image of our attempt at displaying "Pride and Prejudice":

![lesson7_pride_and_prejudice.svg](lesson7_pride_and_prejudice.svg)

Let's count the problems:

1. It totally ignores newlines everywhere
2. It keeps spaces at the end of rows, making the right side ragged 
   (see "said his " in the seventh line)
3. White space at the beginning of rows is shown and it looks bad 
   (see " a neigh" at the beginning of the fifth line)
4. Words are split between lines haphazardly, but this is for later and leads
   to some serious code that needs its own lesson.

Let's hit the issues in order. First, newlines.

The idea is: if we find a newline, we need to break the line. Doesn't sound
particularly complex, specially since lines that are broken intentionally
are never fully justified.

The changes are minor:

* Create a flag `break_line` set to True if we encounter a newline 
  or overflow the page.
* In case of newline, make that box invisible by making it 0-wide and 
  not stretchy.
* When the break_line flag is set, handle as usual by moving to the 
  left, etc.


```python
# lesson8.py
# We add a "separation" constant so you can see the boxes individually
separation = .05


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

        # Handle breaking on newlines
        break_line = False
        # But if it's a newline
        if (box.letter == '\n'):
            break_line = True
            # Newlines take no horizontal space ever
            box.w = 0
            box.stretchy = False

        # Or if it's too far to the right...
        elif (box.x + box.w) > (pages[page].x + pages[page].w):
            break_line = True
            # We adjust the row
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
        previous = box



```

The code changes are small, but the output now looks radically different.

```python
# lesson8.py
draw_boxes(text_boxes, 'lesson8.svg', (32, 52), hide_boxes=True)

```

![lesson8.svg](lesson8.svg)

----------

Further references:

* Full source code for this lesson [lesson8.py](code/lesson8.py)
* [Difference with code from last lesson](diffs/lesson7_lesson8.html)