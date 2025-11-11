from flask import render_template, request, flash, redirect, url_for
from app import app
import requests
import os

POLL_SERVICE_URL = os.getenv('POLL_SERVICE_URL', 'http://localhost:5001')
VOTE_SERVICE_URL = os.getenv('VOTE_SERVICE_URL', 'http://localhost:5002')

@app.route('/')
def index():
    try:
        # Fetch all polls from the poll service
        print(f"Attempting to connect to poll service at: {POLL_SERVICE_URL}/polls")
        response = requests.get(f"{POLL_SERVICE_URL}/polls")
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.text}")
        polls = response.json()
        return render_template('index.html', polls=polls)
    except requests.RequestException as e:
        print(f"Error connecting to poll service: {str(e)}")
        flash(f"Error fetching polls: {str(e)}", "error")
        return render_template('index.html', polls=[])

@app.route('/create_poll', methods=['GET', 'POST'])
def create_poll():
    if request.method == 'POST':
        try:
            poll_data = {
                "question": request.form['question'],
                "options": request.form.getlist('options')
            }
            response = requests.post(f"{POLL_SERVICE_URL}/polls", json=poll_data)
            if response.status_code == 201:
                flash("Poll created successfully!", "success")
                return redirect(url_for('index'))
            else:
                # Try to get the error from the backend
                try:
                    error_msg = response.json().get('error', 'Unknown error')
                except requests.exceptions.JSONDecodeError:
                    error_msg = response.text
                flash(f"Error creating poll: {error_msg}", "error")
        except requests.RequestException as e:
            flash(f"Error creating poll: {str(e)}", "error")
    
    return render_template('create_poll.html')

@app.route('/poll/<poll_id>')
def view_poll(poll_id):
    try:
        # Fetch poll details
        poll_response = requests.get(f"{POLL_SERVICE_URL}/polls/{poll_id}")
        poll = poll_response.json()
        
        # Fetch vote counts
        vote_response = requests.get(f"{VOTE_SERVICE_URL}/polls/{poll_id}/votes")
        votes = vote_response.json() if vote_response.status_code == 200 else {"options": {}}
        print(votes,'<--- votes')
        return render_template('view_poll.html', poll=poll, votes=votes)
    except requests.RequestException as e:
        flash(f"Error fetching poll details: {str(e)}", "error")
        return redirect(url_for('index'))

@app.route('/poll/<poll_id>/vote', methods=['POST'])
def vote(poll_id):
    try:
        option = request.form.get('option')
        if not option:
            flash("Please select an option", "error")
            return redirect(url_for('view_poll', poll_id=poll_id))

        response = requests.post(f"{VOTE_SERVICE_URL}/polls/{poll_id}/vote", 
                               json={"option": option})
        
        if response.status_code == 200:
            flash("Vote recorded successfully!", "success")
        else:
            flash("Error recording vote", "error")
            
    except requests.RequestException as e:
        flash(f"Error recording vote: {str(e)}", "error")
    
    return redirect(url_for('view_poll', poll_id=poll_id))