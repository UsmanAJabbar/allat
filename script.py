import praw
from openai import OpenAI

COMMAND_KEYWORD = '!allat'

# I know I'm exposing these keys, I couldn't care less
CLIENT_SECRET = ''
CLIENT_ID = ''
USER_AGENT = ''
OPEN_API_KEY = ''

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT,
    username='Constant-Ebb-4480',
)
client = OpenAI(api_key=OPEN_API_KEY)

def get_tldr(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Summarize this post: {text}"}
        ],
    )
    return response.choices[0].message.content

def main():
    subreddit = reddit.subreddit('pakistaniiconfessions')
    for comment in subreddit.stream.comments():
        if comment.body.startswith(COMMAND_KEYWORD):
            post = comment.submission
            post_text: str = post.selftext if post.selftext else post.title
            word_count = len(post_text.split(' '))

            if word_count < 300:
                tldr = "Yeah right buddy, I'm not summarizing this short post for you. You're on your own."
            else:
                tldr = get_tldr(post_text)

            print('==============')
            print('==============')
            print('==============')
            print('TLDR', tldr)
            print('==============')
            print('==============')
            print('==============')

            post.reply(f'TL;DR: {tldr}')

if __name__ == '__main__':
    main()
