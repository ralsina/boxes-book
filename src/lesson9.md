# BOXES v8

In the [previous lesson](lesson7.run.html) we started using our layout engine to display text, and ran into some limitations. Let's get rid of them.

We have no changes in our Box class, or the page setup, or how we load and adjust the boxes' sizes. Also unchanged is the drawing code.

```python
from code.fonts import adjust_widths_by_letter

class Box():
    def __init__(self, x=0, y=0, w=1, h=1, stretchy=False, letter='x'):
        """We accept a few arguments to define our box, and we store them."""
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.stretchy = stretchy
        self.letter = letter

    def __repr__(self):
        """This is what is shown if we print a Box. We want it to be useful."""
        return 'Box(%s, %s, %s, %s, "%s")' % (self.x, self.y, self.w, self.y, self.letter)

# A few pages all the same size
pages = [Box(i * 35 + 1, 1, 30, 50) for i in range(10)]

separation = .05
p_and_p = open('pride-and-prejudice.txt').read()
text_boxes = []
for l in p_and_p:
    text_boxes.append(Box(letter=l, stretchy=l==' '))
adjust_widths_by_letter(text_boxes)
```
```python
import svgwrite

def draw_boxes(boxes, name='lesson8.svg', hide_boxes=False):
    dwg = svgwrite.Drawing(name, profile='full', size=(32, 52))
    for page in pages:
        dwg.add(dwg.rect(insert=(page.x, page.y), 
                size=(page.w, page.h), fill='lightyellow'))
    for box in boxes:
        color = 'green' if box.stretchy else 'red'
        if not hide_boxes:
            dwg.add(dwg.rect(insert=(box.x, box.y), size=(box.w, box.h), fill=color))
        if box.letter:
            dwg.add(dwg.text(box.letter, insert=(box.x, box.y + box.h), font_size=box.h, font_family='Arial'))
    dwg.save()
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

In this section we will do things slightly different than before, by doing incremental improvements of the layout function, so this is going to be pretty long but with small changes. 

Let's hit the issues in order.

## Newlines

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

        # The next 10 lines are almost all the change
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

layout(text_boxes)
draw_boxes(text_boxes, 'lesson8_handle_newlines.svg', hide_boxes=True)
```

As mentioned, the code changes are small, but the output now looks radically different.

![lesson8_handle_newlines.svg](lesson8_handle_newlines.svg)

## Spaces against the right and left margins

You can see clearly, in the previous sample output where this happens in one of the latter paragraphs, "to see the place,  " appears ragged when it should not. And a similar thing happens in an earlier paragraph where there is a hole against the left margin in " told me all about it".

In both cases, the cause is because the "empty" space is used by spaces!

So, one possible solution is, when justifying a row, to make all the spaces at the right margins 0-width and not stretchy. At the same time, when adding spaces at the beginning of a row, they should become 0-width and not stretchy.

**BUT** this means the list of boxes will need its width readjusted if they are to be layouted again on different pages! That's because some of the spaces will now be thin and "rigid" so they will work badly if they are **not** against the margin on a different layout.

It's not a big problem, but it's worth keeping in mind, since it's the kind of thing that becomes an obscure bug later on. So, we add it to the docstring.

```python
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

        # The next 10 lines are almost all the change
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
draw_boxes(text_boxes, 'lesson8_handle_spaces.svg', hide_boxes=True)
```

![lesson8_handle_spaces.svg](lesson8_handle_spaces.svg)

As you can see, the justification now is absolutely tight where it needs to be.
With that taken care of, we will keep hyphenation for the next lesson.
