#!/usr/bin/env python3
"""
Chatbot Knowledge Test Script
Tests the AuctionVistas chatbot with 200+ questions across all categories
"""

import requests
import json
import time
import csv
from datetime import datetime
import os

# Test configuration
BASE_URL = "http://127.0.0.1:8001"
CHATBOT_API_BASE = f"{BASE_URL}/chatbot/api"

class ChatbotTester:
    def __init__(self):
        self.session_id = None
        self.results = []
        self.start_time = datetime.now()
        
    def start_chat_session(self):
        """Start a new chat session"""
        try:
            response = requests.post(f"{CHATBOT_API_BASE}/start/")
            if response.status_code == 200:
                data = response.json()
                self.session_id = data.get('session_id')
                print(f"✅ Chat session started: {self.session_id}")
                return True
            else:
                print(f"❌ Failed to start chat session: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error starting chat session: {e}")
            return False
    
    def send_message(self, question):
        """Send a message to the chatbot"""
        if not self.session_id:
            print("❌ No active chat session")
            return None
            
        try:
            payload = {
                'session_id': self.session_id,
                'message': question
            }
            response = requests.post(
                f"{CHATBOT_API_BASE}/send/",
                json=payload,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'response': data.get('response', ''),
                    'timestamp': data.get('timestamp', ''),
                    'status_code': response.status_code
                }
            else:
                return {
                    'success': False,
                    'response': f"HTTP {response.status_code}",
                    'timestamp': datetime.now().isoformat(),
                    'status_code': response.status_code
                }
        except Exception as e:
            return {
                'success': False,
                'response': f"Error: {str(e)}",
                'timestamp': datetime.now().isoformat(),
                'status_code': 0
            }
    
    def test_question(self, category, subcategory, question, expected_keywords=None):
        """Test a single question and record results"""
        print(f"🤖 Testing: {question[:60]}...")
        
        result = self.send_message(question)
        
        test_result = {
            'category': category,
            'subcategory': subcategory,
            'question': question,
            'response': result['response'] if result else 'No response',
            'success': result['success'] if result else False,
            'timestamp': result['timestamp'] if result else datetime.now().isoformat(),
            'status_code': result['status_code'] if result else 0,
            'response_length': len(result['response']) if result and result['response'] else 0,
            'has_expected_keywords': self._check_keywords(result['response'] if result else '', expected_keywords) if expected_keywords else None
        }
        
        self.results.append(test_result)
        
        # Add delay to avoid overwhelming the server
        time.sleep(0.5)
        
        return test_result
    
    def _check_keywords(self, response, keywords):
        """Check if response contains expected keywords"""
        if not keywords or not response:
            return None
        response_lower = response.lower()
        found_keywords = [kw for kw in keywords if kw.lower() in response_lower]
        return len(found_keywords) > 0
    
    def generate_test_questions(self):
        """Generate comprehensive test questions"""
        questions = []
        
        # BIDDING QUESTIONS (40 questions)
        bidding_questions = [
            # Basic Bidding
            ("Bidding", "Basic", "How do I place a bid?", ["place", "bid", "auction"]),
            ("Bidding", "Basic", "What is the minimum bid increment?", ["minimum", "increment", "₹"]),
            ("Bidding", "Basic", "Can I place multiple bids on the same item?", ["multiple", "bids", "same"]),
            ("Bidding", "Basic", "How do I know if I am the highest bidder?", ["highest", "bidder", "status"]),
            ("Bidding", "Basic", "What happens if I win an auction?", ["win", "auction", "notification", "payment"]),
            
            # Bid Management
            ("Bidding", "Management", "Can I cancel my bid?", ["cancel", "bid", "cannot"]),
            ("Bidding", "Management", "How do I track my bids?", ["track", "bids", "dashboard"]),
            ("Bidding", "Management", "What happens if I get outbid?", ["outbid", "notification", "higher"]),
            ("Bidding", "Management", "How do I increase my bid?", ["increase", "bid", "higher"]),
            ("Bidding", "Management", "Can I withdraw my bid?", ["withdraw", "bid", "cancel"]),
            
            # Proxy Bidding
            ("Bidding", "Proxy", "What is proxy bidding?", ["proxy", "bidding", "automatic"]),
            ("Bidding", "Proxy", "How does proxy bidding work?", ["proxy", "maximum", "amount"]),
            ("Bidding", "Proxy", "Can I set a maximum bid amount?", ["maximum", "bid", "amount"]),
            ("Bidding", "Proxy", "Does proxy bidding cost extra?", ["proxy", "cost", "fee"]),
            ("Bidding", "Proxy", "How do I enable proxy bidding?", ["enable", "proxy", "bidding"]),
            
            # Auction Rules
            ("Bidding", "Rules", "What are the auction rules?", ["rules", "binding", "payment"]),
            ("Bidding", "Rules", "Are bids legally binding?", ["binding", "legal", "contract"]),
            ("Bidding", "Rules", "What happens if I don't pay after winning?", ["don't pay", "suspension", "next bidder"]),
            ("Bidding", "Rules", "Can I bid on my own auction?", ["own auction", "shill", "prohibited"]),
            ("Bidding", "Rules", "What is the minimum auction duration?", ["minimum", "duration", "days"]),
            
            # Bid Increments
            ("Bidding", "Increments", "What is the bid increment for ₹500 items?", ["increment", "₹50", "under ₹1,000"]),
            ("Bidding", "Increments", "What is the bid increment for ₹2,000 items?", ["increment", "₹100", "₹1,000-₹5,000"]),
            ("Bidding", "Increments", "What is the bid increment for ₹7,000 items?", ["increment", "₹250", "₹5,000-₹10,000"]),
            ("Bidding", "Increments", "What is the bid increment for ₹15,000 items?", ["increment", "₹500", "above ₹10,000"]),
            ("Bidding", "Increments", "Can I bid any amount?", ["minimum", "increment", "higher"]),
            
            # Auction Timing
            ("Bidding", "Timing", "How long do auctions last?", ["duration", "3", "5", "7", "10", "days"]),
            ("Bidding", "Timing", "What happens at auction end?", ["end", "highest", "winner"]),
            ("Bidding", "Timing", "Can auctions be extended?", ["extended", "final minutes", "bidding"]),
            ("Bidding", "Timing", "When do I need to pay after winning?", ["24 hours", "payment", "winning"]),
            ("Bidding", "Timing", "How long do I have to complete payment?", ["24 hours", "complete", "payment"]),
            
            # Bid Notifications
            ("Bidding", "Notifications", "Do I get notified when outbid?", ["outbid", "notification", "email"]),
            ("Bidding", "Notifications", "How do I get bid notifications?", ["notifications", "settings", "alerts"]),
            ("Bidding", "Notifications", "Can I disable bid notifications?", ["disable", "notifications", "settings"]),
            ("Bidding", "Notifications", "What notifications do I receive?", ["outbid", "auction ending", "updates"]),
            ("Bidding", "Notifications", "How do I check my bid status?", ["bid status", "dashboard", "my bids"]),
            
            # Advanced Bidding
            ("Bidding", "Advanced", "What is a reserve price?", ["reserve", "minimum", "price"]),
            ("Bidding", "Advanced", "How do I know if an auction has a reserve?", ["reserve", "minimum", "visible"]),
            ("Bidding", "Advanced", "Can I see other bidders?", ["other bidders", "anonymous", "privacy"]),
            ("Bidding", "Advanced", "What is the difference between current price and my bid?", ["current price", "my bid", "difference"]),
            ("Bidding", "Advanced", "How do I calculate shipping costs?", ["shipping", "costs", "calculator"])
        ]
        
        # PAYMENT QUESTIONS (35 questions)
        payment_questions = [
            # Payment Methods
            ("Payment", "Methods", "What payment methods do you accept?", ["payment", "methods", "UPI", "bank transfer"]),
            ("Payment", "Methods", "Do you accept credit cards?", ["credit", "cards", "payment"]),
            ("Payment", "Methods", "Can I pay with UPI?", ["UPI", "payment", "method"]),
            ("Payment", "Methods", "Do you accept digital wallets?", ["digital", "wallets", "Paytm", "PhonePe"]),
            ("Payment", "Methods", "Can I pay with QR code?", ["QR code", "payment", "method"]),
            
            # Payment Process
            ("Payment", "Process", "How long do I have to pay after winning?", ["24 hours", "payment", "winning"]),
            ("Payment", "Process", "What happens if I don't pay on time?", ["don't pay", "suspension", "next bidder"]),
            ("Payment", "Process", "Can I pay in installments?", ["installments", "payment plan", "later"]),
            ("Payment", "Process", "Do you offer payment plans?", ["payment plans", "installments", "currently"]),
            ("Payment", "Process", "Can I use multiple payment methods?", ["multiple", "payment", "split"]),
            
            # Payment Security
            ("Payment", "Security", "Are payments secure?", ["secure", "payment", "processing"]),
            ("Payment", "Security", "Is my payment information safe?", ["safe", "secure", "information"]),
            ("Payment", "Security", "Do you store my payment details?", ["store", "payment", "details"]),
            ("Payment", "Security", "What if my payment fails?", ["payment fails", "try again", "different method"]),
            ("Payment", "Security", "Can I get a refund if payment fails?", ["refund", "payment fails", "contact support"]),
            
            # Fees and Charges
            ("Payment", "Fees", "Are there any hidden fees?", ["hidden fees", "no", "clearly displayed"]),
            ("Payment", "Fees", "What fees do buyers pay?", ["buyer fees", "final bid", "shipping"]),
            ("Payment", "Fees", "Do I pay commission as a buyer?", ["commission", "buyer", "no"]),
            ("Payment", "Fees", "What are the seller fees?", ["seller fees", "5-10%", "commission"]),
            ("Payment", "Fees", "Are there transaction fees?", ["transaction fees", "commission", "seller"]),
            
            # Refunds
            ("Payment", "Refunds", "How do I track my refund?", ["track refund", "payment history", "3-5 days"]),
            ("Payment", "Refunds", "How long do refunds take?", ["refunds", "3-5 business days", "processed"]),
            ("Payment", "Refunds", "Can I get a refund for damaged items?", ["refund", "damaged", "contact support"]),
            ("Payment", "Refunds", "What is your refund policy?", ["refund policy", "7 days", "different description"]),
            ("Payment", "Refunds", "Do I get a refund if item doesn't arrive?", ["refund", "doesn't arrive", "investigate"]),
            
            # Payment Issues
            ("Payment", "Issues", "What if my payment fails?", ["payment fails", "try again", "different method"]),
            ("Payment", "Issues", "What if I have insufficient funds?", ["insufficient funds", "different method", "support"]),
            ("Payment", "Issues", "Can I cancel a payment?", ["cancel payment", "contact support", "refund"]),
            ("Payment", "Issues", "What if my card is declined?", ["card declined", "different method", "support"]),
            ("Payment", "Issues", "How do I resolve payment disputes?", ["payment disputes", "contact support", "7 days"]),
            
            # Payment Verification
            ("Payment", "Verification", "How do I verify my payment went through?", ["verify payment", "payment history", "confirmation"]),
            ("Payment", "Verification", "Do I get a payment receipt?", ["payment receipt", "confirmation", "email"]),
            ("Payment", "Verification", "Can I download payment proof?", ["payment proof", "receipt", "download"]),
            ("Payment", "Verification", "How do I know if payment is pending?", ["payment pending", "status", "payment history"]),
            ("Payment", "Verification", "What payment statuses are there?", ["payment status", "pending", "completed", "failed"])
        ]
        
        # SELLING QUESTIONS (35 questions)
        selling_questions = [
            # Creating Auctions
            ("Selling", "Creation", "How do I create an auction?", ["create auction", "navigation", "item details"]),
            ("Selling", "Creation", "What information do I need to create an auction?", ["item details", "images", "price", "duration"]),
            ("Selling", "Creation", "How many images can I upload?", ["images", "upload", "high-quality"]),
            ("Selling", "Creation", "What is the minimum starting price?", ["minimum", "starting price", "no limit"]),
            ("Selling", "Creation", "Can I set a reserve price?", ["reserve price", "minimum", "willing to accept"]),
            
            # Auction Approval
            ("Selling", "Approval", "How long does auction approval take?", ["approval", "24-48 hours", "review"]),
            ("Selling", "Approval", "What do you check during approval?", ["review", "descriptions", "images", "pricing"]),
            ("Selling", "Approval", "Why might my auction be rejected?", ["rejected", "policy", "compliance", "quality"]),
            ("Selling", "Approval", "Can I appeal a rejected auction?", ["appeal", "rejected", "contact support"]),
            ("Selling", "Approval", "How do I know if my auction is approved?", ["approved", "notification", "email"]),
            
            # Auction Management
            ("Selling", "Management", "Can I edit my auction after posting?", ["edit", "before first bid", "minor corrections"]),
            ("Selling", "Management", "How do I change auction details?", ["change", "edit", "before bidding starts"]),
            ("Selling", "Management", "Can I extend auction duration?", ["extend", "duration", "contact support"]),
            ("Selling", "Management", "How do I cancel my auction?", ["cancel auction", "contact support", "before bids"]),
            ("Selling", "Management", "Can I relist a failed auction?", ["relist", "failed auction", "no fees"]),
            
            # Categories and Items
            ("Selling", "Categories", "What categories can I sell in?", ["categories", "Electronics", "Art", "Collectibles"]),
            ("Selling", "Categories", "Can I sell electronics?", ["electronics", "category", "allowed"]),
            ("Selling", "Categories", "Can I sell art and collectibles?", ["art", "collectibles", "category"]),
            ("Selling", "Categories", "Are there restricted items?", ["restricted", "prohibited", "special approval"]),
            ("Selling", "Categories", "How do I choose the right category?", ["choose category", "item type", "description"]),
            
            # Fees and Commission
            ("Selling", "Fees", "What are the seller fees?", ["seller fees", "5-10%", "category", "value"]),
            ("Selling", "Fees", "How much commission do you take?", ["commission", "5-10%", "final sale price"]),
            ("Selling", "Fees", "Are there different fees for different categories?", ["different fees", "electronics 8%", "art 10%"]),
            ("Selling", "Fees", "When do I pay the commission?", ["pay commission", "after sale", "deducted"]),
            ("Selling", "Fees", "Are there any hidden seller fees?", ["hidden fees", "commission", "clearly displayed"]),
            
            # Shipping and Delivery
            ("Selling", "Shipping", "How do I ship items after sale?", ["ship", "3-5 business days", "tracking"]),
            ("Selling", "Shipping", "How long do I have to ship?", ["ship", "3-5 business days", "after payment"]),
            ("Selling", "Shipping", "Do I need to provide tracking?", ["tracking", "numbers", "required"]),
            ("Selling", "Shipping", "Should I insure valuable items?", ["insure", "valuable", "recommended"]),
            ("Selling", "Shipping", "How do I calculate shipping costs?", ["shipping calculator", "accurate costs", "use"]),
            
            # Getting Paid
            ("Selling", "Payment", "How do I get paid for my sales?", ["get paid", "bank account", "3-5 business days"]),
            ("Selling", "Payment", "When do I receive payment?", ["receive payment", "after buyer confirms", "3-5 days"]),
            ("Selling", "Payment", "How do I set up payment details?", ["payment details", "bank account", "profile"]),
            ("Selling", "Payment", "Can I change my payment details?", ["change payment", "profile", "bank account"]),
            ("Selling", "Payment", "What if payment is delayed?", ["payment delayed", "contact support", "investigate"])
        ]
        
        # ACCOUNT QUESTIONS (25 questions)
        account_questions = [
            # Profile Management
            ("Account", "Profile", "How do I update my profile?", ["update profile", "edit profile", "personal information"]),
            ("Account", "Profile", "Can I change my email address?", ["change email", "profile", "contact details"]),
            ("Account", "Profile", "How do I update my phone number?", ["update phone", "profile", "contact details"]),
            ("Account", "Profile", "Can I add multiple shipping addresses?", ["shipping addresses", "profile", "multiple"]),
            ("Account", "Profile", "How do I change my username?", ["change username", "profile", "settings"]),
            
            # Password and Security
            ("Account", "Security", "How do I change my password?", ["change password", "profile settings", "current password"]),
            ("Account", "Security", "What if I forgot my password?", ["forgot password", "reset", "email"]),
            ("Account", "Security", "Can I enable two-factor authentication?", ["two-factor", "authentication", "security"]),
            ("Account", "Security", "How do I secure my account?", ["secure account", "password", "verification"]),
            ("Account", "Security", "What if someone accessed my account?", ["unauthorized access", "contact support", "security"]),
            
            # Account Verification
            ("Account", "Verification", "How do I verify my account?", ["verify account", "phone", "email", "ID proof"]),
            ("Account", "Verification", "Why do I need to verify my account?", ["verification", "high-value", "transactions"]),
            ("Account", "Verification", "How long does verification take?", ["verification", "24 hours", "process"]),
            ("Account", "Verification", "What documents do I need for verification?", ["documents", "ID proof", "verification"]),
            ("Account", "Verification", "Can I use a business account?", ["business account", "contact support", "special arrangements"]),
            
            # Account Management
            ("Account", "Management", "Can I have multiple accounts?", ["multiple accounts", "one person", "suspended"]),
            ("Account", "Management", "How do I delete my account?", ["delete account", "contact support", "active auctions"]),
            ("Account", "Management", "Can I deactivate my account temporarily?", ["deactivate", "temporarily", "contact support"]),
            ("Account", "Management", "How do I export my data?", ["export data", "contact support", "request"]),
            ("Account", "Management", "Can I transfer my account to someone else?", ["transfer account", "not allowed", "contact support"]),
            
            # Purchase History
            ("Account", "History", "How do I view my purchase history?", ["purchase history", "dashboard", "my purchases"]),
            ("Account", "History", "Can I download my transaction history?", ["transaction history", "download", "export"]),
            ("Account", "History", "How long is my history kept?", ["history", "kept", "permanent"]),
            ("Account", "History", "Can I see my bidding history?", ["bidding history", "my bids", "dashboard"]),
            ("Account", "History", "How do I track my spending?", ["track spending", "purchase history", "dashboard"])
        ]
        
        # SUPPORT QUESTIONS (25 questions)
        support_questions = [
            # Contact Support
            ("Support", "Contact", "How do I contact support?", ["contact support", "email", "helpline", "form"]),
            ("Support", "Contact", "What is your support email?", ["support@auctionvistas.com", "email", "contact"]),
            ("Support", "Contact", "Do you have a phone number?", ["phone", "helpline", "call"]),
            ("Support", "Contact", "How quickly do you respond?", ["respond", "24 hours", "support"]),
            ("Support", "Contact", "Is support available 24/7?", ["24/7", "support", "hours"]),
            
            # Damaged Items
            ("Support", "Damaged", "What if I receive a damaged item?", ["damaged item", "contact support", "photos"]),
            ("Support", "Damaged", "How do I report damage?", ["report damage", "photos", "contact support"]),
            ("Support", "Damaged", "Can I get a refund for damaged items?", ["refund", "damaged", "contact support"]),
            ("Support", "Damaged", "What if the item is not as described?", ["not as described", "return", "refund"]),
            ("Support", "Damaged", "How long do I have to report damage?", ["report damage", "immediately", "contact support"]),
            
            # Returns and Refunds
            ("Support", "Returns", "What is your return policy?", ["return policy", "7 days", "different description"]),
            ("Support", "Returns", "Can I return an item I won?", ["return", "7 days", "different description"]),
            ("Support", "Returns", "Who pays for return shipping?", ["return shipping", "buyer", "responsibility"]),
            ("Support", "Returns", "How do I initiate a return?", ["initiate return", "contact support", "process"]),
            ("Support", "Returns", "What if the seller doesn't accept returns?", ["seller doesn't accept", "contact support", "policy"]),
            
            # Disputes and Issues
            ("Support", "Disputes", "How do I dispute a transaction?", ["dispute transaction", "contact support", "7 days"]),
            ("Support", "Disputes", "What if the seller doesn't ship?", ["seller doesn't ship", "contact support", "investigate"]),
            ("Support", "Disputes", "How do I report a problem seller?", ["report seller", "profile page", "report user"]),
            ("Support", "Disputes", "What if I never receive my item?", ["never receive", "contact support", "investigate"]),
            ("Support", "Disputes", "How do you handle disputes?", ["handle disputes", "investigate", "mediate"]),
            
            # Technical Issues
            ("Support", "Technical", "What if the website is not working?", ["website not working", "technical", "contact support"]),
            ("Support", "Technical", "How do I report a bug?", ["report bug", "contact support", "technical"]),
            ("Support", "Technical", "What if I can't log in?", ["can't log in", "password reset", "contact support"]),
            ("Support", "Technical", "How do I clear my browser cache?", ["clear cache", "browser", "technical"]),
            ("Support", "Technical", "What browsers do you support?", ["browsers", "support", "compatible"])
        ]
        
        # PLATFORM QUESTIONS (40 questions)
        platform_questions = [
            # Search and Discovery
            ("Platform", "Search", "How do I search for specific items?", ["search", "search bar", "keywords", "filters"]),
            ("Platform", "Search", "Can I search by category?", ["search by category", "filters", "browse"]),
            ("Platform", "Search", "How do I filter search results?", ["filter", "price", "location", "end time"]),
            ("Platform", "Search", "Can I search by seller?", ["search by seller", "seller name", "filter"]),
            ("Platform", "Search", "How do I find items ending soon?", ["ending soon", "filter", "sort by time"]),
            
            # Watchlists and Favorites
            ("Platform", "Watchlist", "How do I save items to watch later?", ["watch later", "heart icon", "watchlist"]),
            ("Platform", "Watchlist", "Where can I find my watchlist?", ["my watchlist", "dashboard", "saved items"]),
            ("Platform", "Watchlist", "Can I organize my watchlist?", ["organize watchlist", "categories", "folders"]),
            ("Platform", "Watchlist", "How do I remove items from watchlist?", ["remove watchlist", "heart icon", "unwatch"]),
            ("Platform", "Watchlist", "Do I get notified about watched items?", ["notified", "watched items", "alerts"]),
            
            # Notifications
            ("Platform", "Notifications", "How do I get notifications?", ["notifications", "settings", "enable"]),
            ("Platform", "Notifications", "What types of notifications are there?", ["notification types", "outbids", "auction endings"]),
            ("Platform", "Notifications", "Can I customize notifications?", ["customize notifications", "settings", "preferences"]),
            ("Platform", "Notifications", "How do I disable notifications?", ["disable notifications", "settings", "turn off"]),
            ("Platform", "Notifications", "Do I get email notifications?", ["email notifications", "alerts", "updates"]),
            
            # Categories and Browsing
            ("Platform", "Categories", "What are the auction categories?", ["categories", "Electronics", "Art", "Collectibles"]),
            ("Platform", "Categories", "How do I browse by category?", ["browse category", "main menu", "categories"]),
            ("Platform", "Categories", "Are there subcategories?", ["subcategories", "detailed", "specific"]),
            ("Platform", "Categories", "Can I see trending categories?", ["trending categories", "popular", "featured"]),
            ("Platform", "Categories", "How do I find new categories?", ["new categories", "browse", "explore"]),
            
            # Sorting and Filtering
            ("Platform", "Sorting", "How do I sort auction results?", ["sort results", "ending time", "price", "popular"]),
            ("Platform", "Sorting", "Can I sort by price?", ["sort by price", "low to high", "high to low"]),
            ("Platform", "Sorting", "How do I filter by price range?", ["filter price", "range", "minimum", "maximum"]),
            ("Platform", "Sorting", "Can I sort by ending time?", ["sort by ending", "time", "ending soon"]),
            ("Platform", "Sorting", "How do I find the newest auctions?", ["newest auctions", "sort", "newest first"]),
            
            # Auction History
            ("Platform", "History", "Can I see auction history?", ["auction history", "completed", "final prices"]),
            ("Platform", "History", "How do I view past auctions?", ["past auctions", "history", "completed"]),
            ("Platform", "History", "Can I see what items sold for?", ["sold for", "final prices", "auction history"]),
            ("Platform", "History", "How do I research item values?", ["research values", "auction history", "pricing"]),
            ("Platform", "History", "Can I see bidding activity?", ["bidding activity", "history", "number of bidders"]),
            
            # User Management
            ("Platform", "Users", "How do I block a seller?", ["block seller", "profile page", "block user"]),
            ("Platform", "Users", "Can I see seller ratings?", ["seller ratings", "feedback", "profile"]),
            ("Platform", "Users", "How do I report a user?", ["report user", "profile page", "report"]),
            ("Platform", "Users", "Can I follow sellers?", ["follow sellers", "notifications", "updates"]),
            ("Platform", "Users", "How do I view user profiles?", ["user profiles", "seller information", "ratings"]),
            
            # Platform Features
            ("Platform", "Features", "What are the auction time limits?", ["time limits", "3", "5", "7", "10", "days"]),
            ("Platform", "Features", "How do I view my feedback?", ["my feedback", "profile page", "dashboard"]),
            ("Platform", "Features", "What are the platform rules?", ["platform rules", "no fake bids", "accurate descriptions"]),
            ("Platform", "Features", "Can I use the platform on mobile?", ["mobile", "responsive", "app"]),
            ("Platform", "Features", "Is there a mobile app?", ["mobile app", "download", "available"])
        ]
        
        # Combine all questions
        questions.extend(bidding_questions)
        questions.extend(payment_questions)
        questions.extend(selling_questions)
        questions.extend(account_questions)
        questions.extend(support_questions)
        questions.extend(platform_questions)
        
        return questions
    
    def run_comprehensive_test(self):
        """Run the comprehensive test suite"""
        print("🚀 Starting Comprehensive Chatbot Knowledge Test")
        print("=" * 60)
        
        # Start chat session
        if not self.start_chat_session():
            print("❌ Failed to start chat session. Exiting.")
            return
        
        # Get test questions
        test_questions = self.generate_test_questions()
        total_questions = len(test_questions)
        
        print(f"📋 Total questions to test: {total_questions}")
        print("=" * 60)
        
        # Run tests
        for i, (category, subcategory, question, expected_keywords) in enumerate(test_questions, 1):
            print(f"\n[{i}/{total_questions}] Testing {category} > {subcategory}")
            self.test_question(category, subcategory, question, expected_keywords)
            
            # Progress indicator
            if i % 10 == 0:
                print(f"📊 Progress: {i}/{total_questions} ({i/total_questions*100:.1f}%)")
        
        print("\n" + "=" * 60)
        print("✅ Test completed!")
        
        # Generate report
        self.generate_report()
    
    def generate_report(self):
        """Generate comprehensive test report"""
        timestamp = self.start_time.strftime("%Y%m%d_%H%M%S")
        
        # CSV Report
        csv_filename = f"chatbot_test_results_{timestamp}.csv"
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'category', 'subcategory', 'question', 'response', 'success',
                'status_code', 'response_length', 'has_expected_keywords', 'timestamp'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.results)
        
        # Summary Report
        summary_filename = f"chatbot_test_summary_{timestamp}.txt"
        with open(summary_filename, 'w', encoding='utf-8') as summaryfile:
            summaryfile.write("CHATBOT KNOWLEDGE TEST SUMMARY\n")
            summaryfile.write("=" * 50 + "\n\n")
            
            # Overall statistics
            total_tests = len(self.results)
            successful_tests = sum(1 for r in self.results if r['success'])
            failed_tests = total_tests - successful_tests
            
            summaryfile.write(f"Test Date: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            summaryfile.write(f"Total Questions Tested: {total_tests}\n")
            summaryfile.write(f"Successful Responses: {successful_tests}\n")
            summaryfile.write(f"Failed Responses: {failed_tests}\n")
            summaryfile.write(f"Success Rate: {successful_tests/total_tests*100:.1f}%\n\n")
            
            # Category breakdown
            summaryfile.write("CATEGORY BREAKDOWN:\n")
            summaryfile.write("-" * 30 + "\n")
            
            categories = {}
            for result in self.results:
                cat = result['category']
                if cat not in categories:
                    categories[cat] = {'total': 0, 'success': 0}
                categories[cat]['total'] += 1
                if result['success']:
                    categories[cat]['success'] += 1
            
            for category, stats in categories.items():
                success_rate = stats['success'] / stats['total'] * 100
                summaryfile.write(f"{category}: {stats['success']}/{stats['total']} ({success_rate:.1f}%)\n")
            
            # Response length statistics
            response_lengths = [r['response_length'] for r in self.results if r['success']]
            if response_lengths:
                avg_length = sum(response_lengths) / len(response_lengths)
                min_length = min(response_lengths)
                max_length = max(response_lengths)
                
                summaryfile.write(f"\nRESPONSE LENGTH STATISTICS:\n")
                summaryfile.write("-" * 30 + "\n")
                summaryfile.write(f"Average Length: {avg_length:.1f} characters\n")
                summaryfile.write(f"Minimum Length: {min_length} characters\n")
                summaryfile.write(f"Maximum Length: {max_length} characters\n")
            
            # Failed tests analysis
            failed_tests = [r for r in self.results if not r['success']]
            if failed_tests:
                summaryfile.write(f"\nFAILED TESTS ANALYSIS:\n")
                summaryfile.write("-" * 30 + "\n")
                for test in failed_tests[:10]:  # Show first 10 failures
                    summaryfile.write(f"Category: {test['category']} > {test['subcategory']}\n")
                    summaryfile.write(f"Question: {test['question']}\n")
                    summaryfile.write(f"Error: {test['response']}\n")
                    summaryfile.write("-" * 20 + "\n")
        
        print(f"📊 Test results saved to: {csv_filename}")
        print(f"📋 Summary report saved to: {summary_filename}")
        
        # Print quick summary
        print(f"\n📈 QUICK SUMMARY:")
        print(f"   Total Questions: {total_tests}")
        print(f"   Success Rate: {successful_tests/total_tests*100:.1f}%")
        print(f"   Failed: {failed_tests}")
        print(f"   Duration: {datetime.now() - self.start_time}")

def main():
    """Main function to run the test"""
    print("🤖 AuctionVistas Chatbot Knowledge Tester")
    print("=" * 50)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code != 200:
            print("❌ Server is not responding properly")
            return
    except Exception as e:
        print(f"❌ Cannot connect to server at {BASE_URL}")
        print(f"   Error: {e}")
        print("   Make sure the Django server is running on port 8001")
        return
    
    # Run the test
    tester = ChatbotTester()
    tester.run_comprehensive_test()

if __name__ == "__main__":
    main() 