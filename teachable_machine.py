from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np

def get_moodinfo():
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model : h5 파일로 변환된 모델을 가져온다
    model = load_model("keras_model.h5", compile=False)

    # Load the labels : 분위기에 대한 클래스 라벨을 가져온다
    class_names = open("labels.txt", "r").readlines()

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1
    # keras model에 넘겨줄 데이터 : RGB 총 3개 채널을 가진 224*224 크기의 이미지 한 개
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # 이미지 경로를 통해 이미지를 가져온다. 서버에서 받아야 할 것 같은데 일단은 로컬에 있는 이미지로 테스트
    # 이미지가 어떤 식으로 넘어오지?
    image = Image.open("test.jpg").convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    # PIL을 사용하여 이미지 크기를 224*224로 조절
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model : 가장 가능성 높게 측정된 클래스 값을 가져온다
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    # confidence_score = prediction[0][index]

    # labels.txt에서 클래스의 이름을 가져온다. 앞쪽은 라벨 번호이므로 인덱스 2번부터 가져온다. 
    moodinfo = class_name[2:].replace("\n", "")
    return {'mood' : moodinfo}


# 출력 테스트
print(get_moodinfo())
