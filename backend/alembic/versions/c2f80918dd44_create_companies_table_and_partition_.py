"""create companies table and partition reviews

Revision ID: c2f80918dd44
Revises: 988447c399f9
Create Date: 2025-03-09 09:21:42.780386

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c2f80918dd44"
down_revision: Union[str, None] = "988447c399f9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

classification_enum = sa.Enum(
    "POS",
    "NEG",
    "NEU",
    name="classification_enum",
    create_type=False,
    native_enum=False,
)


def upgrade():
    bind = op.get_bind()

    result = bind.execute(
        sa.text("SELECT 1 FROM pg_type WHERE typname = 'classification_enum'")
    ).scalar()
    if result is None:
        op.execute(
            sa.text("CREATE TYPE classification_enum AS ENUM ('POS', 'NEG', 'NEU')")
        )

    op.create_table(
        "companies",
        sa.Column(
            "id",
            sa.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("name", sa.String(), nullable=False, unique=True),
    )

    op.create_table(
        "reviews_partitioned",
        sa.Column(
            "id",
            sa.UUID(as_uuid=True),
            nullable=False,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("customer_id", sa.UUID(as_uuid=True), nullable=False),
        sa.Column("review_date", sa.Date(), nullable=False),
        sa.Column("review_data", sa.String(), nullable=False),
        sa.Column(
            "classification",
            classification_enum,
            nullable=True,
        ),
        sa.Column("classified_at", sa.Date(), nullable=True),
        sa.Column("sentiment_scores", sa.JSON(), nullable=True),
        sa.Column("company_id", sa.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["customer_id"], ["customers.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", "company_id"),
        postgresql_partition_by="LIST (company_id)",
    )

    op.create_index("ix_companies_id", "companies", ["id"])


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS reviews_deepmind;")

    op.execute("DROP TABLE IF EXISTS reviews_partitioned CASCADE;")

    op.execute("DROP TABLE IF EXISTS companies CASCADE;")

    op.execute("DROP INDEX IF EXISTS ix_companies_id;")
