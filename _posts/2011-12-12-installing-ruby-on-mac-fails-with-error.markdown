---
layout: post
title: "Installing Ruby on a Mac fails with an error while running configure"
date: 2011-12-12
comments: false
---
Today I tried to upgrade my Ruby version to the latest (1.9.3-p0) using RVM
(Ruby Version Manager).  When I tried the install it failed with an error:  
  
  
ERROR: Error running ' ./configure
--prefix=/Users/bill/.rvm/rubies/ruby-1.9.3-p0 --enable-shared --disable-
install-doc --with-libyaml-dir=/Users/bill/.rvm/usr ', please read
/Users/bill/.rvm/log/ruby-1.9.3-p0/configure.log  
ERROR: There has been an error while running configure. Halting the
installation.  
  
I wasn't sure what to do but after a bit of digging on google and some forums
I found the solution.  But, before I give you that here is the reasoning I
found for the issue:  
  

> it works with 1.9.2 - BUT I was also not able to get RVM going on Lion. I
have xcode 4.2.The problem is that xcode uses LLVM GCC and not (standard? I
forget the term) GCC.

  
  
  
  
Finally, here is how to get it to install without any issues:  
  
**rvm install 1.9.3 --with-gcc=clang**  
  
  
This solution was found via [dcinzona](https://github.com/plamoni/SiriProxy/is
sues/138#issuecomment-3032544) at github.  He found the answer on
[stackoverflow](http://stackoverflow.com/questions/8259928/error-compiling-
ruby-1-9-3-using-rvm-homebrew-or-macports)  

