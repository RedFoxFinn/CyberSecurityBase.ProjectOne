"""
Admin configuration for the core app - Task Management.
"""
from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'status', 'priority', 'created_at')
    list_filter = ('status', 'priority', 'created_at', 'owner')
    search_fields = ('title', 'description', 'owner__username')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Task Information', {
            'fields': ('title', 'description', 'owner', 'status', 'priority')
        }),
        ('Dates', {
            'fields': ('due_date', 'created_at', 'updated_at')
        }),
    )

    def get_queryset(self, request):
        """Allow admins to see all tasks, regular users only see their own."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)
