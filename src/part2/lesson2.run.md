# BOXES v0.13

I hate magic numbers. I **love** [The Magic Numbers](https://en.wikipedia.org/wiki/The_Magic_Numbers)
but I hate how many numbers are just there in our code. Let's look at some of
it:

```python
# boxes.py
# We add a "separation" constant so you can see the boxes individually
separation = .05

```

```python
# boxes.py
    pages = [Box(i * 35, 0, 30, 50) for i in range(10)]

```

```python
# boxes.py
    draw_boxes(text_boxes, pages, output, (100, 50), True)

```

Magic numbers are what's called a *code smell*. When you read the code, you
should be wrinkling your nose, like when you get sushi and it smells just a
little bit off. Other code smells include global variables, and `separation`
is actually both things, a global magic number!

We are deciding that 0.05 is a reasonable separation between letters. We are
deciding there are 10 pages , they are 30x50 and next to each other with a
specific separation.

Magic numbers are bad because they **encode a choice**. They are literally us
choosing something and making it part of the code. By being inside the code,
they are outside the reach of the user. In some cases the magic numbers have a
good reason for existing. In others they should just be a default for
something the user can change.

There are additional decisions not in numbers, such as using the Arial font,
but we will get around to them later.

So, let's get rid of the stench, and make those things part of the interface
we provide the user.

Let's go in order.

For `separation` we can make an optional argument defaulting to that value.
The `pages` list, we could take a page size argument at least. And for the
drawing size, we will just make the drawing big enough to show all the boxes.

A bit trickier is the number of pages, which was hardcoded to 10. We will just
create a large number of pages and remove the unused ones.

The first two are just a matter of adding them to the docopt data. The parts
between `[]` brackets are optional.

```python
# boxes.py
"""
Usage:
    boxes <input> <output> [--page-size=<WxH>] [--separation=<sep>]
    boxes --version
"""

```

Then getting the values out of the arguments (or use defaults), and pass them
along to our existing functions:

```python
# boxes.py
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

```

Adding the arguments to `convert` and passing them along where they make sense.
Additionally, we calculate the drawing size instead of just hardcoding it.

```python
# boxes.py
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

```

And making the obvious changes in each function. In `create_pages` we use the
page size:

```python
# boxes.py
def create_pages(page_size):
    # A few pages all the same size
    w, h = page_size
    pages = [Box(i * (w + 5), 0, w, h) for i in range(1000)]
    return pages

```

In `layout` we pass `separation` as argument, which requires no changes, and
add a little code to delete the unused pages:

```python
# boxes.py
    # Remove leftover boxes
    del (pages[page:])

```

I suggest you take a close look at [the diff for this lesson.](part2/code/diffs/lesson2_diff.html) to see all these small changes in context.

What have we gained for this effort? Well, we can now do things that used to
require editing code. Such as using very small pages:

```sh
python code/lesson2/boxes.py pride-and-prejudice.txt lesson2.svg --page-size=10x20
```

And that, unfortunately, exposes a whole lot of bugs.

![lesson2.svg](part2/lesson2.svg)

We will get around to them. Don't worry. We just need to do a little more
groundwork.

----------

Further references:

* Full source code for this lesson [boxes.py](part2/code/lesson2/boxes.py)
* [Difference with code from last lesson](part2/code/diffs/lesson2_diff.html)