"""add_invite_fields_to_user

Revision ID: 202506181357
Revises: fe3d49cf3faa
Create Date: 2025-06-18 13:57:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '202506181357'
down_revision = 'fe3d49cf3faa'
branch_labels = None
depends_on = None

def upgrade():
    # Add invitation_status enum
    invitation_status = postgresql.ENUM(
        'PENDING', 'ACCEPTED', 'EXPIRED', 
        name='invitationstatus'
    )
    invitation_status.create(op.get_bind())
    
    # Add new columns
    op.add_column('users', sa.Column(
        'invited_by', 
        sa.Integer(), 
        sa.ForeignKey('users.id'),
        nullable=True
    ))
    op.add_column('users', sa.Column(
        'invitation_status', 
        invitation_status,
        server_default='PENDING',
        nullable=False
    ))
    op.add_column('users', sa.Column(
        'invitation_token', 
        sa.String(100),
        nullable=True
    ))
    op.add_column('users', sa.Column(
        'invitation_sent_at', 
        sa.DateTime(),
        nullable=True
    ))

def downgrade():
    # Remove columns
    op.drop_column('users', 'invited_by')
    op.drop_column('users', 'invitation_status')
    op.drop_column('users', 'invitation_token')
    op.drop_column('users', 'invitation_sent_at')
    
    # Remove enum
    invitation_status = postgresql.ENUM(
        name='invitationstatus'
    )
    invitation_status.drop(op.get_bind())