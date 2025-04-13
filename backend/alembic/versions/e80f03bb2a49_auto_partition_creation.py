"""auto partition creation

Revision ID: e80f03bb2a49
Revises: a80765f471db
Create Date: 2025-03-09 10:00:49.406509

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e80f03bb2a49"
down_revision: Union[str, None] = "a80765f471db"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

company_name = "anthropic"
table_name = f"reviews_{company_name}"


def upgrade():
    result = op.get_bind().execute(
        sa.text("INSERT INTO companies (name) VALUES (:name) RETURNING id"),
        {"name": company_name},
    )
    company_uuid = result.scalar()

    op.execute(f"""
        CREATE TABLE {table_name} PARTITION OF reviews_partitioned
        FOR VALUES IN ('{company_uuid}');
    """)


def downgrade():
    op.execute(f"ALTER TABLE reviews_partitioned DETACH PARTITION {table_name};")
    op.drop_table(table_name)
