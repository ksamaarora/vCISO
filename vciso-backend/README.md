# vCISO - Virtual CISO Application

A FastAPI-based application for generating customized Incident Response (IR) plans for small to medium-sized businesses using AI.

## Features

- **Onboarding Flow**: Collects company context (size, industry, tools, security posture, concerns)
- **Meta-Prompting Engine**: Transforms user inputs into structured prompts for high-quality IR plan generation
- **LLM Integration**: Uses Anthropic's Claude API to generate customized IR plans
- **Guardrails**: PII redaction and safety checks
- **RESTful API**: FastAPI-based endpoints for plan generation

## Setup

### Prerequisites

- Python 3.11+
- Anthropic API key

### Installation

1. Clone the repository and navigate to the backend:
```bash
cd vciso-backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the `vciso-backend` directory:
```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ENVIRONMENT=development
LOG_LEVEL=INFO
CLAUDE_MODEL=claude-sonnet-4-20250514
CLAUDE_MAX_TOKENS=4000
CLAUDE_TEMPERATURE=0.7
```

## Running the Application

### Development Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

Run tests with pytest:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=app tests/
```

## API Usage

### Generate IR Plan

```bash
curl -X POST "http://localhost:8000/api/v1/plans/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "companyName": "Test Corp",
    "employeeCount": "10-50",
    "industry": "tech",
    "tools": {
      "email": ["Gmail"],
      "storage": ["Google Drive"],
      "communication": ["Slack"],
      "crm": []
    },
    "currentSecurity": ["MFA", "Antivirus"],
    "mainConcerns": ["Ransomware", "Phishing"],
    "securityLead": {
      "type": "dedicated",
      "name": "John Doe"
    }
  }'
```

## Project Structure

```
vciso-backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           ├── auth.py
│   │           └── plans.py
│   ├── core/
│   │   ├── guardrails.py      # PII redaction
│   │   ├── llm_client.py      # Claude API client
│   │   └── meta_prompting.py  # Prompt engineering
│   ├── models/
│   │   └── plan.py            # Pydantic models
│   ├── schemas/
│   │   └── plan_schema.py     # API schemas
│   ├── services/
│   │   └── plan_generator.py  # Plan generation service
│   ├── config.py              # Settings
│   └── main.py                # FastAPI app
├── tests/                     # Test files
├── requirements.txt
└── pytest.ini
```

## Onboarding Questions

The application collects the following information:

1. **Company Basics**: Name, employee count
2. **Industry**: Healthcare, Finance, Retail, Manufacturing, Tech, Professional Services, Other
3. **Technology Stack**: Email, Storage, Communication, CRM tools
4. **Current Security Posture**: MFA, Antivirus, Backups, Training, etc.
5. **Main Concerns**: Ransomware, Phishing, Data Breaches, Insider Threats, Downtime
6. **Security Lead**: Who handles IT/security (dedicated person, consultant, owner, none)

## License

MIT
