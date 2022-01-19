from django.contrib.admin.apps import AdminConfig


class GreenhouseAdminConfig(AdminConfig):
    default_site = 'GreenhouseSite.admin.GreenhouseAdminSite'