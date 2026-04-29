from django.contrib import admin
from .models import Message, Attachment


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0
    readonly_fields = ('uploaded_at', 'size')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'recipient', 'status', 'is_read', 'created_at')
    list_filter = ('status', 'is_group', 'is_read')
    search_fields = ('subject', 'body', 'sender__username', 'recipient__username')
    inlines = [AttachmentInline]
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('original_name', 'message', 'size', 'uploaded_at')
    search_fields = ('original_name', 'message__subject')
