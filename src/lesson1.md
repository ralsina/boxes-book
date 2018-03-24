# BOXES v1

Welcome to Boxes v1. I want to be able to draw some boxes. By boxes I don't mean actual boxes,
but rather squares. I found a library called svgwrite that lets you do that pretty easily.

First let's create a data structure. A simple class called Box.

```python-include:code/lesson1.py:1:12

```

As you can see that is a pretty simple class. And we can create a big box.

```python-include:code/lesson1.py:14:14
```

Or many boxes using a [list comprehension](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)

```python-include:code/lesson1.py:17:17
```

So now we have a big box, and 5000 smaller boxes, all alike.

```python
# Print the first 10 boxes
print(many_boxes[:10])
```

```
Output goes here
```

And yes, we can draw those boxes.

```python-include:code/lesson1.py:19:27
```
And here is the output:

![lesson1.svg](lesson1.svg)

That ... was not very interesting. It's a single small red square!

Remember *all our boxes have the same size and position!*

So ... we should do something better. Or at least more interesting, in lesson 2.
