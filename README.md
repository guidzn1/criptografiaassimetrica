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

- **🔑 Geração de Chaves RSA:** Visualização didática das chaves Pública $(e, n)$ e Privada $(d, n)$.
- **💬 Simulação de Chat (Alice & Bob):** Troca de mensagens em tempo real simulada.
- **🔒 Criptografia (Confidencialidade):** Garante que apenas o destinatário leia a mensagem.
- **✍️ Assinatura Digital (Autenticidade):** Garante a autoria, integridade e não-repúdio da mensagem.
- **🧮 Logs Matemáticos em Tempo Real:** Um terminal lateral exibe o passo a passo do cálculo:
  - Conversão ASCII.
  - Cálculo $C = M^e \pmod n$.
  - Verificação $M = C^d \pmod n$.
- **📱 Interface Responsiva:** Design moderno (Dark Mode) adaptável para Desktop e Mobile.
- **🎓 Tutoriais Integrados:** Modais educativos explicam os conceitos conforme o uso.

## 🛠️ Tecnologias Utilizadas

### Frontend (Interface)

- **React (Vite):** Framework principal.
- **CSS Puro (Custom Properties):** Design System moderno e responsivo.
- **Framer Motion:** Animações fluidas de interface.
- **Lucide React:** Ícones intuitivos.
- **Axios:** Comunicação com o backend.

### Backend (Motor Matemático)

- **Python 3:** Linguagem base.
- **Flask:** Servidor API REST.
- **Algoritmo RSA Customizado:** Implementação didática do algoritmo (Geração de Primos, MDC Estendido, Exponenciação Modular).

---

## 📦 Como Rodar o Projeto

**Pré-requisitos:**  
Você precisa ter o **Node.js** e o **Python 3** instalados no seu computador.

### 1. Configurando o Backend (Python)

Abra um terminal na pasta `backend`:

```bash
cd backend
```

Instale as dependências necessárias:

```bash
# Windows
py -m pip install flask flask-cors

# Linux/Mac
pip3 install flask flask-cors
```

Inicie o servidor:

```bash
# Windows
py api.py

# Linux/Mac
python3 api.py
```

O servidor rodará em:  
**http://127.0.0.1:5000**

> ⚠️ Deixe este terminal aberto enquanto estiver usando a aplicação.

---

### 2. Configurando o Frontend (React)

Abra um **novo terminal** na pasta `frontend`:

```bash
cd frontend
```

Instale as dependências:

```bash
npm install
```

Inicie a interface:

```bash
npm run dev
```

O terminal mostrará um link, por exemplo:  
**http://localhost:5173**

Acesse esse link no navegador para abrir o **CryptoLab**.

---

## 📚 Guia de Uso (Roteiro de Aula)

### 1. Início

- Ao abrir a aplicação, leia o **tutorial de boas-vindas**.
- Clique em **"Iniciar"** para carregar o ambiente do laboratório.

### 2. Gerar Chaves

- Clique no botão **"Gerar Chaves"** (ou equivalente).
- O backend irá:
  - Calcular números primos.
  - Gerar as chaves Pública e Privada para **Alice** e **Bob**.
- As chaves serão exibidas de forma didática na interface.

### 3. Teste de Confidencialidade (Criptografia)

1. Certifique-se de que o botão **"Assinatura Digital"** está **DESLIGADO**.
2. Envie uma mensagem de **Alice para Bob** pelo chat.
3. Observe:
   - O **cadeado azul**, indicando mensagem apenas cifrada.
   - No **Log lateral**, o passo a passo da criptografia:
     - Conversão da mensagem para ASCII / números.
     - Cálculo de $C = M^e \pmod n$.
4. Mostre aos alunos como a mensagem original não aparece em claro durante a transmissão.

### 4. Teste de Autenticidade (Assinatura Digital)

1. Ative o botão **"Assinatura Digital"** no cabeçalho.
2. Leia o **modal explicativo** sobre:
   - Integridade.
   - Autenticidade.
   - Não-repúdio.
3. Envie uma nova mensagem.
4. Observe:
   - O **selo verde** de **"Autenticidade Garantida"** na mensagem recebida.
   - No **Log lateral**, o processo de verificação da assinatura matemática.
5. Discuta com os alunos como a assinatura garante que:
   - A mensagem veio realmente de quem diz ter enviado.
   - O conteúdo não foi alterado no meio do caminho.

---

## 🤝 Contribuição

Este é um projeto acadêmico **Open Source**.  
Sinta-se à vontade para:

- Sugerir melhorias.
- Abrir **Issues**.
- Enviar **Pull Requests** com novas funcionalidades ou correções.

---

## 📄 Licença

Este projeto está sob a licença **MIT**.  
Você pode usar, modificar e distribuir o código, desde que mantenha os devidos créditos.

---

Desenvolvido para a disciplina de **Segurança de Sistemas Computacionais**. 🔐💻
