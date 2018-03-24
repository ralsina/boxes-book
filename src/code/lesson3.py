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

big_box = Box(0, 0, 50, 80)

# We add a "separation" constant so you can see the boxes individually
separation = .2


def layout(_boxes):
    # Because we modify the box list, we will work on a copy
    boxes = _boxes[:]
    # The 1st box is at 0,0 so no need to do anything with it, right?
    previous = boxes.pop(0)
    while boxes:
        # We take the new 1st box
        box = boxes.pop(0)
        # And put it next to the other
        box.x = previous.x + previous.w + separation
        # At the same vertical location
        box.y = previous.y
        # But if it's too far to the right...
        if (box.x + box.w) > big_box.w:
            # We go all the way left and a little down
            box.x = 0
            box.y = previous.y + previous.h + separation
        previous = box


layout(many_boxes)

import svgwrite


def draw_boxes(boxes, fname, size):
    dwg = svgwrite.Drawing(fname, profile='full', size=size)
    # Draw the "big box"
    dwg.add(
        dwg.rect(
            insert=(big_box.x, big_box.y),
            size=(big_box.w, big_box.h),
            fill='lightblue',
        )
    )
    # Draw all the boxes
    for box in boxes:
        dwg.add(
            dwg.rect(
                insert=(box.x, box.y), size=(box.w, box.h), fill='red'
            )
        )
    dwg.save()


# Make the visible part of the drawing larger to show big_box
draw_boxes(many_boxes, 'lesson3.svg', (50, 90))
