# BOXES v11

In our [previous lesson](lesson10.run.html) we promised we will improve the
problem of overfull lines in our text layout engine.

The problem: A long string of letters without any hyphenation points or spaces
causes a very long row to be fitted into a smaller page, causing letters to
overlap. Or, if we are unable to break at all, we just spill to the right
forever.

  > ### Underfull and Overfull
  >
  > When a line has too few characters, slack is
  > positive and we have to "spread" them, that is called **underfull**. The
  > opposite, where a line has too many characters, slack is negative and we
  > have to "smush" them, is called **overfull**.

![lesson10_one_break.svg](part1/lesson10_one_break.svg)

As you probably expected... no changes in the Box class.

```python
# lesson11.py
from code.fonts import adjust_widths_by_letter
from code.hyphen import insert_soft_hyphens


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


# Three runs of "a" with spaces between them.
# The ideal breaking point is the second space.
text_boxes = [Box(letter='a') for a in range(72)]
for i in (20, 50):
    text_boxes[i].letter = ' '
    text_boxes[i].stretchy = True
adjust_widths_by_letter(text_boxes)


# A few pages all the same size
pages = [Box(i * 35, 0, 30, 50) for i in range(10)]


def hyphenbox():
    b = Box(letter='-')
    adjust_widths_by_letter([b])
    return b



```

Also no changes in how we draw things.

```python
# lesson11.py
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

So far, our algorithm to break lines is simple:

1. If the next character is a newline: break
2. If we are short, add to the line.
3. If the next character makes the line overfull:
   a. If it's a space or a hyphen: break
   b. If not, add to the line
4. If we broke the line, adjust positions and widths so the line is
   exactly as wide as the page by spreading the slack.

We need a better way to decide what is the best possible breaking point for
the line. If it's too overfull, it will look bad. If it's too underfull, it
will look bad too. And sometimes there is just no good breaking point and we
need to *do something*.

If we were lucky enough to have a breaking point that exactly fills the line,
then we would not have a problem, so usually this will come down to choosing
between two breaking points. One makes the line overfull, one keeps it
underfull.

How good is a breaking point?

* If the slack is smaller, it's better.
* If it's underfull it's slightly better than overfull, since it's better to
  have a spread out line than overlapping letters.
* If we have many spaces, then a bigger slack is acceptable.

This is all subjective, of course. How much *movement* we tolerate on the text
is a judgment call, so it involves some trial and error.

Let's start with some made up numbers, because we have to start somewhere.

* The allowed positive slack is 20% of the width of the spaces in the line.
* The allowed negative slack is 10% of the width of the spaces in the line.

And here's a plan to implement it:

* When adding characters, check if it's a possible breaking point.
* If it is, remember the "goodness" it has
* When reaching an overfull breaking point, check if it's better than the last
  one we saw.
* If the overfull breaking point is better, break.
* If the overfull breaking point is worse, use the underfull breaking point.

The first new thing is a function to calculate how good a breaking point is,
in those terms.

```python
# lesson11.py
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

```

```python
# 10 boxes of width 1, 1 stretchy in the middle
boxes = [Box(x=i, w=1) for i in range(10)]
boxes[5].stretchy = True

# On a page that is 8 units wide:
print(badness(8, boxes))
```

```
-4.0
```

Let's see how that works for page widths between 5 and 15 (remember our row is
10 units wide):

```python
for w in range(5,15):
  print('page_width:', w, ' -> badness:', badness(w, boxes))
```

As you can see, if the page was 10 units wide, it would be optimal. The second
best option is for the page to be slightly wider, then maybe slightly thinner
and so on.

```
page_width: 5  -> badness: -10.0
page_width: 6  -> badness: -8.0
page_width: 7  -> badness: -6.0
page_width: 8  -> badness: -4.0
page_width: 9  -> badness: -2.0
page_width: 10  -> badness: 0.0
page_width: 11  -> badness: 1.0
page_width: 12  -> badness: 2.0
page_width: 13  -> badness: 3.0
page_width: 14  -> badness: 4.0
```

We will need to load data that shows the problem. In this case, it's a row of
20 letters 'a' (without hyphens), a space, then 20, and then 30 more 'a's.

Why?

Like before, the page is about wide enough to fix 58 "a"s. That means the first
run will not be enough to fill the line. The second run will still not be
enough. The third run will, however, badly overfill it. So, we should go all
the way to the end, see that it's too long, and then go back to the second
space and break there.

```python
# lesson11.py
# Three runs of "a" with spaces between them.
# The ideal breaking point is the second space.
text_boxes = [Box(letter='a') for a in range(72)]
for i in (20, 50):
    text_boxes[i].letter = ' '
    text_boxes[i].stretchy = True
adjust_widths_by_letter(text_boxes)


# A few pages all the same size
pages = [Box(i * 35, 0, 30, 50) for i in range(10)]

```

And now we have a problem. The change to our code needed to implement that is
too large. It's so large that it amounts to a rewrite of our layout function
and if we rewrite it, how would we be sure that we are not breaking all the
things we achieved previously?

It turns out this is as far as just sitting down and writing code will take
us. We need to get more serious, and transform this small pile of fragile code
into something we can actually hack confidently and transform without fear of
destroying it.

Therefore, we leave `layout` intact, show the failing test and move on to
Part 2 of the book, where we will reorganize the code into a coherent
software package and then... we will try again.

```python
# lesson11.py
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


layout(text_boxes)

```

```python
# lesson11.py
draw_boxes(text_boxes, 'lesson11.svg', (33, 5), hide_boxes=True)

```

![lesson11.svg](part1/lesson11.svg)

----------

Further references:

* Full source code for this lesson [lesson11.py](lesson11.py.run.html)
* [Difference with code from last lesson](part1/code/diffs/lesson10_lesson11.html)
