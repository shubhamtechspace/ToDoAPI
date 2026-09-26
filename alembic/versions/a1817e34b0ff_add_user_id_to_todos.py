"""add user_id to todos

Revision ID: a1817e34b0ff
Revises: b396b5d1eea7
Create Date: 2026-09-26 17:18:19.439064

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1817e34b0ff'
down_revision: Union[str, Sequence[str], None] = 'b396b5d1eea7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        'todos',
        sa.Column('user_id', sa.Integer(), nullable=False)
    )

    op.create_foreign_key(
        'fk_todos_user_id_users',
        'todos',
        'users',
        ['user_id'],
        ['id']
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        'fk_todos_user_id_users',
        'todos',
        type_='foreignkey'
    )

    op.drop_column('todos', 'user_id')
