from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Validate
    if 'amount' not in data or 'merchant' not in data:
        return jsonify({"error": "Missing 'amount' or 'merchant'"}), 400
    try:
        amount = float(data['amount'])
        merchant = data['merchant'].strip()
    except:
        return jsonify({"error": "Invalid data type"}), 400
    # Risk logic
    risk_score = 0
    if amount > 1000:
        risk_score += 30
    if merchant == "Midnight Mart":
        risk_score += 20
    is_fraud = risk_score >= 30
    level = "High" if risk_score >= 50 else "Medium" if risk_score >= 30 else "Low"
    return jsonify({
        "is_fraud": is_fraud,
        "risk_level": level,
        "risk_score": risk_score,
        "msg": "Rules-based fraud check — no ML needed."
})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
