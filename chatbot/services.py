import openai
import time
import json
import os
from django.conf import settings
from django.utils import timezone
from .models import ChatbotConfiguration, FAQ


class ChatbotService:
    """Service class for handling chatbot interactions with OpenAI"""
    
    def __init__(self):
        # Use environment variable only - no hardcoded keys
        self.api_key = os.getenv('OPENAI_API_KEY')
        if self.api_key:
            openai.api_key = self.api_key
        self.config = self._get_configuration()
    
    def _get_configuration(self):
        """Get the active chatbot configuration"""
        try:
            return ChatbotConfiguration.objects.filter(is_active=True).first()
        except:
            return None
    
    def _get_context_prompt(self, user_context=None):
        """Build context-aware system prompt"""
        base_prompt = self.config.system_prompt if self.config else "You are AuctionVistas Assistant, a helpful AI assistant for an online auction platform."
        
        context_info = ""
        if user_context:
            if user_context.get('current_page'):
                context_info += f"\nUser is currently on: {user_context['current_page']}"
            if user_context.get('user_authenticated'):
                context_info += "\nUser is logged in"
            else:
                context_info += "\nUser is not logged in"
        
        # Add FAQ context
        faqs = FAQ.objects.filter(is_active=True)[:5]
        if faqs:
            context_info += "\n\nRelevant FAQs:"
            for faq in faqs:
                context_info += f"\nQ: {faq.question}\nA: {faq.answer}\n"
        
        return base_prompt + context_info
    
    def _get_fallback_response(self, user_message):
        """Get a fallback response based on FAQ data"""
        user_message_lower = user_message.lower()
        
        # First, try to find exact FAQ matches with better keyword matching
        faqs = FAQ.objects.filter(is_active=True)

        # Create a comprehensive mapping of keywords to FAQ questions for better matching
        keyword_mapping = {
            # Bidding related
            'bid': ['place bid', 'bidding', 'how to bid', 'minimum bid', 'bid increment'],
            'outbid': ['outbid', 'out bid', 'someone bid higher'],
            'proxy': ['proxy bidding', 'auto bid', 'automatic bid'],
            'track': ['track bid', 'track refund', 'monitor', 'my bids'],
            'cancel': ['cancel bid', 'remove bid', 'withdraw bid'],
            'win': ['win auction', 'winner', 'what happens when win'],
            'highest': ['highest bidder', 'am i winning', 'current bid'],
            
            # Payment related
            'payment': ['payment methods', 'pay', 'money', 'accept', 'how to pay'],
            'refund': ['refund', 'get money back', 'return money'],
            'fee': ['fee', 'commission', 'cost', 'charges'],
            'hidden': ['hidden fee', 'extra cost', 'additional charge'],
            'multiple': ['multiple payment', 'split payment', 'different payment'],
            'fail': ['payment fail', 'payment failed', 'payment error'],
            'plan': ['payment plan', 'installment', 'pay later'],
            
            # Selling related
            'create': ['create auction', 'sell', 'start auction', 'list item'],
            'approval': ['auction approval', 'how long approve', 'review time'],
            'edit': ['edit auction', 'change auction', 'modify listing'],
            'ship': ['ship item', 'shipping', 'send item', 'delivery'],
            'reserve': ['reserve price', 'minimum price', 'lowest accept'],
            'category': ['sell category', 'what can sell', 'allowed items'],
            'paid': ['get paid', 'receive money', 'seller payment'],
            
            # Account related
            'profile': ['update profile', 'profile information', 'edit profile'],
            'password': ['change password', 'reset password', 'forgot password'],
            'verify': ['verify account', 'account verification', 'verify identity'],
            'multiple account': ['multiple accounts', 'more than one account'],
            'delete': ['delete account', 'close account', 'remove account'],
            'history': ['purchase history', 'buying history', 'past purchases'],
            
            # Support related
            'damaged': ['damaged item', 'broken', 'problem', 'defective'],
            'contact': ['contact support', 'help', 'customer service', 'support team'],
            'return': ['return policy', 'return item', 'send back'],
            'report': ['report seller', 'report user', 'problem seller'],
            'arrive': ['item arrive', 'never arrive', 'shipping delay'],
            'dispute': ['dispute transaction', 'problem with sale', 'conflict'],
            
            # Platform related
            'search': ['search item', 'find item', 'look for'],
            'watch': ['watch later', 'save item', 'favorite'],
            'notification': ['notification', 'alert', 'email alert'],
            'category': ['auction category', 'item category', 'what categories'],
            'sort': ['sort result', 'order by', 'filter'],
            'history': ['auction history', 'past auction', 'completed auction'],
            'block': ['block seller', 'block user', 'ignore seller'],
            'time': ['auction time', 'duration', 'how long'],
            'feedback': ['feedback', 'rating', 'review'],
            'rule': ['platform rule', 'auction rule', 'policy']
        }

        # Check for specific keyword matches first
        for keyword, related_terms in keyword_mapping.items():
            if any(term in user_message_lower for term in related_terms):
                # Find the most relevant FAQ
        for faq in faqs:
                    faq_lower = faq.question.lower()
                    if any(term in faq_lower for term in related_terms):
                return faq.answer
        
        # Enhanced specific question matching
        if any(word in user_message_lower for word in ['place', 'put', 'make']) and 'bid' in user_message_lower:
            return "To place a bid, navigate to the auction item you want to bid on, enter your bid amount in the bidding section, and click 'Place Bid'. Make sure you have sufficient funds in your account. Your bid must be higher than the current highest bid."
        
        elif any(word in user_message_lower for word in ['payment', 'pay', 'money']) and any(word in user_message_lower for word in ['method', 'accept', 'way']):
            return "We accept various payment methods including bank transfers, UPI, credit/debit cards, digital wallets (Paytm, PhonePe), and QR code payments. All payments are processed securely through our platform."
        
        elif any(word in user_message_lower for word in ['create', 'start', 'list']) and 'auction' in user_message_lower:
            return "To create an auction, click on 'Create Auction' in the navigation menu. Fill in the item details, upload high-quality images, set your starting price and duration, then submit for approval. Approval typically takes 24-48 hours."
        
        elif 'track' in user_message_lower and 'bid' in user_message_lower:
            return "You can track your bids in your account dashboard under 'My Bids'. This shows all your active bids, bid history, and auction status."
        
        elif any(word in user_message_lower for word in ['rule', 'policy', 'guideline']):
            return "Our auction rules include: 1) Bids are binding and cannot be cancelled, 2) Payment must be completed within 24 hours of winning, 3) All items are sold as-is, 4) Shipping costs are additional, 5) No shill bidding allowed."
        
        elif any(word in user_message_lower for word in ['available', 'current', 'active']) and 'auction' in user_message_lower:
            return "You can view all currently available auctions on our homepage or browse by category. Use the search function to find specific items you're interested in."
        
        elif any(word in user_message_lower for word in ['help', 'support', 'assist']):
            return "You can contact our support team through the contact form, by emailing support@auctionvistas.com, or calling our helpline. Our team will respond within 24 hours."
        
        elif 'win' in user_message_lower and 'auction' in user_message_lower:
            return "When you win an auction, you will receive a notification and email. You will need to complete the payment within 24 hours. The seller will then ship the item to you within 3-5 business days."
        
        elif any(word in user_message_lower for word in ['cancel', 'remove', 'withdraw']) and 'bid' in user_message_lower:
            return "Bids cannot be cancelled once placed. Please make sure you want to place a bid before confirming. You can place a higher bid if you want to increase your offer."
        
        elif any(word in user_message_lower for word in ['damaged', 'broken', 'defective', 'problem']):
            return "If you receive a damaged item, contact our support team immediately with photos of the damage. We will help you resolve the issue with the seller, including refunds or replacements."
        
        elif any(word in user_message_lower for word in ['fee', 'commission', 'cost', 'charge']):
            return "Seller fees are typically 5-10% of the final sale price, depending on the item category and sale value. Electronics: 8%, Art: 10%, Collectibles: 7%, General: 5%. No hidden fees for buyers."
        
        elif 'refund' in user_message_lower:
            return "You can track your refund by going to your payment history page. Refunds are typically processed within 3-5 business days after approval. You will receive email updates on refund status."
        
        elif any(word in user_message_lower for word in ['profile', 'account', 'information']) and any(word in user_message_lower for word in ['update', 'change', 'edit']):
            return "To update your profile, go to your profile page and click 'Edit Profile'. You can update your personal information, contact details, shipping addresses, and preferences."
        
        elif any(word in user_message_lower for word in ['search', 'find', 'look']) and 'item' in user_message_lower:
            return "Use the search bar at the top of the page. You can search by item name, category, seller, or keywords. Use filters to narrow results by price, location, or auction end time."
        
        elif any(word in user_message_lower for word in ['save', 'watch', 'favorite']) and 'item' in user_message_lower:
            return "Click the heart icon on any auction to add it to your watchlist. You can view all watched items in your account dashboard under 'My Watchlist'."
        
        elif 'notification' in user_message_lower or 'alert' in user_message_lower:
            return "Enable notifications in your account settings. You'll receive alerts for outbids, auction endings, new items in your categories, and important account updates."
        
        elif 'category' in user_message_lower:
            return "Our main categories include Electronics, Art & Collectibles, Jewelry & Watches, Antiques, Books & Media, Sports & Hobbies, Fashion & Accessories, Home & Garden, and Vehicles."
        
        elif any(word in user_message_lower for word in ['sort', 'order', 'filter']):
            return "Use the sort options on auction listing pages: by ending time, price (low to high), price (high to low), newest first, or most popular."
        
        elif 'history' in user_message_lower and 'auction' in user_message_lower:
            return "Yes, you can view auction history for completed auctions. This shows final prices, number of bidders, and bidding activity. Useful for pricing your own items."
        
        elif any(word in user_message_lower for word in ['block', 'ignore']) and 'seller' in user_message_lower:
            return "Go to any seller's profile page and click 'Block User'. You won't see their auctions in search results, and they cannot bid on your items."
        
        elif any(word in user_message_lower for word in ['time', 'duration', 'how long']) and 'auction' in user_message_lower:
            return "Auctions can be set for 3, 5, 7, or 10 days. Extended bidding may occur if bids are placed in the final minutes. Minimum auction duration is 3 days."
        
        elif any(word in user_message_lower for word in ['feedback', 'rating', 'review']):
            return "Your feedback rating is visible on your profile page. You can view detailed feedback from buyers and sellers in your account dashboard under 'My Feedback'."
        
        elif any(word in user_message_lower for word in ['minimum', 'increment']) and 'bid' in user_message_lower:
            return "The minimum bid increment varies by auction value: ₹50 for items under ₹1,000, ₹100 for items ₹1,000-₹5,000, ₹250 for items ₹5,000-₹10,000, and ₹500 for items above ₹10,000."
        
        elif 'proxy' in user_message_lower and 'bid' in user_message_lower:
            return "Proxy bidding allows you to set a maximum bid amount. The system will automatically bid on your behalf up to that amount, helping you win auctions without constant monitoring."
        
        elif any(word in user_message_lower for word in ['approval', 'review', 'approve']) and 'auction' in user_message_lower:
            return "Auction approval typically takes 24-48 hours. We review item descriptions, images, and pricing to ensure quality and compliance with our policies."
        
        elif any(word in user_message_lower for word in ['edit', 'change', 'modify']) and 'auction' in user_message_lower:
            return "You can edit your auction description and images before the first bid is placed. Once bidding starts, only minor corrections are allowed. Contact support for major changes."
        
        elif any(word in user_message_lower for word in ['ship', 'deliver', 'send']) and 'item' in user_message_lower:
            return "After receiving payment, you have 3-5 business days to ship the item. Use our shipping calculator for accurate costs. Always use tracking numbers and insure valuable items."
        
        elif 'reserve' in user_message_lower and 'price' in user_message_lower:
            return "You can set a reserve price when creating your auction. This is the minimum price you're willing to accept. If bidding doesn't reach the reserve, the item won't sell."
        
        elif any(word in user_message_lower for word in ['payment', 'pay']) and 'time' in user_message_lower:
            return "You have 24 hours to complete payment after winning an auction. Failure to pay may result in account suspension and the item being offered to the next highest bidder."
        
        elif any(word in user_message_lower for word in ['hidden', 'extra', 'additional']) and 'fee' in user_message_lower:
            return "No hidden fees. All fees are clearly displayed: buyer pays the final bid amount plus shipping. Sellers pay our commission (5-10%) based on the final sale price."
        
        elif any(word in user_message_lower for word in ['multiple', 'split']) and 'payment' in user_message_lower:
            return "Yes, you can split payment across multiple methods. For example, pay part with UPI and part with credit card. Contact support if you need assistance with split payments."
        
        elif any(word in user_message_lower for word in ['fail', 'error', 'problem']) and 'payment' in user_message_lower:
            return "If payment fails, try again with a different method. Common issues include insufficient funds, expired cards, or network problems. Contact support if problems persist."
        
        elif any(word in user_message_lower for word in ['plan', 'installment', 'later']) and 'payment' in user_message_lower:
            return "Currently, we don't offer payment plans. Full payment is required within 24 hours of winning. We're working on installment options for high-value items."
        
        elif any(word in user_message_lower for word in ['password', 'reset', 'forgot']):
            return "Go to your profile settings and click 'Change Password'. You'll need to enter your current password and then your new password twice for confirmation."
        
        elif any(word in user_message_lower for word in ['verify', 'verification', 'identity']):
            return "Account verification requires a valid phone number and email address. You may also need to provide ID proof for high-value transactions. Verification typically takes 24 hours."
        
        elif any(word in user_message_lower for word in ['multiple', 'more']) and 'account' in user_message_lower:
            return "No, each person should have only one account. Multiple accounts may be suspended. If you need a business account, contact support for special arrangements."
        
        elif any(word in user_message_lower for word in ['delete', 'close', 'remove']) and 'account' in user_message_lower:
            return "To delete your account, contact support. Note that you cannot delete your account if you have active auctions or pending transactions."
        
        elif any(word in user_message_lower for word in ['purchase', 'buying', 'bought']) and 'history' in user_message_lower:
            return "Your purchase history is available in your account dashboard under 'My Purchases'. This shows all items you've won, payment status, and shipping information."
        
        elif any(word in user_message_lower for word in ['return', 'send back', 'refund']) and 'policy' in user_message_lower:
            return "Returns are accepted within 7 days of receipt if the item is significantly different from the description. Contact support to initiate a return. Shipping costs are typically the buyer's responsibility."
        
        elif any(word in user_message_lower for word in ['report', 'problem']) and 'seller' in user_message_lower:
            return "To report a problem seller, go to their profile page and click 'Report User'. Provide detailed information about the issue. We investigate all reports and take appropriate action."
        
        elif any(word in user_message_lower for word in ['arrive', 'delivery', 'shipping']) and 'never' in user_message_lower:
            return "If your item doesn't arrive within the expected timeframe, contact support with your order details. We will investigate and help resolve the issue, including refunds if necessary."
        
        elif any(word in user_message_lower for word in ['dispute', 'conflict', 'problem']) and 'transaction' in user_message_lower:
            return "To dispute a transaction, contact support within 7 days of the issue. Provide all relevant details and evidence. We will investigate and mediate between buyer and seller."
        
        else:
            return "I'm here to help you with auction-related questions! You can ask me about bidding, payments, creating auctions, tracking bids, auction rules, platform navigation, account management, or support issues. How can I assist you?"
    
    def generate_response(self, user_message, chat_history=None, user_context=None):
        """Generate a response using OpenAI API with fallback"""
        start_time = time.time()
        
        # If no API key is configured, use fallback immediately
        if not self.api_key:
            fallback_response = self._get_fallback_response(user_message)
            return {
                'response': fallback_response,
                'response_time': time.time() - start_time,
                'tokens_used': 0,
                'model_used': 'fallback',
                'success': False,
                'error': 'No OpenAI API key configured'
            }
        
        try:
            # Build conversation history
            messages = []
            
            # Add system prompt
            system_prompt = self._get_context_prompt(user_context)
            messages.append({"role": "system", "content": system_prompt})
            
            # Add chat history (last 10 messages for context)
            if chat_history:
                for msg in chat_history[-10:]:
                    role = "user" if msg.message_type == "user" else "assistant"
                    messages.append({"role": role, "content": msg.content})
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Get configuration
            max_tokens = self.config.max_tokens if self.config else 150
            temperature = self.config.temperature if self.config else 0.7
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                timeout=30
            )
            
            # Extract response
            bot_response = response.choices[0].message.content.strip()
            response_time = time.time() - start_time
            tokens_used = response.usage.total_tokens if hasattr(response, 'usage') else None
            
            return {
                'response': bot_response,
                'response_time': response_time,
                'tokens_used': tokens_used,
                'model_used': 'gpt-3.5-turbo',
                'success': True
            }
            
        except Exception as e:
            # Use fallback response if OpenAI fails
            fallback_response = self._get_fallback_response(user_message)
            return {
                'response': fallback_response,
                'response_time': time.time() - start_time,
                'tokens_used': 0,
                'model_used': 'fallback',
                'success': False,
                'error': str(e)
            }
    
    def get_welcome_message(self):
        """Get the configured welcome message"""
        if self.config and self.config.welcome_message:
            return self.config.welcome_message
        return "Hello! I'm your AuctionVistas assistant. How can I help you today?"
    
    def analyze_intent(self, message):
        """Analyze user intent from message"""
        if not self.api_key:
            return 'general_help', 0.5
            
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Analyze the user's intent and return a JSON response with 'intent' and 'confidence' fields. Intent categories: auction_help, bidding_help, account_help, general_help, technical_support"},
                    {"role": "user", "content": message}
                ],
                max_tokens=50,
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return result.get('intent', 'general_help'), result.get('confidence', 0.5)
            
        except:
            return 'general_help', 0.5


class ChatbotUtils:
    """Utility functions for chatbot operations"""
    
    @staticmethod
    def create_session_id():
        """Generate a unique session ID"""
        import uuid
        return str(uuid.uuid4())
    
    @staticmethod
    def get_user_context(request):
        """Extract user context from request"""
        context = {
            'current_page': request.path,
            'user_authenticated': request.user.is_authenticated,
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'ip_address': request.META.get('REMOTE_ADDR', ''),
        }
        
        if request.user.is_authenticated:
            context['user_id'] = request.user.id
            context['username'] = request.user.username
        
        return context
    
    @staticmethod
    def format_response_time(seconds):
        """Format response time for display"""
        if seconds < 1:
            return f"{seconds*1000:.0f}ms"
        else:
            return f"{seconds:.1f}s" 