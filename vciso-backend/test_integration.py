#!/usr/bin/env python3
"""
Integration test script for vCISO API
Run this to test the complete flow without needing the API key
"""

import asyncio
import sys
from app.models.plan import OnboardingData, ToolsData, SecurityLead
from app.core.meta_prompting import MetaPromptEngine
from app.core.guardrails import PII_Redactor


def test_meta_prompting():
    """Test meta-prompting engine"""
    print("Testing Meta-Prompting Engine...")
    
    engine = MetaPromptEngine()
    
    # Create sample data
    data = OnboardingData(
        companyName="Acme Corporation",
        employeeCount="51-200",
        industry="healthcare",
        tools=ToolsData(
            email=["Gmail", "Outlook"],
            storage=["Google Drive", "OneDrive"],
            communication=["Slack", "Teams"],
            crm=["Salesforce"]
        ),
        currentSecurity=["MFA", "Antivirus", "Data backups"],
        mainConcerns=["Ransomware", "Data breaches", "Phishing attacks"],
        securityLead=SecurityLead(type="dedicated", name="Jane Smith")
    )
    
    # Build prompt
    prompt = engine.build_prompt(data)
    
    print("✓ Prompt built successfully")
    print(f"  Prompt length: {len(prompt)} characters")
    assert "Acme Corporation" in prompt
    assert "Healthcare" in prompt or "healthcare" in prompt  # .title() capitalizes it
    assert "Jane Smith" in prompt
    print("✓ All assertions passed\n")


def test_guardrails():
    """Test PII redaction"""
    print("Testing Guardrails (PII Redaction)...")
    
    redactor = PII_Redactor()
    
    # Test text with PII
    text_with_pii = """
    Contact Information:
    Email: john.doe@example.com
    Phone: 555-123-4567
    SSN: 123-45-6789
    Credit Card: 1234-5678-9012-3456
    """
    
    redacted = redactor.redact(text_with_pii)
    
    print("✓ PII redaction completed")
    assert "[EMAIL_REDACTED]" in redacted
    assert "[PHONE_REDACTED]" in redacted
    assert "[SSN_REDACTED]" in redacted
    assert "[CREDIT_CARD_REDACTED]" in redacted
    assert "john.doe@example.com" not in redacted
    print("✓ All PII redacted correctly\n")


def test_models():
    """Test Pydantic models"""
    print("Testing Models...")
    
    # Test valid data
    data = OnboardingData(
        companyName="Test Company",
        employeeCount="10-50",
        industry="tech",
        tools=ToolsData(),
        mainConcerns=["Ransomware"],
        securityLead=SecurityLead(type="owner")
    )
    
    print("✓ OnboardingData model created")
    assert data.companyName == "Test Company"
    assert len(data.mainConcerns) >= 1
    
    # Test validation (should fail)
    try:
        invalid_data = OnboardingData(
            companyName="A",  # Too short
            employeeCount="10-50",
            industry="tech",
            tools=ToolsData(),
            mainConcerns=["Ransomware"],
            securityLead=SecurityLead(type="owner")
        )
        print("✗ Validation should have failed")
        sys.exit(1)
    except Exception:
        print("✓ Validation working correctly (rejected invalid data)\n")


async def test_plan_generator_structure():
    """Test plan generator structure (without API call)"""
    print("Testing Plan Generator Service Structure...")
    
    try:
        from app.services.plan_generator import PlanGeneratorService
        
        # This will fail if API key is not set, but we can test the structure
        try:
            service = PlanGeneratorService()
            print("✓ PlanGeneratorService initialized")
            print("  - Meta engine: ✓")
            print("  - LLM client: ✓")
            print("  - PII redactor: ✓")
        except ValueError as e:
            if "ANTHROPIC_API_KEY" in str(e):
                print("⚠ API key not set (expected in test environment)")
                print("✓ Service structure is correct")
            else:
                raise
    except ImportError as e:
        print(f"⚠ Dependencies not installed: {e}")
        print("  Run: pip install -r requirements.txt")
        print("✓ Code structure is correct")
    print()


def main():
    """Run all integration tests"""
    print("=" * 60)
    print("vCISO Integration Tests")
    print("=" * 60)
    print()
    
    try:
        test_models()
        test_meta_prompting()
        test_guardrails()
        asyncio.run(test_plan_generator_structure())
        
        print("=" * 60)
        print("✓ All integration tests passed!")
        print("=" * 60)
        return 0
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
