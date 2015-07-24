---
layout: post
title: "Acrobat Reader - slim and sporty"
date: 2005-11-15
comments: false
---
Today I had to spend some time trying to slim Acrobat Reader down to it's
barest minimum in order for it to work. The resulting Reader had to be able to
do just 3 things. Open/display PDF files, allow for the searching of the open
PDF file, and print the PDF file. Anything else was verboten.

Thanks to google I found an abundance of ideas on how to get started in this
pruning but none really did a full job of pruning Reader 7.0x the following
steps get Reader to be as lightweight as I could.




  1. rename the optional directory to backup


  2. copy all plugins and folders from the plugins directory to the backup directory EXCEPT




* ESCRIPT



* EWH32



* Search


for ease of later undo create a plugins directory in the backup directory and
put all that stuff you just
moved into the plugins directory



  3. copy the javascripts directory to the backup directory then delete the websearch.js file from the origional javascripts directory


  4. copy the plugins3d directory to the backup directory then delete everything in the origional plugins3d directory


  5. copy the spplugins directory to the backup directory then delete everything in the origional spplugins directory


  6. move the updater directory to the backup directory


  7. move the browser directory to the backup directory


  8. move the websearch directory to the backup directory


  9. copy the files: AcroRd32Info.exe, AdobeUpdateManager.exe, reader_sl.exe, and Readme.htm to the backup directory



Now, Reader does just what I need it to do and nothing else. It also starts
REALLY FAST (between 0.5-2.0 seconds). Mission Accomplished.

However, even when Reader is this pared down it still has a memory footprint
of over 14MB! The freely available [Foxit
Reader](http://www.foxitsoftware.com/pdf/rd_intro.php) loads just as fast, has
no installation process, doesn't require any slimming down to get to this
point, and only takes up 5MB of memory.

The advantage for normal usage goes to Foxit. However, this exercise in
slimming down Acrobat Reader wasn't for normal usage. It is going somewhere
where the users can't launch a webbrowser and becuase I could remove the
plugins that affect web connectivity Acrobat Reader fits the bill nicely. I
still won't use it on my personal machine. But if you have no choice perhaps
these tips will help you get the most (or the least) out of Acrobat Reader.

## Comments

Anonymous

The newest version of Foxit (2.0) supports form filling and save

Anonymous

I started using foxit to and was going to install it on my parents pc then I
found out it doesn't support interactive forms. These are actually quite
commonly used for fill-it-in-print-it-out-sign-it-and-send-it-back type of
things, so can't recomend it for general use yet. I've just put acrobat 4.05
on and I'll give that and 7 a try and see which suits me best.

Bill

Get a Mac.. thats funny; a little expensive just to find a better pdf reader.

Foxit works perfectly for me. It is lightweight and loads fast. Plus it
required No installation.

Anonymous

get a mac, use preview instead.

