from ultralytics import YOLO
import cv2
import os
import glob


PROJECT_DIR = r"C:\Users\user\Downloads\ujjian_crowd_monitoring"
CROWD_LIMIT = 50

model_files = glob.glob(os.path.join(PROJECT_DIR, '**', '*.pt'), recursive=True)

if not model_files:
    raise FileNotFoundError(f"No YOLO .pt model found in {PROJECT_DIR}")


MODEL_PATH = model_files[0]
print(f"Using YOLO model: {MODEL_PATH}")


model = YOLO(MODEL_PATH)


cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Cannot open webcam or video stream")

print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to read frame from webcam.")
        break

    
    results = model(frame)[0]

    
    annotated_frame = results.plot()


    num_people = (results.boxes.cls == 0).sum().item()

    
    cv2.putText(
        annotated_frame,
        f"Crowd Count: {num_people}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    if num_people > CROWD_LIMIT:
        cv2.putText(
            annotated_frame,
            "⚠ CROWD ALERT!",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0, 0, 255),
            3
        )

    
    cv2.imshow("Ujjian Crowd Monitoring", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
