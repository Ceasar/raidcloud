"""id chunksasdasdwd

Revision ID: 528af8c89a4d
Revises: 16a3478ee1f6
Create Date: 2012-07-22 10:10:58.879439

"""

# revision identifiers, used by Alembic.
revision = '528af8c89a4d'
down_revision = '16a3478ee1f6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.execute('alter table chunk alter column drive_id type varchar(255)')
    pass
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###