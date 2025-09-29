import cv2
import os
import numpy as np
import random
import string

# Função para gerar um ID único de 12 caracteres com letras e números
def generate_unique_id(length=12):
    characters = string.ascii_letters + string.digits  # Letras (maiúsculas + minúsculas) e números
    return ''.join(random.choice(characters) for _ in range(length))

# Diretório onde as imagens de treinamento estão armazenadas
dataset_path = "dataset"
recognizer = cv2.face.LBPHFaceRecognizer_create()
faces = []
labels = []
label_id = 0
label_dict = {}

# Tamanho fixo para redimensionar as imagens
img_size = (100, 100)  # Tamanho padrão das imagens

# Percorre as pastas de usuários dentro do dataset
for user in os.listdir(dataset_path):
    user_path = os.path.join(dataset_path, user)

    # Cria o dicionário associando um ID ao nome do usuário
    label_dict[label_id] = user

    # Caminho onde o .yml do modelo será salvo
    user_trainer_path = os.path.join(user_path, "trainer")

    # Garante que o diretório trainer exista
    os.makedirs(user_trainer_path, exist_ok=True)

    # Verifica se já existe um arquivo .yml para o usuário
    existing_model = None
    for file in os.listdir(user_trainer_path):
        if file.endswith(".yml"):
            existing_model = os.path.join(user_trainer_path, file)
            break

    # Se já existe um modelo, pula o treinamento
    if existing_model:
        print(f"Modelo existente encontrado para {user}: {existing_model}. Pulando treinamento.")
        continue

    # Caso não tenha modelo, treina e salva um novo
    for img_name in os.listdir(user_path):
        img_path = os.path.join(user_path, img_name)
        
        # Verifica se é um arquivo de imagem (não uma pasta)
        if not img_name.endswith((".jpg", ".png", ".jpeg")):
            continue

        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

        # Redimensiona a imagem para garantir que todas tenham o mesmo tamanho
        img_resized = cv2.resize(img, img_size)

        faces.append(img_resized)
        labels.append(label_id)

    # Treinamento do modelo
    faces = np.array(faces)
    labels = np.array(labels)
    recognizer.train(faces, labels)

    # Gerar um ID único de 12 caracteres (letras e números)
    model_id = generate_unique_id(12)
    trainer_filename = os.path.join(user_trainer_path, f"{user}_trainer_{model_id}.yml")

    # Salva o modelo com o ID único
    recognizer.save(trainer_filename)
    print(f"Modelo treinado e salvo como: {trainer_filename}")

    # Resetar as listas para o próximo usuário
    faces = []
    labels = []
    label_id += 1

print("Treinamento concluído para todos os usuários.")
