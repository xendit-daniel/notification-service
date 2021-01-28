"""empty message

Revision ID: 007b329e2b5f
Revises: 059880671a9b
Create Date: 2021-01-28 01:50:38.733163

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from app.main.model.notification import Notification


# revision identifiers, used by Alembic.
revision = '007b329e2b5f'
down_revision = '059880671a9b'
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
