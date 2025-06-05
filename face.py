from flask import Flask, jsonify
import cv2
import threading
import os
app = Flask(__name__)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def show_frame_non_blocking(frame):
     cv2.imwrite(os.path.join('static', 'debug_frame.jpg'), frame)

@app.route('/detect-face', methods=['GET'])
def detect_face():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    if not ret:
        return jsonify({"error": "Unable to capture frame from webcam."}), 500

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    cap.release()

    threading.Thread(target=show_frame_non_blocking, args=(frame,), daemon=True).start()

    if len(faces) > 0:
        return jsonify({"face_detected": True})
    else:
        return jsonify({"face_detected": False})
@app.route('/debug-frame')
def debug_frame():
    return app.send_static_file('debug_frame.jpg')

if __name__ == "__main__":
    app.run(debug=True)
