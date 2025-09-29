import cv2
import os

# Solicita o nome do usuário
user_name = input("Digite o nome do usuário: ").strip()
dataset_path = f"dataset/{user_name}"
os.makedirs(dataset_path, exist_ok=True)

# Inicializa a câmera
cap = cv2.VideoCapture(0)

count = 0
total_photos = 5

print("\nPressione 'ESPACO' para capturar uma foto.")
print("Pressione 'q' para sair a qualquer momento.\n")

while count < total_photos:
    ret, frame = cap.read()
    if not ret:
        print("Erro ao acessar a câmera.")
        break

    # Exibe o vídeo ao vivo
    cv2.imshow("Pressione ESPACO para capturar", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord(' '):  # Tecla ESPAÇO pressionada
        img_path = f"{dataset_path}/img{count+1}.jpg"
        cv2.imwrite(img_path, frame)
        print(f"[{count+1}/{total_photos}] Foto salva em {img_path}")
        count += 1

    elif key == ord('q'):
        print("Saindo sem terminar a captura.")
        break

# Finaliza
cap.release()
cv2.destroyAllWindows()

if count == total_photos:
    print("\nCaptura finalizada com sucesso!")
else:
    print(f"\nForam capturadas {count} fotos.")
