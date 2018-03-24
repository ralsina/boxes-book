# BOXES v9

In the [previous lesson](lesson8.run.html) we fixed the handling of newlines
in our layout engine, and noticed a problem with spaces. Let's fix it!

We have no changes in our Box class, or the page setup, or how we load and adjust the boxes' sizes.

```python
# lesson9.py
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
# lesson9.py
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
    dwg.save()

```

The more obvious problems are:

* It keeps spaces at the end of rows, making the right side ragged.
* White space at the beginning of rows is shown and it looks bad

![lesson8.svg](lesson8.svg)

You can see clearly, in the previous sample output where this happens in one of the latter paragraphs, "to see the place,  " appears ragged when it should not. And a similar thing happens in an earlier paragraph where there is a hole against the left margin in " told me all about it".

In both cases, the cause is because the "empty" space is used by spaces!

So, one possible solution is, when justifying a row, to make all the spaces at the right margins 0-width and not stretchy. At the same time, when adding spaces at the beginning of a row, they should become 0-width and not stretchy.

**BUT** this means the list of boxes will need its width readjusted if they are to be layouted again on different pages! That's because some of the spaces will now be thin and "rigid" so they will work badly if they are **not** against the margin on a different layout.

It's not a big problem, but it's worth keeping in mind, since it's the kind of thing that becomes an obscure bug later on. So, we add it to the docstring.

```python
# lesson9.py
# We add a "separation" constant so you can see the boxes individually
separation = .05


def layout(_boxes):
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

        # Or if it's too far to the right...
        elif (box.x + box.w) > (pages[page].x + pages[page].w):
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


layout(text_boxes)

```

```python
# lesson9.py
draw_boxes(text_boxes, 'lesson9.svg', (30, 50), hide_boxes=True)

```

![lesson9.svg](lesson9.svg)

As you can see, the justification now is absolutely tight where it needs to be.
With that taken care of, we will keep hyphenation for the next lesson.

----------

Further references:

* Full source code for this lesson [lesson9.py](code/lesson9.py)
* [Difference with code from last lesson](diffs/lesson8_lesson9.html)