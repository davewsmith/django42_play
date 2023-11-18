from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path


class CustomAdminSite(admin.AdminSite):
    site_header = "Custom Site Admin header"
    site_title = "Custom Site Admin title"
    index_template = "admin/custom_index.html"

    def custom_page(self, request):
        context = {
            "page_name": "custom page",
            # TODO pass real data
            **self.each_context(request),
        }
        return TemplateResponse(request, "admin/custom_page.html", context)        

    def get_urls(self):
        return [
            path("custom_page/",
                self.admin_view(self.custom_page),
                name="custom_page"),
        ] + super().get_urls()
