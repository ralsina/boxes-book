# BOXES v0.9

In the [previous lesson](lesson8.run.html) we fixed the handling of newlines
in our layout engine, and noticed a problem with spaces. Let's fix it!

We have no changes in our Box class, or the page setup, or how we load and adjust the boxes' sizes.

```python-include:code/lesson9.py:1:28
```
Also unchanged is the drawing code.

```python-include:code/lesson9.py:127:164
```

The more obvious problems are:

* It keeps spaces at the end of rows, making the right side ragged.
* White space at the beginning of rows is shown and it looks bad

![lesson8.svg](part1/lesson8.svg)

You can see clearly, in the previous sample output where this happens in one of the latter paragraphs, "to see the place,  " appears ragged when it should not. And a similar thing happens in an earlier paragraph where there is a hole against the left margin in " told me all about it".

In both cases, the cause is because the "empty" space is used by spaces!

So, one possible solution is, when justifying a row, to make all the spaces at the right margins 0-width and not stretchy. At the same time, when adding spaces at the beginning of a row, they should become 0-width and not stretchy.

**BUT** this means the list of boxes will need its width readjusted if they are to be layouted again on different pages! That's because some of the spaces will now be thin and "rigid" so they will work badly if they are **not** against the margin on a different layout.

It's not a big problem, but it's worth keeping in mind, since it's the kind of thing that becomes an obscure bug later on. So, we add it to the docstring.

```python-include:code/lesson9.py:30:124
```

```python-include:code/lesson9.py:167:167
```

![lesson9.svg](part1/lesson9.svg)

As you can see, the justification now is absolutely tight where it needs to be.
With that taken care of, we will consider the problem of breaking lines inside words and how to fix it using hyphenation in the next lesson.

----------

Further references:

* Full source code for this lesson [lesson9.py](lesson9.py.run.html)
* [Difference with code from last lesson](part1/code/diffs/lesson8_lesson9.html)
