import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from state_manager import initialize_state
from components.layout import inject_custom_css, step_header
from components.sidebar import render_sidebar
from core.openai_client import OpenAIClient
from core.collibra_client import CollibraClient
from core.collibra_importer import CollibraImporter
from core.requirements_agent import RequirementsAgent

initialize_state()
inject_custom_css()
render_sidebar(step=0)

# ── Page Configuration ────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Requirements Agent",
    page_icon="🤖",
    layout="wide",
)

st.markdown(
    '<div class="page-header-wrap">'
    '<h1 class="page-title">AI Requirements Agent</h1>'
    '<div class="page-subtitle">Describe your data product in plain English — I\'ll build the definition for you</div>'
    '</div>',
    unsafe_allow_html=True,
)

# ── Initialize Agent Session ─────────────────────────────────────────────
if "agent" not in st.session_state:
    st.session_state.agent = None
    st.session_state.agent_error = None

# ── API Configuration Check ──────────────────────────────────────────────
st.divider()
st.markdown("#### Configuration")

with st.expander("🔧 API Settings", expanded=False):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**OpenAI API**")
        openai_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=os.getenv("OPENAI_API_KEY", ""),
            help="Your OpenAI API key. Keep this secret!",
        )
        openai_model = st.selectbox(
            "Model",
            ["gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"],
            help="More advanced models = better understanding but higher cost",
        )

    with col2:
        st.markdown("**Collibra Integration (Optional)**")
        collibra_url = st.text_input(
            "Collibra Base URL",
            value=os.getenv("COLLIBRA_BASE_URL", ""),
            placeholder="https://your-collibra-instance.com",
        )
        collibra_user = st.text_input("Collibra Username", value=os.getenv("COLLIBRA_USERNAME", ""))
        collibra_pass = st.text_input(
            "Collibra Password",
            type="password",
            value=os.getenv("COLLIBRA_PASSWORD", ""),
        )

    if st.button("Test API Connection", use_container_width=True):
        try:
            client = OpenAIClient(api_key=openai_key)
            response = client.system_prompt_completion(
                system_prompt="You are a helpful assistant.",
                user_message="Say 'API connection successful' in 5 words or less.",
                max_tokens=50,
            )
            st.success(f"✅ OpenAI API connected: {response[:100]}")
        except Exception as e:
            st.error(f"❌ OpenAI API error: {str(e)}")

# ── Import from Collibra (Optional) ──────────────────────────────────────
st.divider()
st.markdown("#### Import Existing Data Model")

with st.expander("📥 Import from Collibra", expanded=False):
    if not all([collibra_url, collibra_user, collibra_pass]):
        st.info("Configure Collibra credentials above to enable imports.")
    else:
        collibra_domain = st.text_input(
            "Domain Name",
            placeholder="e.g. Asset Management",
            help="The Collibra domain to import",
        )

        if st.button("Import Domain", use_container_width=True):
            try:
                collibra = CollibraClient(
                    base_url=collibra_url,
                    username=collibra_user,
                    password=collibra_pass,
                )

                # Test connection
                if not collibra.test_connection():
                    st.error("Cannot connect to Collibra. Check your credentials.")
                else:
                    # Import the domain
                    importer = CollibraImporter(collibra)
                    model = importer.import_data_model(collibra_domain)

                    st.success(f"✅ Imported {len(model['entities'])} entities and "
                              f"{sum(len(e.get('attributes', [])) for e in model['entities'])} attributes")

                    # Store in session
                    st.session_state.product = model
                    st.session_state.collibra_domain = collibra_domain
                    st.info("Domain imported! Start the conversation or click 'Begin' to use the workflow.")

            except Exception as e:
                st.error(f"Import failed: {str(e)}")

# ── Agent Chat Interface ─────────────────────────────────────────────────
st.divider()
st.markdown("#### Conversation")
st.caption("Tell me about your data product. I'll ask clarifying questions to build a complete definition.")

# Initialize chat history
if "agent_chat" not in st.session_state:
    st.session_state.agent_chat = []

# Display chat history
for message in st.session_state.agent_chat:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Start describing your data product..."):
    # Initialize agent if needed
    if st.session_state.agent is None:
        try:
            openai_client = OpenAIClient(api_key=openai_key or os.getenv("OPENAI_API_KEY"))
            st.session_state.agent = RequirementsAgent(openai_client)
        except Exception as e:
            st.session_state.agent_error = str(e)
            st.error(f"Failed to initialize agent: {str(e)}")
            st.stop()

    # Add user message to chat
    st.session_state.agent_chat.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.agent.chat(prompt)
                st.markdown(response)
                st.session_state.agent_chat.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Agent error: {str(e)}")

# ── Agent Actions ────────────────────────────────────────────────────────
if st.session_state.agent:
    st.divider()
    st.markdown("#### Next Steps")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📋 View Definition", use_container_width=True):
            definition = st.session_state.agent.get_product_definition()
            st.json(definition)

    with col2:
        if st.button("🚀 Import to Wizard", use_container_width=True):
            # Import agent's extracted product into the workflow
            definition = st.session_state.agent.get_product_definition()
            st.session_state.product.update(definition)
            st.success("Imported into workflow! Go to Step 1 to refine details.")
            st.page_link("pages/1_Business_Context.py", label="Go to Wizard")

    with col3:
        if st.button("💾 Download JSON", use_container_width=True):
            import json
            definition = st.session_state.agent.get_product_definition()
            st.download_button(
                label="Download",
                data=json.dumps(definition, indent=2),
                file_name="data_product_definition.json",
                mime="application/json",
            )

# ── Instructions ─────────────────────────────────────────────────────────
st.divider()
with st.expander("❓ How This Works"):
    st.markdown("""
    **The AI Requirements Agent** is designed for business people who want to build data products
    without learning technical details. Here's the workflow:

    1. **Configure APIs** — Add your OpenAI API key (required for the agent to work)
    2. **Start Conversation** — Describe what you want. Ask for clarifications.
    3. **Review Definition** — See the extracted data product definition
    4. **Import or Export** — Load into the workflow for detailed refinement, or download as JSON

    ### What the Agent Learns
    - Product name and business objective
    - Data sources and where they come from
    - Tables (entities) and columns (attributes)
    - Data classification and compliance needs (GDPR, CCPA, HIPAA, etc.)
    - Data quality and freshness requirements
    - Transformations and business logic

    ### Pro Tips
    - Be specific: "3 months" not "recent"
    - Mention regulations if applicable: "GDPR", "HIPAA"
    - Give context: "We're in asset management" helps the agent understand
    - If the agent asks, give more detail — vagueness wastes back-and-forth
    """)
