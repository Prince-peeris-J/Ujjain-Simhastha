from flask import Flask, render_template, Response, request, redirect, url_for
import cv2
import os
from ultralytics import YOLO
from werkzeug.utils import secure_filename

app = Flask(__name__)


model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)
UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            
            results = model(frame)
            annotated_frame = results[0].plot()
            crowd_count = len(results[0].boxes)

            
            cv2.putText(annotated_frame, f"Crowd Count: {crowd_count}",
                        (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0), 2)

            if crowd_count > 10:
                cv2.putText(annotated_frame, "⚠ ALERT: Crowd Exceeds Limit!",
                            (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 0, 255), 3)

            
            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/upload', methods=['POST'])
def upload_image() -> 'Response':
    if "file" not in request.files:
        return redirect(url_for("index"))
    
    file = request.files["file"]
    if file.filename == "":
        return redirect(url_for("index"))

    if file and file.filename:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        results = model(filepath)
        annotated_frame = results[0].plot()

        crowd_count = len(results[0].boxes)

        result_path = os.path.join(RESULT_FOLDER, filename)
        cv2.imwrite(result_path, annotated_frame)

        return render_template("index.html",
                               uploaded_image=url_for('static', filename=f"uploads/{filename}"),
                               result_image=url_for('static', filename=f"results/{filename}"),
                               crowd_count=crowd_count)


if __name__ == "__main__":
    app.run(port=3001)
