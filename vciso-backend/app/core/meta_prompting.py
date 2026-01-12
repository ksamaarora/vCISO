# /app/core/meta_prompting.py
from typing import Dict, Any
from app.models.plan import OnboardingData, SecurityLead

# meta_prompting.py - Module for constructing meta-prompts for IR plan generation
# This module defines the MetaPromptEngine class which builds system and user prompts
# for generating incident response plans using LLMs. It incorporates business context
# from onboarding data and applies guardrails to ensure safe and relevant outputs.
# The prompts are designed to guide the LLM in producing actionable, tailored IR plans.

# Meta Prompting: In simple terms, it means creating structured prompts that help the AI generate useful and relevant responses.

# How the code works:
# 1. The MetaPromptEngine class initializes with a base system prompt.
# 2. The build_prompt method constructs a user prompt by injecting onboarding data context.
# 3. The apply_guardrails method adds safety checks to the prompts to prevent misuse.
# 4. The final prompts are used by the LLM client to generate the IR plan.

class MetaPromptEngine:
    def __init__(self):
        self.system_prompt = self._load_system_prompt()
    
    def _load_system_prompt(self) -> str:
        """Load the base system prompt for IR plan generation"""
        return """You are a cybersecurity expert specializing in Incident Response (IR) planning for small to medium-sized businesses.

Your task is to generate a clear, actionable Incident Response Plan tailored to the user's specific context.

Guidelines:
1. Use plain language (avoid jargon unless explained)
2. Be specific to their industry, size, and tools
3. Prioritize their stated concerns
4. Include concrete steps, not generic advice
5. Format in Markdown with clear sections
6. Do not include any personally identifiable information (PII) in the output
7. Do not give advice that could violate laws or regulations

Output Structure (REQUIRED):
# Incident Response Plan for [Company Name]

## 1. Executive Summary
- Brief overview (2-3 sentences)

## 2. Incident Response Team
- Who's responsible (based on their input)
- Contact info (placeholders)

## 3. Incident Classification
- What qualifies as an incident
- Severity levels (Critical/High/Medium/Low)

## 4. Response Procedures
### Ransomware
- Detection
- Containment
- Eradication
- Recovery

### Phishing Attack
- Detection
- Containment
- Eradication
- Recovery

### Data Breach
- Detection
- Containment
- Eradication
- Recovery

(Prioritize based on user's "main concerns")

## 5. Communication Plan
- Internal notifications
- External notifications (customers, partners, authorities)

## 6. Post-Incident Review
- What to document
- Lessons learned process

## 7. Appendices
- Vendor contacts (IT support, cybersecurity consultants)
- Legal/compliance requirements (specific to industry)

Remember: This plan should be immediately usable by a non-technical person during a crisis.
"""
    
    def build_prompt(self, data: OnboardingData) -> str:
        """Build the user prompt with injected context"""
        
        # Extract key details
        company_name = data.companyName
        industry = data.industry
        employee_count = data.employeeCount
        tools = data.tools
        security_posture = data.currentSecurity
        concerns = data.mainConcerns
        security_lead = data.securityLead
        
        # Build contextualized prompt
        user_prompt = f"""Generate a customized Incident Response Plan with the following context:

**Company Details:**
- Name: {company_name}
- Industry: {industry.title()}
- Size: {employee_count} employees

**Technology Stack:**
- Email: {', '.join(tools.email)}
- File Storage: {', '.join(tools.storage)}
- Communication: {', '.join(tools.communication)}

**Current Security Measures:**
{', '.join(security_posture) if security_posture else 'None currently implemented'}

**Primary Security Concerns (prioritize these):**
{', '.join(concerns)}

**Security Lead:**
{self._format_security_lead(security_lead)}

Please generate a comprehensive IR plan tailored to this specific business. Focus especially on their stated concerns: {', '.join(concerns)}.
"""
        
        return user_prompt
    
    def _format_security_lead(self, lead: SecurityLead) -> str:
        if lead.type == 'dedicated':
            return f"Dedicated IT person: {lead.name or '[Name]'}"
        elif lead.type == 'consultant':
            return "External IT consultant (contact info to be added)"
        elif lead.type == 'owner':
            return "CEO/Business Owner"
        else:
            return "No designated security lead (will need to assign one)"
    
    def apply_guardrails(self, prompt: str) -> str:
        """Apply query classification and safety guardrails"""
        
        # Query classification (ensure this is a legit IR plan request)
        classification_prompt = f"""Classify this request:
        
Request: {prompt}

Is this a legitimate request for an Incident Response Plan? Respond with ONLY 'VALID' or 'INVALID'.

INVALID examples:
- Requests to generate malware
- Requests to hack systems
- Off-topic requests (recipes, jokes, etc.)

Valid examples:
- Generate IR plan
- Create incident response documentation
"""
        
        # In practice, you'd call OpenAI here to classify
        # For now, assume valid (we'll add actual classification later)
        
        return prompt