from flask import Flask, request, jsonify
from flask_cors import CORS
from predict import predict_image
# Инициализация Flask-приложения
app = Flask(__name__)
CORS(app)  # Разрешаем запросы с другого порта (React frontend)

# Роут обработки POST-запроса с изображением
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    prediction = predict_image(file)
    return jsonify({'style': prediction})

# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)

