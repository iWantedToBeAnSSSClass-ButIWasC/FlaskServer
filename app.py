from flask import Flask, request, jsonify, send_file
import random
import naver_api
import teachable_machine
import json_data
import math

app = Flask(__name__)
json_data = json_data.json_data

@app.route('/receive_info', methods=['POST'])
def receive_info():
    try:
        # 이미지를 포함한 요청에서 이미지 데이터를 받아오기
        uploaded_image = request.files['image'].read()
        
        # naver api, teacahble machine 사용하여 정보 추출
        face_info = naver_api.get_faceinfo_from_api(uploaded_image)
        mood = teachable_machine.get_moodinfo(uploaded_image)
        face_info['mood'] = mood['mood']

        #일치하는 향수들을 저장
        matching_info = []

        # 사용자 이미지 최종 정보 출력
        print(face_info)

        # 주어진 기준과 각 항목을 비교하여 일치하는지 확인
        for perfume, attributes in json_data.items():
            # 분위기를 비교하여 다르다면 pass
            if attributes["mood"] != face_info["mood"]:
                continue

            # 성별을 비교하여 다르다면 pass
            if not face_info["gender"].lower() in attributes["gender"]:
                continue

            # 나잇대에 포함된다면 append
            if math.floor(face_info["age"] / 10) * 10 in attributes["age"]:
                matching_info.append(perfume)

        # 맞는 향수가 없는 경우
        if len(matching_info) < 1:
            return jsonify({
                'name' : "",
                'content' : "향수라는 틀에 가둘 수 없는 너란 사람. 아주 특별해",
                'url' : ""})

        # 선택된 향수들 중 하나를 랜덤으로 선택하고 반환
        thisIsForYou = random.choice(matching_info)

        return jsonify({
            'name' : thisIsForYou,
            'content' : json_data[thisIsForYou]["content"],
            'url' : json_data[thisIsForYou]["url"]})

    # 향수를 찾을 수 없는 경우
    except Exception as e:
        print(e)
        return str(e)


if __name__ == '__main__':
    app.run()