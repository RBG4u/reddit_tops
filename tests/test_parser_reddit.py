import pytest
from parser_reddit import parsing_comments, parsing_posts
from token_auth import get_token
import config


def test__parsing_comments__input_non_existent_subreddit_name():
    subreddit = 'non_existent_subreddit'
    token = get_token()
    user_agent = config.USER_AGENT

    result = parsing_comments(subreddit, token, user_agent)

    assert result == [] or result == 'Error'


def test__parsing_comments__input_existent_subreddit_name():
    subreddit = 'Health'
    token = get_token()
    user_agent = config.USER_AGENT

    result = parsing_comments(subreddit, token, user_agent)

    assert result != [] and result != 'Error'


def test__parsing_posts__input_non_existent_subreddit_name():
    subreddit = 'non_existent_subreddit'
    token = get_token()
    user_agent = config.USER_AGENT

    result = parsing_posts(subreddit, token, user_agent)

    assert result == [] or result == 'Error'


def test__parsing_posts__input_existent_subreddit_name():
    subreddit = 'Health'
    token = get_token()
    user_agent = config.USER_AGENT

    result = parsing_posts(subreddit, token, user_agent)

    assert result != [] and result != 'Error'
    