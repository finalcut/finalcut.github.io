---
layout: single
title: Example Post with Featured Image
category: blogging
tags: [example, images]
comments: true
featured: true
date: 2025-11-10
author: Bill Rawlinson
description: An example showing how to add featured images to Jekyll posts for better social sharing
excerpt: Learn how to add featured images to your Jekyll posts so they display properly when shared on social media platforms.

# Featured image options (choose one approach):

# Option 1: Simple image field (will be used for teaser and og_image)
image: /assets/images/posts/my-featured-image.jpg

# Option 2: Full header configuration with different images for different purposes
# header:
#   image: /assets/images/posts/my-header-image.jpg     # Full-width header (1280x400px recommended)
#   teaser: /assets/images/posts/my-teaser-image.jpg    # Thumbnail for post lists (500x300px recommended)
#   og_image: /assets/images/posts/my-og-image.jpg      # Social sharing image (1200x630px recommended)
#   caption: "Photo credit: [Your Name](https://example.com)"

# Option 3: Just Open Graph image for social sharing
# header:
#   og_image: /assets/images/posts/my-social-image.jpg

---

# Your Post Content Here

This is an example of how to structure a post with a featured image that will display properly when shared on social media platforms like Facebook, Twitter, LinkedIn, etc.

## Image Recommendations

- **Open Graph (og_image)**: 1200x630px - Used by Facebook, LinkedIn, Slack
- **Teaser**: 500x300px - Used in post listings and archives
- **Header**: 1280x400px - Full-width header image at top of post
- **Simple image**: 1200x630px works well as a multipurpose featured image

## File Organization

Store your images in:
```
assets/
  images/
    posts/
      2025/
        your-post-images.jpg
```

This keeps your post images organized by year and separate from site assets.