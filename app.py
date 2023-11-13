from flask import Flask, request, jsonify, send_file
from PIL import Image
from io import BytesIO
import json
import random
import naver_api
import teachable_machine

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/get_image', methods=['POST'])
def get_image():

    try:
        # 이미지를 포함한 요청에서 이미지 데이터를 받아오기
        uploaded_image = request.files['image'].read()

        # BytesIO를 사용하여 이미지를 PIL Image 객체로 변환
        image = Image.open(BytesIO(uploaded_image))
        
        # 여기서 image를 사용하여 원하는 로직 수행

        return "사진 전송 완료됨"
    except Exception as e:
        return str(e), 500


@app.route('/receive_info', methods=['POST'])
def receive_info():
    try:
        # 이미지를 포함한 요청에서 이미지 데이터를 받아오기
        uploaded_image = request.files['image'].read()

        # BytesIO를 사용하여 이미지를 PIL Image 객체로 변환
        image = Image.open(BytesIO(uploaded_image))

        face_info = naver_api.get_faceinfo_from_api(image)

        # 여기서 data를 사용하여 나이, 성별, 감정, 분위기 정보를 변수에 저장
        age = face_info.get('age')
        gender = face_info.get('gender')
        emotion = face_info.get('emotion')
        mood = teachable_machine.get_moodinfo(image)

        # perfume = "선택된 향수 정보"

        ###################################### 향수 선별을 위한 알고리즘

        # 향수 정보가 저장된 json 파일 위치
        json_data = {
            "perfume1": {
                "age": 25,
                "gender": "Male",
                "emotion": "fire",
                "mood": "cold",
                "url" : "asdf123"
                        },

            "perfume11": {
                "age": 25,
                "gender": "Male",
                "emotion": "fire",
                "mood": "cold",
                "url" : "asdf123"
            },

            "perfume111": {
                "age": 25,
                "gender": "Male",
                "emotion": "fire",
                "mood": "cold",
                "url" : "asdf123"
            },

            "perfume2": {
                "age": 22,
                "gender":  "Female",
                "emotion": "happy",
                "mood": "warm",
                "url" : "asdf123"
                        },

            "perfume3": {
                "age": 23,
                "gender": "Male",
                "emotion": "sad",
                "mood": "cute",
                "url" : "asdf123"
                        },

            "perfume4": {
                "age": 24,
                "gender": "Female",
                "emotion":"angry",
                "mood": "powerful",
                "url" : "asdf123"
                        }
        }

        json_file_path = json_data
        # with open(json_file_path, 'r') as file:
        #     perfumedata = json.load(file)

        #일치하는 향수들을 저장
        matching_info = []

        for perfume, attributes in json_data.items():
            # 주어진 기준과 각 항목을 비교하여 일치하는지 확인
            # 향수 데이터 전체에 대해, 유저 데이터를 비교하며 반복문 수행
            if all(attributes[key] == face_info[key] for key in 4):
                matching_info.append(perfume)

        # 맞는 향수가 없는 경우
        if len(matching_info) < 1:
            return "향수라는 틀에 가둘 수 없는 너란 사람. 아주 특별해"

        # 선택된 향수들 중 하나를 랜덤으로 선택하고 반환
        thisIsForYou = random.choice(matching_info)

        

        #이 지점에 향수 정보를 가져오는 코드를 추가하면 어떨까
        return jsonify({
            'perfume' : {
            'name' : thisIsForYou,
            'content' : json_data[thisIsForYou]["content"],
            'url' : json_data[thisIsForYou]["url"]}})

    # 향수를 찾을 수 없는 경우
    except Exception as e:
        return "예외가 발생했습니다. 발생 지점 receive_info"



if __name__ == '__main__':
    app.run()
