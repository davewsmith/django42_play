# Speed running the Django Tutorial

Because I haven't started a Django project from scratch for entirely too long.

See https://docs.djangoproject.com/en/4.2/faq/install/#what-python-version-can-i-use-with-django for Python version requirements.
(Python 3.8.x is the minimum for 4.0, 4.1, and 4.2; Django 3.2 can be used with 3.6.x.)ZZ

## [Writing your first Django app, part 1](https://docs.djangoproject.com/en/4.2/intro/tutorial01/)

    $ python -m django --version

So, they're assuming it's intalled globally. Translation to `venv` is trivial.

    $ cd where-i-want-to-put-it
    $ django-admin startproject mysite

results in

    mysite/
        manage.py
        mysite/
            __init__.py
            settings.py
            urls.py
            asgi.py
            wsgi.py

then

    $ python manage.py runserver

or

    $ python manage.py runserver 0.0.0.0:8000  # if in VM or container

brings it up on port 8000.

    $ python manage.py runserver 0.0.0.0:8000

### Adding an app

    $ python manage.py startapp polls

adds

    polls/
        __init__.py
        admin.py
        apps.py
        migrations/
            __init__.py
        models.py
        tests.py
        views.py

https://docs.djangoproject.com/en/4.2/intro/tutorial01/#write-your-first-view adds a view
which, oddly, requires manually creating `urls.py`.

See that doc for a discussion of `route()` and its options.

## [Writing your first Django app, part 2](https://docs.djangoproject.com/en/4.2/intro/tutorial02/)


Database setup, noting that SQLite3 is the default.

A quick overview of `settings.py` with a note to set `TIME_ZONE`.

`INSTALLED_APPS` contains what it's contained since last I looked.

    $ python manage.py migrate

Runs migrations for whatever is installed.

### [Creating Models](https://docs.djangoproject.com/en/4.2/intro/tutorial02/#creating-models)

...

Add `polls` to `INSTALLED_APPS` then

    $ python manage.py makemigrations polls

"By running makemigrations, you’re telling Django that you’ve made some changes to your models (in this case, you’ve made new ones) and that you’d like the changes to be stored as a migration."

    $ python manage.py sqlmigrate polls 0001

pre-flights the migration by showing what SQL would be used. ('0001' is in the output from `makemigration`). Then

    $ python manage.py migrate

to apply unapplied migrations.

### [Playing with the API](https://docs.djangoproject.com/en/4.2/intro/tutorial02/#playing-with-the-api)

   $ python manage.py shell

and then a demo, which requires knowing what to import.

Adding convenience methods to Models.

### [Introducing the Django Admin](https://docs.djangoproject.com/en/4.2/intro/tutorial02/#introducing-the-django-admin)

    $ python manage.py createsuperuser

to add the first user, who'll get the staff perms needed to see the admin.

    http://127.0.0.1:8000/admin/

Make the app visibile in the admin. Edit `polls/admin.py` to add

    from django.contrib import admin
    from .models import Question
    admin.site.register(Question)

A brief discussion of what you get for free. Looks unchanged.


## [Writing your first Django app, part 3](https://docs.djangoproject.com/en/4.2/intro/tutorial03/)

Views and url patterns. We haven't added these for `polls` yet.

