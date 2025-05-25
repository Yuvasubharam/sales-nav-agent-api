import os
from flask import Flask, request, jsonify
from sales_nav_agent import run_agent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

REQUIRED_FIELDS = [
    'company_name',
    'website',
    'phantom_key',
    'phantom_id',
    'sheet_id',
    'creds_file'
]

@app.route('/')
def index():
    return "SalesNav Agent API Running"

@app.route('/process', methods=['POST'])
def process():
    if not request.is_json:
        return jsonify({
            "status": "error",
            "message": "Request must be JSON"
        }), 400

    data = request.json

    # Validate required fields
    missing_fields = [field for field in REQUIRED_FIELDS if not data.get(field)]
    if missing_fields:
        return jsonify({
            "status": "error",
            "message": f"Missing required fields: {', '.join(missing_fields)}"
        }), 400

    try:
        # Use environment variables as the fallback
        run_agent(
            company_name=data['company_name'],
            website=data['website'],
            phantom_key=data.get('phantom_key') or os.getenv('PHANTOMBUSTER_API_KEY'),
            phantom_id=data.get('phantom_id') or os.getenv('PHANTOMBUSTER_AGENT_ID'),
            sheet_id=data.get('sheet_id') or os.getenv('GOOGLE_SHEET_ID'),
            creds_file=data.get('creds_file') or os.getenv('GOOGLE_CREDENTIALS_PATH')
        )
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "type": type(e).__name__
        }), 500
