from flask import Blueprint, jsonify, request
from .models import Message
from .extensions import db

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return "DevOps TASK"

@main.route("/add", methods=["GET", "POST"])
def add_message():
    """Add a new message to the database"""
    try:
        # Support both GET (for simple testing) and POST (for proper API)
        if request.method == "POST":
            data = request.get_json() or {}
            text = data.get("text", "Hello CI/CD")
        else:
            text = request.args.get("text", "Hello CI/CD")
        
        msg = Message(text=text)
        db.session.add(msg)
        db.session.commit()
        return jsonify({"message": "Message Added", "id": msg.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@main.route("/messages")
def list_messages():
    """List all messages"""
    try:
        messages = Message.query.all()
        return jsonify({
            "messages": [msg.to_dict() for msg in messages],
            "count": len(messages)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/health")
def health_check():
    """Health check endpoint for CI/CD"""
    try:
        # Test database connection
        db.session.execute(db.text('SELECT 1'))
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 503

