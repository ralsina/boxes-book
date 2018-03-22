# BOXES v1


Welcome to Boxes v1. I want to be able to draw some boxes. By boxes I don't mean actual boxes,
but rather squares. I found a library called svgwrite that lets you do that pretty easily.

First let's create a data structure. A simple class called Box.

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
```

As you can see that is a pretty simple class. And we can create a big box.

```python
big_box = Box(0, 0, 80, 100)
```

Or many boxes using a [list comprehension](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)

```python
many_boxes = [Box() for i in range(5000)]
```

So now we have a big box, and 5000 smaller boxes, all alike.

```python
# Print the first 10 boxes
print(many_boxes[:10])
```

```
Output goes here
```

And yes, we can draw those boxes.

```python
import svgwrite

def draw_boxes(boxes, with_boxes=True):
    dwg = svgwrite.Drawing('lesson1.svg', profile='full', size=(100, 100))
    for box in boxes:
        dwg.add(dwg.rect(insert=(box.x, box.y), size=(box.w, box.h), fill='red'))
    dwg.save()

draw_boxes(many_boxes)
```
And here is the output:

<img src="lesson1.svg" width="100%" style='border: 1px solid green;'>


That ... was not very interesting. It's a single small red square!

Remember *all our boxes have the same size and position!*

So ... we should do something better. Or at least more interesting, in lesson 2.
