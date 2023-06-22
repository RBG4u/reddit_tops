import requests
from datetime import datetime, timedelta
from collections import Counter

from token_auth import get_token
import config


def parsing_posts(subreddit: str, token: str, user_agent: str) -> list[str] | str:
    last_item_fullname = None
    authors = []

    while True:
        try:
            headers = {'User-Agent': user_agent, 'Authorization': f"bearer {token}"}
            url = f'https://oauth.reddit.com/r/{subreddit}/new'
            params = {'limit': 100, 'after': last_item_fullname}

            response = requests.get(url=url, headers=headers, params=params) 
            if response.status_code != 200:
                return 'Error'

            data = response.json()
            posts = data['data']['children']
    
            last_item_fullname = posts[-1]['data']['name']
            three_days_ago = datetime.utcnow() - timedelta(days=3)

            for post in posts:
                post_time = datetime.utcfromtimestamp(post['data']['created_utc'])
                if post_time > three_days_ago:
                    authors.append(post['data']['author'])
                else:
                    return authors
        except IndexError:
            return authors


def parsing_comments(subreddit: str, token: str, user_agent: str) -> list[str] | str:
    last_item_fullname = None
    authors = []

    while True:
        try:
            headers = {'User-Agent': user_agent, 'Authorization': f"bearer {token}"}
            url = f'https://oauth.reddit.com/r/{subreddit}/comments'
            params = {'limit': 100, 'after': last_item_fullname}

            response = requests.get(url=url, headers=headers, params=params)  
            if response.status_code != 200:
                return 'Error'

            data = response.json()
            comments = data['data']['children']
    
            last_item_fullname = comments[-1]['data']['name']
            three_days_ago = datetime.utcnow() - timedelta(days=3)

            for comment in comments:
                comment_time = datetime.utcfromtimestamp(comment['data']['created_utc'])
                if comment_time > three_days_ago:
                    authors.append(comment['data']['author'])
                else:
                    return authors
        except IndexError:
            return authors


def do_top_10(subreddit: str) -> tuple[list[str], list[str] | str, str]:
    token = get_token()
    posts_authors = parsing_posts(subreddit, token, config.USER_AGENT)
    comments_authors = parsing_comments(subreddit, token, config.USER_AGENT)

    if posts_authors == 'Error' or comments_authors == 'Error':
        return 'Error', 'Error'

    counter_posts = Counter(posts_authors)
    counter_comments = Counter(comments_authors)
    top_authors_posts = counter_posts.most_common(10)  
    top_authors_comments = counter_comments.most_common(10)  
    return top_authors_posts, top_authors_comments


def output_top():
    while True:
        subreddit = input('Введите имя сабреддита: ')
        top_authors_posts, top_authors_comments = do_top_10(subreddit)

        if top_authors_posts == [] or top_authors_posts == 'Error':
            print('\nВведено некорректное имя сабреддита, или за последние 3 дня не было постов!\nВведите корректное имя!\n')
            continue
        else:
            print('\nТоп авторов постов за последние 3 дня:')
            for author, count in top_authors_posts:
                print(f'Автор: {author}, количество постов: {count}')
            print('\nТоп авторов комментариев за последние 3 дня:')
            for author, count in top_authors_comments:
                print(f'Автор: {author}, количество комментариев: {count}')
            break
        

if __name__=='__main__':
    output_top()
