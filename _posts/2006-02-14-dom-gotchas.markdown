---
layout: post
title: "DOM Gotchas"
date: 2006-02-14
comments: false
categories:
 - javascript
 - dom
 - ajax
---
In an effort to help others avoid the pitfalls I find I am detailing here two
trouble spots I recently ran into with Internet Explorer and The DOM.  
  
First look at this javascript:  
  
```js  
var obj = getObjectRefByID(someID);  
var tbl = document.createElement("table");  
var tr = document.createElement("tr");  
var td = document.createElement("td");  
var tn = document.createTextNode("This is a test");  
td.appendChild(tn);  
tr.appendChild(td);  
tbl.appendChild(tr);  
obj.appendChild(tbl);  
  
//purely for testing purposes  
alert(obj.innerHTML);  
  
```  
  
Why do you think the table wouldn't appear in the webpage within the element?
It's kind of sly why it doesn't. For further confusion add an
alert(obj.innerHTML) to the end of the code. You will see all the html needed
to render the table. What gives?  
  
```js  
var obj = getObjectRefByID(someID);**  
var tbdy = document.createElement("tbody");**  
var tbl = document.createElement("table");  
var tr = document.createElement("tr");  
var td = document.createElement("td");  
var tn = document.createTextNode("This is a test");  
td.appendChild(tn);  
tr.appendChild(td);  
tbdy.appendChild(tr);**  
tbl.appendChild(tbdy);  
obj.appendChild(tbl);**  
```  
  
You'll see I added a tbody element and now the table renders properly. Without
that IE won't display the table object I built up and inserted into the DOM.
This is a subtle addition but very important. Note: without the tbody object
the table was rendered fine in Mozilla browsers.  
  
