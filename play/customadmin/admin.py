import os

from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path

from sensors.models import Sensor


class CustomAdminSite(admin.AdminSite):
    site_header = "Custom Site Admin header"
    site_title = "Custom Site Admin title"
    index_template = "admin/custom_index.html"

    def custom_page(self, request):
        context = {
            "page_name": "custom page",  # for breadcrumb
            "title": "custom page",
            "subtitle": "",
            "motd": os.getenv("MOTD", "No message today. Maybe there's no .env"),
            "sensor_count": self.get_sensor_count(request.user),
            **self.each_context(request),
        }
        return TemplateResponse(request, "admin/custom_page.html", context)        

    def get_sensor_count(self, user):
        return Sensor.objects.filter(user=user).count()
        

    def get_urls(self):
        return [
            path("custom_page/",
                self.admin_view(self.custom_page),
                name="custom_page"),
        ] + super().get_urls()
