---
layout: post
title: "Moved to Octopress"
date: 2013-07-27 11:59
comments: true
category: general
tags: [jekyll,octopress,blogger]
---
I've decided to move my development blog away from blogger and into octopress which uses GitHub pages to host.  I am doing this for a couple reasons but none of them are super important.  Mostly I just wanted to try out using Jekyll and it will give me an excuse to play with rake a bit.

I have plans to build a neat project I've been thinking about for a long time (ten years or so) and I think I'm going to build it in Ruby.  I'll be using github for my version control and moving my blog over is just a beginning step to getting used to a more git focused workflow.

I've turned on disqus comments - which I may or may not stick with.

Here is a tip for anyone moving from Blogger to Octopress - your blogger post titles that have double quotes in them won't work properly.  You'll have to git rid of the double quotes before the `rake generate` command will work.  Fortunately the `rake generate` throws an error on the first post it runs into with a bad title.  Fix it, `rake generate` again, and then fix again until it `rake generate` works.
