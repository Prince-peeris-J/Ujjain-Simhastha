import os
import shutil
import random

dataset_path = r"C:\Users\user\Downloads\ujjian_crowd_monitoring\dataset"
images_path = os.path.join(dataset_path, "images")
labels_path = os.path.join(dataset_path, "labels")

train_img = os.path.join(images_path, "train")
val_img = os.path.join(images_path, "val")
train_lbl = os.path.join(labels_path, "train")
val_lbl = os.path.join(labels_path, "val")

# Create train/val folders
for p in [train_img, val_img, train_lbl, val_lbl]:
    os.makedirs(p, exist_ok=True)

# Get all images
images = [f for f in os.listdir(images_path) if f.endswith((".jpg", ".png"))]

print(f"🔎 Found {len(images)} images in {images_path}")

random.shuffle(images)
split_idx = int(0.8 * len(images))
train_files = images[:split_idx]
val_files = images[split_idx:]

missing_labels = []

def move_files(files, img_dest, lbl_dest):
    for f in files:
        img_src = os.path.join(images_path, f)
        lbl_src = os.path.join(labels_path, f.rsplit(".", 1)[0] + ".txt")

        if os.path.exists(img_src) and os.path.exists(lbl_src):
            shutil.copy(img_src, os.path.join(img_dest, f))
            shutil.copy(lbl_src, os.path.join(lbl_dest, f.rsplit(".", 1)[0] + ".txt"))
        else:
            missing_labels.append(f)

move_files(train_files, train_img, train_lbl)
move_files(val_files, val_img, val_lbl)

print(f"✅ Split completed: {len(train_files)} train, {len(val_files)} val")
if missing_labels:
    print(f"⚠ Warning: {len(missing_labels)} images had no matching labels. Example: {missing_labels[:5]}")
