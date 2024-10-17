import praw
import json
import os
import re

# Reddit API credentials
reddit = praw.Reddit(client_id='eKkc1qfruJfkwBeHCU4NPA',
                     client_secret='aJ0B1uHMd-qRDTDn0Z9EHrFHFl1GDg',
                     user_agent='test')


def clean_filename(filename):
    return re.sub(r'\W', '_', filename)


def scrape_reddit_posts(subreddit_name, post_limit):
    subreddit = reddit.subreddit(subreddit_name)
    posts = subreddit.hot(limit=post_limit)

    post_data = []
    for post in posts:
        comments_data = []
        comments = post.comments.list()
        for comment in comments:
            if isinstance(comment, praw.models.Comment):
                author_name = comment.author.name if comment.author else "anonymous"
                comments_data.append({'username': author_name, 'comment': comment.body})

        post_data.append({'title': post.title, 'score': post.score, 'url': post.url, 'comments': comments_data})

        # Save comments to file
        # save_comments_to_file(clean_filename(post.title), comments_data)

    return post_data


def save_to_json(data, filename):

    print("Hello ____________________________________________ Ji")
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


# def save_comments_to_file(post_title, comments_data):
#     filename = os.path.join('comments', (post_title[:240] + '_comments.json'))
#     with open(filename, 'w', encoding='utf-8') as file:
#         json.dump(comments_data, file, indent=4)


def reddit_main(subreddit_name, post_limit):

    output_file = 'reddit_posts.json'

    reddit_posts = scrape_reddit_posts(subreddit_name, post_limit)
    save_to_json(reddit_posts, output_file)
    print("Reddit posts saved to", output_file)


    return reddit_posts

if __name__ == "__main__":

    subreddit_name = input("Enter the topic_name: ")

    # Number of posts to scrape
    post_limit = int(input("Enter the post limit: "))



    reddit_main(subreddit_name, post_limit)
