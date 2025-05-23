"""Initial migration

Revision ID: 688dc2f5951a
Revises: 
Create Date: 2025-05-17 23:57:07.171494

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '688dc2f5951a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('BoardMembers', 'board_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('BoardMembers', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('Boards', 'created_by_user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('Columns', 'board_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('TaskMembers', 'task_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('TaskMembers', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('Tasks', 'column_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Tasks', 'column_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('TaskMembers', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('TaskMembers', 'task_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('Columns', 'board_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('Boards', 'created_by_user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('BoardMembers', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('BoardMembers', 'board_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
