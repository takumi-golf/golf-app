"""Update datetime fields

Revision ID: e028beded054
Revises: ebe82283b901
Create Date: 2025-05-06 06:05:23.893694

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e028beded054'
down_revision = 'ebe82283b901'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # PlayerProfileテーブルの作成
    op.create_table(
        'player_profiles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(), nullable=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('head_speed', sa.Float(), nullable=False),
        sa.Column('handicap', sa.Float(), nullable=False),
        sa.Column('age', sa.Integer(), nullable=False),
        sa.Column('gender', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)')),
        sa.PrimaryKeyConstraint('id')
    )

    # PlayerClubSetupテーブルの作成
    op.create_table(
        'player_club_setups',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('player_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)')),
        sa.ForeignKeyConstraint(['player_id'], ['player_profiles.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # PlayerClubテーブルの作成
    op.create_table(
        'player_clubs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('setup_id', sa.Integer(), nullable=False),
        sa.Column('specification_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)')),
        sa.ForeignKeyConstraint(['setup_id'], ['player_club_setups.id'], ),
        sa.ForeignKeyConstraint(['specification_id'], ['club_specifications.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # SQLiteではALTER TABLEが制限されているため、テーブルを再作成
    op.create_table(
        'recommendations_new',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('player_profile_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('segment', sa.String(), nullable=False),
        sa.Column('shaft_recommendation', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)')),
        sa.Column('feedback', sa.Text(), nullable=True),
        sa.Column('rating', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['player_profile_id'], ['player_profiles.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 既存のデータを新しいテーブルにコピー（必要なカラムのみ）
    op.execute('''
        INSERT INTO recommendations_new (
            id, user_id, segment, shaft_recommendation, created_at, updated_at, feedback, rating
        )
        SELECT 
            id, user_id, 'default', club_shaft, created_at, updated_at, club_description, NULL
        FROM recommendations
    ''')
    
    # 古いテーブルを削除
    op.drop_table('recommendations')
    
    # 新しいテーブルの名前を変更
    op.rename_table('recommendations_new', 'recommendations')


def downgrade() -> None:
    # ダウングレードは実装しない（データの損失を避けるため）
    pass 