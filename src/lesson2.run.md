# BOXES v2

In our [previous lesson](lesson1.run.html) we created a rather disappointing 
drawing using boxes. Let's introduce a new wrinkle, and **layout** the many
boxes.

This code is just like before:

```python
# lesson2.py
class Box():

    def __init__(self, x=0, y=0, w=1, h=1):
        """Accept arguments to define our box, and store them."""
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __repr__(self):
        return 'Box(%s, %s, %s, %s)' % (self.x, self.y, self.w, self.y)


many_boxes = [Box() for i in range(5000)]

```

But now, so they are not all stuck one on top of the other, let's lay the boxes down in a line, one next to the other.

```python
# lesson2.py
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
[(0.0, 0), (1.2, 0), (2.4, 0), (3.5999999999999996, 0), (4.8, 0), (6.0, 0), (7.199999999999999, 0), (8.4, 0), (9.6, 0), (10.799999999999999, 0)]
```

Let's draw them!

```python
# lesson2.py
import svgwrite


def draw_boxes(boxes):
    dwg = svgwrite.Drawing('lesson2.svg', profile='full', size=(100, 5))
    for box in boxes:
        dwg.add(
            dwg.rect(
                insert=(box.x, box.y), size=(box.w, box.h), fill='red'
            )
        )
    dwg.save()


draw_boxes(many_boxes)

```
And here is the output:

![lesson2.svg](lesson2.svg)

That was more or less what we expected, right? Of course since there are 5000 small
boxes that row of boxes goes on for quite a while.

We *could* just go to the right for a while, then start a new row. Let's do that in
the next lesson.

----------

Further references:

* [Full source code for this lesson](code/lesson2.py)
* [Difference with code from last lesson](diffs/lesson1_lesson2.html)