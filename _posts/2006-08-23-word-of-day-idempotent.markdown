---
layout: post
title: "Word of the Day Idempotent"
date: 2006-08-23
comments: false
---
It is rare that I encounter a word that I am completely unfamiliar with and
based on it's usage I still can determine it's meaning. However, today I must
admit that I encountered such a word - Idempotent.


Now, as a person with a computer science degree and around 7 years of on the
job experience it seems kind of odd to me that I haven't heard this word
before. I encountered it for the first time today while reading a [white paper
published by Google dealing with their MapReduce
library](http://static.googleusercontent.com/media/research.google.com/en//archive/mapreduce-osdi04.pdf). (warning, pdf)


I've recently seen a few
[notable](http://joelonsoftware.com/items/2006/08/01.html)
[people](http://feeds.feedburner.com/~r/raganwald/~3/15443434/anything-
ridiculously-easy-is-going-to.html) discussing MapReduce and decided I'd like
to know more about it. Nestled down in section 4.5 is this mysterious word.
Thankfully, with Google's help, I was quickly able to find a nice succinct
definition of the word.



Idempotent



[from mathematical techspeak] Acting as if used only once, even if used multiple times. This term is often used with respect to C header files, which contain common definitions and declarations to be included by several source files. If a header file is ever included twice during the same compilation (perhaps due to nested #include files), compilation errors can result unless the header file has protected itself against multiple inclusion; a header file so protected is said to be idempotent. The term can also be used to describe an initialization subroutine that is arranged to perform some critical action exactly once, even if the routine is called several times. [Source](http://www.catb.org/jargon/html/I/idempotent.html)


So, it would seem, that the creation of a Singleton is an idempotent action.

## Comments

Anonymous

also try Nilpotent or nilpotence
