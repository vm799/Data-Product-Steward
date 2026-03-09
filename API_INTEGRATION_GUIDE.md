# API Integration Guide

This document explains how to set up and use the OpenAI and Collibra integrations in the Data Product Steward application.

## Table of Contents

1. [OpenAI Integration](#openai-integration)
2. [Collibra Integration](#collibra-integration)
3. [AI Requirements Agent](#ai-requirements-agent)
4. [Security & Credential Management](#security--credential-management)
5. [Architecture Overview](#architecture-overview)
6. [Troubleshooting](#troubleshooting)

---

## OpenAI Integration

### Overview

The OpenAI integration enables the AI Requirements Agent, which guides non-technical users through defining data products using conversational AI.

### Setup

#### Option 1: Environment Variables (Recommended for Production)

```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_MODEL="gpt-4-turbo"  # or gpt-4, gpt-3.5-turbo
export OPENAI_BASE_URL="https://api.openai.com/v1"  # Optional, for custom endpoints
```

Then run the app:
```bash
streamlit run streamlit_app.py
```

#### Option 2: Streamlit Secrets (Recommended for Development)

Create or edit `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "sk-..."
OPENAI_MODEL = "gpt-4-turbo"
OPENAI_BASE_URL = "https://api.openai.com/v1"
```

#### Option 3: Manual Entry in Settings Page

1. Go to Settings page (⚙️ in navigation)
2. Expand "OpenAI Configuration"
3. Enter API key and select model
4. Click "Test OpenAI Connection"

### Getting an OpenAI API Key

1. Visit https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy and save the key securely

### API Endpoints Used

```python
# Chat Completions (used by Requirements Agent)
POST https://api.openai.com/v1/chat/completions

# Embeddings (for future semantic search features)
POST https://api.openai.com/v1/embeddings
```

### Configuration Options

```python
from config import OPENAI_CONFIG

OPENAI_CONFIG = {
    "api_key": "sk-...",           # Required
    "base_url": "https://api.openai.com/v1",  # Optional
    "model": "gpt-4-turbo",        # Model to use
    "timeout": 30,                 # Request timeout in seconds
    "max_retries": 3,              # Retry attempts for rate limiting
}
```

### Rate Limiting & Costs

- **Rate Limits**: OpenAI has per-minute token limits based on your account tier
- **Costs**: Charged per 1K tokens (input + output)
- **Model Costs** (approximate as of 2026):
  - GPT-4 Turbo: ~$0.01 per 1K input tokens, ~$0.03 per 1K output tokens
  - GPT-4: ~$0.03 per 1K input tokens, ~$0.06 per 1K output tokens
  - GPT-3.5 Turbo: ~$0.0005 per 1K input tokens, ~$0.0015 per 1K output tokens

### Error Handling

The client includes automatic retry logic with exponential backoff for:
- Rate limiting (429 errors)
- Connection errors
- Timeout errors

Max retries: 3 (configurable)

---

## Collibra Integration

### Overview

The Collibra integration allows you to:
- Import existing data models from Collibra
- Extract governance policies (classification, compliance, retention)
- Reuse assets across data products
- Sync Collibra metadata with Data Product Steward

### Setup

#### Option 1: Environment Variables (Recommended for Production)

```bash
export COLLIBRA_BASE_URL="https://your-instance.collibra.com"
export COLLIBRA_USERNAME="your_username"
export COLLIBRA_PASSWORD="your_password"
```

#### Option 2: Streamlit Secrets

Edit `.streamlit/secrets.toml`:

```toml
COLLIBRA_BASE_URL = "https://your-instance.collibra.com"
COLLIBRA_USERNAME = "your_username"
COLLIBRA_PASSWORD = "your_password"
```

#### Option 3: Manual Entry in Settings

1. Go to Settings page
2. Expand "Collibra Configuration"
3. Enter connection details
4. Click "Test Collibra Connection"

### Configuration Options

```python
from config import COLLIBRA_CONFIG

COLLIBRA_CONFIG = {
    "base_url": "https://your-instance.collibra.com",
    "username": "your_username",
    "password": "your_password",
    "timeout": 30,
    "max_retries": 3,
    "verify_ssl": True,
}
```

### Supported Operations

#### Get Assets
```python
from core.collibra_client import CollibraClient

client = CollibraClient()

# Get all assets of a type
assets = client.get_assets(
    asset_type="Data Entity",
    limit=100,
    offset=0
)

# Get assets in a domain
domain_assets = client.get_domain_assets("Asset Management")

# Search for assets
search_results = client.search_assets("investor_position", limit=50)
```

#### Get Asset Details
```python
# Get full asset details
asset = client.get_asset("asset-uuid-here")

# Get asset attributes
attrs = client.get_asset_attributes("asset-uuid-here")

# Get asset relations/lineage
relations = client.get_asset_relations("asset-uuid-here")

# Get quality rules
rules = client.get_data_quality_rules("asset-uuid-here")
```

### API Endpoints Used

```
GET  /api/v1/assets
GET  /api/v1/assets/{id}
GET  /api/v1/assets/{id}/relations
GET  /api/v1/assets/search
POST /api/v1/assets
PATCH /api/v1/assets/{id}
```

### Supported Asset Types

- **Data Entity** / **Table** / **DataSet** — represents a database table
- **Data Attribute** / **Column** / **Field** — represents a column
- **Data Source** / **System** / **Database** / **API** — represents a data source
- **Data Product** — the overall product

---

## AI Requirements Agent

### Overview

The AI Requirements Agent (`pages/0_AI_Requirements_Agent.py`) is a conversational interface designed for non-technical business users to define data products without technical knowledge.

### How It Works

1. **User describes their needs** — "I need a dataset of all investor positions from our trading platform"
2. **Agent asks clarifying questions** — "How many records per day? How fresh does it need to be?"
3. **Agent extracts structured data** — Product name, domain, sources, entities, governance, quality
4. **User reviews and refines** — View the extracted definition as JSON
5. **Import or export** — Load into the wizard for detailed configuration or download as JSON

### Conversation Flow

The agent guides users through these topics (in flexible order):

1. **Business Context**
   - Product name and objective
   - Business domain
   - Intended consumers/users

2. **Data Sources**
   - Source system names
   - Data owners
   - Criticality level

3. **Data Model**
   - Tables/entities
   - Key columns
   - Calculations or transformations

4. **Governance**
   - Data sensitivity (Public/Internal/Confidential/Restricted)
   - Applicable regulations (GDPR, CCPA, HIPAA, SOX, etc.)
   - Data ownership and access roles

5. **Data Quality**
   - Data freshness requirements
   - Completeness thresholds
   - Accuracy expectations

6. **Transformations**
   - Aggregations or calculations
   - Cleansing logic
   - Business rules

### Usage

#### Starting a Conversation

1. Click **🤖 AI Agent** on the landing page
2. (Optional) Configure OpenAI API key in the settings expander
3. (Optional) Import a Collibra domain for context
4. Type your first message: "I need to build a data product that..."

#### Example Conversation

```
User: I need a dataset of all investor positions across our AUM

Agent: Great! Let me help you build that. First, what would you like to call this data product?
For example: "Investor_Position_Summary" or "AUM_Positions_Daily"

User: Investor Position Summary

Agent: Perfect! Now, who will use this data? Are they traders, risk managers, operations, or someone else?

User: Risk managers and portfolio managers

Agent: Got it. How many unique investors are we talking about, and how many records per day?

User: About 5,000 investors, millions of positions

Agent: [continues asking questions about governance, quality, retention, etc.]
```

#### Viewing the Definition

After the conversation, click **View Definition** to see the extracted JSON:

```json
{
  "name": "Investor Position Summary",
  "objective": "Provide risk managers and portfolio managers with comprehensive position data",
  "domain": "Asset Management",
  "sources": ["Trading Platform", "Position Database"],
  "entities": ["POSITION", "INVESTOR", "TRADE"],
  "classification": "Confidential",
  "compliance_frameworks": ["SEC", "FINRA"],
  "retention_policy": "7 Years",
  "quality_rules": {
    "completeness": 99,
    "timeliness_hours": 1
  }
}
```

#### Importing to the Wizard

1. After reviewing, click **Import to Wizard**
2. This loads the extracted definition into the step-by-step builder
3. You can now refine each section in detail (entities, attributes, quality rules, etc.)
4. Generate final artifacts when complete

#### Exporting for Version Control

1. Click **Download JSON**
2. Save to your git repository
3. Share with team for review

### Prompting Best Practices

**Good prompts:**
- "I need a daily dataset of all investor positions, updated by 8am"
- "This contains account numbers and customer names (PII), subject to GDPR"
- "About 50,000 records per day from our Postgres database"

**Avoid vague language:**
- ❌ "A data product for trading"
- ✅ "A dataset that shows all active trades per portfolio, updated hourly for the trading desk"

---

## Security & Credential Management

### API Key Security

**DO:**
- ✅ Use environment variables in production
- ✅ Use Streamlit secrets in development
- ✅ Rotate keys regularly
- ✅ Use minimal-privilege API keys
- ✅ Store credentials in secure secret management (AWS Secrets Manager, HashiCorp Vault, etc.)

**DON'T:**
- ❌ Hardcode keys in source code
- ❌ Commit keys to git repositories
- ❌ Share keys in Slack, email, or chat
- ❌ Use the same key across environments
- ❌ Use keys longer than necessary

### Collibra Authentication

The Collibra client uses HTTP Basic Authentication:

```python
from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth(username, password)
```

**Best practices:**
- Use a dedicated service account for API access
- Give the account only necessary permissions in Collibra
- Rotate credentials periodically
- Monitor API usage for anomalies

### SSL/TLS Verification

By default, SSL verification is enabled (`verify_ssl=True`).

For self-signed certificates in development only:
```python
COLLIBRA_CONFIG["verify_ssl"] = False  # NOT for production!
```

---

## Architecture Overview

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit App                             │
│  (pages/0_AI_Requirements_Agent.py, pages/9_Settings.py)    │
└──────────────────┬────────────────────┬──────────────────────┘
                   │                    │
         ┌─────────▼──────┐   ┌────────▼────────┐
         │  OpenAI Client │   │ Collibra Client │
         │  (Chat, Embed) │   │  (Assets, Mgmt) │
         └────────┬────────┘   └────────┬────────┘
                  │                     │
    ┌─────────────┴───────┬─────────────┴──────────────┐
    │                     │                            │
┌───▼──────┐    ┌─────────▼──────┐    ┌──────────────▼─┐
│ OpenAI   │    │  Collibra      │    │ Requirements   │
│ API      │    │  API           │    │ Agent Logic    │
│          │    │                │    │                │
│ models/  │    │ /assets        │    │ Conversation   │
│ /embed   │    │ /search        │    │ + Extraction   │
│          │    │ /relations     │    │                │
└──────────┘    └────────────────┘    └────────────────┘
```

### Data Flow

```
User Input → RequirementsAgent.chat()
    ↓
OpenAIClient.system_prompt_completion()
    ↓
OpenAI API → GPT-4-Turbo
    ↓
Response + Extraction
    ↓
UI + Update session state
    ↓
Display to user + Offer import/export
```

### File Structure

```
core/
├── openai_client.py          # OpenAI API wrapper
├── collibra_client.py         # Collibra API wrapper
├── collibra_importer.py       # Collibra → Data Product converter
├── requirements_agent.py      # Conversation logic
└── [existing generators...]

pages/
├── 0_AI_Requirements_Agent.py # Conversational AI interface
├── 1_Business_Context.py      # ... existing wizard pages ...
└── 9_Settings.py              # API configuration & credential management

config.py                       # API configuration
requirements.txt               # Python dependencies
```

---

## Troubleshooting

### OpenAI Connection Issues

**Problem:** "OPENAI_API_KEY not set"

**Solution:**
1. Check environment variable: `echo $OPENAI_API_KEY`
2. Or add to `.streamlit/secrets.toml`
3. Restart Streamlit: `streamlit run streamlit_app.py`

**Problem:** "Rate limited after retries"

**Solution:**
1. Check OpenAI account usage: https://platform.openai.com/account/billing/overview
2. Increase `max_retries` in `config.py`
3. Use GPT-3.5-turbo (cheaper, fast for many tasks)
4. Implement request queuing for high volume

**Problem:** "Timeout errors"

**Solution:**
1. Increase `timeout` in config (currently 30 seconds)
2. Check network connectivity
3. Try from a different location/network
4. Contact OpenAI support if API is down

### Collibra Connection Issues

**Problem:** "Connection refused" or "Cannot connect"

**Solution:**
1. Verify Collibra URL is correct: `https://your-instance.collibra.com` (not `http://`)
2. Check if Collibra instance is running
3. Test manually: `curl -u username:password https://your-instance.collibra.com/api/v1/assets`
4. Check firewall/VPN access

**Problem:** "Authentication failed"

**Solution:**
1. Verify username and password are correct
2. Check if user has API access permissions in Collibra
3. Try basic auth manually: `curl -u username:password https://instance.com/api/v1/assets`
4. Check for special characters in password (may need URL encoding)

**Problem:** "No results imported"

**Solution:**
1. Verify domain name matches exactly (case-sensitive)
2. Check domain exists in Collibra: `GET /api/v1/domains`
3. Verify user has read permissions on domain
4. Try searching for assets: `client.search_assets("*", limit=1)`

### Requirements Agent Issues

**Problem:** "Agent keeps asking the same questions"

**Solution:**
- This is normal if context wasn't extracted. Be more specific:
  - ❌ "It's for trading"
  - ✅ "Dataset of all executed trades from our Bloomberg terminal"

**Problem:** "Extracted definition missing key fields"

**Solution:**
- Ensure you answered agent questions
- Click "View Definition" to see what was captured
- The agent improves with more context provided
- Refinements can always be made in the wizard

**Problem:** "Import to Wizard fails"

**Solution:**
1. Check console for error messages
2. Ensure wizard is initialized: go to landing page first
3. Try exporting JSON and importing via Settings → Import section
4. Check browser console (F12 → Console tab) for JavaScript errors

---

## Advanced Configuration

### Using Custom OpenAI Endpoints

For Azure OpenAI or other providers:

```python
# In environment or secrets
OPENAI_BASE_URL="https://your-instance.openai.azure.com/v1"
OPENAI_API_KEY="your-azure-key"
```

### Caching Collibra Data

For performance with large domains:

```python
from config import CACHE_CONFIG

CACHE_CONFIG = {
    "ttl_seconds": 3600,    # 1 hour
    "max_size_mb": 100,
}
```

Implement caching in your page:

```python
@st.cache_data(ttl=3600)
def get_domain_assets(domain_name):
    client = CollibraClient()
    return client.get_domain_assets(domain_name)
```

### Streaming Responses

For real-time UI updates (not currently used but available):

```python
client = OpenAIClient()
for chunk in client.streaming_completion(messages, max_tokens=1000):
    st.write(chunk, end="")
```

---

## Getting Help

- **OpenAI Docs**: https://platform.openai.com/docs/api-reference
- **Collibra API**: https://your-instance.collibra.com/api (built-in API docs)
- **Streamlit Docs**: https://docs.streamlit.io
- **GitHub Issues**: https://github.com/vm799/Data-Product-Steward/issues

---

## Version History

- **v1.1.0** (Current) — OpenAI and Collibra integration, Requirements Agent
- **v1.0.0** — Initial release with 7-step wizard
