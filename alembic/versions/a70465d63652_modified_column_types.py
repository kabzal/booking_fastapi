"""modified column types

Revision ID: a70465d63652
Revises: da0ddb6465df
Create Date: 2024-07-02 21:11:43.653068

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a70465d63652'
down_revision: Union[str, None] = 'da0ddb6465df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('bookings', 'start_time',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('bookings', 'end_time',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('bookings', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('bookings', 'table_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('tables', 'table_type',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('tables', 'table_type',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('bookings', 'table_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('bookings', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('bookings', 'end_time',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('bookings', 'start_time',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    # ### end Alembic commands ###
