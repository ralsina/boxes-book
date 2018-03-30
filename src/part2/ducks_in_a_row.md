# Part 2: Ducks in a Row

In Part 1 of this book we worked on a text layout engine. That is, code that
knows how and where letters from a text go in a page. It's not a great engine,
it is far from perfect, but it's the one we've got and for the purposes of
this book, I like it.

We built it by experimenting. However, after a while, it got to the point
where things are too complicated to add. We have an idea on how to do the next
step, but I (really, I) am not confident I can do it without throwing away all
the code and starting over.

Which is why, yes, we **will** throw most of that code away. But we will do it
in a very specific, controlled manner, and we will end up with a much better
thing in its place, without ever breaking it.

Welcome to the world of refactoring and testing.

I will show you how to use a tool called [pytest](https://docs.pytest.org/en/latest/)
and using it we will learn how to do incremental improvements with confidence
and radical changes without fear. Well, without too much fear.