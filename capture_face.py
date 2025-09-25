import cv2
import os

# Nome do usuário
user_name = "Bruno"
dataset_path = f"dataset/{user_name}"
os.makedirs(dataset_path, exist_ok=True)

cap = cv2.VideoCapture(0)
count = 0

while count < 20:  # captura 20 fotos
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Capture", frame)
    key = cv2.waitKey(1) & 0xFF

    # Salvar foto
    cv2.imwrite(f"{dataset_path}/img{count}.jpg", frame)
    count += 1

    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
