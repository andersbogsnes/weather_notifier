"""initial commit

Revision ID: 64e113ab3dbb
Revises:
Create Date: 2022-04-28 00:02:23.248983

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "64e113ab3dbb"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "subscriptions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("subscription_uuid", sa.VARCHAR(length=36), nullable=True),
        sa.Column("country_code", sa.VARCHAR(length=2), nullable=True),
        sa.Column("city", sa.VARCHAR(length=100), nullable=True),
        sa.Column("email", sa.VARCHAR(length=250), nullable=True),
        sa.Column("conditions", sa.JSON()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_subscriptions_subscription_uuid"),
        "subscriptions",
        ["subscription_uuid"],
        unique=True,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_subscriptions_subscription_uuid"), table_name="subscriptions"
    )
    op.drop_table("subscriptions")
    # ### end Alembic commands ###
