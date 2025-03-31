from flask import Flask, request, jsonify, send_from_directory, render_template, url_for
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Change static_folder to point to the build directory
app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# Get MongoDB URI from environment variable
MONGODB_URI = os.getenv('MONGODB_URI')

try:
    client = MongoClient(MONGODB_URI)
    print("✅ MongoDB Connection Successful!")
    db = client.kirana_suvidha
    shopping_lists = db.shopping_lists
except Exception as e:
    print("❌ MongoDB Connection Error:", str(e))

# Serve React app - root route
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    try:
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')
    except Exception as e:
        print(f"Error serving static files: {e}")
        return "Not Found", 404

# API endpoint for saving shopping lists
@app.route('/api', methods=['POST'])
def save_shopping_list():
    try:
        data = request.json
        print("📥 Received data at /api:", data)  # Log the incoming data
        
        # Handle both single object and array of items
        items = data if isinstance(data, list) else [data]
        
        # Add created_at to each item
        for item in items:
            item['created_at'] = datetime.utcnow()
            result = shopping_lists.insert_one(item)
            print("✅ Saved to MongoDB with ID:", result.inserted_id)  # Log the MongoDB insertion result

        return jsonify({
            'success': True,
            'message': f'Successfully saved {len(items)} items'
        }), 201
    except Exception as e:
        print("❌ Error while processing /api request:", str(e))  # Log any errors
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'message': 'Hello Abhishek! The Flask server is running.',
        'status': 'success'
    }), 200

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    print("🚀 Server starting on http://localhost:" + str(port))
    app.run(host='0.0.0.0', port=port, debug=False)