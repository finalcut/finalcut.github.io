---
layout: post
title: "Install PHP PEAR on Windows 7"
date: 2012-02-29
comments: false
categories:
 - iis7
 - windows
 - php
 - pear
---
This seems like it should be obvious but it turns out getting PEAR isn't
straight forward.  The documentation at pear.php.net is inaccurate for a
windows install where you use the installer at php.iis.net to install PHP on
IIS7. It turns out there is no go-pear.bat file in your php directory after
installing this way.  However, after some trial and error and a bit of luck I
figured out this seven steps to getting PEAR installed.  
  

  1. Download go-pear.phar at <http://pear.php.net/go-pear.phar>
  2. put that file in your php home directory.
  3. open a command window as administrator; move to your php home directory
  4. enter "php go-pear.phar" without quotes
  5. accept the default value for everything it asks about; system wide, path options, updating your php.ini etc
  6. once the script is done pear is installed; you just have one last step
  7. in windows explorer go to your php home directory and double click on PEAR_ENV.reg to update your registry

  

  

## Comments

phil

The PEAR Manual is a nightmare. Totally unclear of how to install.  
Thanks so much for these easy steps!

Stevenmcconnon

Thank you! I'm not too good with windows and these steps worked a charm

