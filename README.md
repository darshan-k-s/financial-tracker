# Expense Tracker

Expense Tracker will help you track expense, show charts and statistics about your expenses.

---

![Homepage](https://github.com/darshan-k-s/financial-tracker/blob/acd56dea015565551678c26999ead5ff8ae95e47/demo/homePage.jpeg)

## Installation

For installing the Django application, clone the repository and run:

     pipenv install

This will install the virtual environments and all dependencies.

Then start the virtual environment:

     pipenv shell

Run migrations:

    python manage.py makemigrations
    python manage.py migrate

Create a superuser:

    python manage.py createsuperuser

Now you can start server:

    python manage.py runserver

The site will be live at http://localhost:8000/

---

## Features of the website

- Expense list.
- Expense charts.
- Statistics table.
- Monthly budget bar.
- Form validation.
- Authentication.
- Pagination.

---

![Statistics page](https://github.com/darshan-k-s/financial-tracker/blob/acd56dea015565551678c26999ead5ff8ae95e47/demo/statsPage.jpeg)

---

## Stack used

- Django.
- Postgres.
- Chart.js.

---

## Authors
- Darshan K S
- Siddarth Kotian
