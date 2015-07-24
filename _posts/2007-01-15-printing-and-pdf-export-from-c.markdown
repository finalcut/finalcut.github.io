---
layout: post
title: "Printing and PDF Export from C#"
date: 2007-01-15
comments: false
categories:
 - wordwrap
 - graphics
 - c#
 - printing
 - linewrap
---
Today I was working on a pretty simple C# project that involves printing out
potentially long strings into small constrained areas (in a printable report).
I am pretty new to C# and don't have a deep knowledge or familiarity with the
language so I wasn't really sure where to begin beyond the Graphics library.

As it turns out the task was easier than I first envisioned. I had thought I
was going to have to chop my text string up into little strings based on the
MeasureString method and then determine where words ended and do the line-wrap
that way. Fortunately, it is substantially easier; almost so easy that I could
feel guilty.

Each of the fields I need to print out is defined in an XML file - a file
which I defined so that each field had an x and y coordinate for where it
needed to be on the page. To make this technique work I just had to add a
height and width attribute and I was good to go:


```c#
Font typeFace = new Font("Arial", 7, FontStyle.Bold)

float x = float.Parse(element.Attributes["x"].Value);
float y = float.Parse(element.Attributes["y"].Value);
float width = float.Parse(element.Attributes["width"].Value);
float height = float.Parse(element.Attributes["height"].Value);
RectangleF rect = new RectangleF(x, y, width, height);

using (StringFormat formatter = new StringFormat())
{
formatter.FormatFlags = StringFormatFlags.LineLimit;
graphics.DrawString(text_to_print, typeFace, Brushes.Black, rect, formatter);
}

```


I've kind of picked apart my code to just give you the relevant bits.
Hopefully it is enough to give you an idea. The key to this trick was the
StringFormat class. I told it to use the LineLimit [StringFormatFlags
enumeration](http://msdn2.microsoft.com/en-
us/library/system.drawing.stringformatflags.aspx).

Overall it was a surprisingly painless process. Of course, when I was done
with that I needed to be able to export the printout to PDF if the user
decided so I dipped into the freely available package
[PDFSharp](http://www.pdfsharp.com). It seems to be a great package and has
plenty of examples to get you going.

