from app import app

# Create the app instance using our factory

if __name__ == '__main__':
    # Run the app. We use port 5001 for the poll-service.
    app.run(host='0.0.0.0', debug=True, port=5002)