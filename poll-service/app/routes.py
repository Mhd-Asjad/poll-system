from flask import request, jsonify
from . import db, app
from bson.objectid import ObjectId
from bson.errors import InvalidId

polls_collection = db.polls

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Poll API!"})


@app.route('/polls', methods=['POST'])
def create_poll():
    data = request.get_json()

    if not data or 'question' not in data or 'options' not in data:
        return jsonify({"error": "Missing 'question' or 'options'"}), 400
    if not isinstance(data['options'], list) or len(data['options']) < 2:
        return jsonify({"error": "Options must be a list with at least 2 items"}), 400

    try:
        result = polls_collection.insert_one(data)
        
        # Return a success message with the new poll's ID
        return jsonify({
            "message": "Poll created successfully",
            "id": str(result.inserted_id)
        }), 201 # 201 means "Created"
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/polls/',methods=['GET'])
def get_all_polls():

    all_polls = []
    try:
        for poll in polls_collection.find():
            poll['_id'] = str(poll['_id'])  # Convert ObjectId to string
            all_polls.append(poll)
        return jsonify(all_polls), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/polls/<poll_id>', methods=['GET'])
def get_poll(poll_id):
    try:
        poll = polls_collection.find_one({"_id": ObjectId(poll_id)})
        if poll:
            poll['_id'] = str(poll['_id'])  # Convert ObjectId to string
            return jsonify(poll), 200
        else:
            return jsonify({"error": "Poll not found"}), 404
    except InvalidId:
        return jsonify({"error": "Invalid poll ID format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    