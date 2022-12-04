import cv2
from keras.models import load_model
import numpy as np
import time
import random


font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
fontColor = (255, 0, 0)
thickness = 2
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


def get_computer_choice():
    options = ["Rock", "Paper", "Scissors"]
    choice = random.choice(options)
    return choice


def get_user_choice():
    user_choice = input("Enter your choice(Rock, Paper, or Scissors):")
    return user_choice


def get_winner(computer_choice, user_choice):
    if computer_choice == user_choice:
        print("It is a tie!")
        return "Tie"
    elif (computer_choice == "Rock" and user_choice == "Scissors"):
        print("You lost")
        return "Computer"
    elif (computer_choice == "Paper" and user_choice == "Rock"):
        print("You lost")
        return "Computer"
    elif (computer_choice == "Scissors" and user_choice == "Paper"):
        print("You lost")
        return "Computer"
    else:
        print("You won!")
        return "User"


countdown = 5
round_over = False
game_over = False
current_time = time.time()


computer_wins = 0
user_wins = 0

user_text = ""
computer_text = ""
winner_text = ""
result_text = ""

while True:
    ret, frame = cap.read()
    resized_frame = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
    image_np = np.array(resized_frame)
    normalized_image = (image_np.astype(np.float32) /
                        127.0) - 1  # Normalize the image
    data[0] = normalized_image

    countdown_txt = f"Show your choice in {countdown}"

    if countdown == 0 and round_over == False:
        countdown_txt = ""
        user_choice = get_prediction(data)
        if user_choice != "Nothing":
            print(f"You chose {user_choice}")
            user_text = f"You chose {user_choice}"
            computer_choice = get_computer_choice()
            computer_text = f"Computer chose {computer_choice}"
            winner = get_winner(computer_choice, user_choice)
            if winner == "Tie":
                winner_text = f"It is a tie!"
            else:
                winner_text = f"{winner} wins this round!"
                if winner == "Computer":
                    computer_wins += 1
                if winner == "User":
                    user_wins += 1
            round_over = True

    cv2.putText(frame, countdown_txt,
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

    cv2.putText(frame, user_text,
                (10, 60),
                font,
                fontScale,
                fontColor,
                thickness,
                lineType)

    cv2.putText(frame, computer_text,
                (10, 90),
                font,
                fontScale,
                fontColor,
                thickness,
                lineType)

    cv2.putText(frame, winner_text,
                (10, 120),
                font,
                fontScale,
                fontColor,
                thickness,
                lineType)

    score_text = f"User: {user_wins}    Computer: {computer_wins}"
    cv2.putText(frame, score_text,
                (10, 400),
                font,
                fontScale,
                fontColor,
                thickness,
                lineType)

    if round_over == True:
        if user_wins > 2 or computer_wins > 2:
            if user_wins > 2:
                final_winner = "User"
            if computer_wins > 2:
                final_winner = "Computer"
            result_text = f"{final_winner} is the winner! \n Press r to restart game \n Press q to quit"
            game_over = True
        else:
            result_text = "Press n to start next round \n Press q to quit"

    y0, dy = 200, 30
    for i, line in enumerate(result_text.split('\n')):
        y = y0 + i*dy
        # cv2.putText(img, line, (50, y ), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
        cv2.putText(frame, line,
                    (90, y),
                    font,
                    fontScale,
                    fontColor,
                    thickness,
                    lineType)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if round_over == True:
        pressed_key = cv2.waitKey(0)
        if pressed_key == ord('n'):
            countdown = 5
            result_text = ""
            user_text = ""
            computer_text = ""
            winner_text = ""
            round_over = False
        if pressed_key == ord('q'):
            break

    if game_over == True:
        pressed_key = cv2.waitKey(0)
        if pressed_key == ord('r'):
            countdown = 5
            result_text = ""
            user_text = ""
            computer_text = ""
            computer_wins = 0
            user_wins = 0
            game_over = False
        if pressed_key == ord('q'):
            break


# After the loop release the cap object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()
