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

