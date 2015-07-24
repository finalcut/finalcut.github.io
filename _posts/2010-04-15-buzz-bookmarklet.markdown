---
layout: post
title: "Buzz Bookmarklet"
date: 2010-04-15
comments: false
categories:
 - buzz
 - delicious
 - bookmarklet
 - bookmarks
---
A while ago I read [a pretty valid argument for providing additional
information with your delicious bookmarks](http://blog.jonudell.net/2008/10/22
/why-and-how-to-blurb-your-social-bookmarks/). The article was written by Jon
Udell - a technology evangelist for Microsoft - and he provided [a nice
bookmarklet](http://jonudell.net/delicious-bookmarklet.html) to make it easy
to do just what he was advocating.  
  
Today I heard about the [buzz api
buttons](http://www.google.com/buzz/api/admin/site) and so my initial thought
was to modify Jon's delicious bookmarklet to work with Buzz and thus that's
what I have here.  
  
Basically, just drag this [Buzz
This](javascript:\(function\(\){var%20notes=window.getSelection ?
window.getSelection\(\).toString\(\) :
\(document.selection?document.selection.createRange\(\).text : ''\);
notes=encodeURIComponent\(notes\); f='http://www.google.com/buzz/post?url='
+encodeURIComponent\(window.location.href\) +'&message='+notes+'&v=5&';
a=function\(\) {if\(!window.open\(f,
'buzzer','location=yes,links=no,scrollbars=no,
toolbar=no,width=725,height=550'\)\) location.href=f};
if\(/Firefox/.test\(navigator.userAgent\)\)
{setTimeout\(a,0\)}else{a\(\)}}\)\(\)) link to your bookmarks bar and you'll
have a great bookmarklet for buzzing with. If you select any content on the
page your buzz will be pre-populated with the content of your selection.  
  
Enjoy.  
  
If for some reason the bookmarklet you drag up doesn't work you can copy the
code here and edit your bookmarklet:  
  

    
    
      
    javascript:(function(){var%20notes=window.getSelection ? window.getSelection().toString() : (document.selection?document.selection.createRange().text : ''); notes=encodeURIComponent(notes); f='http://www.google.com/buzz/post?url=' +encodeURIComponent(window.location.href) +'&message;='+notes+'&v;=5&'; a=function() {if(!window.open(f, 'buzzer','location=yes,links=no,scrollbars=no, toolbar=no,width=725,height=550')) location.href=f}; if(/Firefox/.test(navigator.userAgent)) {setTimeout(a,0)}else{a()}})()  
    ```
    
    
    
    
    
    ## Comments
    
    
    
    
    
    
    
    
    
    
    techniq
    
    
    
    
    
    Thanks, I'll have to use this.  I usually use the 'Note in Reader' bookmarklet, which puts it in Google Reader, and then gets sucked into Buzz, but now I have the option to go straight to Buzz if needed.
    
    
    
    
    
    
    
    
    

