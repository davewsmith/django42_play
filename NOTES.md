# NOTES

Goals:
  - Kick the tires on Django 4.2
  - Play with customizing the Admin
  - See what's involved in building a standalone, no-Model Admin page

Options:
  - `x-forwarded-for` middleware. See [here](https://django-book-new.readthedocs.io/en/latest/chapter17.html)
  - See how Celery plays with 4.2
  - Django REST Framework
  - Run behind gunicorn with logging sorted out

Non Goals:
  - Not building a production-ready app here
  - Social Auth

To Do:
  - Provision the db with `PRAGMA journal_mode=wal;`
  - Sort out how to backup/restore db to support experimental branches
  - with a custom Admin page to show sensor samples
  - write a normal view page to show sensor samples
  - Add a management Action to poll selected sensors

Done:
  - Add an app and play with customizing the Admin
  - Build a no-Model Admin page
  - Add Sensor/SensorSample
  - Add a management command to poll sensors

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

LATER: Oh. This a Vagrant issue. Time to upgrade. That ends this side quest.

Starting points for Admin explorations:
 - https://stackoverflow.com/questions/1379376/django-admin-section-without-model
 - https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.get_urls
 - https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#overriding-admin-templates
 - https://www.rockandnull.com/django-admin-custom-view/
 - https://blog.ovalerio.net/archives/2251

## Round 2

What's it take to make a model-less Admin page?

    ./manage.py startapp customadmin

Added 'customadmin' to the top of `INSTALLED_APPS`, added a template to override `base_site.html`,
and injected custom nav stuff.
Didn't look quite as I expected, but I probably misread the Admin HTML/CSS.

What I'd envisioned is better achieved by

    {% block header %}{{ block.super }}
    <div> my new stuff </div>
    {% endblock %}

Styling was somewhat straightforward. Punting collectstatic down the road to deployment.

Now we have a way to put in a custom nav var. Next up, a custom, no-model view.

Following https://blog.ovalerio.net/archives/2251

Have a custom page hooked into the Admin index, and can show it. Things hook to be
reasonably well hooked up.

No need for my earlier custom nav now. It looks odd sitting there.

The machinations needed to get a clean slate for `admin/custom_page.html` deserve their own template to extend.

## Round 3

Added a context processor to add a `secret` variable for templates. Just because.

Added out outline of `admin/base.html`, because we might be using it again.

Next up:
  - Add an app to hold some config data
  - Add a manage command to read the config, do a think, and save results
  - Some way of visualizing results
    - an app view
    - a custom admin view? might have to deal with circular imports somehow

## Round 4

    (venv) vagrant@ubuntu-focal:/vagrant/play$ ./manage.py test
    Found 0 test(s).
    System check identified no issues (0 silenced).

    ----------------------------------------------------------------------
    Ran 0 tests in 0.000s

    OK

Well, nothing fails. But on with the show!

    ./manage.py startapp sensors

and flesh out a simple set of models.

SQLite3 needs to be induced to play well with foreign keys.
[This Stackoverflow question](https://stackoverflow.com/questions/4477269/how-to-make-on-delete-cascade-work-in-sqlite-3-7-4) purports to have a recipe.
I wonder if it could similarly be used to turn on WAL.

    (venv) vagrant@ubuntu-focal:/vagrant/play$ python manage.py makemigrations sensors
    Migrations for 'sensors':
      sensors/migrations/0001_initial.py
        - Create model Sensor
        - Create model SensorSample

Followed by this (with manual reformatting):

    (venv) vagrant@ubuntu-focal:/vagrant/play$ ./manage.py sqlmigrate sensors 0001
    BEGIN;
    --
    -- Create model Sensor
    --
    CREATE TABLE "sensors_sensor" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "created" datetime NOT NULL, "sensor_id" integer unsigned NOT NULL CHECK ("sensor_id" >= 0),
        "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
    --
    -- Create model SensorSample
    --
    CREATE TABLE "sensors_sensorsample" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "sampled_at" datetime NOT NULL,
        "data" text NOT NULL,
        "sensor_id" bigint NOT NULL REFERENCES "sensors_sensor" ("id") DEFERRABLE INITIALLY DEFERRED);
    CREATE INDEX "sensors_sensor_user_id_bb274f19" ON "sensors_sensor" ("user_id");
    CREATE INDEX "sensors_sensorsample_sensor_id_5237ddb8" ON "sensors_sensorsample" ("sensor_id");
    COMMIT;

which isn't showing any trace of that cascading delete. Uh... Maybe a full rebuild of the db?

Nope. sqlite3 `.schema` is showing

    CREATE TABLE IF NOT EXISTS "sensors_sensorsample" (
      "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
      "sampled_at" datetime NOT NULL,
      "data" text NOT NULL,
      "sensor_id" bigint NOT NULL REFERENCES "sensors_sensor" ("id") DEFERRABLE INITIALLY DEFERRED);

Added the rest of the plumbing to get Sensor and SensorSample into the Admin. Looks good.

Added a sensor, added a dummy sample, deleted the sensor, and noted that the Admin advise that the sample would also be deleted.
So it appears Django is involved in enforcing the cascade.
I wonder if the intervention I added from the Stackoverflow question is having any effect? An experiment shows no, so removing it.

Plumbed in support for `django-dotenv` per their docs. Added example usage.

Plumbed in a management command to pool sensors and save fake samples. Now to decide where the real polling code belongs.

And, yay! We're pulling data from https://api.purpleair.com

That isn't the intent of this exercise, though it provides an excuse to do a bit more Admin customization.

Not a fan of embedding markup in models, but that's what the Django docs suggest for some custom Admin columns.

### Further populating a custom admin page

Looking ahead a step `django.utils.module_loading.import_string` is
a way to do a deferred import, as I might need to do in a custom Admin page.
See how `admin/templates/backends/jinja2.py` handles the `context_processors` list.

And... circular imports weren't a problem when adding the logged-in user's sensor count to the custom admin page. Cool.

## Post Round 4 Thoughts

The way to build custom admin pages is kind of weird. It's not a normal view. Can it support pagination? Probably.

Injecting pages in sideways, by way of /admin/whatever/ urls that the Admin doesn't know about might kind of work,
but could take a lot of futzing to reproduce context.

Thinking that maybe getting links to non-Admin pages into the Admin list might be a good next step.
Views for these would have to enforce the same requirements as Admin (`is_staff`).

To recap: A goal is to provide extra, possibly non-Model tooling to staff users.
Status dashboards, for example. Strictly speaking, these don't have to be part of the Admin,
though the affordance for adding Admin urls does seem to want them to be.

Gotta think on this.

## A brief digression into making SQL happen

https://docs.djangoproject.com/en/4.2/topics/db/queries/

Here's a way to iterate toward queries:

```
(venv) vagrant@ubuntu-focal:/vagrant/play$ ./manage.py shell
...
>>> from sensors.models import Sensor
>>> q = Sensor.objects.filter(id=1)
>>> print(q.query)
SELECT "sensors_sensor"."id", "sensors_sensor"."user_id", "sensors_sensor"."created", "sensors_sensor"."sensor_id"
FROM "sensors_sensor"
WHERE "sensors_sensor"."id" = 1
>>> 
```

## Round 5 Prelims

Back on (repaired) primary laptop. YAY!

Two common approaches to URLs:

  * project/urls.py knows about all of the views
  * app/urls.py knows about that app's views, and is referenced from the project/urls.py, which only knows about apps
  * (Class-based is a third, but uncommon in my experience)

The advantages of the former is that all app urls are visible in one place.
The downside, in theory, is that it makes apps less reusable across projects.
In practices, apps rarely get reused.

The official tutorial uses the latter, but oddly, `startapp` doesn't construct it. It's mentioned in a comment project/urls.py.
One more file, but once a new app is hooked up, adding a view only touches files within the app.

I can image an inflection point, but at the scale I'm working, the benefit of seeing all of the URLs layed out in one place
outweighs the minor nuisance of having to change a file outside of the app when adding a view.

## Round 5

Views, templates, and Forms oh my. Wondering how much progress I can make without leaving the dev runner.

 * Wired up a trivial view from sensors.
 * Use a template
 * Refactor out a base template
 * Add a stylesheet (which, oddly, 404d until restarting the dev server)

Well, requiring login. Yeah. Getting login set up with templates is out-of-scope for this effort unless I later decide otherwise,
so delegate login to Admin. Definitely mixed feelings here.

Bludgeoned logging into working. Not happy with the result, but it works.
