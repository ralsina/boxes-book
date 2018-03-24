# BOXES v7

So far in our previous lessons we have worked in an abstract world of boxes.
Some hints of a direction were visible, like organizing our boxes in *pages* and trying to achieve a *justified layout* among others.

So, let's just say it, we are going to be doing text layout. But not the easy one. No, sir. No monospaced fonts for us. We want to do the whole enchilada, we are going to have variable-width fonts with kerning, and multi-page, fully-justified text layouts **with hyphenation**.

Ok, perhaps about 50% of the enchilada, because it will have no bidirectional support, only wok in english, only read UTF-8 encoded files, and so on a lot of things. But it's still a lot of mexican food!

And we are going to do that in lessons not much longer than the ones you have been seeing so far. Except this one. This one is much longer. So let's get started.

Clearly, we want our boxes to have letters. And our "stretchy" boxes are special because they have things like spaces. In fact, let's just say they have spaces.

We will now expand our Box class to support letters inside the boxes.

```python-include:code/lesson7.py:1:23
```

We can keep using the exact same layout function.

```python-include:code/lesson7.py:24:87
```

And tweak the drawing function to show us letters, and to make the colored boxes optional.

```python-include:code/lesson7.py:90:130
```

![lesson7.svg](lesson7.svg)

Of course this is very boring, so we need to spice up our data a little.
We can use different letters, and then make the right ones stretchy. That is easy!

```python-include:code/lesson7.py:133:142
```

![lesson7_different_letters.svg](lesson7_different_letters.svg)

As you can see, there are very minor horizontal shifts and stretches, since all boxes are the same size.

But as a text layout engine we have a **major** failure: we are ignoring the size of the letters we are layouting!

This is a very complex thing to do called *text shaping*. You need to understand the content of the font you are using to display the text, and more subtle things like what happens if you put specific letters next to each other (kerning) and much more.

The good news is that it's already done for us, in libraries called Harfbuzz and Freetype.

This paragraph is perhaps the most important one in this book. I am about to show you some obscure code. And I will tell you the secret of how it got here:
**I copied it from the documentation for the libraries I am using.** Sometimes you will need to do something complicated only once in your life. It's perfectly ok to just google how to do it. And as long as you are confident you can find it again if needed, it's ok to just forget about it.

I will show you this code, and then put it in a separate file called `fonts.py` and from now on I will not show it in the lessons, because we are *not* going to change it, *ever*.


```python-include:code/fonts.py
```

And now we will pretend we know what that does, based on its docstring and use it.

```python-include:code/lesson7.py:145:151
```

![lesson7_adjusted_letters.svg](lesson7_adjusted_letters.svg)

And nicer, without the boxes:

```python-include:code/lesson7.py:154:161
```

![lesson7_adjusted_letters_no_boxes.svg](lesson7_adjusted_letters_no_boxes.svg)

And of course, we can just load text there instead of random letters. For example, here we load what is going to be our example test from now on, 
Jane Austen's [Pride and Prejudice from Project Gutenberg](http://www.gutenberg.org/ebooks/1342)

```python-include:code/lesson7.py:164:175
```

![lesson7_pride_and_prejudice.svg](lesson7_pride_and_prejudice.svg)

And that is ... maybe disappointing? While we spent a lot of time on things like justifying text, we have not even looked at newlines!

Also, spaces at the end of lines make the line appear ragged again, now that they are not boxes.

So, we know what to hit in the next lesson.

----------

Further references:

* Full source code for this lesson [lesson7.py](code/lesson7.py)
* [Difference with code from last lesson](diffs/lesson6_lesson7.html)