from logging.config import fileConfig
import asyncio
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine
from alembic import context
from app.db.connection import engine  # Import your async engine from the app
from app.models import Base  # Import your models
import sys
import os


# Add the `/app` directory to sys.path to allow imports of the app module
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# Interpret the config file for Python logging.
config = context.config
fileConfig(config.config_file_name)

# Set the target metadata for Alembic (the models' metadata).
target_metadata = Base.metadata

# Function to run migrations online (with async engine)
def run_migrations_online():
    connectable = engine  # Use the async engine here

    async def do_run_migrations():
        async with connectable.connect() as connection:
            await connection.run_sync(run_migrations)

    asyncio.run(do_run_migrations())

# Function to actually run the migrations
def run_migrations(connection: Connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,  # To include type changes in migrations
        version_table="alembic_version",
        process_revision_directives=None,
    )
    with context.begin_transaction():
        context.run_migrations()

# Call the async migration function
run_migrations_online()
