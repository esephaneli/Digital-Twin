import cv2
import mediapipe as mp
import numpy as np
import time

def run_ultimate_digital_twin():
    # Kütüphaneleri çağır (Holistic tüm vücut için, Face Mesh iris indeksleri için)
    mp_holistic = mp.solutions.holistic
    mp_face_mesh = mp.solutions.face_mesh 
    mp_drawing = mp.solutions.drawing_utils

    # Kamerayı aç
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    pTime = 0

    # KRİTİK NOKTA: refine_face_landmarks=True ile iris (göz bebeği) koordinatlarını açıyoruz!
    with mp_holistic.Holistic(
        min_detection_confidence=0.6, 
        min_tracking_confidence=0.6,
        refine_face_landmarks=True) as holistic:

        while cap.isOpened():
            success, image = cap.read()
            if not success: break

            image = cv2.flip(image, 1) # Ayna efekti
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image_rgb.flags.writeable = False

            # Tüm vücut, yüz, eller ve irisleri tek seferde algıla
            results = holistic.process(image_rgb)

            image_rgb.flags.writeable = True
            image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

            # Holografik Canvas (Siyah Arka Plan)
            h, w, c = image.shape
            digital_twin_canvas = np.zeros((h, w, c), dtype=np.uint8)

            # --- SİBERPUNK ARAYÜZ ---
            cv2.rectangle(digital_twin_canvas, (10, 10), (w - 10, h - 10), (0, 255, 0), 1)
            cv2.putText(digital_twin_canvas, ':: ULTIMATE COGNITIVE TWIN V1.0 ::', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.line(digital_twin_canvas, (20, 40), (w - 20, 40), (0, 150, 0), 1)

            # --- 1. GÖVDE VE KOLLAR (Neon Yeşil) ---
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    image=digital_twin_canvas,
                    landmark_list=results.pose_landmarks,
                    connections=mp_holistic.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=1))
                
                # Omuz hizalama analizi
                pose_lm = results.pose_landmarks.landmark
                shoulder_diff = abs(pose_lm[mp_holistic.PoseLandmark.LEFT_SHOULDER].y - pose_lm[mp_holistic.PoseLandmark.RIGHT_SHOULDER].y) * 100
                shoulder_status = "STABLE" if shoulder_diff < 5 else "UNSTABLE"
            else:
                shoulder_status = "UNKNOWN"

            # --- 2. ELLER (Neon Mavi) ---
            if results.left_hand_landmarks:
                mp_drawing.draw_landmarks(
                    digital_twin_canvas, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2))
            if results.right_hand_landmarks:
                mp_drawing.draw_landmarks(
                    digital_twin_canvas, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2))

            # --- 3. YÜZ VE İRİS TAKİBİ (Neon Mavi ve Kırmızı) ---
            blink_status = "CALCULATING..."
            if results.face_landmarks:
                # Yüz Ağı Çizimi
                mp_drawing.draw_landmarks(
                    image=digital_twin_canvas,
                    landmark_list=results.face_landmarks,
                    connections=mp_holistic.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=1, circle_radius=1))
                
                face_lm = results.face_landmarks.landmark
                
                # Göz kırpma analizi
                blink_ratio = abs(face_lm[159].y - face_lm[145].y) * 100
                blink_status = "BLINKING" if blink_ratio < 1.0 else "EYE OPEN"

                # SİBERPUNK İRİS (KIRMIZI NOKTALAR) - Senin İstediğin Olay!
                iris_indices = list(mp_face_mesh.FACEMESH_IRISES)
                for iris_connection in iris_indices:
                    start_idx, end_idx = iris_connection
                    start_point = face_lm[start_idx]
                    end_point = face_lm[end_idx]
                    
                    sx, sy = int(start_point.x * w), int(start_point.y * h)
                    ex, ey = int(end_point.x * w), int(end_point.y * h)
                    
                    cv2.circle(digital_twin_canvas, (sx, sy), 2, (0, 0, 255), -1) # Kırmızı lazer gözler
                    cv2.circle(digital_twin_canvas, (ex, ey), 2, (0, 0, 255), -1)

            # --- 4. ANALİTİK TERMİNAL PANELİ ---
            info_x = 20
            y_offset = 70
            info_text_color = (255, 255, 0) # Cyan
            cv2.putText(digital_twin_canvas, f'[SYSTEM]: OPTIMIZED EDGE AI', (info_x, y_offset), cv2.FONT_HERSHEY_PLAIN, 1.2, info_text_color, 1)
            cv2.putText(digital_twin_canvas, f'[SHOULDER]: {shoulder_status}', (info_x, y_offset + 25), cv2.FONT_HERSHEY_PLAIN, 1.2, info_text_color, 1)
            cv2.putText(digital_twin_canvas, f'[BLINK]: {blink_status}', (info_x, y_offset + 50), cv2.FONT_HERSHEY_PLAIN, 1.2, info_text_color, 1)

            # Otonom Ajan Etiketi (Sağ Alt)
            cv2.putText(digital_twin_canvas, 'FULL-BODY & GAZE TRACKING v1.0', (info_x, h - 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 200, 0), 1)

            # FPS Hesaplama
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(image, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Birleştir ve Göster
            combined_view = np.hstack((image, digital_twin_canvas))
            cv2.imshow('Ultimate Digital Twin', combined_view)

            if cv2.waitKey(5) & 0xFF == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_ultimate_digital_twin()