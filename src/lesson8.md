# BOXES v8

In the [previous lesson](lesson7.run.html) we started using our layout engine to display text, and ran into some limitations. Let's get rid of them.

We have no changes in our Box class, or the page setup, or how we load and adjust the boxes' sizes. 

```python-include:code/lesson8.py:1:28
```

Also unchanged is the drawing code.

```python-include:code/lesson8.py:107:144
```

But we need to work on our layout engine, a lot. Here is the image of our attempt at displaying "Pride and Prejudice":

![lesson7_pride_and_prejudice.svg](lesson7_pride_and_prejudice.svg)

Let's count the problems:

1. It totally ignores newlines everywhere
2. It keeps spaces at the end of rows, making the right side ragged 
   (see "said his " in the seventh line)
3. White space at the beginning of rows is shown and it looks bad 
   (see " a neigh" at the beginning of the fifth line)
4. Words are split between lines haphazardly, but this is for later and leads
   to some serious code that needs its own lesson.

Let's hit the issues in order. First, newlines.

The idea is: if we find a newline, we need to break the line. Doesn't sound
particularly complex, specially since lines that are broken intentionally
are never fully justified.

The changes are minor:

* Create a flag `break_line` set to True if we encounter a newline 
  or overflow the page.
* In case of newline, make that box invisible by making it 0-wide and 
  not stretchy.
* When the break_line flag is set, handle as usual by moving to the 
  left, etc.


```python-include:code/lesson8.py:30:104
```

The code changes are small, but the output now looks radically different.

```python-include:code/lesson8.py:148:148
```

![lesson8.svg](lesson8.svg)

----------

Further references:

* Full source code for this lesson [lesson8.py](code/lesson8.py)
* [Difference with code from last lesson](diffs/lesson7_lesson8.html)