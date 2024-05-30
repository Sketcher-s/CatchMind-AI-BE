from flask import Flask, request, jsonify
import os
from ultralytics import YOLO
from PIL import Image

# Flask 애플리케이션 초기화
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
DEV_SERVER_URL = 'dev.catchmind.shop'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# YOLOv8 모델 불러오기
model = YOLO('best.pt')

# 응답 메시지
ERROR_MESSAGE_NO_FILE = 'No file part'
ERROR_MESSAGE_NO_SELECTED_FILE = 'No selected file'
ERROR_MESSAGE_FILE_UPLOAD_FAILED = 'File upload failed'
SUCCESS_MESSAGE = 'Prediction sent successfully'

# 상수
RESULT_TEXT_FILE = 'result.txt'


@app.route('/predict', methods=['POST'])
def predict():
    # 요청에서 파일 가져오기
    if 'file' not in request.files:
        return jsonify({'error': ERROR_MESSAGE_NO_FILE}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': ERROR_MESSAGE_NO_SELECTED_FILE}), 400

    if file:
        # 파일 저장
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # 예측 수행
        img = Image.open(file_path)
        results = model.predict(img)  # 이미지 객체를 사용하여 예측
        os.remove(file_path)

        # 결과가 없을 경우 빈 문자열 반환
        if len(results) == 0 or len(results[0].boxes) == 0:
            return " "

        # 결과 처리 및 텍스트 파일로 저장
        result_txt_path = os.path.join(app.config['UPLOAD_FOLDER'], RESULT_TEXT_FILE)
        results[0].save_txt(result_txt_path)  # 첫 번째 결과를 텍스트 파일로 저장
        results[0].save(filename='result.jpg')

        # 텍스트 파일의 내용을 String으로 변환하고 \n을 공백으로 바꿈
        with open(result_txt_path, 'r') as f:
            predictions_txt = f.read().replace('\n', ' ')

        os.remove(result_txt_path)

        return predictions_txt

    return jsonify({'error': ERROR_MESSAGE_FILE_UPLOAD_FAILED}), 500


@app.route('/predict-test', methods=['POST'])
def predict_test():

    # 요청에서 파일 가져오기
    if 'file' not in request.files:
        return jsonify({'error': ERROR_MESSAGE_NO_FILE}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': ERROR_MESSAGE_NO_SELECTED_FILE}), 400

    if file:
        # 파일 저장
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # 예측 수행
        img = Image.open(file_path)
        results = model.predict(img)  # 이미지 객체를 사용하여 예측
        os.remove(file_path)

        # 결과가 없을 경우 빈 문자열 반환
        if len(results) == 0 or len(results[0].boxes) == 0:
            return " "

        # 결과 처리 및 텍스트 파일로 저장
        result_txt_path = os.path.join(app.config['UPLOAD_FOLDER'], RESULT_TEXT_FILE)
        results[0].save_txt(result_txt_path)  # 첫 번째 결과를 텍스트 파일로 저장
        results[0].save(filename='result.jpg')

        # 텍스트 파일의 내용을 String으로 변환하고 \n을 공백으로 바꿈
        with open(result_txt_path, 'r') as f:
            predictions_txt = f.read().replace('\n', ' ')

        os.remove(result_txt_path)

        return jsonify({'predictions': predictions_txt})

    return jsonify({'error': ERROR_MESSAGE_FILE_UPLOAD_FAILED}), 500


@app.route('/health')
def health_check():
    return 'OK!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
