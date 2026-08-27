import os
import urllib.request

import cv2
import mediapipe as mp


# ============================================================
# KONFIGURASI
# ============================================================

MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
)

MODEL_FILE = "hand_landmarker.task"


# ============================================================
# DOWNLOAD MODEL MEDIAPIPE JIKA BELUM ADA
# ============================================================

def download_model():
    if os.path.exists(MODEL_FILE):
        print("Model MediaPipe sudah tersedia.")
        return

    print("Model MediaPipe belum ditemukan.")
    print("Sedang mendownload model...")

    try:
        urllib.request.urlretrieve(MODEL_URL, MODEL_FILE)
        print("Model berhasil didownload.")

    except Exception as e:
        print("Gagal mendownload model MediaPipe.")
        print("Error:", e)
        print()
        print("Pastikan komputer terhubung ke internet.")
        raise


# ============================================================
# DOWNLOAD MODEL
# ============================================================

download_model()


# ============================================================
# INISIALISASI MEDIAPIPE HAND LANDMARKER
# ============================================================

BaseOptions = mp.tasks.BaseOptions
VisionRunningMode = mp.tasks.vision.RunningMode
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions


options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path=MODEL_FILE
    ),

    running_mode=VisionRunningMode.IMAGE,

    num_hands=2,

    min_hand_detection_confidence=0.7,

    min_hand_presence_confidence=0.7,

    min_tracking_confidence=0.6,
)


hands_detector = HandLandmarker.create_from_options(options)


# ============================================================
# INDEX LANDMARK JARI
# ============================================================

FINGER_TIPS = {
    "thumb": 4,
    "index": 8,
    "middle": 12,
    "ring": 16,
    "pinky": 20,
}

FINGER_PIPS = {
    "thumb": 3,
    "index": 6,
    "middle": 10,
    "ring": 14,
    "pinky": 18,
}


# ============================================================
# CEK JARI LURUS
# ============================================================

def is_finger_extended(landmarks, finger_name):
    """
    Mengecek apakah jari dalam posisi lurus.

    Untuk jari telunjuk, tengah, manis, dan kelingking:
    ujung jari harus berada lebih tinggi daripada PIP.

    Pada koordinat MediaPipe:
    nilai Y lebih kecil = posisi lebih tinggi.
    """

    tip = landmarks[FINGER_TIPS[finger_name]]
    pip = landmarks[FINGER_PIPS[finger_name]]

    return tip.y < pip.y


# ============================================================
# CEK PEACE SIGN
# ============================================================

def is_peace_sign(landmarks):
    """
    Gesture peace sign:

    Telunjuk  -> LURUS
    Tengah    -> LURUS
    Manis     -> TERLIPAT
    Kelingking-> TERLIPAT

    Jempol diabaikan.
    """

    index_up = is_finger_extended(
        landmarks,
        "index"
    )

    middle_up = is_finger_extended(
        landmarks,
        "middle"
    )

    ring_down = not is_finger_extended(
        landmarks,
        "ring"
    )

    pinky_down = not is_finger_extended(
        landmarks,
        "pinky"
    )

    return (
        index_up
        and middle_up
        and ring_down
        and pinky_down
    )


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print()
    print("=" * 60)
    print("   KAMERA AUTO-BLUR - PEACE SIGN x2")
    print("=" * 60)
    print()
    print("Kamera sedang diaktifkan...")
    print("Tunjukkan gesture ✌️✌️ dengan DUA tangan.")
    print("Jika dua tangan membentuk peace sign, blur aktif.")
    print("Tekan Q untuk keluar.")
    print()

    # --------------------------------------------------------
    # BUKA WEBCAM
    # --------------------------------------------------------

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():

        print(
            "ERROR: Tidak bisa mengakses kamera."
        )

        print(
            "Pastikan webcam tersedia dan tidak "
            "sedang digunakan aplikasi lain."
        )

        hands_detector.close()

        return

    # --------------------------------------------------------
    # LOOP KAMERA
    # --------------------------------------------------------

    while True:

        success, frame = cap.read()

        if not success:

            print(
                "Gagal membaca frame dari kamera."
            )

            break

        # ----------------------------------------------------
        # MIRROR CAMERA
        # ----------------------------------------------------

        frame = cv2.flip(frame, 1)

        # ----------------------------------------------------
        # BGR -> RGB
        # ----------------------------------------------------

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # ----------------------------------------------------
        # BUAT MEDIAPIPE IMAGE
        # ----------------------------------------------------

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # ----------------------------------------------------
        # DETEKSI TANGAN
        # ----------------------------------------------------

        results = hands_detector.detect(
            mp_image
        )

        peace_count = 0

        # ----------------------------------------------------
        # CEK SETIAP TANGAN
        # ----------------------------------------------------

        if results.hand_landmarks:

            for hand_landmarks in results.hand_landmarks:

                if is_peace_sign(
                    hand_landmarks
                ):

                    peace_count += 1

        # ----------------------------------------------------
        # DUA TANGAN PEACE SIGN
        # ----------------------------------------------------

        is_double_peace = peace_count >= 2

        # ----------------------------------------------------
        # AKTIFKAN BLUR
        # ----------------------------------------------------

        if is_double_peace:

            frame = cv2.GaussianBlur(
                frame,
                (55, 55),
                0
            )

            cv2.putText(
                frame,
                "BLUR AKTIF: PEACE x2",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 0, 255),
                2,
                cv2.LINE_AA
            )

            cv2.putText(
                frame,
                "PRIVACY MODE",
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
                cv2.LINE_AA
            )

        # ----------------------------------------------------
        # BLUR TIDAK AKTIF
        # ----------------------------------------------------

        else:

            status_text = (
                f"Peace Sign: "
                f"{peace_count}/2"
            )

            cv2.putText(
                frame,
                status_text,
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2,
                cv2.LINE_AA
            )

            cv2.putText(
                frame,
                "Tunjukkan Peace x2",
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
                cv2.LINE_AA
            )

        # ----------------------------------------------------
        # TAMPILKAN FRAME
        # ----------------------------------------------------

        cv2.imshow(
            "Kamera Auto-Blur - Peace Sign x2",
            frame
        )

        # ----------------------------------------------------
        # TEKAN Q UNTUK KELUAR
        # ----------------------------------------------------

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):

            print()
            print("Program dihentikan.")

            break

    # --------------------------------------------------------
    # CLEANUP
    # --------------------------------------------------------

    cap.release()

    cv2.destroyAllWindows()

    hands_detector.close()


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":
    main()