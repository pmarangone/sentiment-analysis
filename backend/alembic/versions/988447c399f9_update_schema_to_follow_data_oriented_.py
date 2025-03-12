"""update schema to follow data oriented design

Revision ID: 988447c399f9
Revises: de9f928c71ae
Create Date: 2025-02-10 20:42:01.967742

"""

from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "988447c399f9"
down_revision: Union[str, None] = "de9f928c71ae"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    classification_enum = sa.Enum(
        "POS", "NEG", "NEU", name="classification_enum", create_type=True
    )
    classification_enum.create(op.get_bind(), checkfirst=True)

    # Replace empty strings with NULL in the classification column
    op.execute(
        sa.text("UPDATE reviews SET classification = NULL WHERE classification = ''")
    )

    # Criar tabela de clientes
    op.create_table(
        "customers",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True, index=True),
        sa.Column("name", sa.String, nullable=False, unique=True),
    )

    # Criar uma tabela temporária para fazer a migração correta dos dados
    reviews_table = sa.table(
        "reviews", sa.column("customer_name", sa.String), sa.column("id", sa.UUID)
    )

    # Criar os clientes com UUIDs únicos e mapear para os reviews
    conn = op.get_bind()
    existing_reviews = conn.execute(
        sa.select(reviews_table.c.customer_name, reviews_table.c.id)
    ).fetchall()

    customer_map = {}
    for customer_name, review_id in existing_reviews:
        if customer_name not in customer_map:
            customer_id = str(uuid4())  # Gerar um UUID novo para o cliente
            conn.execute(
                sa.text("INSERT INTO customers (id, name) VALUES (:id, :name)"),
                {"id": customer_id, "name": customer_name},
            )
            customer_map[customer_name] = customer_id

        # Atualizar os reviews com os novos customer_id
        conn.execute(
            sa.text(
                "UPDATE reviews SET customer_name = :customer_id WHERE id = :review_id"
            ),
            {"customer_id": customer_map[customer_name], "review_id": review_id},
        )

    # Agora podemos renomear a coluna e alterar seu tipo
    op.alter_column(
        "reviews",
        "customer_name",
        new_column_name="customer_id",
        existing_type=sa.String,
        type_=sa.UUID(as_uuid=True),
        existing_nullable=False,
        postgresql_using="customer_name::uuid",
    )

    # Criar a Foreign Key
    op.create_foreign_key(
        "fk_reviews_customers",
        "reviews",
        "customers",
        ["customer_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # Modificações adicionais na tabela reviews
    op.alter_column(
        "reviews",
        "classification",
        type_=classification_enum,
        existing_nullable=True,
        postgresql_using="classification::classification_enum",
    )
    op.drop_column("reviews", "classified")
    op.drop_column("reviews", "pos_score")
    op.drop_column("reviews", "neu_score")
    op.drop_column("reviews", "neg_score")
    op.add_column(
        "reviews",
        sa.Column(
            "sentiment_scores", sa.dialects.postgresql.JSONB, nullable=True, default={}
        ),
    )


def downgrade() -> None:
    op.drop_constraint("fk_reviews_customers", "reviews", type_="foreignkey")
    op.alter_column(
        "reviews",
        "customer_id",
        new_column_name="customer_name",
        existing_type=sa.UUID(as_uuid=True),
        type_=sa.String,
        existing_nullable=False,
    )

    op.alter_column(
        "reviews", "classification", type_=sa.String, existing_nullable=True
    )
    op.add_column(
        "reviews", sa.Column("classified", sa.Boolean, nullable=False, index=True)
    )
    op.add_column(
        "reviews", sa.Column("pos_score", sa.Float, nullable=True, default=0.0)
    )
    op.add_column(
        "reviews", sa.Column("neu_score", sa.Float, nullable=True, default=0.0)
    )
    op.add_column(
        "reviews", sa.Column("neg_score", sa.Float, nullable=True, default=0.0)
    )
    op.drop_column("reviews", "sentiment_scores")

    op.drop_table("customers")

    # Drop the enum type only if it exists
    bind = op.get_bind()
    result = bind.execute(
        "SELECT 1 FROM pg_type WHERE typname = 'classification_enum'"
    ).scalar()
    if result is not None:
        op.execute("DROP TYPE classification_enum")
