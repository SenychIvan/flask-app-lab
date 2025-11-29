"""Add user_id to posts

Revision ID: 602d5fbe095c
Revises: 94646825e316
Create Date: 2025-11-29 19:42:25.531072

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '602d5fbe095c'
down_revision = '94646825e316'
branch_labels = None
depends_on = None


def upgrade():

    # === 1. TIMESHIFT: спочатку додаємо user_id nullable=True ===
    with op.batch_alter_table('post') as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.drop_column('author')

    # === 2. Створюємо foreign key ===
    with op.batch_alter_table('post') as batch_op:
        batch_op.create_foreign_key(
            batch_op.f('fk_post_user_id_users'),
            'users', ['user_id'], ['id']
        )

    # === 3. Заповнюємо старі записи (ALL posts -> user_id = 1) ===
    op.execute("UPDATE post SET user_id = 1")

    # === 4. Робимо user_id NOT NULL ===
    with op.batch_alter_table('post') as batch_op:
        batch_op.alter_column('user_id', nullable=False)

    # === 5. Оновлення таблиці users ===
    with op.batch_alter_table('users') as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=50), nullable=False))
        batch_op.add_column(sa.Column('email', sa.String(length=100), nullable=False))

        batch_op.drop_constraint(batch_op.f('uq_users_login'), type_='unique')

        batch_op.create_unique_constraint(batch_op.f('uq_users_email'), ['email'])
        batch_op.create_unique_constraint(batch_op.f('uq_users_username'), ['username'])

        batch_op.drop_column('login')
        batch_op.drop_column('password')
        batch_op.drop_column('registered')


def downgrade():

    # === Відкат users ===
    with op.batch_alter_table('users') as batch_op:
        batch_op.add_column(sa.Column('registered', sa.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column('password', sa.VARCHAR(length=200), nullable=False))
        batch_op.add_column(sa.Column('login', sa.VARCHAR(length=50), nullable=False))

        batch_op.drop_constraint(batch_op.f('uq_users_username'), type_='unique')
        batch_op.drop_constraint(batch_op.f('uq_users_email'), type_='unique')
        batch_op.create_unique_constraint(batch_op.f('uq_users_login'), ['login'])

        batch_op.drop_column('email')
        batch_op.drop_column('username')

    # === Відкат post ===
    with op.batch_alter_table('post') as batch_op:
        batch_op.add_column(sa.Column('author', sa.VARCHAR(length=20), nullable=True))
        batch_op.drop_constraint(batch_op.f('fk_post_user_id_users'), type_='foreignkey')
        batch_op.drop_column('user_id')
