import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands()

# Connect to the webcam
camera = cv2.VideoCapture(0)
resolution_x = 1280
resolution_y = 720
camera.set(cv2.CAP_PROP_FRAME_WIDTH, resolution_x)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution_y)

def find_coord_hand(img, side_inverted = False):
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)
    all_hands = []
    if result.multi_hand_landmarks:  # if hands are detected
        for hand_side, hand_landmarks in zip(result.multi_handedness, result.multi_hand_landmarks):
            hand_info = {}
            coords = []
            for mark in hand_landmarks.landmark:
                coord_x, coord_y, coord_z = int(mark.x * resolution_x), int(mark.y * resolution_y), int(mark.z * resolution_x)
                # print(coord_x, coord_y, coord_z)
                coords.append((coord_x, coord_y, coord_z)) #Adiciona tupla dentro da lista
                hand_info['coordenadas'] = coords
                if side_inverted:
                    if hand_side.classification[0].label == "Left":
                        hand_info["side"] = "Right"
                    else:
                        hand_info["side"] = "Left"
                else:
                    hand_info["side"] = hand_side.classification[0].label
                # print(hand_side)
                # print(hand_side.classification[0].label)
                print(hand_info["side"])
                all_hands.append(hand_info)
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    return img, all_hands

while True:
    ret, frame = camera.read()
    # Inverte a imagem
    frame = cv2.flip(frame, 1) # inverte esquerda pela direita
    # img, all_hands = find_coord_hand(frame)
    img, all_hands = find_coord_hand(frame)
    cv2.imshow("Camera", img)
    key = cv2.waitKey(1)
    if key == 27:
        break
