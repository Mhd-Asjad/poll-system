import os
from pymongo import MongoClient
from dotenv import load_dotenv

def get_db():
    """
    Connects to the MongoDB database using the URI
    from the .env file.
    """
    # Load environment variables from .env file
    load_dotenv()
    
    MONGO_URI = os.environ.get('MONGO_URI')

    print(MONGO_URI)

    if not MONGO_URI:
        raise ValueError("No MONGO_URI found. Make sure to set it in your .env file.")

    # Create the client
    client = MongoClient(MONGO_URI)
    
    # Get the database name from the URI and return the db object
    # This is a clean way to get the 'poll_db' database.
    db = client.get_default_database()
    
    print("✅ Database connected!")
    return db