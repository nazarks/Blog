"""add article model

Revision ID: 12e6bfeba482
Revises: 8fd13153c234
Create Date: 2023-01-17 23:37:23.835911

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "12e6bfeba482"
down_revision = "8fd13153c234"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "article",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(length=200), server_default="", nullable=False),
        sa.Column("body", sa.Text(), server_default="", nullable=False),
        sa.Column("dt_created", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=True),
        sa.Column("dt_updated", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["author_id"], ["author.id"], name=op.f("fk_article_author_id_author")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_article")),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("article")
    # ### end Alembic commands ###
