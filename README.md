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

Instale as dependências necessárias:

Bash

# Windows
py -m pip install flask flask-cors

# Linux/Mac
pip3 install flask flask-cors
Inicie o servidor:

Bash

# Windows
py api.py

# Linux/Mac
python3 api.py
O servidor rodará em http://127.0.0.1:5000. Deixe este terminal aberto.

2. Configurando o Frontend (React)
Abra um novo terminal na pasta frontend:

Bash

cd frontend
Instale as dependências:

Bash

npm install
Inicie a interface:

Bash

npm run dev
O terminal mostrará um link (ex: http://localhost:5173). Clique nele para abrir o CryptoLab no seu navegador.

📚 Guia de Uso (Roteiro de Aula)
Início: Ao abrir, leia o tutorial de boas-vindas.

Gerar Chaves: Clique no botão "Iniciar". O backend calculará números primos e gerará as chaves para Alice e Bob.

Teste de Confidencialidade:

Certifique-se que o botão "Assinatura Digital" está DESLIGADO.

Envie uma mensagem de Alice para Bob.

Observe o cadeado azul (apenas cifrado).

Veja no Log lateral o cálculo de criptografia pura.

Teste de Autenticidade:

Ative o botão "Assinatura Digital" no cabeçalho.

Leia o modal explicativo sobre Integridade e Não-Repúdio.

Envie uma nova mensagem.

Observe o selo verde de "Autenticidade Garantida" ao receber.

Veja no Log lateral a verificação da assinatura matemática.

🤝 Contribuição
Este é um projeto acadêmico Open Source. Sinta-se à vontade para sugerir melhorias ou abrir Issues.

📄 Licença
Este projeto está sob a licença MIT.

Desenvolvido para a disciplina de Segurança de Sistemas Computacionais.
