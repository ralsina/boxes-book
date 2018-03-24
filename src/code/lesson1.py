class Box():

    def __init__(self, x=0, y=0, w=1, h=1):
        """Accept arguments to define our box, and store them."""
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __repr__(self):
        return 'Box(%s, %s, %s, %s)' % (self.x, self.y, self.w, self.y)


big_box = Box(0, 0, 80, 100)


many_boxes = [Box() for i in range(5000)]

import svgwrite


def draw_boxes(boxes):
    dwg = svgwrite.Drawing('lesson1.svg', profile='full', size=(5, 2))
    for box in boxes:
        dwg.add(
            dwg.rect(
                insert=(box.x, box.y), size=(box.w, box.h), fill='red'
            )
        )
    dwg.save()


draw_boxes(many_boxes)
