from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    # Demo page
    path('demo/', views.chatbot_demo, name='demo'),
    
    # Chatbot widget
    path('widget/', views.chatbot_widget, name='widget'),
    
    # API endpoints
    path('api/start/', views.start_chat, name='start_chat'),
    path('api/send/', views.send_message, name='send_message'),
    path('api/history/<str:session_id>/', views.get_chat_history, name='get_history'),
    path('api/end/', views.end_chat, name='end_chat'),
    
    # Admin views
    path('analytics/', views.chat_analytics, name='analytics'),
] 