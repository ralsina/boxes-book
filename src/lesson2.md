# BOXES v2

In our [previous lesson](lesson1.run.html) we created a rather disappointing 
drawing using boxes. Let's introduce a new wrinkle, and **layout** the many
boxes.

This code is just like before:

```python
class Box():
    def __init__(self, x=0, y=0, w=1, h=1):
        """We accept a few arguments to define our box, and we store them."""
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __repr__(self):
        """This is what is shown if we print a Box. We want it to be useful."""
        return 'Box(%s, %s, %s, %s)' % (self.x, self.y, self.w, self.y)

many_boxes = [Box() for i in range(5000)]
```

But now, so they are not all stuck one on top of the other, let's lay the boxes down in a line, one next to the other.

```python
# We add a "separation" constant so you can see the boxes individually
separation = .2

def layout(boxes):
    for i, box in enumerate(boxes):
        box.x = i * (1 + separation)

layout(many_boxes)
```

And we can now see that they all have different coordinates now by printing 
a few of them. And yes, some of those numbers do look funny. Floating point
numbers are weird.

```python
print([(box.x, box.y) for box in many_boxes[:10]])
```

```
Output goes here
```

Let's draw them!

```python
import svgwrite

def draw_boxes(boxes):
    dwg = svgwrite.Drawing('lesson2.svg', profile='full', size=(100, 5))
    for box in boxes:
        dwg.add(dwg.rect(insert=(box.x, box.y), size=(box.w, box.h), fill='red'))
    dwg.save()

draw_boxes(many_boxes)
```
And here is the output:

![lesson2.svg](lesson2.svg)

That was more or less what we expected, right? Of course since there are 5000 small
boxes that row of boxes goes on for quite a while.

We *could* just go to the right for a while, then start a new row. Let's do that in
the next lesson.