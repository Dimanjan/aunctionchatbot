#!/usr/bin/env python3
"""
Simple runner script for the Chatbot Knowledge Test
"""

import sys
import os
import subprocess
import time

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import requests
        print("✅ requests library found")
    except ImportError:
        print("❌ requests library not found")
        print("Installing requests...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        print("✅ requests installed successfully")

def check_server():
    """Check if Django server is running"""
    try:
        import requests
        response = requests.get("http://127.0.0.1:8001/", timeout=5)
        if response.status_code == 200:
            print("✅ Django server is running on port 8001")
            return True
        else:
            print("❌ Django server responded with status:", response.status_code)
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Django server on port 8001")
        print("   Please start the server with: python manage.py runserver 8001")
        return False
    except Exception as e:
        print(f"❌ Error checking server: {e}")
        return False

def main():
    """Main function"""
    print("🤖 AuctionVistas Chatbot Knowledge Test Runner")
    print("=" * 50)
    
    # Check dependencies
    print("📦 Checking dependencies...")
    check_dependencies()
    
    # Check server
    print("\n🌐 Checking server status...")
    if not check_server():
        print("\n💡 To start the server:")
        print("   1. Open a terminal in the project directory")
        print("   2. Activate virtual environment: source venv/bin/activate")
        print("   3. Start server: python manage.py runserver 8001")
        print("   4. Run this test in another terminal")
        return
    
    # Run the test
    print("\n🚀 Starting comprehensive chatbot test...")
    print("   This will test 200+ questions across all categories")
    print("   Estimated time: 10-15 minutes")
    print("   Press Ctrl+C to stop the test early")
    print("\n" + "=" * 50)
    
    try:
        # Import and run the test
        from chatbot_test_questions import ChatbotTester
        
        tester = ChatbotTester()
        tester.run_comprehensive_test()
        
        print("\n🎉 Test completed successfully!")
        print("📊 Check the generated CSV and summary files for detailed results")
        
    except KeyboardInterrupt:
        print("\n⏹️  Test stopped by user")
    except Exception as e:
        print(f"\n❌ Error running test: {e}")
        print("   Please check the server logs for more details")

if __name__ == "__main__":
    main() 