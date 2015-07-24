---
layout: post
title: "Calculating a Discreet Date Difference (C# Sample Code)"
date: 2007-09-03
comments: false
categories:
 - .net
 - datetime
 - c#
 - utility
---
I recently had to figure out how to display the exact difference in Years,
Months, and Days between two distinct dates. Here is my solution. A slightly
more useful return type would probably be a fixed 3 element array with {Y:M:D}
and then you could do what you wanted with the numbers. However, for the
moment this solution serves a good job of illustrating how it works.

  
```cs  
private static string DateDiffAsString(DateTime inDate1, DateTime inDate2)  
{  
int y = 0;  
int m = 0;  
int d = 0;  
  
//make sure date1 is before (or equal to) date2..  
DateTime date1 = inDate1 <= inDate2 ? inDate1 : inDate2;  
DateTime date2 = inDate1 <= inDate2 ? inDate2 : inDate1;  
DateTime temp1;  
  
if(DateTime.IsLeapYear(date1.Year) && !DateTime.IsLeapYear(date2.Year) &&
date1.Month == 2 && date1.Day == 29){  
temp1 = new DateTime(date2.Year, date1.Month, date1.Day-1);  
} else {  
temp1 = new DateTime(date2.Year, date1.Month, date1.Day);  
}  
  
y = date2.Year - date1.Year - (temp1 > date2 ? 1 : 0);  
m = date2.Month - date1.Month + (12 * (temp1 > date2 ? 1 : 0));  
d = date2.Day - date1.Day;  
if (d < 0)  
{  
if (date2.Day == DateTime.DaysInMonth(date2.Year, date2.Month) && (date1.Day
>= DateTime.DaysInMonth(date2.Year, date2.Month) || date1.Day >=
DateTime.DaysInMonth(date2.Year, date1.Month)))  
{  
d = 0;  
}  
else  
{  
m--;  
if (DateTime.DaysInMonth(date2.Year, date2.Month) ==
DateTime.DaysInMonth(date1.Year, date1.Month) && date2.Month != date1.Month)  
{  
int dayBase = date2.Month - 1 > 0 ? DateTime.DaysInMonth(date2.Year,
date2.Month - 1) : 31;  
d = dayBase + d;  
}  
else  
{  
// d = DateTime.DaysInMonth(date2.Year, date1.Month) + d;  
d = DateTime.DaysInMonth(date2.Year, date2.Month == 1 ? 12 : date2.Month - 1)
+ d;  
}  
}  
}  
  
string ts = "";  
  
if (y > 0)  
ts += y + "y ";  
if (m > 0)  
ts += m + "m ";  
if (d > 0)  
ts += d + "d ";  
  
return ts;  
}  
```

## Comments

Anonymous

Thanks to help me to calc. date Diff.

Bill

Sadly, I don't really have time to test your VB port but I did add a new test
case to my suite:  
  
[Test]  
public void ComputeTenor19()  
{  
DateTime refDate = new DateTime(2009, 9, 14);  
  
DateTime date1 = new DateTime(2010, 9, 13);  
DateParts expected1 = new DateParts(0, 11, 30);  
DateParts actual1 = DateHelper.DateDiff(refDate, date1);  
Assert.AreEqual(expected1, actual1, "19\. actual19: " \+ actual1.ToString() +
" != expected19: " \+ expected1.ToString());  
}  
  
  
  
