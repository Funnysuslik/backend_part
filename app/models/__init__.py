from sqlalchemy.ext.declarative import declarative_base

# Create the declarative Base
Base = declarative_base()

# Import all models to register them with Alembic
from app.models.user import User  # Import User model
from app.models.token import RefreshToken  # Import RefreshToken model
