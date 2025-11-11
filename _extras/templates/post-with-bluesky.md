---
layout: single
title: "Sample Post with Bluesky Engagement"
date: 2025-11-10
category: blogging
blueskyPostURL: "https://bsky.app/profile/rawlinson.us/post/3m5d2duekhw22"
---

This is a sample post showing how to include Bluesky engagement.

## Your Post Content Here

Write your blog post content normally...

## Discussion

Join the conversation on Bluesky! Here's what people are saying:

{% include bluesky-engagement.html %}

<!-- You can also customize the display options: -->
{% comment %}
{% include bluesky-engagement.html
   show_likes="true"
   show_reposts="true"
   show_replies="true"
   max_avatars="8"
   max_replies="3" %}
{% endcomment %}