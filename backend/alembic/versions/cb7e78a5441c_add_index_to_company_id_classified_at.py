"""add index to (company_id, classified_at)


Revision ID: cb7e78a5441c
Revises: e80f03bb2a49
Create Date: 2025-04-05 23:46:09.667000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cb7e78a5441c"
down_revision: Union[str, None] = "e80f03bb2a49"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "ix_reviews_partitioned_company_classified",
        "reviews_partitioned",
        ["company_id", "classified_at"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_reviews_partitioned_company_classified", table_name="reviews_partitioned"
    )
