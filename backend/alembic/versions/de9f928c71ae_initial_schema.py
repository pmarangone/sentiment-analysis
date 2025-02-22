"""initial schema

Revision ID: de9f928c71ae
Revises:
Create Date: 2025-02-10 20:40:14.114786

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "de9f928c71ae"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "reviews",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True, index=True),
        sa.Column("customer_name", sa.String(length=255), nullable=False),
        sa.Column("review_date", sa.Date(), nullable=False),
        sa.Column("review_data", sa.String(), nullable=False),
        sa.Column("classification", sa.String(), default=""),
        sa.Column("classified", sa.Boolean(), nullable=False, index=True),
        sa.Column("classified_at", sa.Date(), nullable=True, index=True),
        sa.Column("pos_score", sa.Float(), nullable=True, default=0.0),
        sa.Column("neu_score", sa.Float(), nullable=True, default=0.0),
        sa.Column("neg_score", sa.Float(), nullable=True, default=0.0),
    )


def downgrade() -> None:
    op.drop_table("reviews")
