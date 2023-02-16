from django.contrib import admin

from .models import Insight


class InsightAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Insight._meta.fields if field.name != "id"]


admin.site.register(Insight,InsightAdmin)
