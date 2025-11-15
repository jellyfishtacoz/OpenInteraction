import cv2, os
vid = "silksong_capture.mp4"
outdir = "dataset/images/raw"
os.makedirs(outdir, exist_ok=True)
cap = cv2.VideoCapture(vid)
i = 0
skip = 3  # save every 3rd frame (adjust)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    if i % skip == 0:
        cv2.imwrite(os.path.join(outdir, f"frame_{i:06d}.jpg"), frame)
    i += 1
cap.release()
print("done", i)