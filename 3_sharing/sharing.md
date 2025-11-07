# Sharing Blog Posts

We want to share our posts, so people can read them.
Ideally this takes up very little space in our heads, so automations would be useful here.
LinkedIn might be a horrible place, but we can make it a bit better by sharing our blog articles.

## N8N Automation workflow
Jekyll automatically creates an RSS feed URL at `https://yourdomain.com/feed.xml`.
This RSS feed we can periodically query, in case a new article has been posted by you.
If that is the case, we want to fetch the content and query an LLM to build us the perfect LinkedIn post (or multiple for different accounts) from it.
Afterwards we might not want n8n to automatically post it to LinkedIn, we would rather check it first and post it ourselves, so a message to Telegram makes the most sense.
```
[ RSS Feed Trigger ]
       │
       ▼
[ HTTP Request (optional) ]
       │
       ▼
[ OpenAI Node → Generate Post Text ]
       │
       ▼
[ Telegram → Send Message ]
```
