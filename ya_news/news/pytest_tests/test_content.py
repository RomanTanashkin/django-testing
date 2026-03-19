from django.conf import settings


def test_news_count(eleven_news, url_news_home, client):
    """Количество новостей на главной странице — не более 10."""
    response = client.get(url_news_home)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(eleven_news, url_news_home, client):
    """Новости отсортированы от самой свежей к самой старой.

    Свежие новости в начале списка.
    """
    response = client.get(url_news_home)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(news_with_ten_comments, url_news_detail, client):
    """Комментарии отсортированы хронологически: старые — в начале, новые — в конце."""
    response = client.get(url_news_detail)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_dates = [comment.created for comment in all_comments]
    sorted_dates = sorted(all_dates)
    assert all_dates == sorted_dates


def test_anonymous_client_has_no_form(url_news_detail, client):
    """Анонимному пользователю недоступна форма для отправки комментария."""
    response = client.get(url_news_detail)
    assert 'form' not in response.context


def test_authorized_client_has_form(url_news_detail, author_client):
    """Авторизованному пользователю доступна форма для отправки комментария."""
    response = author_client.get(url_news_detail)
    assert 'form' in response.context
    assert type(response.context['form']).__name__ == 'CommentForm'
