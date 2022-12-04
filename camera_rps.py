import cv2
from keras.models import load_model
import numpy as np

options = {}
file = open("labels.txt", "r")
for line in file:
    key, label = line.split()
    options[int(key)] = label
print(options)

model = load_model('keras_model.h5')
cap = cv2.VideoCapture(0)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)


def get_prediction(image):
    prediction = model.predict(data)
    label = options[np.argmax(prediction)]
    return label


while True:
    ret, frame = cap.read()
    resized_frame = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
    image_np = np.array(resized_frame)
    normalized_image = (image_np.astype(np.float32) /
                        127.0) - 1  # Normalize the image
    data[0] = normalized_image

    cv2.imshow('frame', frame)
    print(get_prediction(data))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()
