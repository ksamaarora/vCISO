import pytest
from app.core.guardrails import PII_Redactor


class TestPIIRedactor:
    """Test PII redaction functionality"""
    
    def test_redact_email(self):
        """Test email redaction"""
        redactor = PII_Redactor()
        text = "Contact us at john.doe@example.com for more info"
        result = redactor.redact(text)
        assert "[EMAIL_REDACTED]" in result
        assert "john.doe@example.com" not in result
    
    def test_redact_phone(self):
        """Test phone number redaction"""
        redactor = PII_Redactor()
        text = "Call us at 555-123-4567"
        result = redactor.redact(text)
        assert "[PHONE_REDACTED]" in result
        assert "555-123-4567" not in result
    
    def test_redact_ssn(self):
        """Test SSN redaction"""
        redactor = PII_Redactor()
        text = "SSN: 123-45-6789"
        result = redactor.redact(text)
        assert "[SSN_REDACTED]" in result
        assert "123-45-6789" not in result
    
    def test_redact_credit_card(self):
        """Test credit card redaction"""
        redactor = PII_Redactor()
        text = "Card: 1234-5678-9012-3456"
        result = redactor.redact(text)
        assert "[CREDIT_CARD_REDACTED]" in result
        assert "1234-5678-9012-3456" not in result
    
    def test_redact_multiple_pii(self):
        """Test redaction of multiple PII types"""
        redactor = PII_Redactor()
        text = "Email: test@example.com, Phone: 555-123-4567"
        result = redactor.redact(text)
        assert "[EMAIL_REDACTED]" in result
        assert "[PHONE_REDACTED]" in result
    
    def test_contains_pii(self):
        """Test PII detection"""
        redactor = PII_Redactor()
        assert redactor.contains_pii("Email: test@example.com") is True
        assert redactor.contains_pii("No PII here") is False
    
    def test_no_pii_in_text(self):
        """Test that text without PII remains unchanged"""
        redactor = PII_Redactor()
        text = "This is a normal text without any sensitive information"
        result = redactor.redact(text)
        assert result == text
