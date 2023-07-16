from django.contrib.admin import AdminSite
# Register your models here.

class CustomAdminSite(AdminSite):
    site_header = 'Halaman Admin'
