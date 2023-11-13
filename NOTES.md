# NOTES

Goals:
  - Kick the tires on Django 4.2
  - Play with customizing the Admin
  - See what's involved in building a standalone, no-Model Admin page

Options:
  - `x-forwarded-for` middleware. See [here](https://django-book-new.readthedocs.io/en/latest/chapter17.html)
  - See how Celery plays with 4.2
  - Django REST Framework
  - `x-forwarded-for` middleware. See [here](https://django-book-new.readthedocs.io/en/latest/chapter17.html)
  - Run behind gunicorn with logging sorted out

Non Goals:
  - Not building a production-ready app here
  - Social Auth

To Do:
  - Sort out how to backup/restore db to support experimental branches
  - Add an app and play with customizing the Admin
  - Build a no-Model Admin page
  - Add Job/JobState
    - with a manage command to inject a Job
    - with some flavor of Task queue (Celery? Rq?)
    - with a custom Admin page to show queue statistics
    - results will need to go somewhere, so that too

## Round 1

I'm working on a backup laptop until my main one gets a repair.
The backup is running Ubuntu 18.04, which has Python 3.6.9.
Django 4.2 wants 3.8, meaning Ubuntu 20.04 or later.
I didn't want to bite off the `dist-upgrade` just yet, so VM time.

And thence to re-discover the platform dependencies needed for getting a working version of `pip`
into a virtual environment on 20.04. That took most of the time this round.

Installing Django, making a project, running migrations, and setting up a superuser was a snap.
The (empty) app comes up under `runserver` as expected, with working Admin. Nice.

Ideas for experiments/thinking:

  1. A side quest to explore a platform issue:
     What does it take to get `pip install --upgrade pip` working?
     Does it still mean pinning to an earlier-than-latest version of `pip`?
  2. Sort when in provisioning to set WAL on db.sqlite. Surely it won't hurt to pre-build it if absent.

## Round not quite 2

Hah! I've been using `vagrant` for 8 years now, and have been subsisting mostly on
`vagrant (up|halt|destroy|box update)`, and the docs on how to craft a `Vagrantfile`.
"I bet there's a way to..." led to finally going to other parts of the documentation,
where I discovered `vagrant snapshot (push|pop|list|destroy)`.
Well, damn, that would have saved some time. I should RTFM more often.

This'll help in the current situation, pushing the need for sorting out db backup/restore further down the To Do list.

Now, can I upgrade to the latest pip?

```
(venv) vagrant@ubuntu-focal:/vagrant$ pip --version
pip 20.0.2 from /vagrant/venv/lib/python3.8/site-packages/pip (python 3.8)
(venv) vagrant@ubuntu-focal:/vagrant$ pip install --upgrade pip
Collecting pip
  Downloading pip-23.3.1-py3-none-any.whl (2.1 MB)
     ...
Installing collected packages: pip
  Attempting uninstall: pip
    Found existing installation: pip 20.0.2
    Uninstalling pip-20.0.2:
      Successfully uninstalled pip-20.0.2
ERROR: Could not install packages due to an EnvironmentError: [Errno 39] Directory not empty: '_vendor'
```

No! A bit of searching suggests that doing `pip install --use-pep517` might help. I'll try that later.

Also, try variants of `python -m pip install --upgrade --force --ignore-installed pip`