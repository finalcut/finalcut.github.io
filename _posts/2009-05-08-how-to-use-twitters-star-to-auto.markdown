---
layout: post
title: "How to use Twitter's STAR to auto-retweet"
date: 2009-05-08
comments: false
categories:
 - yahoo
 - yahoo-pipes
 - friendfeed
 - twitter
 - rss
---
If you've ever thought there should be an easier way to re-tweet a message in
twitter well now there is. No longer do you have to copy+paste and prefix "RT:
@" to the mesage and then have to worry about cropping it down to under 140
characters.  
  
Thanks to the power of Yahoo Pipes and FriendFeed you can automatically
retweet any message you mark with a star (favorite). It's fairly easy.  
  
1\. Get a friend feed account if you don't have one. Fortunately it's super
easy now-a-days because you can use your twitter login to create a FriendFeed
account. So go, [get an account](http://friendfeed.com).  
  
2\. Once you have a FF account make sure you add your twitter service. This is
easier than it might seem (and it may have done it automatically if you signed
up with twitter. If not just add your twitter account by going to Settings,
Add Service, click the twitter icon, enter your twitter username, and bam all
done. Honestly, at some point you'll probably want to use friendfeed more than
twitter so feel free to add other accounts you want to bring in as well if
you're feeling up to it.  
  
3\. Now go to this [yahoo
pipe](http://pipes.yahoo.com/pipes/pipe.info?_id=SksD_RE83hGY0gAmPxJ3AQ) and
put your username in the form then hit the button "Run Pipe" - after that is
done right click the "Get as RSS" link and copy that link address.  
  
4\. Go back to friend feed and add a "Custom RSS/ATOM feed" service to your
account using the RSS address you copied from Yahoo Pipes.  
  
5\. <del>Now go to <http://friendfeed.com/settings/posting> \- You might have
to authenticate your account so you can post to twitter from here.. Do that.
Then click the option "Post my friend feed entries to twitter by default" then
pick the option "the services I've selected below" and then pick the one that
looks like this: "Custom RSS/Atom (http://pi...)" then hit save
settings.</del>  
  
5\. Go to twitterfeed.com and setup a feed based on the RSS url you got from
pipes. I setup my twitterfeed to poll every 30 minutes and to post up to 5
items per.. I don't retweet that often so it's probably overkill; but you can
do whatever suites you.  
  
That's it. Now, whenever you star an item it will be pulled into yahoo pipes,
modified a touch to have the RT: @ and then sent to FF which will make sure it
is the right length, add a small url to it so people can chat about it at FF,
and then send it to twitter as a tweet by you.

## Comments

Bill

'd suggest you study the pipe I used; copy it, and figure out the twitter feed
you want to retweet. It shouldn't be a very difficult exercise to modify my
work to suit your needs.

Darmawan

What if i want to auto-retweet other people's tweet? For instance, @me wants
to retweet all of tweets by @they. How could i do that?

Bill

useless.. lol; it has a use to me so I use it. Not sure what your problem is.

Anonymous

So...that was pretty useless. Thanks.

Bill

Well I've given it a few days and it seems that friendfeed isn't pulling the
pipes feed in at all so I setup twitterfeed to pull in the pipes feed and now
it is retweeting like I want it to.  
  
Thus, if you want to use this just use twitterfeed to post to twitter instead
of friendfeed.

Bill

Click on your settings, tab, customize link on the window that pops up, pick
CUSTOM RSS as the service, paste the URL you have in the field it provides,
and then finish..

Heather

How do I do this - Go back to friend feed and add a "Custom RSS/ATOM feed"
service to your account using the RSS address you copied from Yahoo Pipes.

