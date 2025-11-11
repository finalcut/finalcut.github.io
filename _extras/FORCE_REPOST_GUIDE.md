# Force Repost Feature

## Overview
The Jekyll workflow now supports force reposting existing blog posts to Bluesky using a frontmatter flag.

## How to Use

### For New Posts
New posts are automatically posted to Bluesky when they're created (if they don't already have a `blueskyPostURL`).

### For Existing Posts (Force Repost)
To repost an existing blog post to Bluesky:

1. **Edit the post's frontmatter** and add:
   ```yaml
   forceRepost: true
   ```

2. **Commit and push** the changes to the main branch

3. **The workflow will automatically**:
   - Detect the `forceRepost: true` flag
   - Generate a new AI message for the post
   - Post it to Bluesky
   - Update the post with the new `blueskyPostURL`
   - **Remove the `forceRepost` flag** automatically
   - Rebuild the site with the updated frontmatter

## Example Usage

### Before (existing post):
```yaml
---
layout: post-with-discussion
title: My Awesome Post
category: blogging
tags: [example]
comments: true
featured: false
date: 2025-11-11
author: Bill Rawlinson
description: A great post about something
blueskyPostURL: https://bsky.app/profile/rawlinson.us/post/3abcdef123
---
```

### To force repost, change to:
```yaml
---
layout: post-with-discussion
title: My Awesome Post
category: blogging
tags: [example]
comments: true
featured: false
forceRepost: true  # ← Add this line
date: 2025-11-11
author: Bill Rawlinson
description: A great post about something
blueskyPostURL: https://bsky.app/profile/rawlinson.us/post/3abcdef123
---
```

### After workflow runs:
```yaml
---
layout: post-with-discussion
title: My Awesome Post
category: blogging
tags: [example]
comments: true
featured: false
# forceRepost flag automatically removed
date: 2025-11-11
author: Bill Rawlinson
description: A great post about something
blueskyPostURL: https://bsky.app/profile/rawlinson.us/post/3newpost456  # ← Updated URL
---
```

## Use Cases

- **Resharing old content**: Bring attention to older posts
- **Fixed typos**: After updating a post, share it again
- **Added featured images**: Share posts again with new visual content
- **Seasonal content**: Repost relevant content at appropriate times
- **Corrected URLs**: If there were issues with the original post

## Technical Details

- The workflow scans all posts in `_posts/` for the `forceRepost: true` flag
- Posts with this flag are treated like new posts for Bluesky sharing
- AI generates a fresh social media message based on current post content
- The existing `blueskyPostURL` is replaced with the new post URL
- The `forceRepost` flag is automatically removed after successful posting
- The site is automatically rebuilt with the updated frontmatter

## Notes

- Only one post can be force reposted per workflow run
- The workflow processes force reposts alongside new posts
- Force reposts use the same AI message generation as new posts
- The feature respects the same URL generation logic as new posts