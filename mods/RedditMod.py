import praw

class RedditMod:
    rank = 0
    help_dict = {'py_reddit': 'usage: reddit <sub_name>, searches reddit', 'py_r': 'usage: reddit <sub_name>, searches '
                                                                                   'reddit, alias for reddit command'}

    def __init__(self, client, message):
        self.client = client
        self.message = message
        self.filter = __import__("GoogleBlacklistMod").filter

    async def py_reddit(self, sub):
        r = praw.Reddit
        subreddit = r.get_subreddit(subreddit_name=sub)
        posts = subreddit.get_hot(limit=5)
        posts = list(posts)
        done = False
        for post in posts:
            if not done and not post.is_self and (filter and not post.over_18 or not filter) and "spoiler" not in post.link_flair_text and (('gyfcat' or '.png' or '.jpg' or '.jpeg' or '.gif' or '.gfy') in post.url):
                await self.client.send_message(self.message.channel, "**Title**: " + post.title + "\n**Reddit Link**: " + post.short_link + "\n" + post.url)



    async def py_r(self, sub):
        self.py_reddit(sub)
