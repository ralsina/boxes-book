# BOXES v0.13

I hate magic numbers. I **love** [The Magic Numbers](https://en.wikipedia.org/wiki/The_Magic_Numbers)
but I hate how many numbers are just there in our code. Let's look at some of
it:

```python-include-norun:code/lesson1/boxes.py:59:60
```

```python-include-norun:code/lesson1/boxes.py:214:214
```

```python-include-norun:code/lesson1/boxes.py:222:222
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

```python-include-norun:code/lesson2/boxes.py:1:5
```

Then getting the values out of the arguments (or use defaults), and pass them
along to our existing functions:

```python-include-norun:code/lesson2/boxes.py:230
```

Adding the arguments to `convert` and passing them along where they make sense.
Additionally, we calculate the drawing size instead of just hardcoding it.

```python-include-norun:code/lesson2/boxes.py:217:227
```

And making the obvious changes in each function. In `create_pages` we use the
page size:

```python-include-norun:code/lesson2/boxes.py:210:214
```

In `layout` we pass `separation` as argument, which requires no changes, and
add a little code to delete the unused pages:

```python-include-norun:code/lesson2/boxes.py:159:160
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