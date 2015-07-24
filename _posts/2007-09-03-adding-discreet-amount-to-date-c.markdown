---
layout: post
title: "Adding discreet amount to a Date (C# example)"
date: 2007-09-03
comments: false
categories:
 - .net
 - datetime
 - c#
 - utility
---
In my last post I talked about getting the number of years, months, and days
between two dates. Today I'll show how to go the other way, take a date and
add years months and days to it to get a date.

  

The only assumption here is that you are passing in a relDate string in a
format like so: "1y 2m 3d" or any subset of that such as "1y 3d" or "2m 3d" or
even just "1y" or "3d" etc.

  

  
The Microsoft DateTime object has a nice AddYears, AddMonths, and AddDays
method but there is a little catch to using them. You have to add from
smallest to largest date unit. If you do it the other way around you will get
inconsistent results. Here is some sample code that also includes some
examples of inconsistent results if you add in the wrong order. NOTE: these
examples use a "RelativeDateTimeException" which is a custom class I wrote -
you should provide your own exception handling.  

  
```cs  
public static int ParseRelativeDateToNumDays(string relDate, DateTime refDate,
int maxRange)  
{  
int invalidDayCode = -99999;  
int numDays = invalidDayCode;  
DateTime baseDate = refDate;  
  
if (relDate != null)  
{  
try  
{  
string stringToParse = relDate.Trim();  
if (stringToParse.Length > 0)  
{  
string pattern = @"^-?((\d+)\s*y)?\s*((\d+)\s*m)?\s*((\d+)\s*d)*$";  
Match match = Regex.Match(stringToParse, pattern);  
  
Group yearGroup = match.Groups[2];  
Group monthGroup = match.Groups[4];  
Group dayGroup = match.Groups[6];  
  
  
if (yearGroup.Success || monthGroup.Success || dayGroup.Success)  
{  
int yearPart = yearGroup.Success ? Int32.Parse(yearGroup.Value) : 0;  
int monthPart = monthGroup.Success ? Int32.Parse(monthGroup.Value) : 0;  
int dayPart = dayGroup.Success ? Int32.Parse(dayGroup.Value) : 0;  
  
if (stringToParse.ToCharArray()[0] == '-')  
{  
yearPart = -yearPart;  
monthPart = -monthPart;  
dayPart = -dayPart;  
}  
  
/* the larger units need to be added first or else  
* the result will be different (and wrong) since we are  
* trying to get the number of days from refDate and not refDate+days..  
* for instance lets say the refDate = 31 Aug 2007 and you wanted to add  
* in the order: days, months, years the answer for the following scenarios  
* would be:  
* 1. +6m = 29 Feb 2008  
* 2. +5m 29d = 29 Feb 2008 (feb has 29 days in 2008 leap year and all)  
* 3. +5m 30d = 29 Feb 2008 (what? well Sep 30 2007 + 5m = feb 29 2008)  
*   
* now if you added in years, months, days..  
* 1. +6m = 29 Feb 2008  
* 2. +5m 29d = 29 Feb 2008  
* 3. +5m 30d = 01 Mar 2008  
*   
* Ah, but what happens then, in this case if we are adding 1 year + 6m?  
* if we add in days, months, years:  
* 1. +ly 6m = 28 Feb 2008  
* 2. +1y 5m 28d = 28 Feb 2008  
* 3. +1y 5m 29d = 28 Mar 2008 (wrong again)  
*  
* * if we add in years, months, days:  
* 1. +ly 6m = 28 Feb 2008  
* 2. +1y 5m 28d = 28 Feb 2008  
* 3. +1y 5m 29d = 01 Mar 2008  
*/  
refDate = refDate.AddYears(yearPart);  
refDate = refDate.AddMonths(monthPart);  
refDate = refDate.AddDays(dayPart);  
  
  
numDays = (int)DateAndTime.DateDiff(DateInterval.Day, baseDate, refDate);  
  
if (stringToParse.ToCharArray()[0] == '-')  
{  
//numDays = -numDays;  
}  
  
}  
else  
{  
int tDays = 0;  
if (int.TryParse(stringToParse, out tDays))  
{  
// we curently have numDays months (default on entry is months if no specifier  
refDate = refDate.AddMonths(tDays);  
numDays = (int)DateAndTime.DateDiff(DateInterval.Day, DateTime.Now, refDate);  
}  
  
}  
}  
}  
catch(Exception e)  
{  
throw new RelativeDateException(RelativeDateException.ExceptionType.OutOfBound
sException, e.InnerException, "");  
}  
}  
  
if (numDays == invalidDayCode)  
{  
throw new RelativeDateException(RelativeDateException.ExceptionType.InvalidFor
matException, null, "");  
}  
else if (numDays > Math.Abs(maxRange))  
{  
throw new RelativeDateException(RelativeDateException.ExceptionType.OutOfMaxRa
ngeException, null, "");  
}  
  
return numDays;  
}  
```