Interestingly, according to the [HTML4
standard](http://www.w3.org/TR/html4/struct/tables.html#h-11.2.3) a tbody
isn't required within a table:  

>  
Table rows may be grouped into a table head, table foot, and one or more table
body sections, using the THEAD, TFOOT and TBODY elements, respectively. This
division enables user agents to support scrolling of table bodies
independently of the table head and foot. When long tables are printed, the
table head and foot information may be repeated on each page that contains
table data.  

  
  
This next one is pretty subtle too and again only occurs in Internet Explorer
(as far as I know).  
  
```js  
var obj = getObjectRefByID(someID);  
var cbx = document.createElement("checkbox");  
cbx.type = "checkbox";  
cbx.id = "myCBX";  
cbx.setAttribute("checked","checked");  
obj.appendChild(cbx);  
  
// for debugging purposes  
alert(cbx.checked);  
```  
  
You will noticed I set the checked status on the checkbox. But when IE renders
that code the checkbox is unchecked. But when I do the alert it tells me true.
What the...? Well, it turns out IE's rendering doesn't care what I do to the
checkbox before I insert it into the document. IE only reflects those changes
made after the insertion - so the order of events has to be as follows:  
  
```js  
var obj = getObjectRefByID(someID);  
var cbx = document.createElement("input");  
cbx.type = "checkbox";  
cbx.id = "myCBX";  
obj.appendChild(cbx);  
cbx.setAttribute("checked","checked");  
```  
  
One more thing related to that last example. You need to assign the type to
the object before you insert it into the document or else IE will complain and
show a text element instead of a checkbox. My natural inclination was to fully
prepare the object before I inserted it into the document which was almost
correct except for that checked attribute. Again, the first code sample worked
flawlessly in Mozilla.  
  
Wierd stuff to be sure. They are also highly annoying and can be difficult to
debug since IE tells you everything you did is correct. Hopefully these two
"gotchas" won't get you!

## Comments

Bill

rejitha,  
  
No suggestions really. I imagine there may be some security implications with
inserting an iframe into a webpage dynamically since the iframe can load
content from a remote site.

rejitha

# td.appendChild(iframe); //does not work.. any clues or tips..

Zecc

No one said it yet, but the checked/defaultChecked thing applies to radio
buttons too (at least in IE6).  
  
Edit: ok, so Pramod Biligiri did mention it. Still, I confirm.

Anonymous

Another way to set events effectively in IE is to do the following:  
  
var myLink = document.createElementById("a");  
myLink.onClick = "alert('test')";  
  
document.body.appendChild(myLink);  
document.body.innerHTML = document.body.innerHTML;  
  
I suppose you could also use myLink.parentNode.innerHTMl =
myLink.parentNode.innerHTML

Anonymous

Thank you for explaining the strange rendering behavior requiring tbody tags
to be present within tables inserted via DOM nodes in IE.  
  
You have saved me from pulling out the little remaining hair I have left.

Alan

Thank you. You saved much anguish!

Rex

As you've noticed, there are a tonne of issues with IE, and creating elements,
and setting attributes, and events. (yikes!)  
  
For some additional info on these bugs (and many others) check out this blog
for tracking browser bugs.  
  
http://webbugtrack.blogspot.com/2007/08/bug-242-setattribute-doesnt-always-
work.html

smileyriley

Thanks so much, I tend to code for firefox first, and then look at IE issues.  
  
Reading this post solved all issues and im now a happy chappy.  
  
Cheers

Anonymous

Can I just add to what most of the others above me said..  
**THANK YOU!!!**  
The table not displaying in IE got me for a few hours, I'm away from the
machine I was coding it on, but was thinking I'd end up adding thead, tbody
and tfooter and see what happened. Now I know it's going to work when I do!
Yey!  
  
Steve Daniels

Anonymous

to make  
  
inp1[onclick] = function () {alert("hello");};  
  
work in the ie I had to add "  
  
inp1[**"**onclick**"**] = function () {alert("hello");};  
  
thanks though - saved me a lot of time

Anonymous

thank you _thank you_ **thank you**

Anonymous

Awesome! Googled on the IE table problem.. but didn't expect to find
anything.. thanks soooo much.  
but please fix the code.. noticed the same as others.. have to add the row to
the Tbody, then to the Table.

Anonymous

I was going thru this, Seems ok and i have done the same. For me I have added
row to a table , 5 new cells and in cells select boxes are there.  
now  
1\. rows are created.  
2\. Select box is created  
3\. methods does work on select box change.  
  
but when I submit the form i do not get values for newly created rows on
firefox. where as in IE i do get values. suppose there were 2 rows when page
was loaded now if i add 2 more... IE will show 4 as total on server side and
firefoxwill still show only 2 in struts form (server side).. If i add alert
before submit firefox does show 4 as total length of table... no idea what's
going wrong.

Anonymous

i just came across a similar issue when setting col widths on the table:
<col width="10%"> for instance. I was appending them to the table
element. However, IE wont render until you have created a "colgroup" (appended
to table) and append all the col elements to this. Not sure what the spec
says, but Firefox didn't seem to mind either way :-)

Anonymous

Thank you very much!  
I lost hours trying to get that checkbox checked.  
  
GhoulLord

radicalbright

thanks for the help. ie resets checkboxes when they are added. why why why????
hahahaha

bawb

Thank you. Very helpful.

Bill

thanks, it is now fixed. odd I didn't notice that before. Thanks again!

Anonymous

Regarding Hemant's comment, the code in your original post is still  
  
var cbx = document.createElement("checkbox");  
  
(Might want to edit that.)

Bill

Feel free to post your comments here JiYung. The conversation will be a little
slow (due to comment moderation) but this is a good place to address issues
with dynamic table creation.

JiYung

**yes, it did.  
thanks bill.**  
i hate IE how IE is so different  
i'm trying to build a dynamic table creater.which can contain general input
elements.  
i had encountered a lot of strang problems on making it compatible with IE.  
some of them ware solved , some ware not. i wonder can we discuss them on this
post.  
they may make the post going to far

Bill

Jiyung,  
  
You can specify the element name as so:  
  
inp1.name ="list";  
  
that will work in opera, firefox, and ie.

JiYung

i finally found that change the following code:  
**  
inp1.setAttribute("onclick",'alert("hello");'); **  
  
to this:  
**inp1[onclick] = function () {alert("hello");};  
**  
will work well in IE  
  
but i found anothor problem in IE  
either this line  
**inp1.setAttribute("name","list"); **  
or this line  
**inp1[name]="list";**  
doesn't make sense to IE  
how to specify the element's name in javascript

JiYung

thanks for nice guide.  
i've tried to insert some dynamic  
generated javascipt in dom  
like the code shows below  
(i simplied the problem by using a alert function)  
  
  
var table1 = document.getElementById("tbody1");  
var row = document.createElement("TR");  
var cell1 = document.createElement("TD");  
var inp1 = document.createElement("INPUT");  
inp1.setAttribute("type","button");  
inp1.setAttribute("name","list");  
inp1.setAttribute("value","hello");  
**inp1.setAttribute("onclick",'alert("hello");'); **  
cell1.appendChild(inp1);  
row.appendChild(cell1);  
table1.appendChild(row);  
  
  
the code did work in firefox 1.5x and opera 8.5x.  
but IE seams not working well.  
how do I apply this In IE?  
thanks for any suggestions.

JiYung

thanks for the nice guide.  
i've tried to insert some dynamic  
generated javascipt in dom  
like the code shows below  
(i simplied the problem by using a alert function)  
  
_  
var table1 = document.getElementById("tbody1");  
var row = document.createElement("TR");  
var cell1 = document.createElement("TD");  
var inp1 = document.createElement("INPUT");  
inp1.setAttribute("type","button");  
inp1.setAttribute("name","list");  
inp1.setAttribute("value","hello");  
**inp1.setAttribute("onclick",'alert("hello");'); **  
cell1.appendChild(inp1);  
row.appendChild(cell1);  
table1.appendChild(row);  
_  
  
the code did work in firefox 1.5x and opera 8.5x.  
but IE seams not working well.  
how do I apply this In IE?  
thanks for any suggestions.

Bill

good point Jeff. I never really read it that way but perhaps that is how it
was meant to be read.  
  
  
Thanks for the alternate way of looking at it.

Jeff

To be fair, the spec says "one or more" tbody elements may be used in a table.
It does not specifically say a table can be devoid of a tbody element.

vsumner

className is cross browser  
  
class is not

Aaron Averett

Dude, you are _the man_! I just wasted like four hours on the non-displaying-
table nightmare.  
  
You have a mistake in your example code, though. You have to append the tbody
element as a child of the table, and then append the table as a child of obj,
or it still doesn't display.  
  
It should look like this, I think. (Changed parts are in bold)  
var obj = getObjectRefByID(someID);  
var tbdy = document.createElement("tbody");  
var tbl = document.createElement("table");  
var tr = document.createElement("tr");  
var td = document.createElement("td");  
var tn = document.createTextNode("This is a test");  
td.appendChild(tn);  
tr.appendChild(td);  
tbdy.appendChild(tr);  
**tbl.appendChild(tbdy);**  
obj.appendChild(**tbl**);

Ahmader

Bill, man million of thanks i was not only pulling my hair out but i was going
to cut my self body aparts this DOM is getting me crazy specialy making it
working for both Mozilla and IE.  
  
one more tip FLOAT guyz any one had trouble with them !!  
  
IE only accept  
obj.style.styleFloat  
  
and mozilla  
obj.style.cssFloat  
  
I dont know why desktop developers just hate web developers I am spending days
to find out bug or stuff that for no sence. Thanks millions again

Anonymous

That checkbox thing (IE resets the value of "checked" upon insertion) is
incredibly annoying. Of course, if you're building a large-ish amount of HTML
using DOM methods, setting it after insertion might be a cumbersome hack...
one way to work around it in IE is to set the "defaultChecked" property; IE
will honor this after insertion and set the checked property correctly.

Anonymous

thanks a lot man !! i was getting crazy trying to display dynamic tables.

Anonymous

Thanks alot. Wasted 4 hours trying to get the dynamic rows to show up in IE.

Anonymous

The TBODY stuff has also to be considered when adding rows to an existing
table. Rather than appending it to the table itself ist has to be appended to
the table's firstChild (which is in fact the TBODY).  
  
Thanks for the tip.

Anonymous

Thanks man, I was looking for this information:  
  
'You need to assign the type to the object before you insert it into the
document or else IE will complain and show a text element instead of a
checkbox.'  
  
Many many thanks! :)

