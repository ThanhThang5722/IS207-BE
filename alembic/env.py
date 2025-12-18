import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from app.models.base import Base  # Chỉ import metadata, không engine async

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

# env.py
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.models.base import Base
import os

target_metadata = Base.metadata

def get_sync_database_url():
    url = os.getenv("DATABASE_URL")
    if url.startswith("postgresql+asyncpg://"):
        url = url.replace("postgresql+asyncpg://", "postgresql+psycopg2://")
    return url

configuration = context.config.get_section(config.config_ini_section)
configuration["sqlalchemy.url"] = get_sync_database_url()

connectable = engine_from_config(configuration, prefix="sqlalchemy.", poolclass=pool.NullPool)

with connectable.connect() as connection:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_offline():
    url = get_sync_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_sync_database_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
