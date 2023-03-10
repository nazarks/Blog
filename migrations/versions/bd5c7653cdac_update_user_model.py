"""update user model

Revision ID: bd5c7653cdac
Revises: 2e27000bec39
Create Date: 2023-01-13 22:37:53.043670

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "bd5c7653cdac"
down_revision = "2e27000bec39"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.add_column(sa.Column("first_name", sa.String(length=120), server_default="", nullable=False))
        batch_op.add_column(sa.Column("last_name", sa.String(length=120), server_default="", nullable=False))
        batch_op.create_unique_constraint(batch_op.f("uq_user_username"), ["username"])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f("uq_user_username"), type_="unique")
        batch_op.drop_column("last_name")
        batch_op.drop_column("first_name")

    # ### end Alembic commands ###
