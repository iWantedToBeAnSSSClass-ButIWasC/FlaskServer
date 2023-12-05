import requests
import api_key

def get_faceinfo_from_api(image):
    client_id = api_key.client_id
    client_secret = api_key.client_secret
    url = "https://openapi.naver.com/v1/vision/face" # 얼굴감지
    

    files = {'image': image}

    headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret }
    response = requests.post(url,  files=files, headers=headers)
    rescode = response.status_code

    # 얼굴 정보 딕셔너리 
    face_info = {"gender" : "", "age" : 0, "emotion" : ""}
    if(rescode==200):
        data = response.json()  # JSON 데이터를 파이썬 객체로 로드합니다.
        
        # face 정보가 넘어오지 않았을 경우 예외 처리
        if len(data["faces"]) > 0:
            gender = data["faces"][0]["gender"]["value"]
            age = data["faces"][0]["age"]["value"]
            emotion = data["faces"][0]["emotion"]["value"]

            age_range = age.split("~")

            # 평균 계산
            age = int((int(age_range[0]) + int(age_range[1])) / 2)

            print(gender, age, emotion)

            face_info["gender"] = gender
            face_info["age"] = age
            face_info["emotion"] = emotion
    else:
        print("Error Code:", rescode)
    
    return face_info # 딕셔너리 반환

