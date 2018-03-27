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


![lesson10_one_break.svg](lesson10_one_break.svg)

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

As you probably expected... no changes in the Box class,  or in how we load the data.

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


p_and_p = open('pride-and-prejudice.txt').read()
p_and_p = insert_soft_hyphens(p_and_p)  # Insert invisible hyphens
text_boxes = []
for l in p_and_p:
    text_boxes.append(Box(letter=l, stretchy=l == ' '))
adjust_widths_by_letter(text_boxes)

# A few pages all the same size
pages = [Box(i * 35, 0, 30, 50) for i in range(10)]


def hyphenbox():
    b = Box(letter='-')
    adjust_widths_by_letter([b])
    return b


# We add a "separation" constant so you can see the boxes individually
separation = .05

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


draw_boxes(text_boxes, 'lesson10.svg', (30, 50), hide_boxes=True)

```


----------

Further references:

* Full source code for this lesson [lesson11.py](code/lesson11.py)
* [Difference with code from last lesson](diffs/lesson10_lesson11.html)