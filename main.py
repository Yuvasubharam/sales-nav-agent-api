from flask import Flask, request, jsonify
from sales_nav_agent import run_agent

app = Flask(__name__)


@app.route('/')
def index():
    return "SalesNav Agent API Running"


@app.route('/process', methods=['POST'])
def process():
    data = request.json
    try:
        run_agent(company_name=data['company_name'],
                  website=data['website'],
                  phantom_key=data['phantom_key'],
                  phantom_id=data['phantom_id'],
                  sheet_id=data['sheet_id'],
                  creds_file=data['creds_file'])
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
