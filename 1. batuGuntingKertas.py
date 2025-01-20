import cv2 as cv
import mediapipe as mp
import random
import time

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def detect_hand_gesture(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
    middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
    ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y

    if thumb_tip < index_finger_tip and middle_finger_tip < ring_finger_tip and pinky_tip < ring_finger_tip:
        return "Rock"
    elif index_finger_tip < thumb_tip and middle_finger_tip < ring_finger_tip and pinky_tip > ring_finger_tip:
        return "Scissors"
    else:
        return "Paper"

def determine_winner(player_move, computer_move):
    if player_move == computer_move:
        return "Draw"
    elif (player_move == "Rock" and computer_move == "Scissors") or \
         (player_move == "Scissors" and computer_move == "Paper") or \
         (player_move == "Paper" and computer_move == "Rock"):
        return "Player Wins!"
    else:
        return "Computer Wins!"

cap = cv.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    start_time = time.time()
    game_interval = 5 
    result = "Show your move!"
    player_move = "None"
    computer_move = "None"

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        hand_results = hands.process(rgb_frame)

        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                player_move = detect_hand_gesture(hand_landmarks)

        current_time = time.time()
        if current_time - start_time >= game_interval:
            possible_moves = ["Rock", "Paper", "Scissors"]
            weights = [0.3, 0.4, 0.3] 
            computer_move = random.choices(possible_moves, weights=weights, k=1)[0]

            if player_move != "None":
                result = determine_winner(player_move, computer_move)
            else:
                result = "No Move Detected!"

            start_time = current_time
            player_move = "None"

        cv.putText(frame, f"Player: {player_move}", (10, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv.putText(frame, f"Computer: {computer_move}", (10, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv.putText(frame, result, (10, 150), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        cv.imshow('Rock-Paper-Scissors Game', frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv.destroyAllWindows()
