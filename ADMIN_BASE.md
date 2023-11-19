# admin/base.html

An outline of the base admin template

    head
      title {% block title %}
      link stylesheet {% block stylesheet %} admin/css/base.css
      {% block dark-mode-vars %}
        link stylesheet admin/css/dark_mode.css
        script admin/js/theme.js
      link stylesheet admin/css/nav_sidebar.css
      script admin/js/nav_sidebar.js
      {% block extrastyle %}
      {% block extrahead %}
      {% block responsive %}
        meta viewport
        link stylesheet admin/css/responsive.css
      {% block blockbots %}

    body {% block bodyclass %}
      a href #content-start
      div #container
        {% block header %}
          div #header
            div #branding {% block branding %}
            {% block usertools %}
              div #user-tools
                {% block welcome-msg %} Welcome, ...
                {% block userlinks %} ... logout / theme toggle
          {% block nav-breadcrumbs %}
            nav
              {% block breadcrumbs %}
                div #breadcrumbs
          div #main
            {% block nav-sidebar %}
              {% include admin/nav_sidebar.html %}
            div #content-start
              {% block messages %} ... messagelist
              div #content {% block coltype %}
                {% block pretitle %}
                {% block content_title %} h1 {{ title }}
                {% block content_subtitle %} h2 {{ subtitle }}
                {% block content %}
                  {% block object-tools %}
                  {{ content }}
                {% block sidebar %}
              {% block footer %}
