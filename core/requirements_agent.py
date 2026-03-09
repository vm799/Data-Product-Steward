"""
Data Product Requirements Agent
Guides non-technical users through defining data products using conversational AI.
"""

from typing import List, Dict, Optional
import json
from .openai_client import OpenAIClient


SYSTEM_PROMPT = """You are a friendly Data Product Requirements Assistant. Your job is to help non-technical business users define data products through conversation.

You will:
1. Ask clarifying questions about their data product needs (one question at a time)
2. Extract structured information about: business context, data sources, data model, governance, quality requirements, and transformations
3. Guide them to create production-ready data product definitions in Snowflake/dbt

Important guidelines:
- Use plain English, avoid technical jargon
- Ask ONE clear question at a time
- Remember context from the conversation
- Extract actionable requirements (names, thresholds, compliance needs)
- When the user provides vague answers, ask for specifics (e.g., "How many records per day?")
- Confirm your understanding before moving forward

Current conversation context:
{context}

Guide the user through this sequence (ask about items not yet covered):
1. BUSINESS CONTEXT: What is this data product called? What business problem does it solve? Who will use it?
2. DATA SOURCES: Where does the data come from? What are the names of the source systems?
3. DATA MODEL: What are the main entities/tables? What columns matter most?
4. GOVERNANCE: Is this data sensitive? What regulations apply (GDPR, CCPA, etc.)?
5. DATA QUALITY: How fresh must the data be? What completeness/accuracy is acceptable?
6. TRANSFORMATIONS: What calculations or transformations are needed?

When user says they're done or satisfied, provide a JSON summary of the defined product."""


