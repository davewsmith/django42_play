# Playing around with Django 4.2

It's been a while since I started a Django project from scratch,
and that was on a much older version. An opportunity to explore!

## Setup

With `vagrant` and `virtualbox` installed,

    vagrant up

setup up an Ubuntu 20.04 VM, and does the needful for installing
Django 4.2.7 in a virtual environment.

## Running

    vagrant ssh
    cd /vagrant
    . venv/bin/activate
    cd play
    ./manage.py runserver

## Additional Setup

Start the project. (Already done an merged.)

    ./manage.py startproject play

Run migrations. This'll create `play/db.sqlite3`

    ./manage.py migrate

Create a superuser

    ./manage.py createsuperuser


## License

Nope. Nothing original here. This is strictly use-at-your-own-risk ware.
