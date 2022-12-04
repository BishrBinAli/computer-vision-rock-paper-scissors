import cv2
from keras.models import load_model
import numpy as np
import time


font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
fontColor = (0, 0, 0)
thickness = 1
lineType = 2


options = {}
file = open("labels.txt", "r")
for line in file:
    key, label = line.split()
    options[int(key)] = label


model = load_model('keras_model.h5')
cap = cv2.VideoCapture(0)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)


def get_prediction(image):
    prediction = model.predict(image)
    label = options[np.argmax(prediction)]
    return label

# def countdown(duration, delay=5):
#     i = duration
#     current_time = time.time()
#     print(i)
#     while i > 0:
#         if time.time() - current_time > delay:
#             i -= 1
#             print(i)
#             current_time = time.time()


countdown = 10
stop = False
current_time = time.time()
prediction_text = ""
while True:
    ret, frame = cap.read()
    resized_frame = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
    image_np = np.array(resized_frame)
    normalized_image = (image_np.astype(np.float32) /
                        127.0) - 1  # Normalize the image
    data[0] = normalized_image

    img_txt = f"Show your choice in {countdown}"
    cv2.putText(frame, img_txt,
                (10, 30),
                font,
                fontScale,
                fontColor,
                thickness,
                lineType)

    if countdown != 0:
        if time.time() - current_time > 1:
            countdown -= 1
            print(countdown)
            current_time = time.time()

    if countdown == 0 and stop == False:
        prediction = get_prediction(data)
        if prediction != "Nothing":
            print(f"You chose {prediction}")
            prediction_text = f"You chose {prediction}"
            stop = True

    cv2.putText(frame, prediction_text,
                (10, 60),
                font,
                fontScale,
                fontColor,
                thickness,
                lineType)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# After the loop release the cap object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()
