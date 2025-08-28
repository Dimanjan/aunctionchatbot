// Enhanced Chatbot JavaScript
class ChatbotWidget {
    constructor() {
        this.currentSessionId = null;
        this.isTyping = false;
        this.messageQueue = [];
        this.isInitialized = false;
        
        this.init();
    }
    
    init() {
        document.addEventListener('DOMContentLoaded', () => {
            console.log('Enhanced chatbot widget loaded');
            this.setupEventListeners();
            this.addWelcomeMessage();
            this.isInitialized = true;
        });
    }
    
    setupEventListeners() {
        // Add click animation to button
        const button = document.getElementById('chatbot-button');
        if (button) {
            button.addEventListener('click', (e) => {
                this.addClickAnimation(e.target);
            });
        }
        
        // Close chat when clicking outside
        document.addEventListener('click', (e) => {
            this.handleOutsideClick(e);
        });
        
        // Handle input changes
        const input = document.getElementById('chatbot-input');
        if (input) {
            input.addEventListener('input', () => this.updateSendButton());
            input.addEventListener('keypress', (e) => this.handleKeyPress(e));
        }
    }
    
    addClickAnimation(element) {
        element.style.transform = 'scale(0.95)';
        setTimeout(() => {
            element.style.transform = 'scale(1)';
        }, 150);
    }
    
    addWelcomeMessage() {
        const messagesContainer = document.getElementById('chatbot-messages');
        if (messagesContainer && messagesContainer.children.length === 0) {
            const welcomeDiv = document.createElement('div');
            welcomeDiv.className = 'chatbot-message bot';
            welcomeDiv.innerHTML = `
                <div class="chatbot-message-content">
                    👋 Hi there! I'm your AuctionVistas assistant. I can help you with:
                    <br><br>
                    • Placing bids and auction rules<br>
                    • Payment methods and security<br>
                    • Creating and managing auctions<br>
                    • Account and technical support<br><br>
                    How can I assist you today?
                </div>
                <div class="chatbot-message-time">${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>
            `;
            messagesContainer.appendChild(welcomeDiv);
        }
    }
    
    toggleChat() {
        const window = document.getElementById('chatbot-window');
        const button = document.getElementById('chatbot-button');
        
        if (window.classList.contains('active')) {
            window.classList.remove('active');
            button.style.transform = 'scale(1)';
        } else {
            window.classList.add('active');
            window.classList.remove('minimized');
            button.style.transform = 'scale(1.1)';
            
            // Start chat if not already started
            if (!this.currentSessionId) {
                this.startChat();
            }
            
            // Focus input
            setTimeout(() => {
                const input = document.getElementById('chatbot-input');
                if (input) input.focus();
            }, 300);
        }
    }
    
    minimizeChat() {
        const window = document.getElementById('chatbot-window');
        window.classList.add('minimized');
    }
    
    async startChat() {
        try {
            const response = await fetch('/chatbot/api/start/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCookie('csrftoken')
                },
                body: JSON.stringify({})
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.currentSessionId = data.session_id;
                // Welcome message is already added by addWelcomeMessage()
            } else {
                console.error('Failed to start chat:', data.error);
            }
        } catch (error) {
            console.error('Error starting chat:', error);
        }
    }
    
    async sendMessage() {
        const input = document.getElementById('chatbot-input');
        const sendBtn = document.getElementById('chatbot-send');
        const message = input.value.trim();
        
        if (!message || this.isTyping) return;
        
        // Add loading state to send button
        sendBtn.classList.add('loading');
        sendBtn.disabled = true;
        
        // Add user message
        this.addMessage('user', message);
        input.value = '';
        this.updateSendButton();
        
        // Show typing indicator
        this.showTyping(true);
        
        try {
            const response = await fetch('/chatbot/api/send/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCookie('csrftoken')
                },
                body: JSON.stringify({
                    session_id: this.currentSessionId,
                    message: message
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.addMessage('bot', data.response, data.timestamp);
            } else {
                this.addMessage('bot', 'Sorry, I encountered an error. Please try again.');
            }
        } catch (error) {
            console.error('Error sending message:', error);
            this.addMessage('bot', 'Sorry, I\'m having trouble connecting. Please try again.');
        } finally {
            this.showTyping(false);
            // Remove loading state
            sendBtn.classList.remove('loading');
            sendBtn.disabled = false;
        }
    }
    
    sendQuickReply(message) {
        const input = document.getElementById('chatbot-input');
        if (input) {
            input.value = message;
            this.sendMessage();
        }
    }
    
    addMessage(type, content, timestamp = null) {
        const messagesContainer = document.getElementById('chatbot-messages');
        if (!messagesContainer) return;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `chatbot-message ${type}`;
        
        const time = timestamp ? 
            new Date(timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : 
            new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        
        messageDiv.innerHTML = `
            <div class="chatbot-message-content">${this.escapeHtml(content)}</div>
            <div class="chatbot-message-time">${time}</div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        
        // Smooth scroll to bottom
        setTimeout(() => {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }, 100);
        
        // Hide quick replies after first message
        if (type === 'user') {
            const quickReplies = document.getElementById('quick-replies');
            if (quickReplies) {
                quickReplies.style.display = 'none';
            }
        }
    }
    
    showTyping(show) {
        const typingIndicator = document.getElementById('chatbot-typing');
        if (typingIndicator) {
            typingIndicator.style.display = show ? 'flex' : 'none';
        }
        this.isTyping = show;
    }
    
    handleKeyPress(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            this.sendMessage();
        }
    }
    
    updateSendButton() {
        const input = document.getElementById('chatbot-input');
        const sendBtn = document.getElementById('chatbot-send');
        
        if (input && sendBtn) {
            const hasText = input.value.trim().length > 0;
            sendBtn.disabled = !hasText;
        }
    }
    
    handleOutsideClick(event) {
        const widget = document.getElementById('chatbot-widget');
        const window = document.getElementById('chatbot-window');
        
        if (widget && window && !widget.contains(event.target) && window.classList.contains('active')) {
            this.toggleChat();
        }
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // Public methods for global access
    static getInstance() {
        if (!ChatbotWidget.instance) {
            ChatbotWidget.instance = new ChatbotWidget();
        }
        return ChatbotWidget.instance;
    }
}

// Initialize chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.chatbot = ChatbotWidget.getInstance();
});

// Global functions for onclick handlers
function toggleChat() {
    if (window.chatbot) {
        window.chatbot.toggleChat();
    }
}

function minimizeChat() {
    if (window.chatbot) {
        window.chatbot.minimizeChat();
    }
}

function sendMessage() {
    if (window.chatbot) {
        window.chatbot.sendMessage();
    }
}

function sendQuickReply(message) {
    if (window.chatbot) {
        window.chatbot.sendQuickReply(message);
    }
}

function handleKeyPress(event) {
    if (window.chatbot) {
        window.chatbot.handleKeyPress(event);
    }
}

function handleInputChange() {
    if (window.chatbot) {
        window.chatbot.updateSendButton();
    }
} 