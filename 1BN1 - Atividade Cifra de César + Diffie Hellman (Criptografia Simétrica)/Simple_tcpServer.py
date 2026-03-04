from socket import *
import random

# ==============================
# Funções Criptografia
# ==============================

def cifra_cesar(texto, chave):
    resultado = ""
    for c in texto:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            resultado += chr((ord(c) - base + chave) % 26 + base)
        else:
            resultado += c
    return resultado


def decifra_cesar(texto, chave):
    return cifra_cesar(texto, -chave)


# ==============================
# Teste de Primalidade
# ==============================

def eh_primo(N):
    if N < 2:
        return False
    for i in range(2, int(N**0.5) + 1):
        if N % i == 0:
            return False
    return True


# ==============================
# Configuração TCP
# ==============================

serverPort = 12500
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("127.0.0.1", serverPort))
serverSocket.listen(1)

print("Servidor TCP aguardando conexão...\n")

connectionSocket, addr = serverSocket.accept()
print("Conectado por:", addr)


# ==============================
# Diffie-Hellman
# ==============================

p = 23
g = 5

if not eh_primo(p):
    print("Erro: p não é primo.")
    exit()

b = random.randint(1, 10)
B = pow(g, b, p)

# Envia chave pública do servidor
connectionSocket.send(str(B).encode())

# Recebe chave pública do cliente
A = int(connectionSocket.recv(1024).decode())

# Calcula chave secreta
chave = pow(A, b, p)

print("Chave secreta (Servidor):", chave)

shift = chave % 26


# ==============================
# Comunicação
# ==============================

mensagem = connectionSocket.recv(1024).decode()
print("Mensagem criptografada recebida:", mensagem)

decriptado = decifra_cesar(mensagem, shift)
print("Mensagem descriptografada:", decriptado)

resposta = decriptado.upper()
criptografado = cifra_cesar(resposta, shift)

connectionSocket.send(criptografado.encode())

connectionSocket.close()