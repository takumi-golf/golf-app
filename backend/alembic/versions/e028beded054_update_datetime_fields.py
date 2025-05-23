"""Update datetime fields

Revision ID: e028beded054
Revises: ebe82283b901
Create Date: 2025-05-02 11:25:45.679106

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e028beded054'
down_revision = 'ebe82283b901'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('recommendations', 'club_description',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=True)
    op.alter_column('recommendations', 'created_at',
               existing_type=sa.DATETIME(),
               nullable=False,
               existing_server_default=sa.text('(CURRENT_TIMESTAMP)'))
    op.alter_column('recommendations', 'updated_at',
               existing_type=sa.DATETIME(),
               nullable=False)
    op.alter_column('users', 'is_active',
               existing_type=sa.INTEGER(),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.alter_column('users', 'created_at',
               existing_type=sa.DATETIME(),
               nullable=False,
               existing_server_default=sa.text('(CURRENT_TIMESTAMP)'))
    op.alter_column('users', 'updated_at',
               existing_type=sa.DATETIME(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'updated_at',
               existing_type=sa.DATETIME(),
               nullable=True)
    op.alter_column('users', 'created_at',
               existing_type=sa.DATETIME(),
               nullable=True,
               existing_server_default=sa.text('(CURRENT_TIMESTAMP)'))
    op.alter_column('users', 'is_active',
               existing_type=sa.Boolean(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.alter_column('recommendations', 'updated_at',
               existing_type=sa.DATETIME(),
               nullable=True)
    op.alter_column('recommendations', 'created_at',
               existing_type=sa.DATETIME(),
               nullable=True,
               existing_server_default=sa.text('(CURRENT_TIMESTAMP)'))
    op.alter_column('recommendations', 'club_description',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=True)
    # ### end Alembic commands ### 