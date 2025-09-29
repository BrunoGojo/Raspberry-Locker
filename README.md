# Raspberry Locker - Configuração do Face ID

Para começar a utilizar o Face ID, siga os passos abaixo.

## 1. Captura de Rosto (Capture_face)

O primeiro passo é registrar o rosto do usuário. O sistema irá capturar 5 fotos do seu rosto para criar um dataset único. 

### Passos:
- Pressione a tecla **Espaço** para realizar cada uma das 5 capturas de foto do seu rosto.
- Certifique-se de que o rosto esteja bem iluminado e posicionado de forma clara para cada captura.

## 2. Treinamento do Modelo (Train Model)

Após a captura das fotos, um dataset será criado e nomeado com o nome do usuário. 

### Passos:
- O sistema usará as imagens capturadas para treinar um modelo de reconhecimento facial.
- O processo de treinamento gera um arquivo com a extensão `.yml`, que contém os dados processados do rosto do usuário.

> **Observação:** O treinamento pode levar alguns minutos, dependendo da qualidade e quantidade das imagens capturadas.

## 3. Verificação por Face ID

Com o modelo treinado e o arquivo `.yml` gerado, o sistema de Face ID estará pronto para realizar a verificação facial em tempo real.

### Passos:
- Ao tentar acessar o sistema, o reconhecimento facial será realizado automaticamente.
- O modelo treinado será utilizado para identificar o usuário com base nas características faciais registradas.

Agora, o seu sistema está pronto para usar o Face ID com segurança!
