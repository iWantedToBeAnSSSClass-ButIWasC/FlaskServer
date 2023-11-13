import requests
import api_key

def get_faceinfo_from_api(image):

    client_id = api_key.client_id
    client_secret = api_key.client_secret
    url = "https://openapi.naver.com/v1/vision/face" # 얼굴감지

    # TODO: 이 부분의 image를 앱에서 넘겨받은 image로 변경 
    files = image
    #이전 코드files = {'image': open('멋진남자 윤태섭.jpg', 'rb')}

    headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret }
    response = requests.post(url,  files=files, headers=headers)
    rescode = response.status_code

    # 얼굴 정보 딕셔너리 
    face_info = {"gender" : "", "age" : 0, "emotion" : ""}

    if(rescode==200):
        print (response.text," ")

        data = response.json()  # JSON 데이터를 파이썬 객체로 로드합니다.

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
        print("Error Code:" + rescode)
    
    return face_info # 딕셔너리 반환


# 호출 확인
get_faceinfo_from_api()