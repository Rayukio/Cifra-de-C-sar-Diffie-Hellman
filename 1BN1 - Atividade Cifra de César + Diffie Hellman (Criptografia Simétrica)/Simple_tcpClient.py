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
# Configuração TCP
# ==============================

serverName = "127.0.0.1"
serverPort = 12500

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))


# ==============================
# Diffie-Hellman
# ==============================

p = 23
g = 5

a = random.randint(1, 10)
A = pow(g, a, p)

# Recebe chave pública do servidor
B = int(clientSocket.recv(1024).decode())

# Envia chave pública do cliente
clientSocket.send(str(A).encode())

# Calcula chave secreta
chave = pow(B, a, p)

print("Chave secreta (Cliente):", chave)

shift = chave % 26


# ==============================
# Comunicação
# ==============================

sentence = input("Digite uma mensagem: ")

criptografado = cifra_cesar(sentence, shift)
clientSocket.send(criptografado.encode())

resposta = clientSocket.recv(1024).decode()

decriptado = decifra_cesar(resposta, shift)

print("Resposta descriptografada:", decriptado)

clientSocket.close()