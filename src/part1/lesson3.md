# BOXES v3

In our [previous lesson](lesson2.run.html) we ended with something like a line
of army ants, all our boxes lined up. Let's make it better by making them
organize themselves in rows.

This code is just like before:

```python-include:code/lesson3.py:1:14
```

But now, let's organize our boxes in rank and file. In fact, let's put our
many boxes inside a big box.

```python-include:code/lesson3.py:16:16
```

We will get our boxes one at a time, put the first in 0,0 and the next one right 
at its right, and so on, and when we are about to step outside of the big box, 
we go back to the left, a little down, and do it all over again.

```python-include:code/lesson3.py:18:42
```

And now we can draw it. Just so we are sure we are staying inside the 
big box, we will draw it too, in light blue.

```python-include:code/lesson3.py:44
```
And here is the output:

![lesson3.svg](lesson3.svg)

That is strangely satisfying! Of course we are doing something wrong in that
we are overflowing the big box vertically.

So, we could have more than one big box. And use them as pages?

----------

Further references:

* Full source code for this lesson [lesson3.py](lesson3.py.run.html)
* [Difference with code from last lesson](part1/code/diffs/lesson2_lesson3.html)
