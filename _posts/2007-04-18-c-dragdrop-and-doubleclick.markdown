---
layout: post
title: "C# - DragDrop and DoubleClick"
date: 2007-04-18
comments: false
categories:
 - doubleclick
 - dragdrop
 - c#
---
I was working on a simple custom control today that displays thumbnails. The
thumbnail ordering can be changed by dragging/dropping and you can double
click a thumbnail to have a full version of the image pop up in a new dialog.
Pretty simple - or is it?

It turns out that the DragDrop functionality is turned on for an object during
the MouseDown event. However, when you double click the MouseDown event is
also fired and thus the app thinks you are dragging after the first click and
the DoubleClick event won't get fired. What's a coder to do?

I looked all over for an idea and the best anyone could suggest was combining
MouseDown (set a flag) with MouseMove (start DragDrop if flag is set) to start
the DragDrop. This doesn't work too well though if you do a mouseup outside
the app (and then drag the mouse back in in the up or down state).

It turns out though that there is a easy and pretty clean solution. The
MouseDown event passes along a collection of MouseEventArgs. One of those
values is "Clicks" that tells you how many times the mouse was clicked. The
event gets called once for a click and again for a double click. So when you
double click it calls MouseDown twice. The first time it "enter drag mode" but
as soon as you raise the button to click the second time it exits drag mode.
The second mousedown has a "Clicks" value of 2 and you can avoid going into
drag mode and thus the DoubleClick will be fired.


```c#
void pictureBox_MouseDown(object sender, MouseEventArgs e)
{
if (e.Button == MouseButtons.Left && e.Clicks ==1)
{
PictureBox pb = (PictureBox)sender;
DoDragDrop((ImageData)pb.Tag, DragDropEffects.Copy);
}
}


```


In the prior example I only want to enter Drag mode if the left button is
clicked AND it was only clicked one time. I couldn't find this information
anywhere else so hopefully this post will help someone.

## Comments

Anonymous

Thanks, concise and to the point.
Saved me some time suckage!

Anonymous

Let's see .. it's 2:01 CST August 20, 2012 WAY in the future.
Thanks. Looking forward to your next big thing.

Little

It works perfectly. Thanks!

Anonymous

Many thanks!!

Anonymous

THC! Even better than THX!

Crazistor

I had to port my application from Lazarus to C# and you saved me a lot of time
with this nice solution. Many thanks!

Crazistor

I had to port my application from Lazarus to C# and you saved me a lot of time
with this nice solution. Many thanks!

Eric Enright

Thank you for taking the time to post this snippet. It is exactly the solution
I was looking for.

Anonymous

This saved me some time also. Thanks

Anonymous

4.5 years later, folks are still thanking you for posting this. I guess you
hit that nail on the head, huh? :)

Duncan

PS: thanking you for posting this!

Anonymous

Thanks, just what I needed. :D

Anonymous

Thanks a lot - this one was really bothering me... :-/

Anonymous

SUPER tip !!!

Thanks,
Eddy.

Anonymous

Thanks ! Really :)

Anonymous

easy and works thx

Paul Buisman

Thank you. Solved the problem for me too :-)

Anonymous

thank you !

Anonymous

Again - thanks. One comment. If for any reason it doesn't work haev a look to
ensure that the clickable item is set as AllowDrop. I needed to do this
otherwise a double click would treat the item as being dropped onto itself and
funny things happened if it wasn't itself set as AllowDrop.

Bill

To all the thanks - You're welcome. Glad to help!

Ali Koyuncu

Thank you, dude. You savde my day.

Anonymous

Just what I needed !

Anonymous

**Excelente! Gracias!**

chuvahin

Thanks. Very helpful

heringer

Thanks!

LambyPie66

Just what I needed and a great explanation - thankyou

sbetberg

Thank You

sbetberg

Thanks

sbetberg

Thank You

steve

Works great. Just had this problem today. ty

Mike

Thanks for the help with this. Unfortunately I still couldn't get it to work
in my TreeView. In fact, it even stopped triple-clicking from invoking the
ItemDoubleClick event, which had worked in the past. Maybe I have a strange
combination of other things also interfering like AfterSelect events and so
on.

For anyone having similar problems to me, though, I did find [another
workaround](http://social.msdn.microsoft.com/forums/en-
US/winforms/thread/0b756636-0acb-4972-9fb8-00627cb9f764/) where someone has
suggested making the DoDragDrop() call from the .ItemDrag() event instead of
from the MouseDown() event. Perhaps this just ensures the user is actually
trying to drag it beforehand, or something like that.

It seems to work perfectly for me, at least.

Anonymous

thanks :)

Anonymous

Sometimes it's the little things in life that mean a lot ....

Thank you!

Anonymous

Thanks a lot!!!!

jabbot

Wow, you are a life saver. Ever so simple to think about it. You've saved me
hours!

Anonymous

Very nice and elegant solution that works :-)

Anonymous

Top stuff. Thanks!

Anonymous

Looked Everywhere for this. Worked like a charm! Thanks!

Dima

1) Thanks for the post!

2) Anonimous - Mouse DoubleClick fires 2 events - one with Clicks==1 and one
with Cliks==2.
if you put a break point in MouseDown event, then VS2008 will jump on the
first click and second will never happen.
Try to set a breakpoint with Condition "e.Clicks == 2".

Bill

I have no idea. I still use VS 2005 and have not had a chance to try out any
code in VS 2008.

It seems unlikely that the drag and drop and double click behavior would
change so much but it is possible.

Anonymous

This doesn't work for me. I'm using Visual Studio 2008, and every time I
double-click, the MouseDown event always fires with a Clicks == 1.

Could it be that this behavior has changed with VS2008?

Anonymous

thanks!!!!

alexz

Nice solution, thanks!

Richard Potter

Was worried about this - thanks for such an elegant solution

Andreea

Thank you so much !!

Anonymous

Thanks this is great..Keep up the good work!!

james

Thanks, solved a big headache!

Anonymous

Thanks!

Anonymous

Perfect, fast, complete solution to my exact problem. Lots of time saved

Anonymous

Brilliant idea!

Anonymous

Great work. Thanks.

Anonymous

Great !!

Anonymous

Many thanks! I had the same problem, this worked perfectly.

Anonymous

Thanks!!

Mike Lasseter

thanks. this saved my some time googling

