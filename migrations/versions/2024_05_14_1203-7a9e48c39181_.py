"""empty message

Revision ID: 7a9e48c39181
Revises: 23b6b013a3b3
Create Date: 2024-05-14 12:03:54.868917

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from fastapi_users_db_sqlalchemy.generics import TIMESTAMPAware


# revision identifiers, used by Alembic.
revision: str = "7a9e48c39181"
down_revision: Union[str, None] = "23b6b013a3b3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "refresh_token",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("token", sa.String(length=1024), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("created_at", TIMESTAMPAware(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="cascade"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token"),
    )
    op.create_index(
        op.f("ix_refresh_token_created_at"),
        "refresh_token",
        ["created_at"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_refresh_token_created_at"), table_name="refresh_token")
    op.drop_table("refresh_token")
    # ### end Alembic commands ###
