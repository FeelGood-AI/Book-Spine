from django.contrib import admin
from .models import Memoir


class MemoirAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Memoir._meta.fields if field.name != "id"]


admin.site.register(Memoir,MemoirAdmin)
