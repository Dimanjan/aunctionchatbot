from django.core.management.base import BaseCommand
from chatbot.models import FAQ, ChatbotConfiguration


class Command(BaseCommand):
    help = 'Populate FAQ data for the chatbot'

    def handle(self, *args, **options):
        # Create default chatbot configuration
        config, created = ChatbotConfiguration.objects.get_or_create(
            is_active=True,
            defaults={
                'name': 'AuctionVistas Assistant',
                'welcome_message': "Hello! I'm your AuctionVistas assistant. I can help you with:\n• Finding auctions\n• Understanding bidding\n• Account questions\n• Platform navigation\n\nHow can I help you today?",
                'system_prompt': "You are AuctionVistas Assistant, a helpful AI assistant for an online auction platform. Help users with auction-related questions, bidding guidance, account issues, and platform navigation. Be friendly, concise, and accurate.",
                'max_tokens': 150,
                'temperature': 0.7
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created chatbot configuration')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Chatbot configuration already exists')
            )

        # Comprehensive FAQ data
        faqs_data = [
            # Bidding Questions
            {
                'question': 'How do I place a bid on an auction?',
                'answer': 'To place a bid, navigate to the auction item you want to bid on, enter your bid amount in the bidding section, and click "Place Bid". Make sure you have sufficient funds in your account. Your bid must be higher than the current highest bid.',
                'category': 'Bidding'
            },
            {
                'question': 'What is the minimum bid increment?',
                'answer': 'The minimum bid increment varies by auction value: ₹50 for items under ₹1,000, ₹100 for items ₹1,000-₹5,000, ₹250 for items ₹5,000-₹10,000, and ₹500 for items above ₹10,000.',
                'category': 'Bidding'
            },
            {
                'question': 'Can I place multiple bids on the same item?',
                'answer': 'Yes, you can place multiple bids on the same item. Each new bid must be higher than your previous bid. The system will automatically use your highest bid amount.',
                'category': 'Bidding'
            },
            {
                'question': 'What happens if I win an auction?',
                'answer': 'When you win an auction, you will receive a notification and email. You will need to complete the payment within 24 hours. The seller will then ship the item to you within 3-5 business days.',
                'category': 'Bidding'
            },
            {
                'question': 'Can I cancel my bid?',
                'answer': 'Bids cannot be cancelled once placed. Please make sure you want to place a bid before confirming. You can place a higher bid if you want to increase your offer.',
                'category': 'Bidding'
            },
            {
                'question': 'How do I track my bids?',
                'answer': 'You can track your bids in your account dashboard under "My Bids". This shows all your active bids, bid history, and auction status.',
                'category': 'Bidding'
            },
            {
                'question': 'What is proxy bidding?',
                'answer': 'Proxy bidding allows you to set a maximum bid amount. The system will automatically bid on your behalf up to that amount, helping you win auctions without constant monitoring.',
                'category': 'Bidding'
            },
            {
                'question': 'What happens if I get outbid?',
                'answer': 'If you get outbid, you will receive an email notification. You can then place a higher bid to stay in the auction. You can also set up proxy bidding to avoid being outbid.',
                'category': 'Bidding'
            },
            {
                'question': 'How do I know if I am the highest bidder?',
                'answer': 'You can check your bid status in "My Bids" section. The current highest bidder is shown on each auction page. You will also receive notifications if you are outbid.',
                'category': 'Bidding'
            },
            {
                'question': 'What are the auction rules?',
                'answer': 'Our auction rules include: 1) Bids are binding and cannot be cancelled, 2) Payment must be completed within 24 hours of winning, 3) All items are sold as-is, 4) Shipping costs are additional, 5) No shill bidding allowed.',
                'category': 'Bidding'
            },
            
            # Selling Questions
            {
                'question': 'How do I create an auction?',
                'answer': 'To create an auction, click on "Create Auction" in the navigation menu. Fill in the item details, upload high-quality images, set your starting price and duration, then submit for approval. Approval typically takes 24-48 hours.',
                'category': 'Selling'
            },
            {
                'question': 'What are the seller fees?',
                'answer': 'Seller fees are typically 5-10% of the final sale price, depending on the item category and sale value. Electronics: 8%, Art: 10%, Collectibles: 7%, General: 5%. Detailed fee structure is available in your seller dashboard.',
                'category': 'Selling'
            },
            {
                'question': 'How long does auction approval take?',
                'answer': 'Auction approval typically takes 24-48 hours. We review item descriptions, images, and pricing to ensure quality and compliance with our policies.',
                'category': 'Selling'
            },
            {
                'question': 'Can I edit my auction after posting?',
                'answer': 'You can edit your auction description and images before the first bid is placed. Once bidding starts, only minor corrections are allowed. Contact support for major changes.',
                'category': 'Selling'
            },
            {
                'question': 'How do I ship items after sale?',
                'answer': 'After receiving payment, you have 3-5 business days to ship the item. Use our shipping calculator for accurate costs. Always use tracking numbers and insure valuable items.',
                'category': 'Selling'
            },
            {
                'question': 'What if my item doesn\'t sell?',
                'answer': 'If your item doesn\'t sell, you can relist it with a lower starting price or different description. There are no fees for unsold items. You can also try different auction durations.',
                'category': 'Selling'
            },
            {
                'question': 'How do I set a reserve price?',
                'answer': 'You can set a reserve price when creating your auction. This is the minimum price you\'re willing to accept. If bidding doesn\'t reach the reserve, the item won\'t sell.',
                'category': 'Selling'
            },
            {
                'question': 'What categories can I sell in?',
                'answer': 'We accept items in categories like Electronics, Art, Collectibles, Jewelry, Antiques, Books, Sports Equipment, Fashion, Home & Garden, and more. Some categories require special approval.',
                'category': 'Selling'
            },
            {
                'question': 'How do I get paid for my sales?',
                'answer': 'Payments are processed after the buyer confirms receipt. Funds are transferred to your registered bank account within 3-5 business days, minus our commission fees.',
                'category': 'Selling'
            },
            
            # Payment Questions
            {
                'question': 'What payment methods are accepted?',
                'answer': 'We accept various payment methods including bank transfers, UPI, credit/debit cards, digital wallets (Paytm, PhonePe), and QR code payments. All payments are processed securely through our platform.',
                'category': 'Payments'
            },
            {
                'question': 'How do I track my refund?',
                'answer': 'You can track your refund by going to your payment history page. Refunds are typically processed within 3-5 business days after approval. You will receive email updates on refund status.',
                'category': 'Payments'
            },
            {
                'question': 'How long do I have to pay after winning?',
                'answer': 'You have 24 hours to complete payment after winning an auction. Failure to pay may result in account suspension and the item being offered to the next highest bidder.',
                'category': 'Payments'
            },
            {
                'question': 'Are there any hidden fees?',
                'answer': 'No hidden fees. All fees are clearly displayed: buyer pays the final bid amount plus shipping. Sellers pay our commission (5-10%) based on the final sale price.',
                'category': 'Payments'
            },
            {
                'question': 'Can I use multiple payment methods?',
                'answer': 'Yes, you can split payment across multiple methods. For example, pay part with UPI and part with credit card. Contact support if you need assistance with split payments.',
                'category': 'Payments'
            },
            {
                'question': 'What if my payment fails?',
                'answer': 'If payment fails, try again with a different method. Common issues include insufficient funds, expired cards, or network problems. Contact support if problems persist.',
                'category': 'Payments'
            },
            {
                'question': 'Do you offer payment plans?',
                'answer': 'Currently, we don\'t offer payment plans. Full payment is required within 24 hours of winning. We\'re working on installment options for high-value items.',
                'category': 'Payments'
            },
            
            # Account & Profile Questions
            {
                'question': 'How do I update my profile information?',
                'answer': 'To update your profile, go to your profile page and click "Edit Profile". You can update your personal information, contact details, shipping addresses, and preferences.',
                'category': 'Account'
            },
            {
                'question': 'How do I change my password?',
                'answer': 'Go to your profile settings and click "Change Password". You\'ll need to enter your current password and then your new password twice for confirmation.',
                'category': 'Account'
            },
            {
                'question': 'How do I verify my account?',
                'answer': 'Account verification requires a valid phone number and email address. You may also need to provide ID proof for high-value transactions. Verification typically takes 24 hours.',
                'category': 'Account'
            },
            {
                'question': 'Can I have multiple accounts?',
                'answer': 'No, each person should have only one account. Multiple accounts may be suspended. If you need a business account, contact support for special arrangements.',
                'category': 'Account'
            },
            {
                'question': 'How do I delete my account?',
                'answer': 'To delete your account, contact support. Note that you cannot delete your account if you have active auctions or pending transactions.',
                'category': 'Account'
            },
            {
                'question': 'How do I view my purchase history?',
                'answer': 'Your purchase history is available in your account dashboard under "My Purchases". This shows all items you\'ve won, payment status, and shipping information.',
                'category': 'Account'
            },
            
            # Support & Help Questions
            {
                'question': 'What if I receive a damaged item?',
                'answer': 'If you receive a damaged item, contact our support team immediately with photos of the damage. We will help you resolve the issue with the seller, including refunds or replacements.',
                'category': 'Support'
            },
            {
                'question': 'How do I contact seller support?',
                'answer': 'You can contact seller support through our contact form, by emailing support@auctionvistas.com, or calling our helpline. Our team will respond within 24 hours.',
                'category': 'Support'
            },
            {
                'question': 'What is your return policy?',
                'answer': 'Returns are accepted within 7 days of receipt if the item is significantly different from the description. Contact support to initiate a return. Shipping costs are typically the buyer\'s responsibility.',
                'category': 'Support'
            },
            {
                'question': 'How do I report a problem seller?',
                'answer': 'To report a problem seller, go to their profile page and click "Report User". Provide detailed information about the issue. We investigate all reports and take appropriate action.',
                'category': 'Support'
            },
            {
                'question': 'What if my item never arrives?',
                'answer': 'If your item doesn\'t arrive within the expected timeframe, contact support with your order details. We will investigate and help resolve the issue, including refunds if necessary.',
                'category': 'Support'
            },
            {
                'question': 'How do I dispute a transaction?',
                'answer': 'To dispute a transaction, contact support within 7 days of the issue. Provide all relevant details and evidence. We will investigate and mediate between buyer and seller.',
                'category': 'Support'
            },
            
            # Platform & Navigation Questions
            {
                'question': 'How do I search for specific items?',
                'answer': 'Use the search bar at the top of the page. You can search by item name, category, seller, or keywords. Use filters to narrow results by price, location, or auction end time.',
                'category': 'Platform'
            },
            {
                'question': 'How do I save items to watch later?',
                'answer': 'Click the heart icon on any auction to add it to your watchlist. You can view all watched items in your account dashboard under "My Watchlist".',
                'category': 'Platform'
            },
            {
                'question': 'How do I get notifications?',
                'answer': 'Enable notifications in your account settings. You\'ll receive alerts for outbids, auction endings, new items in your categories, and important account updates.',
                'category': 'Platform'
            },
            {
                'question': 'What are the auction categories?',
                'answer': 'Our main categories include Electronics, Art & Collectibles, Jewelry & Watches, Antiques, Books & Media, Sports & Hobbies, Fashion & Accessories, Home & Garden, and Vehicles.',
                'category': 'Platform'
            },
            {
                'question': 'How do I sort auction results?',
                'answer': 'Use the sort options on auction listing pages: by ending time, price (low to high), price (high to low), newest first, or most popular.',
                'category': 'Platform'
            },
            {
                'question': 'Can I see auction history?',
                'answer': 'Yes, you can view auction history for completed auctions. This shows final prices, number of bidders, and bidding activity. Useful for pricing your own items.',
                'category': 'Platform'
            },
            {
                'question': 'How do I block a seller?',
                'answer': 'Go to any seller\'s profile page and click "Block User". You won\'t see their auctions in search results, and they cannot bid on your items.',
                'category': 'Platform'
            },
            {
                'question': 'What are the auction time limits?',
                'answer': 'Auctions can be set for 3, 5, 7, or 10 days. Extended bidding may occur if bids are placed in the final minutes. Minimum auction duration is 3 days.',
                'category': 'Platform'
            },
            {
                'question': 'How do I view my feedback?',
                'answer': 'Your feedback rating is visible on your profile page. You can view detailed feedback from buyers and sellers in your account dashboard under "My Feedback".',
                'category': 'Platform'
            },
            {
                'question': 'What are the platform rules?',
                'answer': 'Key rules: No fake bids, accurate item descriptions, timely payments and shipping, respectful communication, no prohibited items, and compliance with local laws.',
                'category': 'Platform'
            }
        ]

        # Create FAQ entries
        created_count = 0
        for faq_data in faqs_data:
            faq, created = FAQ.objects.get_or_create(
                question=faq_data['question'],
                defaults={
                    'answer': faq_data['answer'],
                    'category': faq_data['category'],
                    'is_active': True
                }
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} FAQ entries')
        )
        
        total_faqs = FAQ.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f'Total FAQ entries in database: {total_faqs}')
        ) 