from flask import request, jsonify
from . import db, app
from bson.objectid import ObjectId
from bson.errors import InvalidId
from pymongo import ReturnDocument



votes = db.votes
polls_collection = db.polls

@app.route('/polls/<poll_id>/vote', methods=['POST'])
def cast_vote(poll_id):
    data = request.get_json()

    print(data)

    if not data or 'option' not in data:
        return jsonify({"error": "Missing 'poll_id' or 'option'"}), 400
    
    
    try:
        oid = ObjectId(poll_id)
    except InvalidId:
        return jsonify({"error": "Invalid poll_id"}), 400

    option = data['option']

    poll = polls_collection.find_one({"_id": oid})
    if not poll:
        return jsonify({"error": "Poll not found"}), 404

    # Expecting poll document to have an 'options' subdocument mapping option names to counts
    if 'options' not in poll or option not in poll['options']:
        return jsonify({"error": f"Option '{option}' not found in poll"}), 400


    # Initialize the document with the option if it doesn't exist
    updated = votes.find_one_and_update(
        {"poll_id": oid},
        {"$inc": {f"options.{option}": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    print(updated,'<--- updated')
    # Handle the case where options might not exist in the document
    if 'options' not in updated:
        updated['options'] = {option: 1}
    new_count = updated['options'].get(option, 0)
    return jsonify({"poll_id": str(oid), "option": option, "votes": new_count}), 200


@app.route('/polls/<poll_id>/votes', methods=['GET'])
def get_votes(poll_id):
    """Return vote counts for a poll.

    Response format:
      {"poll_id": "<id>", "options": {"option1": count, ...}}
    Returns 404 if the poll itself does not exist.
    """
    try:
        oid = ObjectId(poll_id)
    except InvalidId:
        return jsonify({"error": "Invalid poll_id"}), 400

    poll = polls_collection.find_one({"_id": oid})
    if not poll:
        return jsonify({"error": "Poll not found"}), 404

    vote_doc = votes.find_one({"poll_id": oid})
    if not vote_doc:
        return jsonify({"poll_id": str(oid), "options": {}}), 200

    options = vote_doc.get('options', {}) or {}
    # ensure keys are strings (in case of unusual types)
    options = {str(k): int(v) for k, v in options.items()}
    return jsonify({"poll_id": str(oid), "options": options}), 200

