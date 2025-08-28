# 🤖 Chatbot Knowledge Test Suite

This comprehensive test suite evaluates the AuctionVistas chatbot's knowledge and response quality across 200+ questions covering all major auction platform topics.

## 📋 Test Overview

### **Test Categories:**
- **🎯 Bidding (40 questions)** - Basic bidding, bid management, proxy bidding, auction rules, increments, timing, notifications
- **💰 Payments (35 questions)** - Payment methods, process, security, fees, refunds, issues, verification
- **🛒 Selling (35 questions)** - Creating auctions, approval, management, categories, fees, shipping, getting paid
- **👤 Account (25 questions)** - Profile management, security, verification, account management, purchase history
- **🆘 Support (25 questions)** - Contact support, damaged items, returns, disputes, technical issues
- **🌐 Platform (40 questions)** - Search, watchlists, notifications, categories, sorting, history, user management, features

### **Total Questions:** 200+ comprehensive questions

## 🚀 Quick Start

### **Prerequisites:**
1. Django server running on port 8001
2. Virtual environment activated
3. Chatbot app properly configured

### **Running the Test:**

#### **Option 1: Simple Runner (Recommended)**
```bash
python run_chatbot_test.py
```

#### **Option 2: Direct Test Script**
```bash
python chatbot_test_questions.py
```

### **What the Test Does:**
1. ✅ Starts a new chat session
2. 📝 Sends 200+ questions to the chatbot
3. 📊 Records responses and success rates
4. 🔍 Checks for expected keywords in responses
5. 📈 Generates comprehensive reports

## 📊 Understanding Results

### **Generated Files:**
- `chatbot_test_results_YYYYMMDD_HHMMSS.csv` - Detailed CSV with all responses
- `chatbot_test_summary_YYYYMMDD_HHMMSS.txt` - Summary report with statistics

### **Key Metrics:**

#### **1. Success Rate**
- **Definition:** Percentage of questions that received successful responses
- **Target:** >90% for a well-functioning chatbot
- **Calculation:** (Successful Responses / Total Questions) × 100

#### **2. Response Quality**
- **Response Length:** Average characters per response
- **Keyword Matching:** Whether responses contain expected keywords
- **Relevance:** How well responses match the question intent

#### **3. Category Performance**
- **Bidding:** Should handle all bidding-related questions
- **Payments:** Payment methods, fees, refunds
- **Selling:** Auction creation, management, fees
- **Account:** Profile, security, verification
- **Support:** Contact, issues, disputes
- **Platform:** Navigation, features, functionality

### **Sample Results Interpretation:**

```
📈 QUICK SUMMARY:
   Total Questions: 200
   Success Rate: 95.5%
   Failed: 9
   Duration: 0:12:34

CATEGORY BREAKDOWN:
Bidding: 38/40 (95.0%)
Payments: 33/35 (94.3%)
Selling: 34/35 (97.1%)
Account: 24/25 (96.0%)
Support: 24/25 (96.0%)
Platform: 38/40 (95.0%)
```

## 🔍 Detailed Analysis

### **CSV File Columns:**
- `category` - Main category (Bidding, Payments, etc.)
- `subcategory` - Specific topic within category
- `question` - The exact question asked
- `response` - Chatbot's complete response
- `success` - Whether the response was successful (True/False)
- `status_code` - HTTP status code from API
- `response_length` - Number of characters in response
- `has_expected_keywords` - Whether response contains expected keywords
- `timestamp` - When the question was asked

### **Analyzing Failed Tests:**
1. **Check the summary file** for failed test details
2. **Look for patterns** in failed questions
3. **Identify missing knowledge** areas
4. **Review response quality** for successful but poor responses

## 🎯 Improving Chatbot Performance

### **Based on Test Results:**

#### **If Success Rate < 80%:**
- Review FAQ database completeness
- Check chatbot service logic
- Verify API endpoints are working
- Test with simpler questions first

#### **If Success Rate 80-90%:**
- Identify weak categories
- Add missing FAQ entries
- Improve keyword matching
- Enhance fallback responses

#### **If Success Rate > 90%:**
- Focus on response quality
- Improve response relevance
- Add more specific answers
- Optimize response length

### **Common Issues & Solutions:**

#### **1. Generic Responses**
- **Problem:** Chatbot gives same response for different questions
- **Solution:** Improve keyword matching and add more specific FAQ entries

#### **2. Missing Information**
- **Problem:** Questions about specific topics get generic answers
- **Solution:** Add detailed FAQ entries for those topics

#### **3. API Errors**
- **Problem:** HTTP errors in responses
- **Solution:** Check server logs, verify API endpoints

#### **4. Timeout Issues**
- **Problem:** Tests take too long or fail
- **Solution:** Increase delays between requests, check server performance

## 🛠️ Customizing the Test

### **Adding New Questions:**
Edit `chatbot_test_questions.py` and add questions to the appropriate category:

```python
("Category", "Subcategory", "Your question here?", ["expected", "keywords"])
```

### **Modifying Test Parameters:**
- **Delay between requests:** Change `time.sleep(0.5)` in `test_question()`
- **Expected keywords:** Modify keyword lists for better matching
- **Categories:** Add new categories or subcategories

### **Running Partial Tests:**
Comment out unwanted categories in `generate_test_questions()`:

```python
# questions.extend(bidding_questions)  # Comment out to skip bidding tests
questions.extend(payment_questions)
```

## 📈 Performance Benchmarks

### **Excellent Performance:**
- Success Rate: >95%
- Average Response Length: 100-300 characters
- Keyword Match Rate: >90%
- All Categories: >90% success

### **Good Performance:**
- Success Rate: 85-95%
- Average Response Length: 50-500 characters
- Keyword Match Rate: 70-90%
- Most Categories: >80% success

### **Needs Improvement:**
- Success Rate: <85%
- Average Response Length: <50 or >500 characters
- Keyword Match Rate: <70%
- Multiple Categories: <80% success

## 🔧 Troubleshooting

### **Common Errors:**

#### **Connection Refused:**
```
❌ Cannot connect to Django server on port 8001
```
**Solution:** Start the Django server with `python manage.py runserver 8001`

#### **Import Error:**
```
❌ requests library not found
```
**Solution:** Install requests with `pip install requests`

#### **API Errors:**
```
❌ Failed to start chat session: 500
```
**Solution:** Check Django server logs for errors

#### **Timeout Errors:**
```
❌ Error: timeout
```
**Solution:** Increase timeout values or check server performance

### **Getting Help:**
1. Check Django server logs for errors
2. Verify chatbot app is properly configured
3. Test individual API endpoints manually
4. Review FAQ database content

## 📝 Test Maintenance

### **Regular Testing:**
- Run tests after adding new FAQ entries
- Test after modifying chatbot logic
- Verify performance after updates
- Monitor success rates over time

### **Updating Questions:**
- Keep questions relevant to current features
- Add questions for new functionality
- Remove outdated questions
- Update expected keywords as needed

---

**Happy Testing! 🎉**

This test suite will help you ensure your chatbot provides accurate, helpful responses across all aspects of your auction platform. 