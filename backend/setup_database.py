"""Script to set up the database tables."""
from app.models.base import Base, engine
from app.config import settings

def setup_database():
    """Create all database tables."""
    print("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        print(f"Database URL: {settings.database_url.split('@')[-1] if '@' in settings.database_url else 'configured'}")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        print("\nMake sure:")
        print("1. PostgreSQL is running")
        print("2. DATABASE_URL in .env is correct")
        print("3. Database exists and user has permissions")

if __name__ == "__main__":
    setup_database()

