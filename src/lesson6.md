# BOXES v6

In our [previous lesson](lesson5.run.html) we created a fully justified layout of varying-width boxes spread across multiple pages. But we cheated.

To achieve full justification, we spread the "slack" evenly in the space between all boxes in the row. If we were trying to layout text, that is not the proper way.

You see, text comes separated in words. And usually, in western languages, the words have characters called spaces between them. So what we do, when laying out text, is to make the special **space** boxes slightly larger and keep the separation between boxes constant (in fact, we also tweak separations between letters, but let's ignore that for now. Or for ever.

How about we choose some boxes and decide they, and only they, are stretchy?

That way, our strategy to fully justify the text will be: stretch the stretchy bits on each row just enough so that the row is exactly the width we need.

For the first time in a few lessons, we need to change our Box class:

```python-include:code/lesson6.py:1:23
```

The changes in the layout function are not so big.

```python-include:code/lesson6.py:25:51
```

When finishing a row, see if it has stretchy boxes in it.

If it doesn't, bump each box a little to the right like we did before.

```python-include:code/lesson6.py:52:58
```

If we do have stretchy boxes in the row, make each one wider.


```python-include:code/lesson6.py:59:66
```

And continue like we did before.

```python-include:code/lesson6.py:69:88
```

The drawing code needs a change so we can see the "stretchy" boxes in a different color.

```python-include:code/lesson6.py:91
```

![lesson6.svg](lesson6.svg)

This layout strategy works:

* With multiple pages of arbitrary sizes and positions
* With many boxes of different widths and stretch capabilities
* Even if nothing can stretch

But the next lesson will start taking things to the next level.

----------

Further references:

* Full source code for this lesson [lesson6.py](lesson6.py.run.html)
* [Difference with code from last lesson](diffs/lesson5_lesson6.html)
