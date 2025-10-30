from flask import Flask, jsonify
from data_handler import load_questions
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

@app.route('/get-questions', methods=['GET'])
def get_questions():
    questions = load_questions()  # Fetch from the Excel file
    return jsonify(questions)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Run on all IPs to allow local network access
