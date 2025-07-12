from django.contrib import admin
from .models import TaskStatus, Message

@admin.register(TaskStatus)
class TaskStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'result', 'created', 'updated')
    search_fields = ('id', 'status', 'result')
    list_filter = ('status', 'created', 'updated', 'result')
    readonly_fields = ('created', 'updated')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'category', 'created', 'updated')
    search_fields = ('id', 'text', 'category')
    list_filter = ('category', 'created', 'updated', 'text')
    readonly_fields = ('created', 'updated')
