"""Initial Ceroc DB Create

Revision ID: e946911e2b4a
Revises: 
Create Date: 2019-03-26 18:43:01.899338

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e946911e2b4a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event_type',
    sa.Column('event_type_id', sa.Integer(), nullable=False),
    sa.Column('event_type_name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('event_type_id')
    )
    op.create_index(op.f('ix_event_type_event_type_name'), 'event_type', ['event_type_name'], unique=False)
    op.create_table('person',
    sa.Column('person_id', sa.Integer(), nullable=False),
    sa.Column('firstname', sa.String(length=64), nullable=False),
    sa.Column('lastname', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('mobile', sa.String(length=12), nullable=True),
    sa.Column('ismember', sa.Boolean(), nullable=True),
    sa.Column('gender', sa.String(length=6), nullable=True),
    sa.Column('address1', sa.String(length=100), nullable=True),
    sa.Column('address2', sa.String(length=100), nullable=True),
    sa.Column('suburb', sa.String(length=50), nullable=True),
    sa.Column('postcode', sa.String(length=6), nullable=True),
    sa.Column('accept_newsletter', sa.Boolean(), nullable=True),
    sa.Column('accept_social_media', sa.Boolean(), nullable=True),
    sa.Column('signed_disclaimer', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('person_id')
    )
    op.create_index(op.f('ix_person_email'), 'person', ['email'], unique=True)
    op.create_index(op.f('ix_person_firstname'), 'person', ['firstname'], unique=False)
    op.create_index(op.f('ix_person_lastname'), 'person', ['lastname'], unique=False)
    op.create_table('sales_type',
    sa.Column('sales_type_id', sa.Integer(), nullable=False),
    sa.Column('sale_name', sa.String(length=64), nullable=False),
    sa.Column('member_only', sa.Boolean(), nullable=True),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.Column('default_price', sa.Integer(), nullable=True),
    sa.Column('payment_type', sa.String(length=10), nullable=True),
    sa.Column('is_a_default', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('sales_type_id')
    )
    op.create_index(op.f('ix_sales_type_sale_name'), 'sales_type', ['sale_name'], unique=False)
    op.create_table('event',
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('event_name', sa.String(length=64), nullable=False),
    sa.Column('event_date', sa.Date(), nullable=True),
    sa.Column('event_type', sa.Integer(), nullable=True),
    sa.Column('min_num', sa.Integer(), nullable=True),
    sa.Column('max_num', sa.Integer(), nullable=True),
    sa.Column('booking_required', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['event_type'], ['event_type.event_type_id'], ),
    sa.PrimaryKeyConstraint('event_id')
    )
    op.create_index(op.f('ix_event_event_name'), 'event', ['event_name'], unique=False)
    op.create_table('attendance',
    sa.Column('attendance_id', sa.Integer(), nullable=False),
    sa.Column('fk_person_id', sa.Integer(), nullable=True),
    sa.Column('fk_event_id', sa.Integer(), nullable=True),
    sa.Column('fk_sales_type_id', sa.Integer(), nullable=True),
    sa.Column('payment_type', sa.String(length=10), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['fk_event_id'], ['event.event_id'], ),
    sa.ForeignKeyConstraint(['fk_person_id'], ['person.person_id'], ),
    sa.ForeignKeyConstraint(['fk_sales_type_id'], ['sales_type.sales_type_id'], ),
    sa.PrimaryKeyConstraint('attendance_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('attendance')
    op.drop_index(op.f('ix_event_event_name'), table_name='event')
    op.drop_table('event')
    op.drop_index(op.f('ix_sales_type_sale_name'), table_name='sales_type')
    op.drop_table('sales_type')
    op.drop_index(op.f('ix_person_lastname'), table_name='person')
    op.drop_index(op.f('ix_person_firstname'), table_name='person')
    op.drop_index(op.f('ix_person_email'), table_name='person')
    op.drop_table('person')
    op.drop_index(op.f('ix_event_type_event_type_name'), table_name='event_type')
    op.drop_table('event_type')
    # ### end Alembic commands ###
