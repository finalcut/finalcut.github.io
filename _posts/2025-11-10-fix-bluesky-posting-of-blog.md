---
firstprop: first
layout: post-with-discussion
title: Fix the Bluesky Posting of Blog Posts
category: blogging
tags:
  - github-pages
  - github-actions
  - bluesky
comments: false
featured: false
date: 2025-11-10
author: Bill Rawlinson
description: Autopost to Bluesky and get the URL of that post back
blueskyPostURL: https://bsky.app/profile/rawlinson.us/post/3m5feqffzdr27
---
A few months ago I talked about [autoposting to bluesky](https://rawlinson.us/blogging/auto-share-a-new-blog-post-to-bluesky/) but there was a limitation to the github action I was importing and it didn't return the bluesky uri.  That meant that I couldn't update the front matter properly and track the bluesky post to the blog post - meaning the same thing might get posted to bluesky multiple times unless I remembered to go manually get the bluesky uri.  yuck.  TOIL is my enemy.

So today I used a bit of copilot AI and updated the github action.  I'm pretty sure it works properly and I [submitted a PR back to the original author](https://github.com/zentered/bluesky-post-action/pull/17/files).  For the time being I just have some [hand-rolled code in my github action](https://github.com/finalcut/finalcut.github.io/blob/a5b7acc33814f570b776cbc7251f4454f3a14e1c/.github/workflows/jekyll.yml#L214) that implements the suggestions from copilot.  So this post acts as both an annoucement and a test of the functionality.

The PR has some unit tests but sometimes its nice to get a concerete example so - here it is.  Ideally, after I submit this it will auto-post to bluesky, add the frontmatter for `blueskyPostURL` and commit that without reposting ad infinium (it won't).

One other thing I discovered (or maybe it changed) since I last visited this was the need to format the post in a way that links in the post show up properly.  So this tests that approach.

