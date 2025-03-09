"""create companies table and partition reviews

Revision ID: c2f80918dd44
Revises: 988447c399f9
Create Date: 2025-03-09 09:21:42.780386

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
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

    # Ensure the enum type exists before creating it
    result = bind.execute(
        sa.text("SELECT 1 FROM pg_type WHERE typname = 'classification_enum'")
    ).scalar()
    if result is None:
        op.execute(
            sa.text("CREATE TYPE classification_enum AS ENUM ('POS', 'NEG', 'NEU')")
        )

    # Create the companies table
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

    # Create the partitioned reviews table with company_id in the primary key
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
        sa.PrimaryKeyConstraint("id", "company_id"),  # FIX: Add company_id here
        postgresql_partition_by="LIST (company_id)",
    )

    # Create indexes
    op.create_index("ix_companies_id", "companies", ["id"])


def downgrade() -> None:
    # Step 1: Drop the partition (if it exists)
    op.execute("DROP TABLE IF EXISTS reviews_deepmind;")

    # Step 2: Drop the partitioned reviews table
    op.execute("DROP TABLE IF EXISTS reviews_partitioned CASCADE;")

    # Step 3: If you need to remove the companies table, drop it after dependencies are removed
    op.execute("DROP TABLE IF EXISTS companies CASCADE;")

    # Step 4: Drop indexes if they were created in the migration
    op.execute("DROP INDEX IF EXISTS ix_companies_id;")
