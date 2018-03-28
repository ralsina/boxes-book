# BOXES v4

In the [previous lesson](lesson3.run.html) we totally nailed drawing between the lines ... horizontally. Let's improve on that by being bidimensional.

This code is just like before:

```python-include:code/lesson4.py:1:14
```

But now, instead of a big box, let's have a list of, say, 10 pages (or large boxes), one below the other, slighty separated.

```python-include:code/lesson4.py:16:16
```

Of course our layout routine needs improvements to handle overflowing a
page vertically.

```python-include:code/lesson4.py:18:55
```

We need to change our drawing code to draw more than one page.

```python-include:code/lesson4.py:58:82
```

And here is the output:

![lesson4.svg](lesson4.svg)

Would this work if the pages are arranged differently? Let's put the pages
side by side instead.

```python-include:code/lesson4.py:84:86
```

![lesson4_side_by_side.svg](lesson4_side_by_side.svg)

And how about pages of different sizes?

```python-include:code/lesson4.py:89:96
```

![lesson4_random_sizes.svg](lesson4_random_sizes.svg)

So, we can fill pages and pages with little red squares now. Nice!

How about we make the squares not be all the same width?

```python-include:code/lesson4.py:98:100
```

This adds "noise" to the width of the boxes, so they are now anything between 0.5 and 1.5 units wide.

![lesson4_random_box_sizes.svg](lesson4_random_box_sizes.svg)

That looks interesting...

----------

Further references:

* Full source code for this lesson [lesson4.py](code/lesson4.py.run.html)
* [Difference with code from last lesson](diffs/lesson3_lesson4.html)
