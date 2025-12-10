# 🛡️ CryptoLab - Simulador Didático RSA

> Uma ferramenta interativa para ensino e aprendizagem de Criptografia Assimétrica e Assinatura Digital.

![Status](https://img.shields.io/badge/Status-Concluído-success)
![License](https://img.shields.io/badge/License-MIT-blue)
![Python](https://img.shields.io/badge/Backend-Python%20%7C%20Flask-yellow)
![React](https://img.shields.io/badge/Frontend-React%20%7C%20Vite-blue)

## 📖 Sobre o Projeto

O **CryptoLab** é uma aplicação Full Stack desenvolvida para desmistificar o funcionamento do algoritmo **RSA**. Diferente de chats comuns que escondem a criptografia, esta ferramenta **revela a matemática** por trás de cada mensagem trocada.

O projeto foi desenhado respeitando as **Heurísticas de Usabilidade de Nielsen**, garantindo uma interface amigável, feedbacks constantes e prevenção de erros para alunos iniciantes em Segurança da Informação.

## 🚀 Funcionalidades Principais

* **🔑 Geração de Chaves RSA:** Visualização didática das chaves Pública $(e, n)$ e Privada $(d, n)$.
* **💬 Simulação de Chat (Alice & Bob):** Troca de mensagens em tempo real simulada.
* **🔒 Criptografia (Confidencialidade):** Garante que apenas o destinatário leia a mensagem.
* **✍️ Assinatura Digital (Autenticidade):** Garante a autoria, integridade e não-repúdio da mensagem.
* **🧮 Logs Matemáticos em Tempo Real:** Um terminal lateral exibe o passo a passo do cálculo:
    * Conversão ASCII.
    * Cálculo $C = M^e \pmod n$.
    * Verificação $M = C^d \pmod n$.
* **📱 Interface Responsiva:** Design moderno (Dark Mode) adaptável para Desktop e Mobile.
* **🎓 Tutoriais Integrados:** Modais educativos explicam os conceitos conforme o uso.

## 🛠️ Tecnologias Utilizadas

### Frontend (Interface)
* **React (Vite):** Framework principal.
* **CSS Puro (Custom Properties):** Design System moderno e responsivo.
* **Framer Motion:** Animações fluidas de interface.
* **Lucide React:** Ícones intuitivos.
* **Axios:** Comunicação com o backend.

### Backend (Motor Matemático)
* **Python 3:** Linguagem base.
* **Flask:** Servidor API REST.
* **Algoritmo RSA Customizado:** Implementação didática do algoritmo (Geração de Primos, MDC Estendido, Exponenciação Modular).

---

## 📦 Como Rodar o Projeto

Pré-requisitos: Você precisa ter o **Node.js** e o **Python** instalados no seu computador.

### 1. Configurando o Backend (Python)

Abra um terminal na pasta `backend`:

```bash
cd backend
