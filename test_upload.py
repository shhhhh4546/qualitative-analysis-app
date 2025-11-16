#!/usr/bin/env python3
"""Quick test script to verify CSV upload works"""
import requests
import sys

def test_upload():
    url = "http://localhost:8000/api/upload/csv"
    
    with open("sample_data.csv", "rb") as f:
        files = {"file": ("sample_data.csv", f, "text/csv")}
        data = {"source": "tulip"}
        
        print("Uploading sample_data.csv...")
        response = requests.post(url, files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Upload successful!")
            print(f"   Uploaded: {result.get('uploaded', 0)} conversations")
            if result.get('errors'):
                print(f"   Errors: {result['errors']}")
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"   Error: {response.text}")

if __name__ == "__main__":
    test_upload()

