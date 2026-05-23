import os
from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

#Load the model at startup
model = joblib.load('fraud_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    #Validate
    if 'amount' not in data or 'merchant' not in data:
      return jsonify({"error": "Missing fields"}), 400

    amount = float(data['amount'])
    merchant = data['merchant']

    #Calculate risk score(same logic)
    risk = 0
    if amount > 1000:
      risk += 30
    if merchant == 'Midnight Mart':
      risk += 20

    # Predict using saved model
    pred = model.predict([[amount,risk]])[0]
    prob = model.predict_proba([[amount,risk]])[0][1]

    return jsonify ({
        "is_fraud": bool(pred),
        "risk_score": risk,
        "confidence": float(prob)
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    app.run(host='0.0.0.0',port=port)