Modifying `pools/views.py` and `polls/urls.py`

    app_name = "pools"  # adds in implicit /polls/
    url_patterns = [
        path("", views.index, name="index"),
        ...

This is different from what I remember, which involved tweaking settings.

Create a `templates` directory in `polls`.
Advise on deeper nesting to avoid name conflicts.
E.g., `polls/templates/polls/index.html`.


`render()` shortcut. `get_object_or_404` shortcut. `get_list_or_404` shortcut, which raises on an empty list.

Templates. Looks unchanged.

Instead of `<a href="/polls/{{ question.id }}/">` use `<a href="{% url 'detail' question.id %}">`

Or, if urls are namespaced, `<a href="{% url 'polls:detail' question.id %}">`.


## [Writing your first Django app, part 4](https://docs.djangoproject.com/en/4.2/intro/tutorial04/)

Minimal forms, with `{% csrf_token %}`!

`forloop.counter` is 1-based.

`request.GET` and `request.POST` are dicionary-like; values are always strings.

    from django.http import HttpResponse, HttpResponseRedirect
    from django.urls import reverse
    ...
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    # redirect to /pools/3/results/

### [Use generic views: Less code is better](https://docs.djangoproject.com/en/4.2/intro/tutorial04/#use-generic-views-less-code-is-better)

This is a part I skipped over years back. Revisit later.


## [Writing your first Django app, part 5](https://docs.djangoproject.com/en/4.2/intro/tutorial05/#writing-your-first-django-app-part-5)

Finally, testing.

Still based on `unittest`. I.e., `from django.test import TestCase`


    $ python manage.py test polls


### [Test a View](https://docs.djangoproject.com/en/4.2/intro/tutorial05/#test-a-view)

    $ python manage.py shell
    >>> from django.test.utils import setup_test_environment
    >>> setup_test_environment()
    >>> from django.test import Client
    >>> # create an instance of the client for our use
    >>> client = Client()

    >>> response = client.get("/")
    Not Found: /
    >>> response.status_code
    404

    >>> from django.urls import reverse
    >>> response = client.get(reverse("polls:index"))
    >>> response.status_code
    200
    >>> response.content
    b'...'
    >>> response.context["latest_question_list"]
    <QuerySet [<Question: What's up?>]>

https://docs.djangoproject.com/en/4.2/topics/testing/ is more comprehensive

"Django includes LiveServerTestCase to facilitate integration with tools like Selenium."

https://docs.djangoproject.com/en/4.2/topics/testing/advanced/#topics-testing-code-coverage


## [Writing your first Django app, part 6](https://docs.djangoproject.com/en/4.2/intro/tutorial06/)

Dealing with static files

"Django’s STATICFILES_FINDERS setting contains a list of finders that know how to discover static files from various sources. One of the defaults is AppDirectoriesFinder which looks for a “static” subdirectory in each of the INSTALLED_APPS, like the one in polls we just created. The admin site uses the same directory structure for its static files."

Create `polls/static/polls/style.css` the in templates do

    {% load static %}
    <link rel="stylesheet" href="{% static 'polls/style.css' %}">

Q: No more `collectstatic`?


## [Writing your first Django app, part 7](https://docs.djangoproject.com/en/4.2/intro/tutorial07/)

Customizing the Admin

Change `polls/admin.py`

    from django.contrib import admin
    from .models import Question

    class QuestionAdmin(admin.ModelAdmin):
        fields = ["pub_date", "question_text"]


    admin.site.register(Question, QuestionAdmin)

This changes the orer of fields presented for `Question`.

Using `fieldsets` to break an admin page into sections.

Subclassing `admin.StackedInLine` add the ability to edit related (by foreign key) objects.

`admin.TabularInline` does this more compactly.

Adding model methods to `list_display` (they'll be read-only and can't be sorted on).

`list_filter = ["pub_date"]` for adding a sidebar

`search_fields = ["question_text"]` to add a search box (which fronts a LIKE query)

and others

### [Customize the admin look and feel](https://docs.djangoproject.com/en/4.2/intro/tutorial07/#customize-the-admin-look-and-feel)

Create a top-level `templates/` in the same directory as `manage.py`. Then edit `settings.py` and add

    TEMPLATES = [
        ...
        "DIRS": [BASE_DIR / "templates"],  # < add this
        "APP_DIRS": True,

Then create `./templates/admin` and copy `admin/base_site.html` from the Django admin templates. Modify!

Ditto with `admin/index.html`

There's more doc on this elsewhere.

## [Writing your first Django app, part 8]

Third-party stuff. E.g., Django Debug Toolbar

    $ python -m pip install django-debug-toolbar

then follow [it's installation guide](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html)

## End of Tutorial

