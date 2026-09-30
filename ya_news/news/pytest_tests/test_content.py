from django.conf import settings


def test_news_count(eleven_news, url_news_home, client):
    """The home page shows no more than 10 news items."""
    response = client.get(url_news_home)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(eleven_news, url_news_home, client):
    """News items are sorted from newest to oldest.

    The newest news items come first.
    """
    response = client.get(url_news_home)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(news_with_ten_comments, url_news_detail, client):
    """Comments are sorted chronologically.

    Oldest first, newest last.
    """
    response = client.get(url_news_detail)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_dates = [comment.created for comment in all_comments]
    sorted_dates = sorted(all_dates)
    assert all_dates == sorted_dates


def test_anonymous_client_has_no_form(url_news_detail, client):
    """An anonymous user does not see the comment form."""
    response = client.get(url_news_detail)
    assert 'form' not in response.context


def test_authorized_client_has_form(url_news_detail, author_client):
    """An authorised user sees the comment form."""
    response = author_client.get(url_news_detail)
    assert 'form' in response.context
    assert type(response.context['form']).__name__ == 'CommentForm'
