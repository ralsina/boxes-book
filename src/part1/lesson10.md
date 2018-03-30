# BOXES v10

In our [previous lesson](lesson9.run.html) we created a serviceable text
layout engine. It has many problems, but remember our goal is not to create
the best possible thing, this is an educational experience. The spit and
polish will appear later on.

But there is a glaring problem, it breaks words in all the wrong places.
Examples of it appear in almost every line of the output. So, how does one fix
that?

The traditional answer (and the one we will be using) is hyphenation, breaking
words between lines in the correct places.

Instead of breaking anywhere, we will break only in the places where the [rules of each language](https://english.stackexchange.com/questions/385/what-are-the-rules-for-splitting-words-at-the-end-of-a-line)
allow us to.

Just as it happened with [text shaping](lesson7.run.html) we are lucky to live
in a moment in time when almost everything we need to do it right is already
in place. In particular, we will use a library called [Pyphen](https://github.com/Kozea/Pyphen)
mostly because I already have used it in another project.

Am I sure it's the best one? No. Do I know exactly how it does what it does?
No. I know enough to make it work, and it works *well enough* so for this
stage in the life of this project that is more than enough. In fact, it takes
the rules for word-breaking from dictionaries provided by an Office Suite, so
it does about as good a job as the dictionary does. It even supports
subtleties such as the differences between British and American English!

Here's an example of how it works:

```python
import pyphen
dic = pyphen.Pyphen(lang='en_GB')
print('en_GB:', dic.inserted('dictionary', '-'))
dic = pyphen.Pyphen(lang='en_US')
print('en_US:', dic.inserted('dictionary', '-'))
```

```
Output goes here
```

Keep in mind that this is not magic. If you feed it garbage, it will give you
garbage.

```python
dic = pyphen.Pyphen(lang='es_ES')
print('es_ES:', dic.inserted('dictionary', '-'))
```

```
Output goes here
```

Where is it proper to break a line?

* On a newline character
* On a space
* On a breaking point as defined by Pyphen

One of those things is not like the others. We have boxes with newlines in
them and we have boxes with spaces in them, but there are no boxes with
breaking points in them.

But we can add them! There is Unicode symbol for that:

> ### SOFT HYPHEN (SHY)
>
> The [soft hyphen](https://en.wikipedia.org/wiki/Soft_hyphen) serves as an
> invisible marker used to specify a place in text where a hyphenated break
> is allowed without forcing a line break in an inconvenient place if the
> text is re-flowed. It becomes visible only after word wrapping at the end
> of a line.

So, if we insert them in all the right places, then we can use them to decide
whether we are at a suitable breaking point. We will put this in a file called
`hyphen.py`

```python-include:code/hyphen.py
```

```python
from code.hyphen import insert_soft_hyphens

print (insert_soft_hyphens('Roses are red\nViolets are blue', '-'))
```


```
Output goes here
```

So, with this code ready, we can get to work on implementing hyphenation
support in our layout function.

First, this code is exactly as it was before:

```python-include:code/lesson10.py:1:19
```

We do need to make a small change to how we load our text, to add the hyphens:

```python-include:code/lesson10.py:22:30
```

No changes in how we draw things.

```python-include:code/lesson10.py:148:185
```

And now our layout function. One first approach, which we will refine later,
is to simply refuse to break lines if we are not in a "good" place to break it.

Then, we inject a box with a visible hyphen in the line break, and that's it.

Here is the code to create a box with a hyphen:

```python-include:code/lesson10.py:33:36
```

And here finally, our layout supports hyphens:

```python-include:code/lesson10.py:39:145
```

```python-include:code/lesson10.py:188:188
```

![lesson10.svg](part1/lesson10.svg)

And there in "proper-ty" you can see it in action. Of course this is
a naïve implementation. What happens if you just can't break?

```python
many_boxes = [Box(letter='a') for i in range(200)]
adjust_widths_by_letter(many_boxes)
layout(many_boxes)
draw_boxes(many_boxes, 'lesson10_lots_of_a.svg', (35, 6), hide_boxes=True)
```

![lesson10_lots_of_a.svg](part1/lesson10_lots_of_a.svg)

Since it can't break at all, it just goes on and on.

And there are other corner cases!

```python
many_boxes = [Box(letter='a') for i in range(200)]
many_boxes[100] = Box(letter=' ', stretchy=True)
adjust_widths_by_letter(many_boxes)
layout(many_boxes)
draw_boxes(many_boxes, 'lesson10_one_break.svg', (35, 6), hide_boxes=True)
```

![lesson10_one_break.svg](part1/lesson10_one_break.svg)

Because there is only one place to break the line, it then tries to
wedge 100 letter "a" where there is room for 54 (I counted!) and something interesting happens... the "slack" is negative!

Instead of stretching out a "underfilled" line, we are squeezing a "overfilled" one. Everything gets packed too tight, and the letters start
overlapping one another.

The lesson is that just because it works for the usual case it doesn't mean
it's **done**. Even in the case of words, it can happen that breaking points take a while to appear and our line becomes overfull.

We will tackle that problem next.

----------

Further references:

* Full source code for this lesson [lesson10.py](lesson10.py.run.html)
* [Difference with code from last lesson](part1/code/diffs/lesson9_lesson10.html)
