#!/usr/bin/env python3
"""
HealFind AI - Quick Demo & Test Script
Run this to verify the application is working correctly
"""

import requests
import json
import time
import os

BASE_URL = "http://localhost:5000"

def test_server_health():
    """Test if the server is running"""
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and healthy")
            return True
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to server: {e}")
        return False

def test_medicine_search():
    """Test medicine search functionality"""
    print("\n🔍 Testing Medicine Search...")
    
    test_data = {
        "medicine": "Paracetamol",
        "manufacturer": ""
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/search-medicine",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                results = data.get('results', [])
                print(f"✅ Found {len(results)} medical shops with Paracetamol")
                if results:
                    shop = results[0]
                    print(f"   📍 Top result: {shop['shopName']} - ₹{shop['price']} ({shop['distance']})")
                return True
            else:
                print(f"❌ Search failed: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ Search request failed with status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Medicine search test failed: {e}")
        return False

def test_ai_analysis():
    """Test AI document analysis"""
    print("\n🤖 Testing AI Document Analysis...")
    
    # Create a mock medical document
    mock_document_content = """
    Patient: John Doe
    Date: 2024-09-15
    
    Chief Complaint: Chest pain and shortness of breath
    
    Examination:
    - Blood pressure: 140/90 mmHg
    - Heart rate: 85 bpm
    - ECG shows irregular rhythm
    - Chest X-ray normal
    
    Assessment: Possible cardiac arrhythmia
    Recommendation: Cardiology consultation
    """
    
    try:
        # Prepare form data
        files = {'files': ('medical_report.txt', mock_document_content, 'text/plain')}
        data = {'message': 'Please analyze my medical report and recommend doctors'}
        
        response = requests.post(
            f"{BASE_URL}/api/analyze-documents",
            files=files,
            data=data,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ AI analysis completed successfully")
                print(f"   🎯 Detected specialty: {result.get('specialty', 'N/A')}")
                print(f"   🧠 Confidence: {result.get('confidence', 'N/A')}%")
                
                doctors = result.get('doctors', [])
                print(f"   👨‍⚕️ Recommended {len(doctors)} doctors")
                
                if doctors:
                    top_doctor = doctors[0]
                    print(f"   🏆 Top recommendation: Dr. {top_doctor['name']} ({top_doctor['specialty']})")
                    print(f"      Experience: {top_doctor['experience']} years, Success: {top_doctor['successRate']}%")
                
                return True
            else:
                print(f"❌ AI analysis failed: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ AI analysis request failed with status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ AI analysis test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🏥 HealFind AI - System Test")
    print("=" * 50)
    
    # Check if server is running
    if not test_server_health():
        print("\n💡 Please start the server first:")
        print("   - Double-click 'run.bat' (Windows)")
        print("   - Or run: cd backend && python app.py")
        return
    
    # Run tests
    tests_passed = 0
    total_tests = 2
    
    if test_medicine_search():
        tests_passed += 1
    
    if test_ai_analysis():
        tests_passed += 1
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! HealFind AI is working correctly.")
        print(f"\n🌐 Open your browser and visit: {BASE_URL}")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")
    
    print("\n📱 Try these features in your browser:")
    print("   1. Medicine Search: Search for 'Paracetamol' or 'Aspirin'")
    print("   2. AI Assistant: Upload a text file with medical symptoms")
    print("   3. Doctor Recommendations: Get AI-powered specialist suggestions")

if __name__ == "__main__":
    main()