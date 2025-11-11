---
<%*
let title = tp.file.title;
let fileName = title;
if (fileName.includes("Untitled")) {
	fileName = await tp.system.prompt("Meeting Subject")
}
title = fileName;
fileName = fileName.replace(/ +/g, '-').toLowerCase();
fileName = fileName.replace(/-+/g, '-');
await tp.file.move("_posts/" + tp.date.now("YYYY-MM-DD") + "-" + fileName)
-%>
firstprop: first
layout: post-with-discussion
title: <% title %>
category:
tags: []
comments: false
featured: false
date: <% tp.file.creation_date('YYYY-MM-DD') %>
author: Bill Rawlinson
description:
excerpt:
header:
  image: # Full-width header image (recommended: 1280x400px)
  teaser: # Thumbnail image (recommended: 500x300px)
  og_image: # Open Graph image for social sharing (recommended: 1200x630px)
  caption: # Optional caption for header image
image: # Alternative way to set featured image (will be used as teaser and og_image if others not specified)
---

<!-- Your post content goes here -->