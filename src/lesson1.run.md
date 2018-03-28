# BOXES v1

Welcome to Boxes v1. I want to be able to draw some boxes. By boxes I don't mean actual boxes,
but rather squares. I found a library called svgwrite that lets you do that pretty easily.

First let's create a data structure. A simple class called Box.

```python
# lesson1.py
class Box():

    def __init__(self, x=0, y=0, w=1, h=1):
        """Accept arguments to define our box, and store them."""
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __repr__(self):
        return 'Box(%s, %s, %s, %s)' % (self.x, self.y, self.w, self.y)

```

As you can see that is a pretty simple class. And we can create a big box.

```python
big_box = Box(0, 0, 80, 100)
```

Or many boxes using a [list comprehension](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)

```python
# lesson1.py
many_boxes = [Box() for i in range(5000)]

```

So now we have a big box, and 5000 smaller boxes, all alike.

```python
# Print the first 10 boxes
print(many_boxes[:10])
```

```
[Box(0, 0, 1, 0), Box(0, 0, 1, 0), Box(0, 0, 1, 0), Box(0, 0, 1, 0), Box(0, 0, 1, 0), Box(0, 0, 1, 0), Box(0, 0, 1, 0), Box(0, 0, 1, 0), Box(0, 0, 1, 0), Box(0, 0, 1, 0)]
```

And yes, we can draw those boxes.

```python
# lesson1.py
import svgwrite


def draw_boxes(boxes, fname, size):
    dwg = svgwrite.Drawing(fname, profile='full', size=size)
    # Draw all the boxes
    for box in boxes:
        dwg.add(
            dwg.rect(
                insert=(box.x, box.y), size=(box.w, box.h), fill='red'
            )
        )
    dwg.save()


draw_boxes(many_boxes, 'lesson1.svg', (5, 2))

```
And here is the output:

![lesson1.svg](lesson1.svg)

That ... was not very interesting. It's a single small red square!

Remember *all our boxes have the same size and position!*

So ... we should do something better. Or at least more interesting, in lesson 2.

----------

Further references:

* Full source code for this lesson: [lesson1.py](lesson1.py.run.html)
