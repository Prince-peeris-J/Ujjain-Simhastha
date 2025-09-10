import os
import shutil


old_images = r"C:\Users\user\Downloads\ujjian crowd dataset\images"
old_labels = r"C:\Users\user\Downloads\ujjian crowd dataset\yolo_labels"


new_images = r"C:\Users\user\Downloads\ujjian_crowd_monitoring\dataset\images"
new_labels = r"C:\Users\user\Downloads\ujjian_crowd_monitoring\dataset\labels"


for f in os.listdir(old_images):
    src = os.path.join(old_images, f)
    dst = os.path.join(new_images, f)
    if os.path.isfile(src):   
        shutil.copy(src, dst)


for f in os.listdir(old_labels):
    src = os.path.join(old_labels, f)
    dst = os.path.join(new_labels, f)
    if os.path.isfile(src):   
        shutil.copy(src, dst)

print("✅ Dataset moved successfully!")
