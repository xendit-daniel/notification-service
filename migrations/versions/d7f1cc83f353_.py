"""empty message

Revision ID: d7f1cc83f353
Revises: fefca8113d96
Create Date: 2021-01-28 01:13:18.687739

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from app.main.model.notification import Notification


# revision identifiers, used by Alembic.
revision = 'd7f1cc83f353'
down_revision = 'fefca8113d96'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notification', sa.Column('delivery_status', sqlalchemy_utils.types.choice.ChoiceType(Notification.DELIVERY_STATUS_TYPES), nullable=True))
    op.execute("UPDATE notification SET delivery_status = {}".format(Notification.IN_PROGRESS))
    op.alter_column('notification', 'delivery_status', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('notification', 'delivery_status')
    # ### end Alembic commands ###
