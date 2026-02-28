"""
Snowflake Generator
Generates Snowflake DDL statements from the data product definition.
"""


class SnowflakeGenerator:
    """Produces Snowflake-compatible DDL from the data model."""

    def __init__(self, state_snapshot: dict):
        self.state = state_snapshot

    def generate_ddl(self) -> str:
        """Generate CREATE TABLE statements for all entities."""
        model = self.state.get("data_model", {})
        entities = model.get("entities", [])
        statements = []

        for entity in entities:
            stmt = self._create_table(entity)
            if stmt:
                statements.append(stmt)

        return "\n\n".join(statements)

    def _create_table(self, entity: dict) -> str:
        """Generate a single CREATE TABLE statement."""
        name = entity.get("name", "UNNAMED")
        columns = entity.get("columns", [])
        pk = entity.get("primary_key", "")

        col_defs = []
        for col in columns:
            col_name = col.get("name", "unnamed")
            col_type = col.get("type", "VARCHAR")
            col_defs.append(f"    {col_name} {col_type}")

        if pk:
            col_defs.append(f"    PRIMARY KEY ({pk})")

        cols_sql = ",\n".join(col_defs)
        comment = entity.get("description", "").replace("'", "''")

        return (
            f"CREATE TABLE IF NOT EXISTS {name} (\n{cols_sql}\n)"
            f"\nCOMMENT = '{comment}';"
        )

    def generate_grants(self) -> str:
        """Generate GRANT statements based on governance roles."""
        gov = self.state.get("governance_security", {})
        roles_raw = gov.get("access_roles", "")
        if not roles_raw:
            return "-- No access roles defined."

        roles = [r.strip() for r in roles_raw.split(",") if r.strip()]
        model = self.state.get("data_model", {})
        entities = model.get("entities", [])

        grants = []
        for entity in entities:
            table = entity.get("name", "UNNAMED")
            for role in roles:
                grants.append(f"GRANT SELECT ON TABLE {table} TO ROLE {role};")

        return "\n".join(grants)
