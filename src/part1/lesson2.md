# BOXES v2

In our [previous lesson](lesson1.run.html) we created a rather disappointing 
drawing using boxes. Let's introduce a new wrinkle, and **layout** the many
boxes.

This code is just like before:

```python-include:code/lesson2.py:1:14
```

But now, so they are not all stuck one on top of the other, let's lay the boxes down in a line, one next to the other.

```python-include:code/lesson2.py:16:25
```

And we can see that they all have different coordinates now by printing 
a few of them. And yes, some of those numbers do look funny. Floating point
numbers are weird.

```python
print([(box.x, box.y) for box in many_boxes[:10]])
```

```
Output goes here
```

Let's draw them!

```python-include:code/lesson2.py:27:42
```
And here is the output:

![lesson2.svg](lesson2.svg)

That was more or less what we expected, right? Of course since there are 5000 small
boxes that row of boxes goes on for quite a while.

We *could* just go to the right for a while, then start a new row. Let's do that in
the next lesson.

----------

Further references:

* Full source code for this lesson [lesson2.py](lesson2.py.run.html)
* [Difference with code from last lesson](part1/code/diffs/lesson1_lesson2.html)
