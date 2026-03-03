import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from state_manager import initialize_state, mark_step_complete
from components.layout import inject_custom_css, step_header
from components.sidebar import render_sidebar
from components.helpers import render_step_nav, render_step_nav_bottom, render_step_complete

initialize_state()
inject_custom_css()
render_sidebar(step=5)

render_step_nav(5)
step_header(
    5,
    "Data Quality",
    "Define quality rules at the attribute level. Create constraints, primary keys, references, and custom validations.",
)

product = st.session_state.product
qr = product.get("quality_rules", {})

# ── Global Quality Settings ──────────────────────────────────────────────
st.markdown("#### Global Quality Settings")
st.caption(
    "These thresholds apply across your product. Specify SLA monitoring and alerting channels."
)

gc1, gc2, gc3 = st.columns(3)
with gc1:
    global_completeness = st.number_input(
        "Default Completeness Threshold (%)",
        min_value=0,
        max_value=100,
        value=qr.get("global_completeness", 95),
        help="Industry baseline is 95%. Override per attribute below.",
    )
with gc2:
    timeliness_hours = st.number_input(
        "Timeliness SLA (hours)",
        min_value=1,
        max_value=720,
        value=qr.get("timeliness_hours", 24),
        help="Maximum acceptable delay from source refresh to product availability.",
    )
with gc3:
    monitoring_channel = st.text_input(
        "Alerting Channel",
        value=qr.get("monitoring_channel", ""),
        placeholder="e.g. #data-quality-alerts or ops@firm.com",
        help="Where quality alerts are sent when thresholds breached.",
    )

# ── Attribute-Level Quality Rules ────────────────────────────────────────
st.divider()
st.markdown("#### Attribute-Level Quality Rules")
st.caption(
    "Define completeness, uniqueness, and validation rules per attribute. "
    "Uniqueness = 100% for primary keys, lower for dimensions."
)

# Get attributes from entities
attr_options = []
attr_map = {}
for ent in product.get("entities", []):
    for attr in ent.get("attributes", []):
        full_name = f"{ent['name']}.{attr['name']}"
        attr_options.append(full_name)
        attr_map[full_name] = {"entity": ent["name"], "attr": attr["name"], "type": attr.get("data_type", "STRING")}

if not attr_options:
    st.info("Create entities and attributes in Step 3 first.")
else:
    # ── Add Attribute Rule ──────────────────────────────────────────────
    st.markdown("**Add Attribute Quality Rule**")

    with st.form("add_attr_rule_form"):
        attr_select = st.selectbox(
            "Select Attribute",
            attr_options,
            help="Choose an attribute to define quality constraints.",
        )

        c1, c2 = st.columns(2)
        with c1:
            completeness_pct = st.number_input(
                "Completeness (%)",
                min_value=0,
                max_value=100,
                value=95,
                help="Percentage of non-null values. 100% = NOT NULL required.",
            )
            is_primary_key = st.checkbox(
                "Primary Key?",
                help="If checked, uniqueness is set to 100% and not null is enforced.",
            )

        with c2:
            uniqueness_pct = st.number_input(
                "Uniqueness (%)",
                min_value=0,
                max_value=100,
                value=100 if is_primary_key else 0,
                disabled=is_primary_key,
                help="100% = no duplicates. Primary keys always 100%.",
            )
            is_foreign_key = st.checkbox(
                "Foreign Key Reference?",
                help="If checked, values must exist in a reference table.",
            )

        if is_foreign_key:
            fk_col1, fk_col2 = st.columns(2)
            with fk_col1:
                ref_table = st.text_input(
                    "Reference Table",
                    placeholder="e.g. DIM_INVESTOR",
                    help="The table this foreign key references.",
                )
            with fk_col2:
                ref_column = st.text_input(
                    "Reference Column",
                    placeholder="e.g. INVESTOR_ID",
                    help="The column in the reference table.",
                )
        else:
            ref_table = ""
            ref_column = ""

        # Value validation options
        st.markdown("**Value Validation**")
        vv1, vv2 = st.columns(2)
        with vv1:
            value_range_check = st.checkbox(
                "Range Check?",
                help="Validate numeric values fall within min/max bounds.",
            )
            if value_range_check:
                rvmin, rvmax = st.columns(2)
                with rvmin:
                    range_min = st.number_input("Min Value", value=0.0)
                with rvmax:
                    range_max = st.number_input("Max Value", value=1000.0)
            else:
                range_min = None
                range_max = None

        with vv2:
            regex_pattern = st.text_input(
                "Regex Pattern (Optional)",
                placeholder="e.g. ^[A-Z]{3}$ for 3-letter codes",
                help="Validate string formats. E.g. email, currency codes.",
            )

        # Custom SQL rule
        custom_sql = st.text_area(
            "Custom SQL Validation (Optional)",
            placeholder="e.g. INVESTOR_ID IS NOT NULL AND INVESTOR_ID > 0",
            help="Write custom dbt test SQL. Use column reference as {{ column_name }}",
            height=80,
        )

        submitted = st.form_submit_button("Add Attribute Rule")

        if submitted:
            if not attr_select:
                st.error("Select an attribute first.")
            else:
                if "attribute_rules" not in product:
                    product["attribute_rules"] = []

                rule = {
                    "attribute": attr_select,
                    "completeness": completeness_pct,
                    "uniqueness": 100 if is_primary_key else uniqueness_pct,
                    "is_primary_key": is_primary_key,
                    "is_foreign_key": is_foreign_key,
                }

                if is_foreign_key:
                    rule["ref_table"] = ref_table
                    rule["ref_column"] = ref_column

                if value_range_check and range_min is not None:
                    rule["range_check"] = {"min": range_min, "max": range_max}

                if regex_pattern:
                    rule["regex_pattern"] = regex_pattern

                if custom_sql:
                    rule["custom_sql"] = custom_sql

                product["attribute_rules"].append(rule)
                st.success(f"Rule added for **{attr_select}**")
                st.rerun()

