from flask import Flask
from .db import get_db

# Create the app and db objects at the module level
app = Flask(__name__)
db = get_db()

@app.route('/health')
def health_check():
    return {"status": "ok"}, 200

# Import routes *after* app and db are defined
# This is crucial to avoid circular imports
from . import routes