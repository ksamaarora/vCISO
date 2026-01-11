#!/bin/bash
# Test script for vCISO API
# Make sure the server is running: uvicorn app.main:app --reload

BASE_URL="http://localhost:8000"

echo "Testing vCISO API..."
echo "===================="
echo ""

# Test health check
echo "1. Testing health check..."
curl -s "$BASE_URL/health" | python -m json.tool
echo ""

# Test root endpoint
echo "2. Testing root endpoint..."
curl -s "$BASE_URL/" | python -m json.tool
echo ""

# Test plan generation
echo "3. Testing plan generation..."
curl -X POST "$BASE_URL/api/v1/plans/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "companyName": "Acme Corporation",
    "employeeCount": "51-200",
    "industry": "healthcare",
    "tools": {
      "email": ["Gmail", "Outlook"],
      "storage": ["Google Drive", "OneDrive"],
      "communication": ["Slack", "Teams"],
      "crm": ["Salesforce"]
    },
    "currentSecurity": ["MFA", "Antivirus", "Data backups"],
    "mainConcerns": ["Ransomware", "Data breaches", "Phishing attacks"],
    "securityLead": {
      "type": "dedicated",
      "name": "Jane Smith"
    }
  }' | python -m json.tool

echo ""
echo "Done!"
