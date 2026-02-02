import pytest
import os
from app import create_app
from app.extensions import db
from app.models import Message

@pytest.fixture
def app():
    """Create and configure a test app instance"""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "TEST_DATABASE_URL", 
        "mysql+pymysql://flask_user:flask_password@db:3306/flask_test_db"
    )
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create a test client"""
    return app.test_client()

def test_index(client):
    """Test the index route"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.data.decode() == "DevOps TASK"

def test_add_message_get(client, app):
    """Test adding a message via GET request"""
    response = client.get("/add")
    assert response.status_code == 201
    
    data = response.get_json()
    assert data["message"] == "Message Added"
    assert "id" in data
    
    # Verify message was actually saved to database
    with app.app_context():
        message = db.session.get(Message, data["id"])
        assert message is not None
        assert message.text == "Hello CI/CD"

def test_add_message_post(client, app):
    """Test adding a message via POST request with custom text"""
    response = client.post(
        "/add",
        json={"text": "Custom test message"}
    )
    assert response.status_code == 201
    
    data = response.get_json()
    assert data["message"] == "Message Added"
    
    # Verify custom message was saved
    with app.app_context():
        message = db.session.get(Message, data["id"])
        assert message is not None
        assert message.text == "Custom test message"

def test_list_messages(client, app):
    """Test listing all messages"""
    # Add some messages first
    with app.app_context():
        msg1 = Message(text="Test 1")
        msg2 = Message(text="Test 2")
        db.session.add(msg1)
        db.session.add(msg2)
        db.session.commit()
    
    response = client.get("/messages")
    assert response.status_code == 200
    
    data = response.get_json()
    assert data["count"] == 2
    assert len(data["messages"]) == 2

def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.get_json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"

