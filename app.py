from flask import Flask, request, jsonify
import os
from ultralytics import YOLO
import requests

# Flask 애플리케이션 초기화
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
DEV_SERVER_URL = 'dev.catchmind.shop'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# YOLOv8 모델 불러오기
model = YOLO('object-predict.pt')
model.eval()


@app.route('/predict', methods=['POST'])
def predict():
    # 요청에서 파일 가져오기
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        # 파일 저장
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # 예측 수행
        results = model(file_path)

        # 결과 처리
        for result in results:
            result.save_txt(result.txt)

        # 텍스트 파일의 내용을 String으로 변환
        with open('result.txt', 'r') as f:
            predictions_txt = f.read()

        # 스프링 서버로 예측 결과 전송
        spring_server_url = 'https://' + DEV_SERVER_URL + '/endpoint'
        response = requests.post(spring_server_url, json={'predictions_txt': predictions_txt})

        if response.status_code == 200:
            return jsonify({'message': 'Prediction sent successfully', 'predictions': predictions_txt})
        else:
            return jsonify({'error': 'Failed to send prediction to Spring server'}), 500

    return jsonify({'error': 'File upload failed'}), 500


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