class RequirementsAgent:
    """Conversational AI agent for gathering data product requirements."""

    def __init__(self, openai_client: OpenAIClient):
        """Initialize agent with OpenAI client."""
        self.client = openai_client
        self.conversation_history: List[Dict] = []
        self.extracted_product: Dict = {
            "name": "",
            "objective": "",
            "domain": "",
            "geo_scope": "",
            "consumers": "",
            "sources": [],
            "entities": [],
            "classification": "",
            "compliance_frameworks": [],
            "retention_policy": "",
            "quality_rules": {},
            "transformations": [],
        }
        self.stage = "business_context"  # Track where we are in the process

    def _get_context_summary(self) -> str:
        """Generate a summary of what has been collected so far."""
        collected = []
        if self.extracted_product.get("name"):
            collected.append(f"- Product name: {self.extracted_product['name']}")
        if self.extracted_product.get("objective"):
            collected.append(f"- Objective: {self.extracted_product['objective']}")
        if self.extracted_product.get("sources"):
            collected.append(f"- Data sources: {len(self.extracted_product['sources'])} identified")
        if self.extracted_product.get("entities"):
            collected.append(f"- Entities/tables: {len(self.extracted_product['entities'])} identified")
        if self.extracted_product.get("classification"):
            collected.append(f"- Classification: {self.extracted_product['classification']}")
        if self.extracted_product.get("compliance_frameworks"):
            collected.append(f"- Compliance: {', '.join(self.extracted_product['compliance_frameworks'])}")

        return "What we know so far:\n" + "\n".join(collected) if collected else "Just getting started!"

    def chat(self, user_message: str) -> str:
        """
        Send a user message and get agent response.

        Args:
            user_message: User's question or statement

        Returns:
            Agent's response
        """
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": user_message})

        # Check if user is done
        if any(word in user_message.lower() for word in ["done", "finish", "complete", "export", "summary"]):
            return self._generate_summary()

        # Build context
        context = self._get_context_summary()
        system = SYSTEM_PROMPT.format(context=context)

        # Get agent response
        try:
            response = self.client.system_prompt_completion(
                system_prompt=system,
                user_message=user_message,
                temperature=0.6,
                max_tokens=1024,
            )

            # Add assistant response to history
            self.conversation_history.append({"role": "assistant", "content": response})

            # Try to extract structured data from the conversation
            self._extract_from_response(response, user_message)

            return response

        except ValueError as e:
            return f"I encountered an error: {str(e)}. Please try again or check your API configuration."

    def _extract_from_response(self, assistant_response: str, user_message: str):
        """Try to extract structured data from the conversation."""
        lower_user = user_message.lower()
        lower_assistant = assistant_response.lower()

        # Extract product name
        if "product name" in lower_assistant or "called" in lower_user:
            # Simple heuristic - if user said something that looks like a name
            words = user_message.split()
            if len(words) < 6 and not any(word in lower_user for word in ["how", "what", "why", "when", "where"]):
                self.extracted_product["name"] = user_message.strip().strip('"\'')

        # Extract domain
        if "domain" in lower_assistant:
            if "finance" in lower_user or "trading" in lower_user or "asset" in lower_user:
                self.extracted_product["domain"] = self._extract_domain(lower_user)
            elif "healthcare" in lower_user or "medical" in lower_user:
                self.extracted_product["domain"] = "Healthcare"
            elif "retail" in lower_user or "ecommerce" in lower_user:
                self.extracted_product["domain"] = "Retail"

        # Extract compliance
        if "compliance" in lower_assistant or "regulation" in lower_assistant:
            for framework in ["gdpr", "ccpa", "hipaa", "sox", "pci-dss", "soc2", "mifid", "dora"]:
                if framework in lower_user:
                    if framework.upper() not in self.extracted_product["compliance_frameworks"]:
                        self.extracted_product["compliance_frameworks"].append(framework.upper())

        # Extract classification
        if "classification" in lower_assistant:
            for classification in ["public", "internal", "confidential", "restricted"]:
                if classification in lower_user:
                    self.extracted_product["classification"] = classification.capitalize()
                    break

        # Extract retention
        if "retention" in lower_assistant:
            for period in ["30 days", "90 days", "1 year", "3 years", "7 years", "indefinite"]:
                if period in lower_user:
                    self.extracted_product["retention_policy"] = period.title()
                    break

    def _extract_domain(self, text: str) -> str:
        """Extract domain from text."""
        if "finance" in text or "trading" in text or "investment" in text or "asset" in text:
            return "Asset Management"
        elif "risk" in text:
            return "Risk Management"
        elif "operations" in text:
            return "Operations"
        elif "marketing" in text:
            return "Marketing"
        elif "sales" in text:
            return "Sales"
        return "General"

    def _generate_summary(self) -> str:
        """Generate final product definition summary."""
        summary = f"""
Great! Here's a summary of the data product we defined:

**Product Name:** {self.extracted_product.get('name', 'Undefined')}

**Business Objective:** {self.extracted_product.get('objective', 'Undefined')}

**Domain:** {self.extracted_product.get('domain', 'Undefined')}

**Data Sources:** {len(self.extracted_product.get('sources', []))} sources identified

**Entities/Tables:** {len(self.extracted_product.get('entities', []))} tables

**Classification:** {self.extracted_product.get('classification', 'Not specified')}

**Compliance Frameworks:** {', '.join(self.extracted_product.get('compliance_frameworks', [])) or 'None specified'}

**Retention Policy:** {self.extracted_product.get('retention_policy', 'Not specified')}

---

You can now:
1. **Import to Wizard** - Load this into the step-by-step builder for detailed configuration
2. **Export Definition** - Download as JSON for version control
3. **Start Over** - Begin a new conversation for another data product

Would you like to import this into the wizard builder or export it?
"""
        return summary.strip()

    def get_product_definition(self) -> Dict:
        """Get the current extracted product definition."""
        return self.extracted_product.copy()

    def import_collibra_context(self, domain_name: str, assets: List[Dict]):
        """
        Import Collibra domain context to enrich the conversation.

        Args:
            domain_name: Collibra domain name
            assets: List of assets from Collibra
        """
        self.extracted_product["domain"] = domain_name
        entity_names = [
            a.get("name")
            for a in assets
            if a.get("type", {}).get("name") in ["Data Entity", "Table"]
        ]
        if entity_names:
            self.conversation_history.append({
                "role": "system",
                "content": f"Context: User is building a product for domain '{domain_name}' "
                f"with potential entities: {', '.join(entity_names[:5])}",
            })
