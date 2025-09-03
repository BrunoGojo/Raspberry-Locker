import time
import paho.mqtt.client as mqtt

# ---------------------------------------------------------------------------
# CONFIGURAÇÕES
# ---------------------------------------------------------------------------

# Defina como True para rodar sem hardware, em qualquer computador.
# Defina como False quando for rodar no Raspberry Pi com o hardware conectado.
SIMULATION_MODE = True

# Se não estiver em modo de simulação, tentaremos importar a biblioteca GPIO.
# Isso evita erros se você rodar este código em um PC Windows/Mac/Linux.
if not SIMULATION_MODE:
    try:
        import RPi.GPIO as GPIO
        # Configuração do pino GPIO para o relé (numeração BCM)
        RELAY_PIN = 17
    except (ImportError, RuntimeError):
        print("ERRO: Biblioteca RPi.GPIO não encontrada. Rodando em modo de simulação forçado.")
        SIMULATION_MODE = True

# Configurações do Broker MQTT
BROKER_ADDRESS = "broker.hivemq.com"  # Usando um broker público para facilitar o teste
BROKER_PORT = 1883
CLIENT_ID = "smart-locker-sim-01"  # Use um ID único
COMMAND_TOPIC = "locker/sim/1/command"
STATUS_TOPIC = "locker/sim/1/status"

# ---------------------------------------------------------------------------
# FUNÇÕES DE CONTROLE DO HARDWARE (COM SIMULAÇÃO)
# ---------------------------------------------------------------------------

def setup_hardware():
    """Prepara o hardware (ou a simulação dele)."""
    if SIMULATION_MODE:
        print("[SIMULAÇÃO] Ambiente de hardware virtual iniciado.")
    else:
        print("[HARDWARE] Configurando os pinos GPIO...")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RELAY_PIN, GPIO.OUT)
        GPIO.output(RELAY_PIN, GPIO.HIGH) # Garante que o relé comece desligado
        print(f"[HARDWARE] Pino {RELAY_PIN} configurado.")

def open_locker(duration_seconds=5):
    """Lógica para abrir a trava."""
    print(f"AÇÃO: Comando para abrir a trava recebido. Duração: {duration_seconds}s.")
    
    if SIMULATION_MODE:
        print("[SIMULAÇÃO] Relé LIGADO (trava aberta)")
        client.publish(STATUS_TOPIC, "UNLOCKED")
        time.sleep(duration_seconds)
        print("[SIMULAÇÃO] Relé DESLIGADO (trava fechada)")
        client.publish(STATUS_TOPIC, "LOCKED")
    else:
        # Código que será executado no Raspberry Pi
        GPIO.output(RELAY_PIN, GPIO.LOW) # Liga o relé
        client.publish(STATUS_TOPIC, "UNLOCKED")
        time.sleep(duration_seconds)
        GPIO.output(RELAY_PIN, GPIO.HIGH) # Desliga o relé
        client.publish(STATUS_TOPIC, "LOCKED")
    
    print("AÇÃO: Ciclo de abertura finalizado.")

def cleanup():
    """Limpa os recursos ao encerrar."""
    if not SIMULATION_MODE:
        print("[HARDWARE] Limpando a configuração da GPIO.")
        GPIO.cleanup()
    print("INFO: Programa encerrado.")

# ---------------------------------------------------------------------------
# LÓGICA DE COMUNICAÇÃO MQTT (O CORAÇÃO DO SOFTWARE)
# ---------------------------------------------------------------------------

def on_connect(client, userdata, flags, rc):
    """Função chamada quando nos conectamos ao broker."""
    if rc == 0:
        print("MQTT: Conectado ao Broker com sucesso!")
        client.subscribe(COMMAND_TOPIC)
        print(f"MQTT: Inscrito no tópico: {COMMAND_TOPIC}")
        client.publish(STATUS_TOPIC, "ONLINE", retain=True)
    else:
        print(f"MQTT: Falha na conexão, código de retorno: {rc}")

def on_message(client, userdata, msg):
    """Função chamada sempre que uma nova mensagem chega no tópico que assinamos."""
    payload = msg.payload.decode("utf-8")
    print(f"MQTT: Mensagem recebida! Tópico: '{msg.topic}', Payload: '{payload}'")

    # Estrutura de decisão baseada no comando recebido
    if msg.topic == COMMAND_TOPIC:
        if payload.upper() == "OPEN":
            open_locker()
        elif payload.upper() == "STATUS":
            # Exemplo de outro comando: pedir o status atual
            print("INFO: Respondendo a uma solicitação de status.")
            client.publish(STATUS_TOPIC, "ONLINE")
        else:
            print(f"AVISO: Comando '{payload}' não é reconhecido.")
            client.publish(STATUS_TOPIC, f"ERROR_UNKNOWN_COMMAND_{payload}")

# ---------------------------------------------------------------------------
# EXECUÇÃO PRINCIPAL
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    setup_hardware()

    # Inicializa o cliente MQTT
    client = mqtt.Client(client_id=CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message

    # Configura a "última vontade": se o cliente desconectar de forma inesperada,
    # o broker publicará "OFFLINE" no tópico de status.
    client.will_set(STATUS_TOPIC, payload="OFFLINE", qos=1, retain=True)

    try:
        print(f"INFO: Conectando ao broker público em {BROKER_ADDRESS}...")
        client.connect(BROKER_ADDRESS, BROKER_PORT)
        
        # O loop_forever() é o que mantém o programa rodando, escutando por mensagens.
        client.loop_forever()

    except KeyboardInterrupt:
        print("\nINFO: Desconectando do broker e encerrando...")
    finally:
        # Garante que a mensagem de offline seja enviada e a limpeza seja feita
        client.publish(STATUS_TOPIC, "OFFLINE", retain=True)
        client.disconnect()
        cleanup()