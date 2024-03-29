"""initial migration

Revision ID: 8feb1670ee7f
Revises: 
Create Date: 2022-07-11 14:24:57.339503

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8feb1670ee7f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('slug', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_roles')),
    sa.UniqueConstraint('name', name=op.f('uq_roles_name')),
    sa.UniqueConstraint('slug', name=op.f('uq_roles_slug'))
    )
    op.create_table('image_labels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('images_id', sa.Integer(), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['images_id'], ['images.id'], name=op.f('fk_image_labels_images_id_images')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_image_labels'))
    )
    op.create_table('rate_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.Column('first_name', sa.String(length=64), nullable=True),
    sa.Column('last_name', sa.String(length=64), nullable=True),
    sa.Column('organization', sa.String(length=64), nullable=True),
    sa.Column('change_code_hash', sa.String(length=128), nullable=True),
    sa.Column('change_code_time', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name=op.f('fk_users_role_id_roles')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('image_labels')
    op.drop_table('roles')
    # ### end Alembic commands ###