Bill

Thanks Pramod for the tip

Pramod Biligiri

I just wasted some time on the same problem.  
I found you can use the "defaultChecked" attribute to check checkboxes and
radio buttons. This works even when the created DOM node is free-standing and
not yet appended to the DOM.  
Eg: node.defaultChecked = true;  
  
See http://channel9.msdn.com/wiki/default.aspx/Channel9.InternetExplorerProgra
mmingBugs  
and http://www.w3.org/TR/DOM-Level-2-HTML/html.html#ID-20509171

Bill

I am not sure how your attempting to set the attributes. Typically there are
two ways - directly or by using the setAttribute method of the object.  
  
For instance if you want to set a tds class you can do this:  
  
...  
myTd = document.createElement('td');  
myTableRow.appendChild(myTd);  
myTd.className = 'someClassName'  
  
OR  
...  
myTd = document.createElement('td');  
myTableRow.appendChild(myTd);  
myTd.setAttribute("class","someClassName");  
myTd.setAttribute("className","someClassName");  
  
  
In my second example I set both the class and className attribute simply
because I can't remember which one works in both browsers. (but one of them
does).

Rob Welbourn

I, too, was pulling my hair out over the TBODY issue in IE -- thanks for the
tip. Alas, IE stubbornly refuses to act on attribute settings to elements
within the table, even when I set them after the table has been inserted into
the document. With Firefox, setting the attributes either before or after the
elements have been inserted works just fine.  
  
