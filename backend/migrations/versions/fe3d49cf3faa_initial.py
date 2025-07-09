"""initial

Revision ID: fe3d49cf3faa
Revises: 
Create Date: 2025-06-16 14:56:08.123456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe3d49cf3faa'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create core tables
    op.create_table(
        'tenants',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String(100), unique=True, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, onupdate=sa.func.now())
    )
    
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String(50), unique=True, nullable=False),
        sa.Column('permissions', sa.Text)
    )
    
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('tenant_id', sa.Integer, sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('role_id', sa.Integer, sa.ForeignKey('roles.id'), nullable=False),
        sa.Column('username', sa.String(50), unique=True, nullable=False),
        sa.Column('email', sa.String(100), unique=True, nullable=False),
        sa.Column('hashed_password', sa.String(100), nullable=False),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, onupdate=sa.func.now())
    )
    
    # Create CRM tables
    op.create_table(
        'crm_customers',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('tenant_id', sa.Integer, sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('email', sa.String(100)),
        sa.Column('phone', sa.String(20)),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, onupdate=sa.func.now())
    )
    
    # Create Inventory tables
    op.create_table(
        'inventory_products',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('tenant_id', sa.Integer, sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('price', sa.Float, nullable=False),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, onupdate=sa.func.now())
    )
    
    op.create_table(
        'inventory_suppliers',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('tenant_id', sa.Integer, sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('contact_info', sa.Text),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, onupdate=sa.func.now())
    )
    
    # Create Accounting tables
    op.create_table(
        'accounting_accounts',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('tenant_id', sa.Integer, sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('balance', sa.Float, default=0.0),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, onupdate=sa.func.now())
    )
    
    op.create_table(
        'accounting_journal_entries',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('tenant_id', sa.Integer, sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('date', sa.DateTime, nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, onupdate=sa.func.now())
    )
    
    op.create_table(
        'accounting_transactions',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('journal_entry_id', sa.Integer, sa.ForeignKey('accounting_journal_entries.id'), nullable=False),
        sa.Column('account_id', sa.Integer, sa.ForeignKey('accounting_accounts.id'), nullable=False),
        sa.Column('amount', sa.Float, nullable=False),
        sa.Column('type', sa.String(10), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, onupdate=sa.func.now())
    )

def downgrade():
    op.drop_table('accounting_transactions')
    op.drop_table('accounting_journal_entries')
    op.drop_table('accounting_accounts')
    op.drop_table('inventory_suppliers')
    op.drop_table('inventory_products')
    op.drop_table('crm_customers')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('tenants')
