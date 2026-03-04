# 🔐 Secure TCP Communication with Caesar Cipher and Diffie-Hellman

## 📌 Descrição

Este projeto implementa uma comunicação TCP entre cliente (Alice) e servidor (Bob), evoluindo de uma transmissão em texto puro para um modelo com criptografia simétrica utilizando:

- Cifra de César (implementação autoral)
- Troca segura de chave com Diffie-Hellman
- Teste de primalidade
- Análise de tráfego com Wireshark

O objetivo é demonstrar como estabelecer comunicação segura sobre um canal TCP potencialmente inseguro.

---

## 🧠 Etapa 1 – Comunicação TCP Pura

Inicialmente, foi utilizada uma implementação básica de cliente e servidor TCP.

A comunicação ocorre via:

127.0.0.1:12500

Ao analisar com Wireshark (filtro `tcp.port == 12500`), observa-se que os dados trafegam em texto claro, podendo ser interceptados facilmente.

Isso demonstra a necessidade de criptografia.

---

## 🔐 Etapa 2 – Cifra de César (Código Autoral)

Foi implementada uma cifra de substituição baseada em deslocamento modular no alfabeto.

### Conceito

Cada letra é deslocada por um valor `k`:

C = (P + k) mod 26

Onde:
- P = posição da letra no alfabeto
- k = chave de deslocamento
- C = letra criptografada

Funções implementadas:

- `cifra_cesar(texto, chave)`
- `decifra_cesar(texto, chave)`

Nesta etapa, a chave ainda é fixa, representando uma vulnerabilidade caso seja descoberta.

---

## 🔑 Etapa 3 – Diffie-Hellman (Troca de Chave)

Para resolver o problema da distribuição da chave, foi implementado o algoritmo de Diffie-Hellman.

### Funcionamento

1. Escolhem-se valores públicos:
   - `p` → número primo
   - `g` → base geradora

2. Cada lado escolhe um segredo privado:
   - Cliente → `a`
   - Servidor → `b`

3. São geradas chaves públicas:

A = g^a mod p  
B = g^b mod p  

4. Após a troca das chaves públicas:

Cliente calcula:

K = B^a mod p  

Servidor calcula:

K = A^b mod p  

Ambos chegam ao mesmo valor secreto `K`, sem transmiti-lo pela rede.

---

## 🔢 Teste de Primalidade

Foi implementada função para validação de números primos utilizando verificação até a raiz quadrada do número:

```python
def eh_primo(N):
    if N < 2:
        return False
    for i in range(2, int(N**0.5) + 1):
        if N % i == 0:
            return False
    return True
```

Essa verificação é utilizada para validar o valor de p.

---

## 🔄 Integração Final

A chave secreta gerada pelo Diffie-Hellman é utilizada como deslocamento da Cifra de César:

shift = chave % 26

Isso garante que:
   - A chave muda a cada execução
   - Não existe chave fixa
   - A troca ocorre mesmo em canal inseguro

---

## 🔍 Análise com Wireshark

Filtro utilizado:
tcp.port == 12500

Resultados observados:
   - Comunicação TCP com handshake completo
   - Texto puro na etapa inicial
   - Texto criptografado após implementação
   - Chave secreta não trafega pela rede

---

## 📂 Estrutura do Projeto

/socket_tcp_secure
│
├── SimpleTCPServer.py
├── SimpleTCPClient.py
└── README.md

---

##▶ Como Executar

Iniciar servidor:

python SimpleTCPServer.py

Iniciar cliente:

python SimpleTCPClient.py

Utilizar Wireshark com filtro:

tcp.port == 12500

---

## ⚠ Considerações de Segurança
  - A Cifra de César isoladamente não é segura.
  - Diffie-Hellman resolve o problema da troca de chave.
  - O sistema ainda estaria vulnerável a ataques Man-in-the-Middle.
  - Protocolos reais como TLS utilizam esses conceitos de forma robusta.

---

## 🎯 Conclusão

O projeto demonstra:
  - Funcionamento da pilha TCP
  - Implementação de criptografia simétrica
  - Troca segura de chave
  - Aplicação prática de aritmética modular
  - Análise de tráfego de rede


Mostrando, na prática, a importância da criptografia na comunicação em redes.
