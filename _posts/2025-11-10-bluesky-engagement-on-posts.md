---
firstprop: first
layout: single
title: Bluesky Engagement on Posts
category: blogging
tags:
  - github-pages
  - github-actions
  - bluesky
  - ai
  - copilot
comments: false
featured: false
date: 2025-11-10
author: Bill Rawlinson
description: Bluesky in my blog? Sure!
---
Today I did a bunch of work (using copilot AI) to help fix some things with posting to bluesky - but then I thought - why not see if we can include social engagement at the bottom of the blog post much like [Martin Did here](https://www.woodwardweb.com/post/2025/08/automated-bluesky-integration/).

The trick is there wasn't - that I know of - a Jekyll addon for this.  So gave copilot a simple prompt using the description from Martins blog post about what the Atom component does:

```
The BlueSky Likes Component
The real magic happens in the browser with the BlueSky Likes component (massive credit to whitep4nth3r and ashleymcnamara for inspiration). This Astro component:

Fetches social data from BlueSky’s public API
Displays user avatars of people who liked the post
Shows threaded comments from the BlueSky discussion
Provides interactive elements for engaging with the social post
```

And copilot created a fully functional widget for Jekyll.  I'm kind of impressed.  At some point I'll have to extract that out to being a reusable component but, for now, I'm pretty happy with how it works.

## Discussion

Join the conversation on Bluesky and see what people are saying about this post:

{% include bluesky-engagement.html %}
