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
    dwg = svgwrite.Drawing(name, profile='full', size=(32, 20))
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
