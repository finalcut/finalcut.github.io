const OpenAI = require('openai');

(async () => {
  try {
    const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
    
    const response = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: [{
        role: 'user',
        content: `Write a short, engaging social media post (under 280 chars) for this blog post. Title: "${process.env.TITLE}". Excerpt: "${process.env.EXCERPT}". Include the URL at the end: ${process.env.POST_URL}`
      }],
      max_tokens: 100,
      temperature: 0.7
    });
    
    console.log(response.choices[0].message.content.trim());
  } catch (error) {
    console.error('Error generating message:', error);
    process.exit(1);
  }
})();