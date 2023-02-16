from django.contrib import admin

from .models import Prompt

class PromptAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Prompt._meta.fields if field.name != "id"]


admin.site.register(Prompt,PromptAdmin)

