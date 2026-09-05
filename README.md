# Django testing: YaNews & YaNote

Two complete test suites for two Django applications, written with the two major Python test frameworks:

| Project | Framework | Tests |
|---|---|---|
| `ya_news` — news site with comments | **pytest** + pytest-django | 24 |
| `ya_note` — personal notes with authentication | **unittest** (Django `TestCase`) | 14 |

Each suite covers the same three areas: **routes** (availability and redirects for anonymous, authenticated and author users), **content** (context data, ordering, pagination, form presence) and **logic** (create/edit/delete permissions, bad-word filtering, duplicate slugs).

Built during the *Python Developer* course at Yandex Practicum (2025–2026). Every project was reviewed and accepted by a course mentor.

## Tech stack

Python 3 · Django · pytest · pytest-django · unittest

## Run the tests

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

cd ya_news && pytest && cd ..
cd ya_note && python manage.py test && cd ..
```

`run_tests.sh` runs both suites in one go.

## Author

Roman Tanashkin — [github.com/RomanTanashkin](https://github.com/RomanTanashkin)
