from django.contrib import admin
from django.utils.html import format_html
from .models import ChatSession, ChatMessage, ChatbotConfiguration, FAQ, ChatAnalytics


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'user', 'created_at', 'message_count', 'is_active', 'current_page']
    list_filter = ['is_active', 'created_at', 'user']
    search_fields = ['session_id', 'user__username', 'current_page']
    readonly_fields = ['session_id', 'created_at', 'updated_at']
    
    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Messages'


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'message_type', 'content_preview', 'timestamp', 'response_time', 'tokens_used']
    list_filter = ['message_type', 'timestamp', 'model_used']
    search_fields = ['content', 'session__session_id', 'user_intent']
    readonly_fields = ['timestamp']
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content'


@admin.register(ChatbotConfiguration)
class ChatbotConfigurationAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'max_tokens', 'temperature', 'updated_at']
    list_editable = ['is_active', 'max_tokens', 'temperature']
    fieldsets = (
        ('Basic Settings', {
            'fields': ('name', 'is_active')
        }),
        ('Messages', {
            'fields': ('welcome_message', 'system_prompt')
        }),
        ('AI Settings', {
            'fields': ('max_tokens', 'temperature')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ['created_at', 'updated_at']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question_preview', 'category', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['question', 'answer', 'category']
    list_editable = ['is_active']
    
    def question_preview(self, obj):
        return obj.question[:80] + '...' if len(obj.question) > 80 else obj.question
    question_preview.short_description = 'Question'


@admin.register(ChatAnalytics)
class ChatAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_sessions', 'total_messages', 'avg_response_time', 'total_tokens_used']
    list_filter = ['date']
    readonly_fields = ['date', 'total_sessions', 'total_messages', 'avg_response_time', 'total_tokens_used', 'common_questions']
    
    def has_add_permission(self, request):
        return False  # Analytics are auto-generated
