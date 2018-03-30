# BOXES v10

In our [previous lesson](lesson9.run.html) we created a serviceable text
layout engine. It has many problems, but remember our goal is not to create
the best possible thing, this is an educational experience. The spit and
polish will appear later on.

But there is a glaring problem, it breaks words in all the wrong places.
Examples of it appear in almost every line of the output. So, how does one fix
that?

The traditional answer (and the one we will be using) is hyphenation, breaking
words between lines in the correct places.

Instead of breaking anywhere, we will break only in the places where the [rules of each language](https://english.stackexchange.com/questions/385/what-are-the-rules-for-splitting-words-at-the-end-of-a-line)
allow us to.

Just as it happened with [text shaping](lesson7.run.html) we are lucky to live
in a moment in time when almost everything we need to do it right is already
in place. In particular, we will use a library called [Pyphen](https://github.com/Kozea/Pyphen)
mostly because I already have used it in another project.

Am I sure it's the best one? No. Do I know exactly how it does what it does?
No. I know enough to make it work, and it works *well enough* so for this
stage in the life of this project that is more than enough. In fact, it takes
the rules for word-breaking from dictionaries provided by an Office Suite, so
it does about as good a job as the dictionary does. It even supports
subtleties such as the differences between British and American English!

Here's an example of how it works:

```python
import pyphen
dic = pyphen.Pyphen(lang='en_GB')
print('en_GB:', dic.inserted('dictionary', '-'))
dic = pyphen.Pyphen(lang='en_US')
print('en_US:', dic.inserted('dictionary', '-'))
```

```
en_GB: dic-tion-ary
en_US: dic-tio-nary
```

Keep in mind that this is not magic. If you feed it garbage, it will give you
garbage.

```python
dic = pyphen.Pyphen(lang='es_ES')
print('es_ES:', dic.inserted('dictionary', '-'))
```

```
es_ES: dic-tio-na-ry
```

Where is it proper to break a line?

* On a newline character
* On a space
* On a breaking point as defined by Pyphen

One of those things is not like the others. We have boxes with newlines in
them and we have boxes with spaces in them, but there are no boxes with
breaking points in them.

But we can add them! There is Unicode symbol for that:

> ### SOFT HYPHEN (SHY)
>
> The [soft hyphen](https://en.wikipedia.org/wiki/Soft_hyphen) serves as an
> invisible marker used to specify a place in text where a hyphenated break
> is allowed without forcing a line break in an inconvenient place if the
> text is re-flowed. It becomes visible only after word wrapping at the end
> of a line.

So, if we insert them in all the right places, then we can use them to decide
whether we are at a suitable breaking point. We will put this in a file called
`hyphen.py`

```python
# hyphen.py
import pyphen

dic = pyphen.Pyphen(lang='en_US')


def insert_soft_hyphens(text, hyphen='\xad'):
    """Insert the hyphen in breaking pointsaccording to the dictionary.
    
    '\xad' is the Soft Hyphen (SHY) character
    """
    lines = []
    for line in text.splitlines():
        hyph_words = [
            dic.inserted(word, hyphen) for word in line.split()
        ]
        lines.append(' '.join(hyph_words))
    return '\n'.join(lines)

```

```python
from code.hyphen import insert_soft_hyphens

print (insert_soft_hyphens('Roses are red\nViolets are blue', '-'))
```


```
Ros-es are red
Vi-o-lets are blue
```

So, with this code ready, we can get to work on implementing hyphenation
support in our layout function.

First, this code is exactly as it was before:

```python
# lesson10.py
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

```

We do need to make a small change to how we load our text, to add the hyphens:

```python
# lesson10.py
p_and_p = open('pride-and-prejudice.txt').read()
p_and_p = insert_soft_hyphens(p_and_p)  # Insert invisible hyphens
text_boxes = []
for l in p_and_p:
    text_boxes.append(Box(letter=l, stretchy=l == ' '))
adjust_widths_by_letter(text_boxes)

# A few pages all the same size
pages = [Box(i * 35, 0, 30, 50) for i in range(10)]

```

No changes in how we draw things.

```python
# lesson10.py
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

And now our layout function. One first approach, which we will refine later,
is to simply refuse to break lines if we are not in a "good" place to break it.

Then, we inject a box with a visible hyphen in the line break, and that's it.

Here is the code to create a box with a hyphen:

```python
# lesson10.py
def hyphenbox():
    b = Box(letter='-')
    adjust_widths_by_letter([b])
    return b

```

And here finally, our layout supports hyphens:

```python
# lesson10.py
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
# lesson10.py
draw_boxes(text_boxes, 'lesson10.svg', (30, 50), hide_boxes=True)

```

![lesson10.svg](part1/lesson10.svg)

And there in "proper-ty" you can see it in action. Of course this is
a naïve implementation. What happens if you just can't break?

```python
many_boxes = [Box(letter='a') for i in range(200)]
adjust_widths_by_letter(many_boxes)
layout(many_boxes)
draw_boxes(many_boxes, 'lesson10_lots_of_a.svg', (35, 6), hide_boxes=True)
```

![lesson10_lots_of_a.svg](part1/lesson10_lots_of_a.svg)

Since it can't break at all, it just goes on and on.

And there are other corner cases!

```python
many_boxes = [Box(letter='a') for i in range(200)]
many_boxes[100] = Box(letter=' ', stretchy=True)
adjust_widths_by_letter(many_boxes)
layout(many_boxes)
draw_boxes(many_boxes, 'lesson10_one_break.svg', (35, 6), hide_boxes=True)
```

![lesson10_one_break.svg](part1/lesson10_one_break.svg)

Because there is only one place to break the line, it then tries to
wedge 100 letter "a" where there is room for 54 (I counted!) and something interesting happens... the "slack" is negative!

Instead of stretching out a "underfilled" line, we are squeezing a "overfilled" one. Everything gets packed too tight, and the letters start
overlapping one another.

The lesson is that just because it works for the usual case it doesn't mean
it's **done**. Even in the case of words, it can happen that breaking points take a while to appear and our line becomes overfull.

We will tackle that problem next.

----------

Further references:

* Full source code for this lesson [lesson10.py](lesson10.py.run.html)
* [Difference with code from last lesson](part1/code/diffs/lesson9_lesson10.html)
