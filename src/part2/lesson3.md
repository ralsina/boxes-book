# Boxes v0.14

In the [previous lesson](lesson2.md) we mentioned *code smells*, the existence
of hardcoded "magic numbers" and global variables in our code, and we cleaned
it up. There is one other code smell that makes our code pretty funky.

The `layout` function is **long**. It's 101 lines long. That is **nuts**. It's
also one of the undesirable side effects of the process by which we wrote it.
When you write your code organically from the core of an idea, it tends to
produce long functions, because it's easier to just tweak things in place
instead of breaking things into separate functions.

So, in the future you may decide to do that along the way, or just do what we
will now do and fix it afterwards.

This functions does all the following things:

* Breaks our list of boxes into rows
* Insert hyphens if needed
* Justifies lines if needed
* Breaks the rows into pages
* Deletes leftover pages

That is a lot of responsibility for a single function. So, we need to break it
up.

----------

Further references:

* Full source code for this lesson [boxes.py](code/lesson3/boxes.py)
* [Difference with code from last lesson](code/diffs/lesson3_diff.html)