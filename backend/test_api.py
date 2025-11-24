#!/usr/bin/env python3
"""
Simple test script to verify the API is working
"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "http://localhost:8000"

def test_root():
    """Test root endpoint"""
    print("Testing root endpoint...")
    try:
        response = requests.get(f"{API_URL}/")
        print(f"✓ Root endpoint: {response.status_code}")
        print(f"  Response: {response.json()}")
        return True
    except Exception as e:
        print(f"✗ Root endpoint failed: {e}")
        return False

def test_spots():
    """Test spots endpoint"""
    print("\nTesting /spots endpoint...")
    try:
        response = requests.get(f"{API_URL}/spots")
        print(f"✓ Spots endpoint: {response.status_code}")
        spots = response.json()
        print(f"  Found {len(spots)} spots")
        return True
    except Exception as e:
        print(f"✗ Spots endpoint failed: {e}")
        return False

def test_generate():
    """Test generate endpoint"""
    print("\nTesting /generate endpoint...")
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("✗ OPENAI_API_KEY not set in .env file")
        print("  Create a .env file with: OPENAI_API_KEY=your_key_here")
        return False
    
    print(f"✓ OpenAI API key found (length: {len(api_key)})")
    
    # Test request
    test_data = {
        "days": 3,
        "interests": ["history"],
        "include_famous_places": True,
        "include_hidden_spots": False,
        "include_cultural_experiences": True
    }
    
    try:
        print("  Sending request...")
        response = requests.post(
            f"{API_URL}/generate",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=60  # OpenAI can take a while
        )
        
        if response.status_code == 200:
            print(f"✓ Generate endpoint: {response.status_code}")
            result = response.json()
            print(f"  Generated {len(result['itinerary'])} days")
            return True
        else:
            print(f"✗ Generate endpoint failed: {response.status_code}")
            print(f"  Error: {response.text}")
            return False
    except requests.exceptions.Timeout:
        print("✗ Request timed out (OpenAI may be slow)")
        return False
    except Exception as e:
        print(f"✗ Generate endpoint failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Discover Jordan API Test")
    print("=" * 50)
    
    # Check if server is running
    try:
        requests.get(f"{API_URL}/", timeout=2)
    except:
        print(f"✗ Cannot connect to {API_URL}")
        print("  Make sure the server is running:")
        print("  cd backend && uvicorn main:app --reload --port 8000")
        exit(1)
    
    results = []
    results.append(test_root())
    results.append(test_spots())
    results.append(test_generate())
    
    print("\n" + "=" * 50)
    if all(results):
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed. Check the errors above.")
    print("=" * 50)

