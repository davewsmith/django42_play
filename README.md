# Playing around with Django 4.2

It's been a while since I started a Django project from scratch,
and that was on a much older version. An opportunity to explore!

## Setup

With `vagrant` and `virtualbox` installed,

    vagrant up

This build an Ubuntu 20.04 VM, and does the needful for installing
Django 4.2.7 in a virtual environment.

Copy `env.template` to `.env` and fill it out.

Then

    vagrant ssh
    cd /vagrant
    . venv/bin/activate

## Additional Setup

Run migrations. This'll create `play/db.sqlite3` if it's not there yet.

    ./manage.py migrate

Create a superuser

    ./manage.py createsuperuser


## Running

    cd play
    ./manage.py runserver 0.0.0.0:8000

## License

Nope. Nothing original here. This is strictly use-at-your-own-risk ware.
