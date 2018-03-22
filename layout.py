import svgwrite

class Box():
    def __init__(self, x=0, y=0, w=1, h=1, red=False, blue=False, yellow=False, letter=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.red = red
        self.blue = blue
        self.yellow = yellow
        self.letter = letter
    
    def __str__(self):
        return self.letter or 'Box'
    
    def __repr__(self):
        return self.letter or 'Box'

big_box = Box(0, 0, 80, 1000)
pages = []
        

def draw_boxes(boxes, with_boxes=True):
    STYLES = """
    .red { fill: red;}
    .green { fill: green;}
    .blue {fill: blue;}
    .yellow {fill: yellow;}
    .bigbox {fill: cyan; }
    """
    dwg = svgwrite.Drawing('test.svg', profile='full', size=('%d' % big_box.w, '%d' % big_box.w))
    dwg.defs.add(dwg.style(STYLES))
    dwg.add(dwg.rect(insert=(0,0), size=(big_box.w, big_box.h), class_='bigbox'))
    for bb in pages:
        dwg.add(dwg.rect(insert=(bb.x,bb.y), size=(bb.w, bb.h), class_='bigbox'))
    for box in boxes:
        if with_boxes:
            if box.red:
                dwg.add(dwg.rect(insert=(box.x, box.y), size=(box.w, box.h), class_='red'))
            elif box.blue:
                dwg.add(dwg.rect(insert=(box.x, box.y), size=(box.w, box.h), class_='blue'))
            elif box.yellow:
                dwg.add(dwg.rect(insert=(box.x, box.y), size=(box.w, box.h), class_='yellow'))
            else:
                dwg.add(dwg.rect(insert=(box.x, box.y), size=(box.w, box.h), class_='green'))
        if box.letter:
            dwg.add(dwg.text(box.letter, insert=(box.x, box.y + box.h), font_size=box.h, font_family='Arial'))
    dwg.save()



# So, how could we layout the many boxes inside the big_box?
many_boxes = [Box(0, 0, 1, 1) for _ in range(5000)]

# Do nothing ...
# They are all in the same place
# draw_boxes(many_boxes)

# Try to lay them out side by side
# They just go too wide
# We add a "separation" constant so you can see the boxes individually
separation = .2

def layout1(boxes):
    for i, box in enumerate(boxes):
        box.x = i * (1 + separation)

# Put each one next to the other until they reach a width,
# then go down. This is a monospaced layout.

def layout2(boxes):
    for i, box in enumerate(boxes[1:]):
        box.x = boxes[i-1].x + 1 + separation
        box.y = boxes[i-1].y
        if box.x > big_box.w:
            box.x = 0
            box.y = boxes[i-1].y + 1.1

# Now, what happens if some boxes are wider than the others?
# layout2 will make them overlap or have wide breaks between them
import random
many_boxes = [Box(0, 0, 1+random.randint(-2,2)/10, 1) for _ in range(5000)]

# So, we use each box's width instead of a fixed width
def layout3(boxes):
    for i, box in enumerate(boxes[1:], 1):
        prev_box = boxes[i-1]
        box.x = prev_box.x + prev_box.w + separation 
        box.y = prev_box.y
        if box.x > big_box.w:
            box.x = 0
            box.y = prev_box.y + 1.1

# layout3(many_boxes)
# But the right side is ragged

# We can, when we break, put the remaining space spread between boxes
# This is a "justified" layout

def layout4(boxes):
    last_break = 0
    for i, box in enumerate(boxes[1:], 1):
        prev_box = boxes[i-1]
        box.x = prev_box.x + prev_box.w + separation 
        box.y = prev_box.y
        if box.x > big_box.w:
            box.x = 0
            box.y = prev_box.y + 1.1
            slack = big_box.w - (prev_box.x + prev_box.w)
            mini_slack = slack / (i-last_break)
            for j, b in enumerate(boxes[last_break:i]):
                b.x += j * mini_slack
            last_break = i
# layout4(many_boxes)

# But what happens if some boxes are red?
for box in many_boxes:
    if random.randint(1,6) > 5:
        box.red = True
# Well, nothing much, other than they are red

# But what if red means "stretchy" and only those can stretch?
def layout5(boxes):
    last_break = 0
    for i, box in enumerate(boxes[1:], 1):
        prev_box = boxes[i-1]
        box.x = prev_box.x + prev_box.w + separation 
        box.y = prev_box.y
        if box.x > big_box.w:
            box.x = 0
            box.y = prev_box.y + 1.1
            slack = big_box.w - (prev_box.x + prev_box.w)
            row = boxes[last_break:i]
            reds = [b for b in row if b.red]
            # sometimes there is no red in the row. Do nothing.
            if reds:
                mini_slack = slack / len(reds)
                for b in reds:
                    b.w += mini_slack
                for j, b in enumerate(row[1:], 1):
                    b.x = row[j-1].x + row[j-1].w + separation
            last_break = i

# But what happens if a few are blue?
for box in many_boxes:
    if random.randint(1,150) > 149:
        box.blue = True

# Well, nothing much, other than they are blue

# But what if blue means "this row ends here"?
def layout6(boxes):
    last_break = 0
    for i, box in enumerate(boxes[1:], 1):
        prev_box = boxes[i-1]
        box.x = prev_box.x + prev_box.w + separation 
        box.y = prev_box.y
        if prev_box.blue or box.x > big_box.w:
            box.x = 0
            box.y = prev_box.y + 1.1
            slack = big_box.w - (prev_box.x + prev_box.w)
            row = boxes[last_break:i]
            reds = [b for b in row if b.red]
            # sometimes there is no red in the row. Do nothing.
            if reds:
                mini_slack = slack / len(reds)
                for b in reds:
                    b.w += mini_slack
                for j, b in enumerate(row[1:], 1):
                    b.x = row[j-1].x + row[j-1].w + separation
            last_break = i
# Some reds get reeeeeeealy stretchy! That is because rows that
# end because of a blue have very few boxes. So maybe we don't stretch those?

def layout7(boxes):
    last_break = 0
    for i, box in enumerate(boxes[1:], 1):
        prev_box = boxes[i-1]
        box.x = prev_box.x + prev_box.w + separation 
        box.y = prev_box.y
        if prev_box.blue or box.x > big_box.w:
            box.x = 0
            box.y = prev_box.y + 1.1
            if not prev_box.blue:
                row = boxes[last_break:i]
                slack = big_box.w - (row[-1].x + row[-1].w)
                reds = [b for b in row if b.red]
                # sometimes there is no red in the row. Do nothing.
                if reds:
                    mini_slack = slack / len(reds)
                    for b in reds:
                        b.w += mini_slack
                    for j, b in enumerate(row[1:], 1):
                        b.x = row[j-1].x + row[j-1].w + separation
            last_break = i

# What if we want blue boxes break lines but also separate lines a little?

def layout8(boxes):
    last_break = 0
    for i, box in enumerate(boxes[1:], 1):
        prev_box = boxes[i-1]
        box.x = prev_box.x + prev_box.w + separation 
        box.y = prev_box.y
        if prev_box.blue or box.x > big_box.w:
            box.x = 0
            if prev_box.blue:
                box.y = prev_box.y + 2.1
            else: # not blue
                box.y = prev_box.y + 1.1
                row = boxes[last_break:i]
                slack = big_box.w - (row[-1].x + row[-1].w)
                reds = [b for b in row if b.red]
                # sometimes there is no red in the row. Do nothing.
                if reds:
                    mini_slack = slack / len(reds)
                    for b in reds:
                        b.w += mini_slack
                    for j, b in enumerate(row[1:], 1):
                        b.x = row[j-1].x + row[j-1].w + separation
            last_break = i


# So ... what if each box has a letter or a space inside it? 
for box in many_boxes:
    # More than one space so they appear often
    box.letter = random.choice('     abcdefghijklmnopqrstuvwxyz')

# Maybe we should make the box sizes depend on the letter inside it?
# This is complicated, sorry
import harfbuzz as hb
import freetype2 as ft

def adjust_widths_by_letter(boxes):
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

adjust_widths_by_letter(many_boxes)
# layout8(many_boxes)

# There is all that space between letters we added when they were boxes. Let's remove it.

separation = 0
layout8(many_boxes)

# How about we get the letters from a text instead of randomly?
p_and_p = open('pride-and-prejudice.txt').read()
text_boxes = []
for l in p_and_p:
    text_boxes.append(Box(letter=l))
adjust_widths_by_letter(text_boxes)
# layout8(text_boxes)
# Oh, it's all green now, and it's all one thing after another. We should make newlines blue!

for b in text_boxes:
    if b.letter == '\n':
        b.blue = True
# layout8(text_boxes)

# Better, but newlines should not really take any space should they?
def add_blue(boxes):
    for b in boxes:
        if b.letter == '\n':
            b.blue = True
            b.w = 0
add_blue(text_boxes)
# layout8(text_boxes)

# Our big_box is very wide now, that is why we have long lines. Let's make it narrower
big_box = Box(0, 0, 30, 1000)
# layout8(text_boxes)

# But our right side is ragged again! We should make spaces red.
def add_red(boxes):
    for b in boxes:
        if b.letter == ' ':
            b.red = True
add_red(text_boxes)
# layout8(text_boxes)

# The second paragraph of Chapter 1 shows a red space as first thing in the row, and that looks bad!
# So, when the 1st letter in a row is a space, let's make it take no width and not stretch

def layout9(boxes):
    last_break = 0
    for i, box in enumerate(boxes[1:], 1):
        prev_box = boxes[i-1]
        box.x = prev_box.x + prev_box.w + separation 
        box.y = prev_box.y
        if prev_box.blue or box.x > big_box.w:
            box.x = 0
            if box.red:
                box.w = 0
            if prev_box.blue:
                box.y = prev_box.y + 2.1
            else: # not blue
                box.y = prev_box.y + 1.1
                row = boxes[last_break:i]
                slack = big_box.w - (row[-1].x + row[-1].w)
                # If the 1st thing is a red, that one doesn't stretch
                reds = [b for b in row[1:] if b.red]
                # sometimes there is no red in the row. Do nothing.
                if reds:
                    mini_slack = slack / len(reds)
                    for b in reds:
                        b.w += mini_slack
                    for j, b in enumerate(row[1:], 1):
                        b.x = row[j-1].x + row[j-1].w + separation
            last_break = i

# Just for fun, let's draw it without the colored boxes
# layout9(text_boxes)
# draw_boxes(text_boxes, False)

# XXX layout9 rewritten using pop(), need to backport this version

def layout10(_boxes):
    boxes = _boxes[:]  # Work on a copy
    prev_box = boxes.pop(0)
    row = [prev_box]
    while(boxes):
        box = boxes.pop(0)
        row.append(box)
        box.x = prev_box.x + prev_box.w + separation 
        box.y = prev_box.y
        if prev_box.blue or box.x > big_box.w:
            box.x = 0
            row.pop()  # our box will go in the next row
            if box.red:
                box.w = 0
            if prev_box.blue:
                box.y = prev_box.y + 2.1

            else: # not blue
                box.y = prev_box.y + 1.1
                slack = big_box.w - (row[-1].x + row[-1].w)
                # If the 1st thing is a red, that one doesn't stretch
                reds = [b for b in row[1:] if b.red]
                # sometimes there is no red in the row. Do nothing.
                if reds:
                    mini_slack = slack / len(reds)
                    for b in reds:
                        b.w += mini_slack
                    for j, b in enumerate(row[1:], 1):
                        b.x = row[j-1].x + row[j-1].w + separation
            row = [box]
        prev_box = box

# layout10(text_boxes)

# Looks good, except that the words are broken wrong. You can't break good like: g
# ood!

# What if we only break on spaces?

def layout11(_boxes):
    boxes = _boxes[:]  # Work on a copy
    prev_box = boxes.pop(0)
    row = [prev_box]
    while(boxes):
        box = boxes.pop(0)
        row.append(box)
        box.x = prev_box.x + prev_box.w + separation 
        box.y = prev_box.y
        if prev_box.blue or (box.x > big_box.w and box.red) :
            row.pop()  # our box will go in the next row
            box.x = 0
            if box.red:
                box.w = 0
            if prev_box.blue:
                box.y = prev_box.y + 2.1

            else: # not blue
                box.y = prev_box.y + 1.1
                slack = big_box.w - (row[-1].x + row[-1].w)
                # If the 1st thing is a red, that one doesn't stretch
                reds = [b for b in row[1:] if b.red]
                # sometimes there is no red in the row. Do nothing.
                if reds:
                    mini_slack = slack / len(reds)
                    for b in reds:
                        b.w += mini_slack
                    for j, b in enumerate(row[1:], 1):
                        b.x = row[j-1].x + row[j-1].w + separation
            row = [box]
        prev_box = box

# layout11(text_boxes)

# That actually ... worked? Except that when we need to fit something wider than
# big_box because we did not break the row, the slack is NEGATIVE and words get
# smushed together!

# What we actually need is hyphenation.
# We can use pyphen to insert soft-hyphen characters wherever words can break.
# And we can mark those positions yellow.

import pyphen
hyphenator = pyphen.Pyphen(lang='en_GB')  # These things are language dependent

p_and_p = open('pride-and-prejudice.txt').readlines()
for i, l in enumerate(p_and_p):
    words = l.split(' ')
    p_and_p[i] = ' '.join(hyphenator.inserted(w, '\u00AD') for w in words)
p_and_p = ''.join(p_and_p)

text_boxes = []
for l in p_and_p:
    text_boxes.append(Box(letter=l))


# This makes the characters '\u00AD' (soft-hyphen) yellow.
def add_yellow(boxes):
    for b in boxes:
        if b.letter == '\u00AD':
            b.yellow = True

add_blue(text_boxes)
add_red(text_boxes)
add_yellow(text_boxes)
adjust_widths_by_letter(text_boxes)

# And create a new layout function that also breaks on yellow boxes.

def layout12(_boxes):
    boxes = _boxes[:]  # Work on a copy
    prev_box = boxes.pop(0)
    row = [prev_box]
    while(boxes):
        box = boxes.pop(0)
        row.append(box)
        box.x = prev_box.x + prev_box.w + separation 
        box.y = prev_box.y
        if prev_box.blue or (box.x > big_box.w and (box.red or box.yellow)) :
            row.pop()  # our box will go in the next row
            box.x = 0
            if box.red:
                box.w = 0
            if prev_box.blue:
                box.y = prev_box.y + 2.1

            else: # not blue
                box.y = prev_box.y + 1.1
                slack = big_box.w - (row[-1].x + row[-1].w)
                # If the 1st thing is a red, that one doesn't stretch
                reds = [b for b in row[1:] if b.red]
                # sometimes there is no red in the row. Do nothing.
                if reds:
                    mini_slack = slack / len(reds)
                    for b in reds:
                        b.w += mini_slack
                    for j, b in enumerate(row[1:], 1):
                        b.x = row[j-1].x + row[j-1].w + separation
            row = [box]
        prev_box = box

# layout12(text_boxes)

# Better! Since we have more break chances, there is less word-smushing.
# However our typography is wrong, because we are hyphenating but not showing a hyphen!
# So, we need to ADD a box when we hyphenate. That special box is hyphenbox():

def hyphenbox():  # Yes, this is not optimal
    b = Box(letter='-', yellow=True)
    adjust_widths_by_letter([b])
    return b

def layout13(_boxes):
    boxes = _boxes[:]  # Work on a copy
    prev_box = boxes.pop(0)
    row = [prev_box]
    while(boxes):
        box = boxes.pop(0)
        row.append(box)
        box.x = prev_box.x + prev_box.w + separation 
        box.y = prev_box.y
        if prev_box.blue or (box.x > big_box.w and (box.red or box.yellow)):
            row.pop()  # our box will go in the next row
            if box.yellow:  # We need to insert the hyphen!
                h_b = hyphenbox()
                h_b.x = prev_box.x + prev_box.w + separation
                h_b.y = prev_box.y
                _boxes.append(h_b)  # So it's drawn
                row.append(h_b) # So it's justified
            box.x = 0
            if box.red:
                box.w = 0
            if prev_box.blue:
                box.y = prev_box.y + 2.1

            else: # not blue
                box.y = prev_box.y + 1.1
                slack = big_box.w - (row[-1].x + row[-1].w)
                # If the 1st thing is a red, that one doesn't stretch
                reds = [b for b in row[1:] if b.red]
                # sometimes there is no red in the row. Do nothing.
                if reds:
                    mini_slack = slack / len(reds)
                    for b in reds:
                        b.w += mini_slack
                    for j, b in enumerate(row[1:], 1):
                        b.x = row[j-1].x + row[j-1].w + separation
            row = [box]
        prev_box = box


# layout13(text_boxes)

# Good. However, we still have smushing. It's usually considered better to make spaces 
# between words grow, rather than shrink. So, what we should do is, instead of breaking 
# in the 1st yellow/red PAST the break, go back and break in the last BEFORE the break!

# XXX backport simplifications from layout14: separation of blue case

def layout14(_boxes):
    boxes = _boxes[:]  # Work on a copy
    row = [boxes.pop(0)]
    while(boxes):
        prev_box = row[-1]
        box = boxes.pop(0)
        row.append(box)
        box.x = prev_box.x + prev_box.w + separation 
        box.y = prev_box.y
        if prev_box.blue:
            box.x = 0
            box.y = prev_box.y + 2.1
            row.pop()
            row=[box]

        elif box.x > big_box.w:
            while not (box.red or box.yellow):  # backtrack onw
                boxes.insert(0, row.pop())
                # tip of row is now box, previous one is prev_box
                box = row[-1]
                prev_box = row[-2]

            row.pop()  # Breaking box goes in next row
            if box.yellow:  # We need to insert the hyphen!
                h_b = hyphenbox()
                h_b.x = prev_box.x + prev_box.w + separation
                h_b.y = prev_box.y
                _boxes.append(h_b)  # So it's drawn
                row.append(h_b) # So it's justified
            box.x = 0
            box.y = prev_box.y + 1.1
            if box.red:
                box.w = 0
            slack = big_box.w - (row[-1].x + row[-1].w)
            # If the 1st thing is a red, that one doesn't stretch
            reds = [b for b in row[1:] if b.red]
            # sometimes there is no red in the row. Do nothing.
            if reds:
                mini_slack = slack / len(reds)
                for b in reds:
                    b.w += mini_slack
                for j, b in enumerate(row[1:], 1):
                    b.x = row[j-1].x + row[j-1].w + separation
            row = [box]

# With a little separation for niceness, the result is not half bad!
separation = 0.05
# layout14(text_boxes)

# So far, our big_box has been very, very tall. What would happen if it were short?
big_box = Box(0, 0, 30, 60)
# layout14(text_boxes)

# Well, that our text flows straight out of the box! And our initial problem was 
# "So, how could we layout the many boxes inside the big_box?" !
# That won't do. Clearly, if we have more text than fits in a box, we need more than one
# box. Like pages.

# So, let's make many big boxes.


pages = [Box(0, i * 65, 30, 60) for i in range(50)]

# layout14(text_boxes)

# Of course our layout engine does nothing with those pages. Let's fix that.

def layout15(_boxes):
    boxes = _boxes[:]  # Work on a copy
    row = [boxes.pop(0)]

    # Put the 1st box in the beginning of the 1st page
    page = 0
    row[0].x = pages[page].x
    row[0].y = pages[page].y
    
    while(boxes):
        prev_box = row[-1]
        box = boxes.pop(0)
        row.append(box)
        box.x = prev_box.x + prev_box.w + separation 
        box.y = prev_box.y
        if prev_box.blue:
            box.x = 0
            box.y = prev_box.y + 2.1
            row.pop()
            row=[box]

        elif box.x > pages[page].w:
            while not (box.red or box.yellow):  # backtrack onw
                boxes.insert(0, row.pop())
                # tip of row is now box, previous one is prev_box
                box = row[-1]
                prev_box = row[-2]

            row.pop()  # Breaking box goes in next row
            if box.yellow:  # We need to insert the hyphen!
                h_b = hyphenbox()
                h_b.x = prev_box.x + prev_box.w + separation
                h_b.y = prev_box.y
                _boxes.append(h_b)  # So it's drawn
                row.append(h_b) # So it's justified
            box.x = 0
            box.y = prev_box.y + 1.1
            if box.red:
                box.w = 0
            slack = pages[page].w - (row[-1].x + row[-1].w)
            # If the 1st thing is a red, that one doesn't stretch
            reds = [b for b in row[1:] if b.red]
            # sometimes there is no red in the row. Do nothing.
            if reds:
                mini_slack = slack / len(reds)
                for b in reds:
                    b.w += mini_slack
                for j, b in enumerate(row[1:], 1):
                    b.x = row[j-1].x + row[j-1].w + separation
            row = [box]

        if box.y + box.h > pages[page].y + pages[page].h:
            # We need to go to the next page
            page = page + 1
            box.y = pages[page].y

        
layout15(text_boxes)
# And there you go, pagination

draw_boxes(text_boxes, False)
