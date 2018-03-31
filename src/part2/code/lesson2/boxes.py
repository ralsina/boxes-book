"""
Usage:
    boxes <input> <output> [--page-size=<WxH>] [--separation=<sep>]
    boxes --version
"""

from fonts import adjust_widths_by_letter
from hyphen import insert_soft_hyphens

import svgwrite
from docopt import docopt


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


def hyphenbox():
    b = Box(letter='-')
    adjust_widths_by_letter([b])
    return b


def badness(page_width, row):
    """Calculate how 'bad' a position to break is.
    
    bigger is worse.
    """
    # Yes, this is suboptimal. It's easier to optimize working code
    # than fixing fast code.
    row_width = (row[-1].x + row[-1].w) - row[0].x
    slack = page_width - row_width
    stretchies = [b for b in row if b.stretchy]
    if len(stretchies) > 0:
        stretchies_width = sum(s.w for s in stretchies)
        # More stetchy space is good. More slack is bad.
        badness = slack / stretchies_width
    else:  # Nothing to stretch. Not good.
        badness = 1000
    if slack < 0:
        # Arbitrary fudge factor, negative slack is THIS much worse
        badness *= 2
    return badness


def layout(_boxes, pages, separation):
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

    # Remove leftover boxes
    del (pages[page:])


def draw_boxes(boxes, pages, fname, size, hide_boxes=False):
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


def create_text_boxes(input_file):
    p_and_p = open(input_file).read()
    p_and_p = insert_soft_hyphens(p_and_p)  # Insert invisible hyphens
    text_boxes = []
    for l in p_and_p:
        text_boxes.append(Box(letter=l, stretchy=l == ' '))
    adjust_widths_by_letter(text_boxes)
    return text_boxes


def create_pages(page_size):
    # A few pages all the same size
    w, h = page_size
    pages = [Box(i * w + 5, 0, w, h) for i in range(1000)]
    return pages


def convert(input, output, page_size=(30, 50), separation=0.05):
    pages = create_pages(page_size)
    text_boxes = create_text_boxes(input)
    layout(text_boxes, pages, separation)
    draw_boxes(
        text_boxes,
        pages,
        output,
        (pages[-1].w + pages[-1].x, pages[-1].h),
        True,
    )


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Boxes 0.13')

    if arguments['--page-size']:
        p_size = [int(x) for x in arguments['--page-size'].split('x')]
    else:
        p_size = (30, 50)

    if arguments['--separation']:
        separation = float(arguments['--separation'])
    else:
        separation = 0.05


    convert(
        input=arguments['<input>'],
        output=arguments['<output>'],
        page_size=p_size,
        separation=separation,
    )
