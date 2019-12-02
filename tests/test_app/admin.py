from django.contrib import admin

from tests.test_app.models import Page


class PageAdmin(admin.ModelAdmin):
    change_list_template = 'smuggler/change_list.html'


admin.site.register(Page, PageAdmin)
