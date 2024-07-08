"""added columns to User

Revision ID: 80c8a5017a46
Revises: a70465d63652
Create Date: 2024-07-03 15:16:27.767518

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80c8a5017a46'
down_revision: Union[str, None] = 'a70465d63652'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('disabled', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'disabled')
    op.drop_column('users', 'is_admin')
    # ### end Alembic commands ###
