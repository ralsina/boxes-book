# BOXES v0.13

I hate magic numbers. I **love** [The Magic Numbers](https://en.wikipedia.org/wiki/The_Magic_Numbers) but I hate how many numbers are just there in our code. Let's look at some of it:

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
deciding our pages are 10, they are 30x50 and next to each other with a 
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
