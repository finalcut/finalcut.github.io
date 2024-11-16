---
layout: post
title: "Pixelspace to Inkspace"
date: 2007-01-17
comments: false
category: c#
tags: [inkspace,pixelspace,printing,ink]
---
I am working on a Tablet PC application that has some printout's that take
data from a database and put it in a print template. One of the fields is a
users signature which is entered using the pen and "ink" and we need to print
the signature into a specific field on the template. However, the signature
control prints to a Graphics object using a measurement called "inkspace"
which isn't even close to pixel precision (which is how I put the rest of the
data on the printout template in precise locations).  

I tried using the Microsoft.Ink.Renderer.InkSpacePixel and PixelSpaceToInk but
it just didn't work out so well. Luckily, it turns out there is a conversion
ratio you can use to move from inkspace to pixelspace; 26.4. For each pixel
you need to multiply by 26.4 to move the same distance in inkspace.  

This works out great because my printout configuration (stored in an XML file)
is still measured in pixels - while the printing routine can do the correct
conversion for a signature field (multiple measurements by 26.4).  

So remember the magic number is 26.4.

## Comments

Doug

a bit more info...  

Ink uses Himetric units, which are resolution independent units defined as
1/1000 centimeters. The proper conversion number actually depends on the
resolution of your display.  

There are 2.54 centimeters in an inch, so on a display with 96 pixels per inch
(common) one pixel equates to 26.458333333333333... Himetric units.  
