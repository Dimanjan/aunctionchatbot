from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json

from .models import ChatSession, ChatMessage, ChatbotConfiguration
from .services import ChatbotService, ChatbotUtils


def chatbot_widget(request):
    """Render the chatbot widget template"""
    config = ChatbotConfiguration.objects.filter(is_active=True).first()
    welcome_message = config.welcome_message if config else "Hello! How can I help you today?"
    
    return render(request, 'chatbot/widget.html', {
        'welcome_message': welcome_message,
        'config': config
    })


@csrf_exempt
@require_http_methods(["POST"])
def start_chat(request):
    """Start a new chat session"""
    try:
        data = json.loads(request.body)
        user_context = ChatbotUtils.get_user_context(request)
        
        # Create new session
        session_id = ChatbotUtils.create_session_id()
        session = ChatSession.objects.create(
            user=request.user if request.user.is_authenticated else None,
            session_id=session_id,
            current_page=user_context.get('current_page', ''),
            user_agent=user_context.get('user_agent', ''),
            ip_address=user_context.get('ip_address', '')
        )
        
        # Add welcome message
        chatbot_service = ChatbotService()
        welcome_message = chatbot_service.get_welcome_message()
        
        welcome_msg = ChatMessage.objects.create(
            session=session,
            message_type='bot',
            content=welcome_message,
            model_used='system'
        )
        
        return JsonResponse({
            'success': True,
            'session_id': session_id,
            'welcome_message': welcome_message,
            'timestamp': welcome_msg.timestamp.isoformat()
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def send_message(request):
    """Send a message and get bot response"""
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        user_message = data.get('message', '').strip()
        
        if not session_id or not user_message:
            return JsonResponse({
                'success': False,
                'error': 'Session ID and message are required'
            }, status=400)
        
        # Get or create session
        session, created = ChatSession.objects.get_or_create(
            session_id=session_id,
            defaults={
                'user': request.user if request.user.is_authenticated else None,
                'current_page': request.path,
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                'ip_address': request.META.get('REMOTE_ADDR', '')
            }
        )
        
        # Save user message
        user_msg = ChatMessage.objects.create(
            session=session,
            message_type='user',
            content=user_message
        )
        
        # Get chat history
        chat_history = session.messages.filter(
            message_type__in=['user', 'bot']
        ).order_by('timestamp')[:10]
        
        # Get user context
        user_context = ChatbotUtils.get_user_context(request)
        
        # Generate bot response
        chatbot_service = ChatbotService()
        result = chatbot_service.generate_response(
            user_message, 
            chat_history, 
            user_context
        )
        
        # Save bot response
        bot_msg = ChatMessage.objects.create(
            session=session,
            message_type='bot',
            content=result['response'],
            response_time=result['response_time'],
            tokens_used=result['tokens_used'],
            model_used=result['model_used']
        )
        
        # Update session
        session.updated_at = timezone.now()
        session.save()
        
        return JsonResponse({
            'success': True,
            'response': result['response'],
            'response_time': result['response_time'],
            'timestamp': bot_msg.timestamp.isoformat(),
            'session_id': session_id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_chat_history(request, session_id):
    """Get chat history for a session"""
    try:
        session = ChatSession.objects.get(session_id=session_id)
        messages = session.messages.filter(
            message_type__in=['user', 'bot']
        ).order_by('timestamp')
        
        history = []
        for msg in messages:
            history.append({
                'type': msg.message_type,
                'content': msg.content,
                'timestamp': msg.timestamp.isoformat(),
                'response_time': msg.response_time
            })
        
        return JsonResponse({
            'success': True,
            'history': history,
            'session_id': session_id
        })
        
    except ChatSession.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Session not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def end_chat(request):
    """End a chat session"""
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        
        if not session_id:
            return JsonResponse({
                'success': False,
                'error': 'Session ID is required'
            }, status=400)
        
        session = ChatSession.objects.get(session_id=session_id)
        session.is_active = False
        session.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Chat session ended'
        })
        
    except ChatSession.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Session not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def chatbot_demo(request):
    """Demo page for showcasing chatbot functionality"""
    return render(request, 'chatbot/demo.html')


@login_required
def chat_analytics(request):
    """Admin view for chat analytics"""
    from .models import ChatAnalytics
    
    # Get recent analytics
    analytics = ChatAnalytics.objects.order_by('-date')[:30]
    
    # Get recent sessions
    recent_sessions = ChatSession.objects.filter(
        is_active=False
    ).order_by('-updated_at')[:20]
    
    context = {
        'analytics': analytics,
        'recent_sessions': recent_sessions,
        'total_sessions': ChatSession.objects.count(),
        'total_messages': ChatMessage.objects.count(),
    }
    
    return render(request, 'chatbot/analytics.html', context)
