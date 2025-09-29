import cv2
import numpy as np
import os

# Função para carregar múltiplos modelos .yml
def load_recognizers(models_dir="dataset"):
    recognizers = []
    label_dict = {}
    label_id = 0

    for user_dir in os.listdir(models_dir):
        user_path = os.path.join(models_dir, user_dir, "trainer")
        if os.path.isdir(user_path):
            for model_file in os.listdir(user_path):
                if model_file.endswith(".yml"):
                    model_path = os.path.join(user_path, model_file)
                    recognizer = cv2.face.LBPHFaceRecognizer_create()
                    recognizer.read(model_path)
                    recognizers.append((recognizer, label_id))
                    label_dict[label_id] = user_dir
                    label_id += 1
    return recognizers, label_dict

# Inicializa os reconhecedores
recognizers, label_dict = load_recognizers("dataset")

# Carrega o classificador de rostos
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Configura a captura de vídeo
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 420)  # Reduz a largura do quadro para otimizar o processamento
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 340)  # Reduz a altura do quadro para otimizar o processamento

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Converte a imagem para escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detecta rostos na imagem
    faces = face_cascade.detectMultiScale(gray, 1.2, 5)

    # Verifica se há rostos detectados
    if len(faces) == 0:
        print("Nenhum rosto detectado")  # Debug: Nenhum rosto detectado
    else:
        print(f"{len(faces)} rostos detectados")  # Debug: Quantos rostos foram detectados

    for (x, y, w, h) in faces:
        # Verifica se as coordenadas estão dentro dos limites da imagem
        if x < 0 or y < 0 or x + w > frame.shape[1] or y + h > frame.shape[0]:
            print("Coordenadas do rosto fora dos limites da imagem!")  # Debug
            continue

        # Desenha o quadrado ao redor do rosto
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Verde (0,255,0), espessura = 2

        # Região de interesse (ROI) para reconhecer
        roi_gray = gray[y:y+h, x:x+w]
        best_label = None
        best_confidence = float('inf')

        # Percorre os modelos carregados para prever o rosto detectado
        for recognizer, label_id in recognizers:
            label, confidence = recognizer.predict(roi_gray)
            if confidence < best_confidence:  # Escolhe o modelo com a menor confiança
                best_label = label_id
                best_confidence = confidence

        # Se a confiança for suficientemente alta, exibe o nome
        if best_confidence < 100:
            cv2.putText(frame, f"{label_dict[best_label]} {int(best_confidence)}", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Exibe a imagem com os rostos detectados e os nomes
    cv2.imshow("Face Recognition", frame)

    # Encerra se pressionar a tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
