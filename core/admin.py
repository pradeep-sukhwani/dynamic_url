from django.contrib import admin

# Register your models here.
from core.models import URL, URLDetail


class URLAdmin(admin.ModelAdmin):

    def time_seconds(self, obj):
        return obj.created_on.strftime("%d %b %Y %H:%M:%S UTC")

    list_display = ['endpoint', 'time_seconds', 'hit_count']
    exclude = ('hit_count',)


admin.site.register(URL, URLAdmin)
admin.site.register(URLDetail)
