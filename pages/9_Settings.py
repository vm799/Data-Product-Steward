import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from state_manager import initialize_state
from components.layout import inject_custom_css
from components.sidebar import render_sidebar

initialize_state()
inject_custom_css()
render_sidebar(step=9)

st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
    layout="wide",
)

st.markdown(
    '<div class="page-header-wrap">'
    '<h1 class="page-title">Settings</h1>'
    '<div class="page-subtitle">Configure API integrations and security settings</div>'
    '</div>',
    unsafe_allow_html=True,
)

# ── API Configuration ────────────────────────────────────────────────────
st.divider()
st.markdown("## API Configuration")

st.info(
    "🔒 **Security Note:** API credentials are best stored in environment variables or Streamlit secrets, "
    "not in plaintext. Use the form below for testing only."
)

with st.expander("OpenAI Configuration", expanded=True):
    st.markdown("**OpenAI API Setup**")

    # Method 1: Environment variable
    st.markdown("##### Method 1: Environment Variable (Recommended)")
    st.code("export OPENAI_API_KEY='your-api-key-here'", language="bash")
    st.caption("Set this in your shell before running: `streamlit run streamlit_app.py`")

    # Method 2: Streamlit secrets
    st.markdown("##### Method 2: Streamlit Secrets")
    st.markdown(
        "Add to `.streamlit/secrets.toml`:\n```\nOPENAI_API_KEY = 'your-key'\nOPENAI_MODEL = 'gpt-4-turbo'\n```"
    )

    st.divider()
    st.markdown("##### Method 3: Manual Entry (Testing Only)")

    col1, col2 = st.columns(2)
    with col1:
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Get from https://platform.openai.com/api-keys",
        )
    with col2:
        model = st.selectbox(
            "Model",
            ["gpt-4-turbo", "gpt-4", "gpt-3.5-turbo", "gpt-4-turbo-preview"],
        )

    if api_key and st.button("Test OpenAI Connection"):
        try:
            from core.openai_client import OpenAIClient

            client = OpenAIClient(api_key=api_key)
            # Test with a simple request
            response = client.system_prompt_completion(
                system_prompt="You are a helpful assistant.",
                user_message="Reply with just 'OK' if working.",
                max_tokens=10,
            )
            st.success(f"✅ Connection successful! Response: {response.strip()}")

            # Save to session for this session
            os.environ["OPENAI_API_KEY"] = api_key
            os.environ["OPENAI_MODEL"] = model

        except ImportError:
            st.error("❌ OpenAI package not installed. Run: `pip install openai`")
        except Exception as e:
            st.error(f"❌ Connection failed: {str(e)}")

# ── Collibra Configuration ──────────────────────────────────────────────
with st.expander("Collibra Configuration"):
    st.markdown("**Collibra API Setup**")

    st.markdown("##### Environment Variables (Recommended)")
    st.code(
        "export COLLIBRA_BASE_URL='https://your-instance.collibra.com'\n"
        "export COLLIBRA_USERNAME='your-username'\n"
        "export COLLIBRA_PASSWORD='your-password'",
        language="bash",
    )

    st.divider()
    st.markdown("##### Manual Entry (Testing Only)")

    col1, col2, col3 = st.columns(3)
    with col1:
        collibra_url = st.text_input(
            "Base URL",
            placeholder="https://your-instance.collibra.com",
        )
    with col2:
        collibra_user = st.text_input("Username")
    with col3:
        collibra_pass = st.text_input("Password", type="password")

    if all([collibra_url, collibra_user, collibra_pass]) and st.button("Test Collibra Connection"):
        try:
            from core.collibra_client import CollibraClient

            client = CollibraClient(
                base_url=collibra_url,
                username=collibra_user,
                password=collibra_pass,
            )
            if client.test_connection():
                st.success("✅ Connected to Collibra!")

                # Save to session
                os.environ["COLLIBRA_BASE_URL"] = collibra_url
                os.environ["COLLIBRA_USERNAME"] = collibra_user
                os.environ["COLLIBRA_PASSWORD"] = collibra_pass

            else:
                st.error("❌ Could not authenticate with Collibra")

        except ImportError:
            st.error("❌ Requests package not installed. Run: `pip install requests`")
        except Exception as e:
            st.error(f"❌ Connection failed: {str(e)}")

# ── Data Management ─────────────────────────────────────────────────────
st.divider()
st.markdown("## Data Management")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Export")
    st.caption("Download your current data product definition")

    if st.button("📥 Export as JSON", use_container_width=True):
        import json

        product = st.session_state.product
        json_str = json.dumps(product, indent=2, default=str)
        st.download_button(
            label="Download JSON",
            data=json_str,
            file_name="data_product_definition.json",
            mime="application/json",
        )

    if st.button("📄 Export as YAML", use_container_width=True):
        import yaml

        product = st.session_state.product
        yaml_str = yaml.dump(product, default_flow_style=False)
        st.download_button(
            label="Download YAML",
            data=yaml_str,
            file_name="data_product_definition.yaml",
            mime="text/plain",
        )

with col2:
    st.markdown("### Import")
    st.caption("Load a previously exported definition")

    uploaded_file = st.file_uploader("Choose a JSON or YAML file", type=["json", "yaml", "yml"])

    if uploaded_file:
        try:
            import json
            import yaml

            content = uploaded_file.read().decode("utf-8")

            if uploaded_file.name.endswith(".json"):
                product_data = json.loads(content)
            else:
                product_data = yaml.safe_load(content)

            st.session_state.product.update(product_data)
            st.success("✅ Definition imported successfully!")
            st.page_link("pages/1_Business_Context.py", label="Go to Wizard")

        except Exception as e:
            st.error(f"Failed to import: {str(e)}")

# ── Application Settings ────────────────────────────────────────────────
st.divider()
st.markdown("## Application Settings")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Cache Settings")
    cache_enabled = st.checkbox("Enable Collibra data caching", value=True)
    cache_ttl = st.slider("Cache TTL (seconds)", 300, 3600, 3600)

    if cache_enabled:
        st.caption(f"Collibra data will be cached for {cache_ttl} seconds")

with col2:
    st.markdown("### Logging & Debugging")
    debug_mode = st.checkbox("Enable debug logging", value=False)
    verbose_errors = st.checkbox("Show detailed error messages", value=True)

    if debug_mode:
        st.caption("Debug logs will be printed to console")

# ── Reset & Clear ────────────────────────────────────────────────────────
st.divider()
st.markdown("## Reset Application")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 Reset Current Product", use_container_width=True):
        st.session_state.product = {
            "name": "",
            "domain": "",
            "objective": "",
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
        st.success("Product definition cleared")

with col2:
    if st.button("🗑️ Clear All Session Data", use_container_width=True):
        st.session_state.clear()
        st.success("All session data cleared")

# ── About ───────────────────────────────────────────────────────────────
st.divider()
st.markdown("## About")

st.markdown(
    """
    **Data Product Builder v1.0**

    Built to help data teams ship production-ready data products in hours, not weeks.

    - 🏗️ Guided wizard for data product definitions
    - 🤖 AI-powered requirements agent for non-technical users
    - 📊 Automatic artifact generation (DDL, dbt, policies, metadata)
    - 🔐 Enterprise security (PII masking, RLS, encryption)

    [GitHub](https://github.com/vm799/Data-Product-Steward) |
    [Documentation](https://github.com/vm799/Data-Product-Steward/blob/main/README.md) |
    [Issues](https://github.com/vm799/Data-Product-Steward/issues)
    """
)
