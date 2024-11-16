---
layout: post
title: "Coldfusion, CAC Cards, and File Uploads over 48k Oh My!"
date: 2010-03-11
comments: false
categories:
 - coldfusion
 - cac-cards
 - iis
 - form-processing
---
Yesterday I was working on a deployment to a UAT server at a US government
building. The govt uses CAC (Common Access Cards) cards (yes, I know it's
redundant) as a security device on all of their pc's and laptops. All of the
websites I deal with there also are using SSL (which may be a requirement with
the CAC card I'm not sure).

Well, it turns out that, by default, on IIS 6 over SSL with a CAC card you
can't upload via a webform a payload over 48k. Thus, my form, which contained
a few fields and a file field, wouldn't upload any form data if I selected a
file of 48k or larger. The cfdump of the form scope just showed nothing. It
was quite a surprise and it took me a while to realize it was the payload size
and not some other issue when my form processing didn't work.

Anyway a few google searches later brought me to [this
page](http://blogs.msdn.com/jiruss/archive/2007/04/13/http-413-request-entity-
too-large-can-t-upload-large-files-using-iis6.aspx) which explained I had to
update a setting in the IIS metabase using the following command:

```vbnet
cscript adsutil.vbs set w3svc/1/uploadreadaheadsize 204800

```

The number at the end is in bytes so that command roughly increases the upload
size to 200k. Note that you should be careful when using this since it is
technically possible to open yourself up to a DOS attack; but since, in my
case, it is an internal and protected site I feel ok moving forward.

You have to run that command from the cmd prompt but if it isn't in your path
you'll need to go to your ISS admin scripts directory
(C:\inetpub\adminscripts) to execute it as explained in this
[article](http://blogs.technet.com/benw/archive/2007/05/03/exchange-2003-isa-
and-attachment-size.aspx).

UPDATE:
If you want to see what your setting is currently at go into your
c:\inetpub\adminscripts directory and call this:

```vbnet
Cscript adsutil.vbs get w3svc/1/uploadreadaheadsize

```


