from django.contrib import admin
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'user', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'user__username')
