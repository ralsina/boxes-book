# BOXES v7

So far in our previous lessons we have worked in an abstract world of boxes.
Some hints of a direction were visible, like organizing our boxes in *pages* and trying to achieve a *justified layout* among others.

So, let's just say it, we are going to be doing text layout. But not the easy one. No, sir. No monospaced fonts for us. We want to do the whole enchilada, we are going to have variable-width fonts with kerning, and multi-page, fully-justified text layouts **with hyphenation**.

Ok, perhaps about 50% of the enchilada, because no bidirectional support, only in english, only UTF-8 encoded files, and so on a lot of things. But it's still a lot of mexican food!

And we are going to do that in lessons not much longer than the ones you have been seeing so far. So let's get started.

Clearly, we want our boxes to have letters. And our "stretchy" boxes are special because they have things like spaces. In fact, let's just say they have spaces.

We will now expand our Box class to support letters inside the boxes.

```python
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

# Many boxes, all the same width, with an x in them
text_boxes = [Box() for i in range(5000)]
```

We can actually use the exact same layout function.

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

layout(text_boxes)
```

And tweak the drawing function to show us letters, and to make the colored boxes optional.

```python
import svgwrite

def draw_boxes(boxes, name='lesson7.svg', hide_boxes=False):
    dwg = svgwrite.Drawing(name, profile='full', size=(32, 20))
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

draw_boxes(text_boxes)
```

<img src="lesson7.svg" width="100%" style='border: 1px solid green; overflow: auto;'>

Of course this is very boring, so we need to spice up our data a little.
We can use different letters, and then make the right ones stretchy. That is easy!

```python
from random import choice
for box in text_boxes:
    # More than one space so they appear often
    box.letter = choice('     abcdefghijklmnopqrstuvwxyz')
    if box.letter == ' ':  # Spaces are stretchy
        box.stretchy = True

layout(text_boxes)
draw_boxes(text_boxes, 'lesson7_different_letters.svg')
```

<img src="lesson7_different_letters.svg" width="100%" style='border: 1px solid green; overflow: auto;'>

As you can see, there are very minor horizontal shifts and stretches, since all boxes are the same size.

But as a text layout engine we have a **major** failure: we are ignoring the size of the letters we are layouting!

This is a very complex thing to do called *text shaping*. You need to understand the content of the font you are using to display the text, and more subtle things like what happens if you put specific letters next to each other (kerning) and much more.

The good news is that it's already done for us, in libraries called Harfbuzz and Freetype.

This paragraph is perhaps the most important one in this book. I am about to show you some obscure code. And I will tell you the secret of how it got here:
**I copied it from the documentation for the libraries I am using.** Sometimes you will need to do something complicated only once in your life. It's perfectly ok to just google how to do it. And as long as you are confident you can find it again if needed, it's ok to just forget about it.

I will show you this code, and then put it in a separate file called `fonts.py` and from now on I will not show it in the lessons, because we are *not* going to change it, *ever*.


```python
import harfbuzz as hb
import freetype2 as ft

def adjust_widths_by_letter(boxes):
    """Takes a list of boxes as arguments, and uses harfbuzz to
    adjust the width of each box to match the harfbuzz text shaping."""
    buf = hb.Buffer.create()
    buf.add_str(''.join(b.letter for b in boxes))
    buf.guess_segment_properties()
    font_lib =  ft.get_default_lib()
    face = font_lib.find_face('Arial')
    face.set_char_size(size = 1, resolution=64)
    font = hb.Font.ft_create(face)
    hb.shape(font, buf)
    # at this point buf.glyph_positions has all the data we need
    for box, position in zip(boxes, buf.glyph_positions):
        box.w = position.x_advance
```

And now we will pretend we know what that does, based on its docstring and use it.

```python
separation = .05
adjust_widths_by_letter(text_boxes)
layout(text_boxes)
draw_boxes(text_boxes, 'lesson7_adjusted_letters.svg')
```

<img src="lesson7_adjusted_letters.svg" width="100%" style='border: 1px solid green; overflow: auto;'>

And nicer, without the boxes:

```python
separation = .05
adjust_widths_by_letter(text_boxes)
layout(text_boxes)
draw_boxes(text_boxes, 'lesson7_adjusted_letters_no_boxes.svg', hide_boxes=True)
```

<img src="lesson7_adjusted_letters_no_boxes.svg" width="100%" style='border: 1px solid green; overflow: auto;'>

And of course, we can just load text there instead of random letters. For example, here we load what is going to be our example test from now on, 
Jane Austen's [Pride and Prejudice from Project Gutenberg](http://www.gutenberg.org/ebooks/1342)

```python
separation = .05
p_and_p = open('pride-and-prejudice.txt').read()
text_boxes = []
for l in p_and_p:
    text_boxes.append(Box(letter=l, stretchy=l==' '))
adjust_widths_by_letter(text_boxes)
layout(text_boxes)
draw_boxes(text_boxes, 'lesson7_pride_and_prejudice.svg', hide_boxes=True)
```

<img src="lesson7_pride_and_prejudice.svg" width="100%" style='border: 1px solid green; overflow: auto;'>

And that is ... maybe disappointing? While we spent a lot of time on things like justifying text, we have not even looked at newlines!

Also, spaces at the end of lines make the line appear ragged again, now that they are not boxes.

So, we know what to hit in the next lesson.