# ── Display Attribute Rules ──────────────────────────────────────────────
st.divider()
st.markdown("#### Defined Attribute Rules")

attr_rules = product.get("attribute_rules", [])
if attr_rules:
    for idx, rule in enumerate(attr_rules):
        badges = []
        if rule.get("is_primary_key"):
            badges.append("🔑 PK")
        if rule.get("is_foreign_key"):
            badges.append("🔗 FK")
        if rule.get("completeness") == 100:
            badges.append("✓ NOT NULL")

        badge_str = " ".join(badges) if badges else ""

        with st.expander(f"{rule['attribute']} {badge_str}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Completeness", f"{rule['completeness']}%")
            with col2:
                st.metric("Uniqueness", f"{rule['uniqueness']}%")
            with col3:
                st.metric("Rules", sum(1 for k in rule.keys() if k not in ["attribute", "completeness", "uniqueness", "is_primary_key", "is_foreign_key"]))

            if rule.get("is_foreign_key"):
                st.markdown(f"**Foreign Key:** {rule['attribute']} → {rule.get('ref_table', '?')}.{rule.get('ref_column', '?')}")

            if rule.get("range_check"):
                r = rule["range_check"]
                st.markdown(f"**Range Check:** {r['min']} to {r['max']}")

            if rule.get("regex_pattern"):
                st.markdown(f"**Regex Pattern:** `{rule['regex_pattern']}`")

            if rule.get("custom_sql"):
                st.markdown("**Custom SQL Test:**")
                st.code(rule["custom_sql"], language="sql")

            if st.button("Delete Rule", key=f"del_rule_{idx}"):
                product["attribute_rules"].pop(idx)
                st.rerun()
else:
    st.info("No attribute rules defined yet. Add one above to get started.")

# ── Save All Quality Rules ──────────────────────────────────────────────
if st.button("Save All Quality Rules", use_container_width=True, type="primary"):
    product["quality_rules"] = {
        "global_completeness": global_completeness,
        "timeliness_hours": timeliness_hours,
        "monitoring_channel": monitoring_channel,
        "attribute_rules": product.get("attribute_rules", []),
    }
    mark_step_complete("quality")
    st.success("Data quality rules saved successfully.")

# ── Step complete prompt ──────────────────────────────
step_done = len(product.get("attribute_rules", [])) > 0
render_step_complete(5, step_done)

# ── Navigation buttons at bottom ─────────────────────
render_step_nav_bottom(5)
