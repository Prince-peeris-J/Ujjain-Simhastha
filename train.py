from ultralytics import YOLO


model = YOLO("yolov8n.pt")


model.train(
    data="crowd.yaml",
    epochs=5,
    imgsz=640,
    batch=16,
    name="ujjian_crowd_model"
)

metrics = model.val()
print("✅ Validation Results:", metrics)

print("\n🎉 Training Completed! Best weights saved inside: runs/detect/ujjian_crowd_model/weights/best.pt")
