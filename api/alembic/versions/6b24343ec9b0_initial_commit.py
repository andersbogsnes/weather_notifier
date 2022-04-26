"""initial commit

Revision ID: 6b24343ec9b0
Revises: 
Create Date: 2022-04-26 22:01:25.705320

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b24343ec9b0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscriptions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subscription_uuid', sa.VARCHAR(length=36), nullable=True),
    sa.Column('country_code', sa.VARCHAR(length=2), nullable=True),
    sa.Column('city', sa.VARCHAR(length=100), nullable=True),
    sa.Column('email', sa.VARCHAR(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subscriptions_subscription_uuid'), 'subscriptions', ['subscription_uuid'], unique=True)
    op.create_table('conditions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subscription_id', sa.Integer(), nullable=True),
    sa.Column('condition_uuid', sa.VARCHAR(length=36), nullable=True),
    sa.Column('condition', sa.VARCHAR(length=25), nullable=True),
    sa.Column('op', sa.VARCHAR(length=3), nullable=True),
    sa.Column('threshold', sa.Numeric(precision=19, scale=4), nullable=True),
    sa.ForeignKeyConstraint(['subscription_id'], ['subscriptions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('conditions')
    op.drop_index(op.f('ix_subscriptions_subscription_uuid'), table_name='subscriptions')
    op.drop_table('subscriptions')
    # ### end Alembic commands ###