And this test passes as expected (showing a difference of 11mos and 30 days.  
  
Have you stepped through to see how it is coming up with a number not between
1 and 12?

Anonymous

I've had to convert it into VB. Here is the exact code:  
StartDate: Sept 14, 2009  
Enddate Sept 13, 2010.  
  
error: "Month must be between one and twelve. Parameter name: month"  
  
Private Shared Function DateDiffAsString(ByVal inDate1 As DateTime, ByVal
inDate2 As DateTime) As Double  
Dim y As Integer = 0  
Dim m As Integer = 0  
Dim d As Double = 0  
  
'make sure date1 is before (or equal to) date2..  
Dim date1 As DateTime = If(inDate1 <= inDate2, inDate1, inDate2)  
Dim date2 As DateTime = If(inDate1 <= inDate2, inDate2, inDate1)  
  
Dim temp1 As DateTime  
  
If DateTime.IsLeapYear(date1.Year) And Not DateTime.IsLeapYear(date2.Year) And
date1.Month = 2 And date1.Day = 29 Then  
temp1 = New DateTime(date2.Year, date1.Month, date1.Day - 1)  
Else  
temp1 = New DateTime(date2.Year, date1.Month, date1.Day)  
End If  
  
y = date2.Year - date1.Year - (If(temp1 > date2, 1, 0))  
m = date2.Month - date1.Month + (12 * (If(temp1 > date2, 1, 0)))  
d = date2.Day - date1.Day  
  
If d < 0 Then  
If date2.Day = DateTime.DaysInMonth(date2.Year, date2.Month) AndAlso _  
(date1.Day >= DateTime.DaysInMonth(date2.Year, date2.Month) OrElse _  
date1.Day >= DateTime.DaysInMonth(date2.Year, date1.Month)) Then  
d = 0  
Else  
m = m - 1  
If DateTime.DaysInMonth(date2.Year, date2.Month) =
DateTime.DaysInMonth(date1.Year, date1.Month) And date2.Month <>
date1.Month Then  
Dim dayBase As Integer = If(date2.Month - 1 > 0,
DateTime.DaysInMonth(date2.Year, date2.Month - 1), 31)  
d = dayBase + d  
Else  
  
d = DateTime.DaysInMonth(date2.Year, date2.Month = IIf(1, 12, date2.Month) -
1) + d  
  
  
End If  
End If  
End If  
  
  
  
Dim result As Double = 0  
  
If y > 0 Then  
result += y * 12  
End If  
  
If m > 0 Then  
result += m  
End If  
If d > 0 Then  
result += d / System.DateTime.DaysInMonth(System.DateTime.Now.Year,
date2.Month)  
End If  
  
Return result  
End Function

Bill

When I get a chance I'll throw your example into my test cases but I don't
know why your getting a problem.  
  
Can you provide the exact code you used when calling the method? thanks

Anonymous

This is great.. I don't know if it's just me, but I'm getting an error "Month
must be between one and twelve. Parameter name: month" when I compare start:
Sept 14, 2009 with end date Sept 13, 2009. It errors on  
"d = DateTime.DaysInMonth(date2.Year, date2.Month == 1 ? 12 : date2.Month - 1)
+ d;"

Anonymous

Thanks for nice article.

Bill

I just posted a minor update to the function. There was a problem if date1 was
a leapday (feb 29) but date2.year wasn't in a leap year when computing the
value "temp1".

Bill

how about you just email me? My name is bill rawlinson and my email account is
at gmail.  
  
just put a period between my first and last names and the email should get to
me.  
  
The test cases are pretty lengthy and I don't want to fill up the page with
them all.  
  
Thanks  
Bill

Garowetz

I just came up with another algorithm that makes the code a lot simpler, I
think!  
  
Can you post your test cases and answers for me to test against. I've done
preliminary testing but I want to run by some more examples.  
  
Thanks

Bill

the version of the code I had here seemed a little outdated based on what I
have in my utility class so I reposted the entire method with this change.  
  
There were quite a few differences but this is the one that passes all of my
unit tests.

Bill

sweet - your suggested change not only worked but it found a flaw in one of my
other unit tests (where my own math had been incorrect).  
  
Now all 18 of my unit tests pass  
  
I'll update my post accordingly. Thanks

Bill

thanks for the dates - i tried all three and the first one failed my unit
tests.  
  
I'll try your suggested change and see what happens.

Garowetz

I tried to post last night but don't know if it got through...  
  
This could also be a logic error on my part converting back and forth between
Javascript.  
  
Here are the dates I'm using (yyyy,mm,dd):  
2006-02-17 to 2008-02-06 = 1y 11m 20d  
2007-12-25 to 2008-02-06 = 0y 01m 12d  
2008-02-06 to 2009-05-23 = 1y 03m 17d  
  
I also confirmed these with an excel sheet that I created using the
"datediff()" function.  
  
let me know what you think.

Bill

Can you give me some date examples where you don't think it is working
properly?  
  
I have a suite of unit tests I run against this and knowing which dates you
have found aren't working would help me test it again - and to make sure any
changes don't break anything else.  
  
Thanks

Garowetz

I'm having a little trouble with the algorithm now!! ... And I think it all
revolves around the last line of the code:  
  
  
d = DateTime.DaysInMonth(date2.Year, date1.Month) + d;  
  
  
It's the second argument that I'm having trouble with, it's giving me the
wrong number of days. I changed it so that it was calculating the month before
date2.Month so it would be like (I'm trying to convert this logic back from
Javascript):  
  
  
d = DateTime.DaysInMonth(date2.Year, date2.Month == 1 ? 12 : date2.Month - 1)
+ d;  
  
  
I think that's how it's supposed to be written. Anyhow, when I do this it
seems to work better correcting some dates when they are off.  
  
I'm using a calculator and pencil as well as the site below to verify.  
  
[timeanddate.com](http://www.timeanddate.com/date/duration.html)  
  
Let me know what you think.

Bill

Cool - I'm glad you were able to use it. It's always nice to know I was able
to help someone, and it's even better when I find out they are passing along
the help.  
  
If you happen to comeback feel free to put a link to your javascript version
here in the comments so others can find it.

Garowetz

Hey just wanted to say thanks for the algorithm. It was exactly what I was
looking for and saved me a bunch of time. I've now implemented it in Java
script. (with a pointer back to this page!)  
  
Thanks  
  
:)

Bill

No, because when calculating the days difference you can see I use the later
dates year..  
  
I have actually tested this quite a bit and it seems to work regardless of the
dates I pass in.  
  
However, if you use it and come across a date that gives invalid results
please let me know so I can re-evaluate it.  
  
Thanks

Flashsnake

Any problem when dealing with Leap Year?

