---
layout: post
title: "Goodbye Octopress Hello Jeckyll"
description:
headline:
modified: 2015-07-24 17:09:53 -0400
category: personal
tags: []
imagefeature:
mathjax:
chart:
comments: true
featured: false
---
I noticed I've really not been doing a good job of posting to my blog and I want to recitify that.  In order to do so I decided to simplify
by getting rid of octopress and swtiching to plan old Jekyll.

Octopress is built on Jekyll but I often forgot what I was doing with Octopress and I had trouble keeping it working on my windows and mac machines so
I figured it was a good time to simplify.

I am using a theme called "[Notepad](https://github.com/hmfaysal/Notepad/)" written by Hossain Mohd. Faysal. which I've tweaked a little bit for my
tastes.  Overall, I'm pretty happy with it at the moment.

I plan on posting more often now that I've simplified.  Hopefully I can actually follow-through on that plan.

UPDATE:
Well, I can honestly say, the migration to just Jekyll was pretty darn easy overall.  I setup
the Gemfile on my windows machine and did `bundle install` and it worked without a problem there.  Tonight, I checked out the site from git, did a `bundle install` here and the site runs perfectly locally on my macbook as well. Pretty sweet.

To be honest I had to do a bit more.  My mac's RVM was outdated so I had to do a couple other things.

```sh
$ rvm get stable
$ rvm install 2.0.0
$ get checkout {my_git_repo}
$ cd {path_to_repo}
$ bundle install
```

Yeah, my rvm (ruby version manager) was outdated and my ruby was also pretty outdated.  But, thanks to those few simple commands I'm up and running.

I had to do a bunch of cleanup of my blog posts.  For instance, I had, at one point, imported the site from blogger to octopress.  When I did that I basically ended up with a bunch of HTML files with "fore-matter".  fore-matter is a YAML block at the top of each page.  The html pages had some old, outdated code for handling syntax highlighting.  So I spent a bit of time today converting all of those files to markdown and then cleaning up the files to remove the html parts of the syntax highlighting so that Jekyll (via redcarpet and pygments) could do the syntax highlighting for me.

I'll do a post soon that explains how I managed all of that (the python script depended on html2text, a cool python library) along with some minor customizations that took care of the inconsistencies in my own blogging format previously.

When all was said and done all I had to do manually was to clean out some unicode characters that I had floating around in order for my python script to be able to save the markdown files.
