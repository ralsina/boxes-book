# Introduction

This book tries to achieve only one thing:

Show you a project go from **nothing** to **good**.

By nothing I mean, no code at all. Not even a fleshed idea of what it does. No
goals, no committments. Just a vague interest.

And by good I mean it will work, it will have tests, it will be available to
use, it will be **useful** and be a real thing.

Think of it as a sort of documentary on the beginnings of a rock band, only
instead of rockers there is a single overweight argentinian dev, and instead
of a band there is a piece of software.

So, not much like a documentary on the beginnings of a rock band.

## Target Audience

To get the most benefit from this book I expect the reader to have a basic
knowledge of the Python programming language. Knowing and
understanding the contents of the official 
[Python Tutorial.](https://docs.python.org/3/tutorial/) should be enough to be
able to follow all the code in the book, which has been kept as simple as
possible.

Readers with deeper knowledge of the language or more extensive programming
experience may still benefit from it but will find a lot of the first part
boring.

## Requirements

You can try to follow the book by just reading it but that is probably not the
best idea. Actually running the example code is educational. Modifying it
even more so.

So, you will need a working python interpreter.
The examples have only been tested on Linux. I suppose before calling this
book "finished" I will have to make them work on Windows and/or OSX somehow.

Each one of the larger parts of te book requires a separate development 
environment and has a "Chapter 0" about setting it up.

> ### How the book is built
> 
> * It's written in markdown
> * The sections with code are fed to [pyliterate](https://github.com/bslatkin/pyliterate) and its output is built into a "book" by [mdbook](https://github.com/rust-lang-nursery/mdBook)
> * The code uses a ton of things, links are provided in the [Dependencies Appendix](dependencies.html) 
> * All the code and text for the book is available in a [gitlab repo](https://gitlab.com/ralsina/boxes-book) and it's published and updated at [https://ralsina.gitlab.io](https://ralsina.gitlab.io/boxes-book/)