In my case, I'm attempting to apply formatting to my table TDs by means of
classes linked to a stylesheet, and to set an 'onclick' handler for each of
the TDs.  
  
Any thoughts on this issue?  
  
Rob

Bill

yes I have an idea.  
  
You should change your function like so:  
  
var cbx = document.createElement("checkbox");  
  
to  
  
var cbx = document.createElement("input");  
  
you are creating an input element and then making it of type "checkbox" you
have the type setting correct - but the object creation incorrect.

Hemant

Hi followed your suggestions to create checkboxs as follows  
  
function createCheckBox(NODE, id, value) {  
var cbx = document.createElement("checkbox");  
cbx.type = "checkbox";  
cbx.id = id;  
cbx.value = value;  
NODE.appendChild(cbx);  
}  
  
but still get a text element instead of a checkbox.  
  
any ideas?

Bill

no problemo - that's why I posted it so other's wouldn't have to go as crazy
as I did :O)

Jack Killpatrick

It ended up being something about the browser session I was still in. I
probably messed with things so much during dev that the browser was a bit
freaked out. When I closed all browser instances and restarted the browser
that issue went away. Whew~!  
  
Thanks again for the TBODY tip, that was making me nuts!

Bill

off the top of my head no. I vaguely remember encountering this before though.  
  
the only way I could probably answer it is to look at the problem again and to
tool around with the code to try and get something to happen.

Jack Killpatrick

Thanks for the info about IE and TBODY, I was pulling my hair out trying to
figure out why my dynamically created table rows would not display in IE, even
though the innerHTML necessary was present.  
  
However, I have another related problem... maybe you know the answer to? When
the table displays, IE only displays the parts of the table that exist inside
the viewport of the browser, not the right-hand scrollbar nor rows that are
partially "below" the viewport. Only if I resize the browser will the right-
hand scrollbar and the rest of the table appear. Any suggestions? In Firefox
1.5 it all works fine.

