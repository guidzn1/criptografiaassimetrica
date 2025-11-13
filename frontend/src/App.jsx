import React, { useState, useEffect, useRef } from 'react';
import { Send, Lock, RefreshCw, HelpCircle, Shield, Terminal, X } from 'lucide-react';
import axios from 'axios';
import './App.css';

const API_URL = 'http://localhost:5000';

// Modal Educativo
const Modal = ({ title, children, onClose }) => (
  <div className="modal-overlay" onClick={onClose}>
    <div className="modal-content" onClick={e => e.stopPropagation()}>
      <div className="modal-header">
        <h3>{title}</h3>
        <button className="close-icon" onClick={onClose}><X size={20}/></button>
      </div>
      <div className="modal-body">{children}</div>
    </div>
  </div>
);

// Painel de Log (Agora vertical)
const LogPanel = ({ logs }) => {
    const endRef = useRef(null);
    useEffect(() => { endRef.current?.scrollIntoView({ behavior: "smooth" }); }, [logs]);

    return (
        <div className="log-panel">
            <div className="log-header">
                <Terminal size={16} style={{marginRight: 8}}/> 
                Back-end Log (Python)
            </div>
            <div className="log-content">
                {logs.length === 0 && <div className="log-empty">Aguardando ações...</div>}
                {logs.map((log, i) => (
                    <div key={i} className="log-line">
                        <span className="log-time">[{log.time}]</span>
                        <span className={`log-text ${log.type}`}> {log.text}</span>
                    </div>
                ))}
                <div ref={endRef} />
            </div>
        </div>
    );
};

