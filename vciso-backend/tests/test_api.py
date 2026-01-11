import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.plan_schema import OnboardingRequest, ToolsDataSchema, SecurityLeadSchema

client = TestClient(app)


class TestAPIEndpoints:
    """Test API endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert "vCISO" in response.json()["message"]
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_generate_plan_missing_api_key(self):
        """Test plan generation without API key (should fail gracefully)"""
        request_data = {
            "companyName": "Test Company",
            "employeeCount": "10-50",
            "industry": "tech",
            "tools": {
                "email": ["Gmail"],
                "storage": ["Google Drive"],
                "communication": ["Slack"]
            },
            "mainConcerns": ["Ransomware"],
            "securityLead": {
                "type": "owner"
            }
        }
        # This will fail if API key is not set, but should return proper error
        response = client.post("/api/v1/plans/generate", json=request_data)
        # Should return 500 or 400 depending on validation
        assert response.status_code in [400, 500]
    
    def test_generate_plan_invalid_data(self):
        """Test plan generation with invalid data"""
        request_data = {
            "companyName": "A",  # Too short
            "employeeCount": "10-50",
            "industry": "tech",
            "tools": {},
            "mainConcerns": [],  # Empty - should fail
            "securityLead": {
                "type": "owner"
            }
        }
        response = client.post("/api/v1/plans/generate", json=request_data)
        assert response.status_code == 422  # Validation error
    
    def test_generate_plan_missing_required_fields(self):
        """Test plan generation with missing required fields"""
        request_data = {
            "companyName": "Test Company"
            # Missing other required fields
        }
        response = client.post("/api/v1/plans/generate", json=request_data)
        assert response.status_code == 422  # Validation error
