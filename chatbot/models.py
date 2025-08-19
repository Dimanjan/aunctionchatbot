from django.db import models
from django.conf import settings
from django.utils import timezone


class ChatSession(models.Model):
    """Represents a chat session between a user and the chatbot"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    # Context information
    current_page = models.CharField(max_length=200, blank=True)
    user_agent = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Chat Session {self.session_id} - {self.user.username if self.user else 'Anonymous'}"


class ChatMessage(models.Model):
    """Individual messages in a chat session"""
    MESSAGE_TYPES = [
        ('user', 'User Message'),
        ('bot', 'Bot Response'),
        ('system', 'System Message'),
    ]
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    
    # For bot responses
    response_time = models.FloatField(null=True, blank=True)  # in seconds
    tokens_used = models.IntegerField(null=True, blank=True)
    model_used = models.CharField(max_length=50, blank=True)
    
    # For user messages
    user_intent = models.CharField(max_length=100, blank=True)
    confidence_score = models.FloatField(null=True, blank=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.message_type}: {self.content[:50]}..."


class ChatbotConfiguration(models.Model):
    """Configuration settings for the chatbot"""
    name = models.CharField(max_length=100, default="AuctionVistas Assistant")
    welcome_message = models.TextField(
        default="Hello! I'm your AuctionVistas assistant. I can help you with:\n• Finding auctions\n• Understanding bidding\n• Account questions\n• Platform navigation\n\nHow can I help you today?"
    )
    system_prompt = models.TextField(
        default="You are AuctionVistas Assistant, a helpful AI assistant for an online auction platform. Help users with auction-related questions, bidding guidance, account issues, and platform navigation. Be friendly, concise, and accurate."
    )
    max_tokens = models.IntegerField(default=150)
    temperature = models.FloatField(default=0.7)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Chatbot Configuration"
        verbose_name_plural = "Chatbot Configurations"
    
    def __str__(self):
        return f"{self.name} Configuration"


class FAQ(models.Model):
    """Frequently asked questions and their answers"""
    question = models.CharField(max_length=500)
    answer = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'question']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
    
    def __str__(self):
        return f"{self.category}: {self.question[:50]}..."


class ChatAnalytics(models.Model):
    """Analytics data for chatbot usage"""
    date = models.DateField()
    total_sessions = models.IntegerField(default=0)
    total_messages = models.IntegerField(default=0)
    avg_response_time = models.FloatField(default=0.0)
    total_tokens_used = models.IntegerField(default=0)
    common_questions = models.JSONField(default=dict)
    
    class Meta:
        verbose_name = "Chat Analytics"
        verbose_name_plural = "Chat Analytics"
        unique_together = ['date']
    
    def __str__(self):
        return f"Analytics for {self.date}"
