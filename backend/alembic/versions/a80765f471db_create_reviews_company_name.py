"""create reviews_company_name

Revision ID: a80765f471db
Revises: c2f80918dd44
Create Date: 2025-03-09 09:37:02.686632

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a80765f471db"
down_revision: Union[str, None] = "c2f80918dd44"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Ensure company_id is correctly formatted as UUID
    op.execute("""
        CREATE TABLE reviews_deepmind PARTITION OF reviews_partitioned
        FOR VALUES IN ('d3849d9c-1116-4260-b126-96c767c1d5d5'::UUID);
    """)

    # Step 1: Insert data from reviews table into reviews_partitioned with updated company_id
    op.execute("""
        INSERT INTO reviews_partitioned (id, customer_id, review_date, review_data, 
        classification, classified_at, sentiment_scores, company_id)
        SELECT id, customer_id, review_date, review_data, 
        classification, classified_at, sentiment_scores, 
        'd3849d9c-1116-4260-b126-96c767c1d5d5'::UUID
        FROM reviews;
    """)


def downgrade() -> None:
    # Detach the partition before dropping it
    op.execute("ALTER TABLE reviews_partitioned DETACH PARTITION reviews_deepmind;")
    op.drop_table("reviews_deepmind")
