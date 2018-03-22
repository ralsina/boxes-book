# BOXES v8

In the [previous lesson](./lesson7.run.md) we started using our layout engine to display text, and ran into some limitations. Let's get rid of them.

We have no changes in our Box class, or the page setup, or how we load and adjust the boxes' sizes. Also unchanged is the drawing code.

```python
from fonts import adjust_widths_by_letter

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
    dwg = svgwrite.Drawing(name, profile='full', size=(32, 57))
    for page in pages:
        dwg.add(dwg.rect(insert=(page.x, page.y), 
                size=(page.w, page.h), fill='yellow'))
    for box in boxes:
        color = 'green' if box.stretchy else 'red'
        if not hide_boxes:
            dwg.add(dwg.rect(insert=(box.x, box.y), size=(box.w, box.h), fill=color))
        if box.letter:
            dwg.add(dwg.text(box.letter, insert=(box.x, box.y + box.h), font_size=box.h, font_family='Arial'))
    dwg.save()
```

But we need to work on our layout engine, a lot. Here is the image of our attempt at displaying "Pride and Prejudice":

<img src="lesson7_pride_and_prejudice.svg" width="100%" style='border: 1px solid green; overflow: auto;'>

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

<img src="lesson8_handle_newlines.svg" width="100%" style='border: 1px solid green; overflow: auto;'>


## Spaces against the right margin



## Spaces against the left margin

And we will keep hyphenation for the next lesson.