const Phone = ({ user, messages, onSend, onDecrypt, keysReady }) => {
  const [text, setText] = useState('');
  const chatRef = useRef(null);

  useEffect(() => {
    if (chatRef.current) chatRef.current.scrollTop = chatRef.current.scrollHeight;
  }, [messages]);

  return (
    <div className="phone-frame">
      <div className="notch"></div>
      <div className="screen">
        <header>
          <span className="carrier">RSA Secure</span>
          <span className="user-name">{user}</span>
        </header>
        
        <div className="chat-content" ref={chatRef}>
          {messages.length === 0 && (
            <div className="empty-state">
              <Shield size={48} opacity={0.1} />
              <p>Chat Criptografado</p>
            </div>
          )}
          
          {messages.map(msg => {
            const isMe = msg.sender === user;
            const showContent = isMe || msg.decrypted;

            return (
              <div key={msg.id} className={`bubble ${isMe ? 'me' : 'other'}`}>
                {!showContent ? (
                  <div className="encrypted-lock" onClick={() => onDecrypt(msg)}>
                    <div className="lock-icon-bg"><Lock size={14} color="#FFF"/></div>
                    <div className="lock-info">
                        <span className="hex-code">0x{msg.hex ? msg.hex.substring(0, 6) : '...'}..</span>
                        <small>Toque para ler</small>
                    </div>
                  </div>
                ) : (
                  <div className="msg-text">
                      {msg.content}
                      {isMe && !msg.decrypted && <span className="status-check">✓ Enviado cifrado</span>}
                  </div>
                )}
                <span className="time">{msg.time}</span>
              </div>
            );
          })}
        </div>

        <div className="input-bar">
          <input 
            disabled={!keysReady}
            value={text}
            onChange={e => setText(e.target.value)}
            onKeyPress={e => e.key === 'Enter' && (onSend(text), setText(''))}
            placeholder={keysReady ? "Mensagem..." : "Gere chaves"}
          />
          <button disabled={!text || !keysReady} onClick={() => { onSend(text); setText(''); }}>
            <Send size={16} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default function App() {
  const [chat, setChat] = useState([]); 
  const [logs, setLogs] = useState([]);
  const [keysReady, setKeysReady] = useState(false);
  const [showHelp, setShowHelp] = useState(false);
  const [loading, setLoading] = useState(false);

  const addLog = (text, type='info') => {
      const time = new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit', second:'2-digit'});
      setLogs(prev => [...prev, {time, text, type}]);
  };

  const generateKeys = async () => {
    setLoading(true);
    try {
      await axios.post(`${API_URL}/generate_keys`);
      setKeysReady(true);
      setChat([]); 
      setLogs([]);
      addLog("Iniciando servidor RSA...", "system");
      addLog("Gerando primos p e q para Alice...", "system");
      addLog("Gerando primos p e q para Bob...", "system");
      setTimeout(() => addLog("✓ Chaves Públicas/Privadas geradas!", "success"), 500);
    } catch (e) {
      alert("Erro: O backend Python não está respondendo.");
    }
    setLoading(false);
  };

  const handleSend = async (sender, text) => {
    const receiver = sender === 'Alice' ? 'Bob' : 'Alice';
    const tempId = Date.now();
    
    const msgEntry = {
      id: tempId,
      sender,
      receiver,
      content: text, 
      decrypted: false,
      time: new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'})
    };
    
    setChat(prev => [...prev, msgEntry]);
    addLog(`${sender}: Iniciando envio para ${receiver}`, "info");

    try {
      addLog(`> Buscando Chave Pública de ${receiver}...`, "math");
      addLog(`> Aplicando C = M^e mod n`, "math");
      
      const res = await axios.post(`${API_URL}/encrypt`, { sender, receiver, message: text });
      
      setChat(prev => prev.map(m => 
        m.id === tempId ? { 
          ...m, 
          encryptedData: res.data.encrypted_data, 
          hex: res.data.hex_view 
        } : m
      ));
      
      addLog(`✓ Criptografado: [${res.data.hex_view.substring(0, 15)}...]`, "success");

    } catch (e) {
      console.error(e);
      addLog("Erro ao criptografar.", "error");
    }
  };

  const handleDecrypt = async (msg) => {
    addLog(`${msg.receiver}: Recebeu mensagem cifrada.`, "info");
    addLog(`> Usando Chave Privada de ${msg.receiver}...`, "math");
    
    try {
      const res = await axios.post(`${API_URL}/decrypt`, {
        receiver: msg.receiver, 
        encrypted_data: msg.encryptedData
      });

      addLog(`> Aplicando M = C^d mod n`, "math");
      addLog(`✓ Texto original recuperado: "${res.data.original_message}"`, "success");

      setChat(prev => prev.map(m => 
        m.id === msg.id ? { ...m, decrypted: true, content: res.data.original_message } : m
      ));
    } catch (e) {
      addLog("Erro na descriptografia.", "error");
    }
  };

  return (
    <div className="app-container">
      <div className="header-controls">
        <h1>Simulador Criptografia RSA</h1>
        <div className="controls-right">
            <button className="btn-primary" onClick={generateKeys} disabled={loading}>
                <RefreshCw size={16} className={loading ? 'spin' : ''}/>
                {keysReady ? 'Resetar Chaves' : 'Gerar Chaves'}
            </button>
            <button className="btn-secondary" onClick={() => setShowHelp(true)}>
                <HelpCircle size={16} /> Ajuda
            </button>
            <div className={`status-indicator ${keysReady ? 'ready' : ''}`}>
                {keysReady ? 'ONLINE' : 'OFFLINE'}
            </div>
        </div>
      </div>

      <div className="split-layout">
        {/* LADO ESQUERDO: Celulares */}
        <div className="phones-section">
            <Phone 
                user="Alice" 
                messages={chat.filter(m => m.sender === 'Alice' || m.receiver === 'Alice')}
                onSend={(text) => handleSend('Alice', text)}
                onDecrypt={handleDecrypt}
                keysReady={keysReady}
            />
            
            <div className="connector">
                <div className="line"></div>
                <Shield size={24} color="#333" fill="#1c1c1e"/>
            </div>

            <Phone 
                user="Bob" 
                messages={chat.filter(m => m.sender === 'Bob' || m.receiver === 'Bob')}
                onSend={(text) => handleSend('Bob', text)}
                onDecrypt={handleDecrypt}
                keysReady={keysReady}
            />
        </div>

        {/* LADO DIREITO: Logs */}
        <div className="logs-section">
            <LogPanel logs={logs} />
        </div>
      </div>

      {showHelp && (
        <Modal title="Como funciona?" onClose={() => setShowHelp(false)}>
          <div className="step">
            <strong>1. Gerar Chaves</strong>
            <p>O Python cria chaves Matemáticas. A Pública embaralha, a Privada desembaralha.</p>
          </div>
          <div className="step">
            <strong>2. Envio Seguro</strong>
            <p>Alice usa a Chave Pública do Bob. A mensagem vira números ilegíveis (Log lateral).</p>
          </div>
          <div className="step">
            <strong>3. Descriptografia</strong>
            <p>Bob usa sua senha secreta (Chave Privada) para reverter a conta matemática.</p>
          </div>
        </Modal>
      )}
    </div>
  );
}