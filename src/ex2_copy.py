import cv2
import mediapipe as mp
import keyinput
import numpy as np



class HandGestureController:
    def __init__(self,ret, frame, cap):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.ret = ret
        self.image = frame
        self.text = None
        self.cap = cap

    def process_video(self,):
        with self.mp_hands.Hands(
            
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
  
            while self.cap.isOpened():
                if not self.ret:
                    print("Ignoring empty camera frame.")
                    continue

                self.image.flags.writeable = False
                self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
                results = hands.process(self.image)
                imageHeight, imageWidth, _ = self.image.shape

                self.image.flags.writeable = True
                self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR)
                co=[]
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        self.mp_drawing.draw_landmarks(
                            self.image,
                            hand_landmarks,
                            self.mp_hands.HAND_CONNECTIONS,
                            self.mp_drawing_styles.get_default_hand_landmarks_style(),
                            self.mp_drawing_styles.get_default_hand_connections_style())
                        for point in self.mp_hands.HandLandmark:
                            if str(point) == "HandLandmark.WRIST":
                                normalizedLandmark = hand_landmarks.landmark[point]
                                pixelCoordinatesLandmark = self.mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x,
                                                                                                            normalizedLandmark.y,
                                                                                                            imageWidth, imageHeight)
                                try:
                                    co.append(list(pixelCoordinatesLandmark))
                                except:
                                    continue

                if len(co) == 2:
                    x_wrist_1, y_wrist_1 = co[0][0], co[0][1]
                    x_wrist_2, y_wrist_2 = co[1][0], co[1][1]
                    
                    x_mid, y_mid = (x_wrist_1 + x_wrist_2) / 2, (y_wrist_1 + y_wrist_2) / 2
                    radius = 150
                    m = (y_wrist_2 - y_wrist_1) / (x_wrist_2 - x_wrist_1)

                    delta = (radius ** 2 / (1 + m ** 2))
                    x_A = x_mid - np.sqrt(delta)
                    y_A = m * (x_A - x_mid) + y_mid
                    x_B = x_mid + np.sqrt(delta)
                    y_B = m * (x_B - x_mid) + y_mid

                    cv2.circle(img=self.image, center=(int(x_mid), int(y_mid)), radius=radius, color=(195, 255, 62), thickness=15)
                    cv2.line(self.image, (int(x_A), int(y_A)), (int(x_B), int(y_B)), (195, 255, 62), 20)
    

                    if co[0][0] > co[1][0] and co[0][1] > co[1][1] and co[0][1] - co[1][1] > 65:  ### 65 -------- 65 changed
                        self.text = "Turn left"
                        keyinput.press_key('w')

                        keyinput.release_key('s')
                        keyinput.release_key('d')
                        keyinput.press_key('a')
                        if np.sqrt((y_wrist_2 - y_wrist_1) ** 2 + (x_wrist_2 - x_wrist_1) ** 2) < 180:
                            keyinput.press_key('space')
                    
                        # cv2.line(self.image, (int(xbp), int(ybp)), (int(xm), int(ym)), (195, 255, 62), 20)

                    elif co[1][0] > co[0][0] and co[1][1] > co[0][1] and co[1][1] - co[0][1] > 65:  ### 65 -------- 65
                        self.text = "Turn left"
                        keyinput.press_key('w')
                        keyinput.release_key('s')
                        keyinput.release_key('d')
                        keyinput.press_key('a')
                        if np.sqrt((y_wrist_2 - y_wrist_1) ** 2 + (x_wrist_2 - x_wrist_1) ** 2) < 180:
                            keyinput.press_key('space')
                        # cv2.line(self.image, (int(xbp), int(ybp)), (int(xm), int(ym)), (195, 255, 62), 20)


                    elif co[0][0] > co[1][0] and co[1][1] > co[0][1] and co[1][1] - co[0][1] > 65:  ### 65 -------- 65
                        self.text ="Turn right"
                        keyinput.press_key('w')
                        keyinput.release_key('s')
                        keyinput.release_key('a')
                        keyinput.press_key('d')
                        if np.sqrt((y_wrist_2 - y_wrist_1) ** 2 + (x_wrist_2 - x_wrist_1) ** 2) < 180:
                            keyinput.press_key('space')
                        # cv2.line(self.image, (int(xap), int(yap)), (int(xm), int(ym)), (195, 255, 62), 20)

                    elif co[1][0] > co[0][0] and co[0][1] > co[1][1] and co[0][1] - co[1][1] > 65:  ### 65 -------- 65
                        self.text = "Turn right"
                        keyinput.press_key('w')
                        
                        keyinput.release_key('s')
                        keyinput.release_key('a')

                        keyinput.press_key('d')
                        if np.sqrt((y_wrist_2 - y_wrist_1) ** 2 + (x_wrist_2 - x_wrist_1) ** 2) < 180:
                            keyinput.press_key('space')
                        # cv2.line(self.image, (int(xap), int(yap)), (int(xm), int(ym)), (195, 255, 62), 20)

                    
                    
                    else:
                        self.text = "keeping straight"
                        keyinput.release_key('s')
                        keyinput.release_key('a')
                        keyinput.release_key('d')
                        keyinput.press_key('w')
                        keyinput.release_key('space')
                        if np.sqrt((y_wrist_2 - y_wrist_1) ** 2 + (x_wrist_2 - x_wrist_1) ** 2) < 180:
                            keyinput.press_key('space')
  
                if len(co) == 1:
                    self.text = "keeping back"
                    keyinput.release_key('a')
                    keyinput.release_key('d')
                    keyinput.release_key('w')
                    keyinput.press_key('s')
                elif len(co) == 0:
                    keyinput.release_key('a')
                    keyinput.release_key('d')
                    keyinput.release_key('w')
                    keyinput.release_key('s')
                return self.image, self.text