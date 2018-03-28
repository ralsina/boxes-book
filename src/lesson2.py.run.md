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

# We add a "separation" constant so you can see the boxes individually
separation = .2


def layout(boxes):
    for i, box in enumerate(boxes):
        box.x = i * (1 + separation)


layout(many_boxes)

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


draw_boxes(many_boxes, 'lesson2.svg', (5, 2))

```
