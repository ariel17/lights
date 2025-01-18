from django.contrib import admin

from .models import Flag


class FlagAdmin(admin.ModelAdmin):
    model = Flag
    readonly_fields = ["author", "created_at", "updated_at"]
    list_display = ["name", "description", "is_enabled", "author", "created_at", "updated_at"]
    search_fields = ["name", "description"]
    ordering = ["created_at", "updated_at"]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()


admin.site.register(Flag, FlagAdmin)
