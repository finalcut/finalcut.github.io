---
layout: post
title: "Lootly! Development is Beginning - Help Appreciated"
date: 2005-04-26
comments: false
categories:
 - ruby
 - lootly
---
I know, I know, I said before that I was going to keep updating everyone about
the progress of my issue tracking revamping. And I will. In fact, if you read
the last update your pretty much up-to-date because I have been busy with PAID
work since then.

However, not only paid work is starting to eat into my time. I have found a
catalyst to get me moving on Lootly! A reader of this blog, Carlos, offered to
help me get running with Lootly! If you don't know what Lootly is, I suggest
you [go here](http://rawlinson.us/blog/?cat=12) and read a little of the
background info on it.

I have actually already written Lootly! Sort of. It started out in CF5 and
tied into an older version of Amazon Web Services. I then upgraded the xml
processing with CF6 came out but didn't really do any significant work on it
beyond that. For instance, one thing I wanted to do, but never got around to,
was refactoring to take advantage of CFCs.

It was hosted on our companies only public facing server. However, some schmo
installed a poorly written ASP script on the same server, then we were hit by
a hacker, and all personal efforts had to come off the machine since we also
host some customer stuff there. That sucked mainly because it was the only way
I could afford (free!) CF hosting.

So, where does that leave me? Well I have debated back and forth (with myself)
about using something other than CF for Lootly! simply because I can't afford
a CF host that would support my eventual needs. Actually, I just afford any CF
host. I pay about $10/month for my current PHP host and that is about all I
can justify to my wife. My personal debate focused primarilly around Ruby and
PHP. Both pretty cool and feature rich languages that can fill the bill. The
biggest strike against Ruby is the same as CF - finding a host that I can
afford. Everyone offers PHP hosting; but not everyone has Ruby.

However, a big plus in favor of Ruby is Rails. I think it is an incredibly
slick looking framework. I have dug into a bit and it was amazing how quickly
I was able to build a simple application. It was even faster than CF - and CF
is about as fast as you can get really. Ruby also has some really cool
shortcuts for quickly creating mutators (getters/setters).

    
    
      
          class Song  
          attr_reader :name, :artist, :duration  
          end         
    ```
      
    
    
            This creates getters on the Song class for the name, artist and        duration fields.      
    
        Example thanks to [    Philip Jacob](http://www.whirlycott.com/phil/2005/04/13/ruby-first-impressions/).    
    
          Recent development in PHP land such as the release of mach-ii for      PHP and CAKE (a Rails like framework) make PHP very intriguing as      well. Plus, once again there is that cost factor. However, I have      decided to start out with Ruby. I want to learn the language      anyway and this seems like a great opportunity to do so. Who      knows, maybe I'm crazy.    
    
        
    
          Anyway, if you have read about Lootly! at the link I provided      earlier and you think you might want to get involved, contact me      at bill.rawlinson@gmail.com and we can discuss how you and your      skillset can fit into the project. You don't have to know      Ruby (I don't) but you do have to be willing to learn. Some      background in OO is preferred, but again, not required (just a      willingness to learn). I don't expect substantial time      involvement from anyone but 4-8 hours a week would be great! I      hope to hear from you.    
    
    
    

