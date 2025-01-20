import cv2 
import mediapipe as mp

hand = mp.solutions.hands
face = mp.solutions.face_detection
hands = hand.Hands(min_detection_confidence=0.9, min_tracking_confidence=0.9, model_complexity=1)
faces = face.FaceDetection(min_detection_confidence=0.7)

vid = cv2.VideoCapture(0)

garis_akhir_kiri = None
garis_akhir_kanan = None
garis_kiri = []
garis_kanan = []



while vid.isOpened():
    ret, frame = vid.read()
    if not ret:
        break
    
    
    warna = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    tangan = hands.process(warna)
    wajah = faces.process(warna)
    
    if tangan.multi_hand_landmarks:
        for garis_tangan in tangan.multi_hand_landmarks:
            
            multi = tangan.multi_handedness[tangan.multi_hand_landmarks.index(garis_tangan)].classification[0].label
            
            jempol = garis_tangan.landmark[hand.HandLandmark.THUMB_TIP]
            telunjuk = garis_tangan.landmark[hand.HandLandmark.INDEX_FINGER_TIP]
            tengah = garis_tangan.landmark[hand.HandLandmark.MIDDLE_FINGER_TIP]
            manis = garis_tangan.landmark[hand.HandLandmark.RING_FINGER_TIP]
            kelingking = garis_tangan.landmark[hand.HandLandmark.PINKY_TIP]
            
            jempol_telunjuk = ((jempol.x - telunjuk.x) ** 2 + (jempol.y - telunjuk.y) ** 2) ** 0.5
            jempol_tengah = ((jempol.x - tengah.x) ** 2 + (jempol.y - tengah.y)**2) ** 0.5
            manis_jempol = ((manis.x - jempol.x) ** 2 + (manis.y - jempol.y)** 2) ** 0.5
            
            
            h, w, _ = frame.shape
            mulai = (int(jempol.x * w), int(jempol.y * h))
            
            if multi == 'Left':
                if jempol_telunjuk < 0.05:
                    if garis_akhir_kiri is None:
                        garis_akhir_kiri = mulai
                    else:
                        jarak = 10
                        for i in range(jarak + 1):
                            x = int(garis_akhir_kiri[0] + (mulai[0] - garis_akhir_kiri[0]) * i / jarak)
                            y = int(garis_akhir_kiri[1] + (mulai[1] - garis_akhir_kiri[1]) * i / jarak)
                            garis_kiri.append((garis_akhir_kiri, (x, y)))
                        garis_akhir_kiri = mulai
                else:
                    garis_akhir_kiri = None

                if jempol_tengah < 0.05:
                    garis_kiri = []
                    
                if manis_jempol < 0.05:
                    frame = cv2.flip(frame, 1)
                    
            else:
                if jempol_telunjuk < 0.05:
                    if garis_akhir_kanan is None:
                        garis_akhir_kanan = mulai
                    else:
                        jarak = 10
                        for i in range(jarak + 1):
                            x = int(garis_akhir_kanan[0] + (mulai[0] - garis_akhir_kanan[0]) * i / jarak)
                            y = int(garis_akhir_kanan[1] + (mulai[1] - garis_akhir_kanan[1]) * i / jarak)
                            garis_kanan.append((garis_akhir_kanan, (x, y)))
                        garis_akhir_kanan = mulai
                else:
                    garis_akhir_kanan = None

                if jempol_tengah < 0.05:
                    garis_kanan = []
                    
                if manis_jempol < 0.05:
                    frame = cv2.flip(frame, 1)
                
    for garis_tangan in garis_kiri:
        cv2.line(frame, garis_tangan[0], garis_tangan[1], (0, 255, 0), 5)
    
    for garis_tangan in garis_kanan:
        cv2.line(frame, garis_tangan[0], garis_tangan[1], (255, 0, 0), 2)
        
    if wajah.detections:
        for wajah_titik in wajah.detections:
            mp.solutions.drawing_utils.draw_detection(frame, wajah_titik)
            
    cv2.imshow('Garis', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
vid.release()
cv2.destroyAllWindows()