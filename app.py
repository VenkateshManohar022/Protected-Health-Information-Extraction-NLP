from flask import Flask, request, jsonify
from deid_service import PHIDeidentifier

app = Flask(__name__)
deidentifier = PHIDeidentifier()

@app.route("/deid", methods=["POST"])
def deid_report():
    """API endpoint to de-identify a medical report."""
    try:
        data = request.get_json()
        if not data or "report_text" not in data:
            return jsonify({"error": "Invalid request body. 'report_text' field is required."}), 400
        
        report_text = data.get("report_text", "")
        deid_report, deid_entities = deidentifier.deidentify(report_text)
        
        return jsonify({
            "deid_report": deid_report,
            "deid_entities": deid_entities
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5003, debug=True)