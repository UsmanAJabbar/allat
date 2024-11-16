import praw
import os
from openai import OpenAI

COMMAND_KEYWORD = '!allat'

CLIENT_ID = '-namsPzB7Q'
CLIENT_SECRET = '-hTYz_1Q5lpqw'
USER_AGENT = 'allat-bot/0.1 by -Ebb-4480'
OPEN_API_KEY = 'sk-proj--yZ4L_QqFnljEJYYMrTRpLiY6s8qvPBUJtBb4TIGr_tw5tH-rdjZ1wElO7Yv07uTgdlNXGbRoA'
USERNAME = '-bot'
PASSWORD = 'Jyrnej--4huwki'


reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT,
    username=USERNAME,
    password=PASSWORD
)
client = OpenAI(api_key=OPEN_API_KEY)

def get_tldr(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"This is a post that I want you to summarize. Split your response into shorter paragraphs. Keep it short and concise. Summarize this post: {text}"}
        ],
    )
    return response.choices[0].message.content

def find_existing_tldr(post):
    current_user = reddit.user.me().name
    for comment in post.comments:
        if (
            comment.author
            and comment.author.name == current_user
            and comment.body.startswith("TL;DR:")
        ):
            return comment
    return None


def main():
    subreddit = reddit.subreddit('pakistaniiconfessions')
    for comment in subreddit.stream.comments():
        if comment.body == COMMAND_KEYWORD:
            post = comment.submission
            post_text: str = post.selftext if post.selftext else post.title
            word_count = len(post_text.split(' '))

            # Look for an existing TL;DR comment
            existing_tldr_comment = find_existing_tldr(post)

            if existing_tldr_comment:
                # Reply with a link to the existing TL;DR comment
                tldr_link = f"https://www.reddit.com{existing_tldr_comment.permalink}"
                comment.reply(f"Hey! Here's a [link]({tldr_link}) to the TLDR!")
            elif word_count < 300:
                # Reply with a message if the post is too short
                comment.reply("Yeah right buddy, I'm not summarizing this short post for you. You're on your own.")
            else:
                # Generate and post a new TL;DR comment
                tldr = get_tldr(post_text)
                new_tldr_comment = post.reply(f'TL;DR: {tldr}')
                # Reply to the triggering comment with a link to the new TL;DR
                tldr_link = f"https://www.reddit.com{new_tldr_comment.permalink}"
                comment.reply(f"Hey! Here's a [link]({tldr_link}) to the TLDR!")

if __name__ == '__main__':
    main()
