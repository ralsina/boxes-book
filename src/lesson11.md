# BOXES v11

In our [previous lesson](lesson10.run.html) we promised we will improve the
problem of overfull lines in our text layout engine.

The problem: A long string of letters without any hyphenation points or spaces
causes a very long row to be fitted into a smaller page, causing letters to
overlap. Or, if we are unable to break at all, we just spill to the right
forever.

  > ### Underfull and Overfull 
  >
  > When a line has too few characters, slack is
  > positive and we have to "spread" them, that is called **underfull**. The
  > opposite, where a line has too many characters, slack is negative and we
  > have to "smush" them, is called **overfull**.


![lesson10_one_break.svg](lesson10_one_break.svg)

As you probably expected... no changes in the Box class.

```python-include:code/lesson11.py:1:40
```

Also no changes in how we draw things.

```python-include:code/lesson11.py:172:209
```

So far, our algorithm to break lines is simple:

1. If the next character is a newline: break
2. If we are short, add to the line.
3. If the next character makes the line overfull:
   a. If it's a space or a hyphen: break
   b. If not, add to the line
4. If we broke the line, adjust positions and widths so the line is
   exactly as wide as the page by spreading the slack.

We need a better way to decide what is the best possible breaking point for
the line. If it's too overfull, it will look bad. If it's too underfull, it
will look bad too. And sometimes there is just no good breaking point and we
need to *do something*.

If we were lucky enough to have a breaking point that exactly fills the line,
then we would not have a problem, so usually this will come down to choosing
between two breaking points. One makes the line overfull, one keeps it
underfull.

How good is a breaking point?

* If the slack is smaller, it's better.
* If it's underfull it's slightly better than overfull, since it's better to
  have a spread out line than overlapping letters.
* If we have many spaces, then a bigger slack is acceptable.

This is all subjective, of course. How much *movement* we tolerate on the text
is a judgment call, so it involves some trial and error.

Let's start with some made up numbers, because we have to start somewhere.

* The allowed positive slack is 20% of the width of the spaces in the line.
* The allowed negative slack is 10% of the width of the spaces in the line.

And here's a plan to implement it:

* When adding characters, check if it's a possible breaking point.
* If it is, remember the "goodness" it has
* When reaching an overfull breaking point, check if it's better than the last
  one we saw.
* If the overfull breaking point is better, break.
* If the overfull breaking point is worse, use the underfull breaking point.

The first new thing is a function to calculate how good a breaking point is,
in those terms.

```python-include:code/lesson11.py:41:60
```

```python
# 10 boxes of width 1, 1 stretchy in the middle
boxes = [Box(x=i, w=1) for i in range(10)]
boxes[5].stretchy = True

# On a page that is 8 units wide:
print(badness(8, boxes))
```

```
output goes here
```

Let's see how that works for page widths between 5 and 15 (remember our row is
10 units wide):

```python
for w in range(5,15):
  print('page_width:', w, ' -> badness:', badness(w, boxes))
```

As you can see, if the page was 10 units wide, it would be optimal. The second
best option is for the page to be slightly wider, then maybe slightly thinner
and so on.

```
output goes here
```


We will need to load data that shows the problem. In this case, it's a row of
20 letters 'a' (without hyphens), a space, then 20, and then 30 more 'a's.

Why?

As before, the page is about wide enough to fix 58 "a"s. That means the first
run will not be enough to fill the line. The second run will still not be
enough. The third run will, however, badly overfill it. So, we should go all
the way to the end, see that it's too long, and then go back to the second
space and break there.


```python-include:code/lesson11.py:22:32
```

And now we have a problem. The change to our code needed to implement that is
too large. It's so large that it amounts to a rewrite of our layout function
and if we rewrite it, how would we be sure that we are not breaking all the
things we achieved previously?

It turns out this is as far as just sitting down and writing code will take
us. We need to get more serious, and transform this small pile of fragile code
into something we can actually hack confidently and transform without fear of
destroying it.

Therefore, we leave `layout` intact, show the failing test and move on to
Part 2 of the book, where we will reorganize the code into a coherent
software package and then... we will try again.


```python-include:code/lesson11.py:63:169
```

```python-include:code/lesson11.py:212:212
```

![lesson11.svg](lesson11.svg)

----------

Further references:

* Full source code for this lesson [lesson11.py](code/lesson11.py)
* [Difference with code from last lesson](diffs/lesson10_lesson11.html)