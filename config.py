import os

class Config:
    """Base configuration"""
    # MySQL connection format: mysql+pymysql://username:password@host:port/database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", 
        "mysql+pymysql://flask_user:flask_password@10.19.143.72:3306/flask_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

class TestConfig(Config):
    """Testing configuration"""
    TESTING = True
    # Use SQLite for testing (faster and no MySQL dependency needed)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "TEST_DATABASE_URL", 
        "mysql+pymysql://flask_user:flask_password@10.19.143.72:3306/flask_test_db"
    )
class ProductionConfig(Config):
    """Production configuration"""
    # In production, ensure DATABASE_URL and SECRET_KEY are set via environment variables
    pass

