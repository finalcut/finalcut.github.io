/**
 * Bluesky Engagement Widget for Jekyll
 * Fetches and displays likes, reposts, and replies for a Bluesky post
 */
class BlueskyEngagement {
  constructor(container, blueskyUrl, options = {}) {
    this.container = typeof container === 'string' ? document.querySelector(container) : container;
    this.blueskyUrl = blueskyUrl;
    this.options = {
      showLikes: true,
      showReposts: true,
      showReplies: true,
      maxAvatars: 10,
      maxReplies: 5,
      ...options
    };

    this.atUri = null;
    this.postData = null;

    if (this.container && this.blueskyUrl) {
      this.init();
    }
  }

  /**
   * Extract AT URI from Bluesky URL
   * Convert https://bsky.app/profile/username/post/postid to AT URI format
   */
  extractAtUri() {
    const match = this.blueskyUrl.match(/https:\/\/bsky\.app\/profile\/([^\/]+)\/post\/([^\/\?#]+)/);
    if (match) {
      const [, handle, postId] = match;
      return { handle, postId };
    }
    return null;
  }

  /**
   * Resolve handle to DID (Decentralized Identifier)
   */
  async resolveHandleToDid(handle) {
    try {
      const response = await fetch(`https://public.api.bsky.app/xrpc/com.atproto.identity.resolveHandle?handle=${handle}`);
      const data = await response.json();
      return data.did;
    } catch (error) {
      console.error('Error resolving handle:', error);
      return null;
    }
  }

  /**
   * Fetch post data from Bluesky API
   */
  async fetchPostData() {
    const uriData = this.extractAtUri();
    if (!uriData) {
      console.error('Invalid Bluesky URL format');
      return null;
    }

    const { handle, postId } = uriData;
    const did = await this.resolveHandleToDid(handle);

    if (!did) {
      console.error('Could not resolve handle to DID');
      return null;
    }

    this.atUri = `at://${did}/app.bsky.feed.post/${postId}`;

    try {
      // Fetch post thread to get replies and engagement
      const response = await fetch(`https://public.api.bsky.app/xrpc/app.bsky.feed.getPostThread?uri=${encodeURIComponent(this.atUri)}&depth=1`);
      const data = await response.json();

      return data.thread;
    } catch (error) {
      console.error('Error fetching post data:', error);
      return null;
    }
  }

  /**
   * Fetch users who liked the post
   */
  async fetchLikes() {
    if (!this.atUri) return [];

    try {
      const response = await fetch(`https://public.api.bsky.app/xrpc/app.bsky.feed.getLikes?uri=${encodeURIComponent(this.atUri)}&limit=${this.options.maxAvatars}`);
      const data = await response.json();
      return data.likes || [];
    } catch (error) {
      console.error('Error fetching likes:', error);
      return [];
    }
  }

  /**
   * Fetch users who reposted
   */
  async fetchReposts() {
    if (!this.atUri) return [];

    try {
      const response = await fetch(`https://public.api.bsky.app/xrpc/app.bsky.feed.getRepostedBy?uri=${encodeURIComponent(this.atUri)}&limit=${this.options.maxAvatars}`);
      const data = await response.json();
      return data.repostedBy || [];
    } catch (error) {
      console.error('Error fetching reposts:', error);
      return [];
    }
  }

  /**
   * Create avatar HTML
   */
  createAvatar(profile, type = 'liked') {
    const avatar = profile.avatar || 'https://via.placeholder.com/32x32?text=?';
    const handle = profile.handle;
    const displayName = profile.displayName || handle;

    return `
      <a href="https://bsky.app/profile/${handle}"
         class="bluesky-avatar"
         title="${displayName} ${type} this post"
         target="_blank"
         rel="noopener">
        <img src="${avatar}"
             alt="${displayName}"
             class="bluesky-avatar-img"
             loading="lazy" />
      </a>
    `;
  }

  /**
   * Create reply HTML
   */
  createReply(reply) {
    const profile = reply.post.author;
    const avatar = profile.avatar || 'https://via.placeholder.com/24x24?text=?';
    const displayName = profile.displayName || profile.handle;
    const handle = profile.handle;
    const text = reply.post.record.text;
    const createdAt = new Date(reply.post.record.createdAt).toLocaleDateString();

    return `
      <div class="bluesky-reply">
        <div class="bluesky-reply-header">
          <img src="${avatar}" alt="${displayName}" class="bluesky-reply-avatar" loading="lazy" />
          <div class="bluesky-reply-author">
            <a href="https://bsky.app/profile/${handle}" target="_blank" rel="noopener">
              <strong>${displayName}</strong> @${handle}
            </a>
            <span class="bluesky-reply-date">${createdAt}</span>
          </div>
        </div>
        <div class="bluesky-reply-text">${this.formatText(text)}</div>
      </div>
    `;
  }

  /**
   * Basic text formatting (handles mentions and links)
   */
  formatText(text) {
    return text
      .replace(/@([a-zA-Z0-9.-]+)/g, '<a href="https://bsky.app/profile/$1" target="_blank" rel="noopener">@$1</a>')
      .replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank" rel="noopener">$1</a>');
  }

  /**
   * Render the engagement widget
   */
  async render() {
    if (!this.container) return;

    // Show loading state
    this.container.innerHTML = '<div class="bluesky-loading">Loading Bluesky engagement...</div>';

    try {
      // Fetch all data
      const [postThread, likes, reposts] = await Promise.all([
        this.fetchPostData(),
        this.options.showLikes ? this.fetchLikes() : [],
        this.options.showReposts ? this.fetchReposts() : []
      ]);

      if (!postThread) {
        this.container.innerHTML = '<div class="bluesky-error">Could not load Bluesky engagement data.</div>';
        return;
      }

      const post = postThread.post;
      const replies = postThread.replies || [];

      let html = '<div class="bluesky-engagement">';

      // Header
      html += `
        <div class="bluesky-header">
          <h4>💬 Discussion on Bluesky</h4>
          <a href="${this.blueskyUrl}" target="_blank" rel="noopener" class="bluesky-view-post">
            View Post →
          </a>
        </div>
      `;

      // Stats
      const likeCount = post.likeCount || 0;
      const repostCount = post.repostCount || 0;
      const replyCount = post.replyCount || 0;

      html += `
        <div class="bluesky-stats">
          <span class="bluesky-stat">❤️ ${likeCount} likes</span>
          <span class="bluesky-stat">🔄 ${repostCount} reposts</span>
          <span class="bluesky-stat">💬 ${replyCount} replies</span>
        </div>
      `;

      // Likes
      if (this.options.showLikes && likes.length > 0) {
        html += `
          <div class="bluesky-section">
            <h5>Liked by:</h5>
            <div class="bluesky-avatars">
              ${likes.slice(0, this.options.maxAvatars).map(like => this.createAvatar(like.actor, 'liked')).join('')}
              ${likes.length > this.options.maxAvatars ? `<span class="bluesky-more">+${likes.length - this.options.maxAvatars} more</span>` : ''}
            </div>
          </div>
        `;
      }

      // Reposts
      if (this.options.showReposts && reposts.length > 0) {
        html += `
          <div class="bluesky-section">
            <h5>Reposted by:</h5>
            <div class="bluesky-avatars">
              ${reposts.slice(0, this.options.maxAvatars).map(repost => this.createAvatar(repost, 'reposted')).join('')}
              ${reposts.length > this.options.maxAvatars ? `<span class="bluesky-more">+${reposts.length - this.options.maxAvatars} more</span>` : ''}
            </div>
          </div>
        `;
      }

      // Replies
      if (this.options.showReplies && replies.length > 0) {
        html += `
          <div class="bluesky-section">
            <h5>Replies:</h5>
            <div class="bluesky-replies">
              ${replies.slice(0, this.options.maxReplies).map(reply => this.createReply(reply)).join('')}
              ${replies.length > this.options.maxReplies ? `<div class="bluesky-more-replies"><a href="${this.blueskyUrl}" target="_blank" rel="noopener">View ${replies.length - this.options.maxReplies} more replies on Bluesky →</a></div>` : ''}
            </div>
          </div>
        `;
      }

      html += '</div>';

      this.container.innerHTML = html;

    } catch (error) {
      console.error('Error rendering Bluesky engagement:', error);
      this.container.innerHTML = '<div class="bluesky-error">Error loading Bluesky engagement data.</div>';
    }
  }

  /**
   * Initialize the widget
   */
  async init() {
    await this.render();
  }
}

// Auto-initialize widgets on page load
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('[data-bluesky-url]').forEach(container => {
    const url = container.dataset.blueskyUrl;
    const options = {
      showLikes: container.dataset.showLikes !== 'false',
      showReposts: container.dataset.showReposts !== 'false',
      showReplies: container.dataset.showReplies !== 'false',
      maxAvatars: parseInt(container.dataset.maxAvatars) || 10,
      maxReplies: parseInt(container.dataset.maxReplies) || 5
    };

    new BlueskyEngagement(container, url, options);
  });
});

// Export for manual initialization
window.BlueskyEngagement = BlueskyEngagement;