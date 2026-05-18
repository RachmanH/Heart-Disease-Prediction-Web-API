from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import os

# Membuat aplikasi Flask
app = Flask(__name__)
CORS(app)

# Menentukan lokasi file model pipeline
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "model", "heart_model.pkl")

# Nama kolom sesuai urutan training (13 fitur, tanpa target)
FEATURE_COLS = [
    "age", "sex", "cp", "trestbps", "chol", "fbs",
    "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"
]

# Memuat model pipeline (preprocessor + classifier)
pipeline = joblib.load(MODEL_PATH)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "success",
        "message": "API Prediksi Penyakit Jantung berjalan",
        "endpoint": "/predict",
        "method": "POST"
    })


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Mengambil data JSON dari request
        data = request.get_json()

        # Validasi field wajib
        for field in FEATURE_COLS:
            if field not in data:
                return jsonify({
                    "status": "error",
                    "message": f"Field '{field}' wajib diisi"
                }), 400

        # Mengubah input JSON menjadi DataFrame
        input_data = pd.DataFrame([[
            float(data["age"]),
            float(data["sex"]),
            float(data["cp"]),
            float(data["trestbps"]),
            float(data["chol"]),
            float(data["fbs"]),
            float(data["restecg"]),
            float(data["thalach"]),
            float(data["exang"]),
            float(data["oldpeak"]),
            float(data["slope"]),
            float(data["ca"]),
            float(data["thal"])
        ]], columns=FEATURE_COLS)

        # Prediksi langsung dari pipeline (auto preprocess + predict)
        prediction = pipeline.predict(input_data)[0]
        probability = pipeline.predict_proba(input_data)[0][1]

        # Interpretasi hasil prediksi
        if prediction == 1:
            result = "Berisiko Penyakit Jantung"
        else:
            result = "Tidak Berisiko Penyakit Jantung"

        # Tingkat risiko berdasarkan probabilitas
        if probability >= 0.70:
            risk_level = "Tinggi"
        elif probability >= 0.40:
            risk_level = "Sedang"
        else:
            risk_level = "Rendah"

        # Response ke aplikasi web
        return jsonify({
            "status": "success",
            "prediction": int(prediction),
            "result": result,
            "probability": round(float(probability), 4),
            "risk_level": risk_level
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
