from http import HTTPStatus

import pytest
from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from news.pytest_tests.conftest import COMMENT_TEXT
from pytest_django.asserts import assertFormError, assertRedirects

NEW_COMMENT_TEXT = 'Новый текст комментария'
form_data = {'text': NEW_COMMENT_TEXT}


def comments_before_request():
    return Comment.objects.count()


def test_anonymous_user_cant_create_comment(url_news_detail, client):
    """Анонимный пользователь не может отправить комментарий."""
    COMMENTS_BEFORE_REQUEST = comments_before_request()
    client.post(url_news_detail, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == COMMENTS_BEFORE_REQUEST


def test_user_can_create_comment(url_news_detail, admin_client, admin_user, news):
    """Авторизованный пользователь может отправить комментарий."""
    COMMENTS_BEFORE_REQUEST = comments_before_request()
    response = admin_client.post(url_news_detail, data=form_data)
    assertRedirects(response, f'{url_news_detail}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == COMMENTS_BEFORE_REQUEST + 1
    new_comment = Comment.objects.get()
    assert new_comment.text == form_data['text']
    assert new_comment.news == news
    assert new_comment.author == admin_user


@pytest.mark.parametrize('bad_word', BAD_WORDS)
def test_user_cant_use_bad_words(url_news_detail, admin_client, bad_word):
    """Комментарий с запрещёнными словами не публикуется, форма возвращает ошибку."""
    COMMENTS_BEFORE_REQUEST = comments_before_request()
    bad_words_data = {'text': f'Текст, {bad_word}, еще текст'}
    response = admin_client.post(url_news_detail, data=bad_words_data)
    assertFormError(response, 'form', 'text', WARNING)
    comments_count = Comment.objects.count()
    assert comments_count == COMMENTS_BEFORE_REQUEST


def test_author_can_delete_comment(
    url_comment_delete,
    url_news_detail,
    author_client
):
    """Авторизованный пользователь может удалять свои комментарии."""
    COMMENTS_BEFORE_REQUEST = comments_before_request()
    response = author_client.delete(url_comment_delete)
    assertRedirects(response, f'{url_news_detail}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == COMMENTS_BEFORE_REQUEST - 1


def test_user_cant_delete_comment_of_another_user(
    url_comment_delete,
    admin_client
):
    """Авторизованный пользователь не может удалять чужие комментарии."""
    COMMENTS_BEFORE_REQUEST = comments_before_request()
    response = admin_client.delete(url_comment_delete)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == COMMENTS_BEFORE_REQUEST


def test_author_can_edit_comment(
    url_comment_edit,
    url_news_detail,
    comment,
    author,
    news,
    author_client
):
    """Авторизованный пользователь может редактировать свои комментарии."""
    response = author_client.post(url_comment_edit, data=form_data)
    assertRedirects(response, f'{url_news_detail}#comments')
    comment.refresh_from_db()
    assert comment.text == NEW_COMMENT_TEXT
    assert comment.news == news
    assert comment.author == author


def test_user_cant_edit_comment_of_another_user(
    url_comment_edit,
    comment,
    author,
    news,
    admin_client
):
    """Авторизованный пользователь не может редактировать чужие комментарии."""
    response = admin_client.post(url_comment_edit, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == COMMENT_TEXT
    assert comment.news == news
    assert comment.author == author
