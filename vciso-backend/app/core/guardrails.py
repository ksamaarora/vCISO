# /app/core/guardrails.py
import re
from typing import Dict, Pattern

# guardrails.py - Module for PII redaction and detection
# PII redaction and detection utilities - in simple, it means removing or identifying personally identifiable information from text.
# This module provides functions to redact common types of PII such as emails, phone numbers, SSNs, and credit card numbers.
# It uses regular expressions to find and replace PII in the input text.

# How the code works:
# 1. The PII_Redactor class initializes with regex patterns for different PII types.
# 2. The redact method takes a text input and replaces any detected PII with a placeholder.
# 3. The contains_pii method checks if the input text contains any PII.

class PII_Redactor:
    def __init__(self):
        # Regex patterns for common PII
        self.patterns: Dict[str, Pattern] = {
            "email": re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            "phone": re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'),
            "ssn": re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
            "credit_card": re.compile(r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b'),
        }
    
    def redact(self, text: str) -> str:
        """Redact PII from text"""
        redacted = text
        
        for pii_type, pattern in self.patterns.items():
            redacted = pattern.sub(f"[{pii_type.upper()}_REDACTED]", redacted)
        
        return redacted
    
    def contains_pii(self, text: str) -> bool:
        """Check if text contains PII"""
        for pattern in self.patterns.values():
            if pattern.search(text):
                return True
        return False