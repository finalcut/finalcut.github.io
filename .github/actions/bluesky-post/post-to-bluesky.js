const { BskyAgent } = require('@atproto/api');

(async () => {
  try {
    const agent = new BskyAgent({ service: 'https://bsky.social' });
    await agent.login({
      identifier: process.env.BLUESKY_USERNAME,
      password: process.env.BLUESKY_PASSWORD
    });

    const post = await agent.post({
      text: process.env.MESSAGE,
      createdAt: new Date().toISOString()
    });

    console.log('Posted to Bluesky successfully');
    console.log('Post URI:', post.uri);
    console.log('AT_URI=' + post.uri);
  } catch (error) {
    console.error('Error posting to Bluesky:', error);
    process.exit(1);
  }
})();