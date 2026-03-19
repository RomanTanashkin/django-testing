from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'url',
    (
        pytest.lazy_fixture('url_news_home'),
        pytest.lazy_fixture('url_user_login'),
        pytest.lazy_fixture('url_user_signup'),
    )
)
def test_pages_availability_for_anonymous_user(client, url):
    """Главная, страницы регистрации и входа доступны анониму."""
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


def test_logout_availability_for_anonymous_user(client, url_user_logout):
    """Страница выхода из учётной записи доступна анонимным пользователям."""
    response = client.post(url_user_logout)
    assert response.status_code in (
        HTTPStatus.OK, HTTPStatus.FOUND
    )


def test_detail_page_availability(url_news_detail, client):
    """Страница отдельной новости доступна анонимному пользователю."""
    response = client.get(url_news_detail)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND),
    ),
)
@pytest.mark.parametrize(
    'url',
    (
        pytest.lazy_fixture('url_comment_edit'),
        pytest.lazy_fixture('url_comment_delete'),
    ),
)
def test_pages_availability_for_different_users(
        parametrized_client, url, expected_status
):
    """Редактирование и удаление комментария доступны автору."""
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url',
    (
        pytest.lazy_fixture('url_comment_edit'),
        pytest.lazy_fixture('url_comment_delete'),
    ),
)
def test_redirects(url, url_user_login, client):
    """Анонимный пользователь перенаправляется на страницу авторизации."""
    expected_url = f'{url_user_login}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
