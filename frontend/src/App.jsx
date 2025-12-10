import React, { useState, useEffect, useRef } from 'react';
import { Send, Lock, RefreshCw, Shield, Terminal, Key, Smartphone, ArrowRight, BookOpen, CheckCircle, AlertTriangle, Feather, Play, Fingerprint, X, Info } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import './App.css';

const rawUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000';
const API_URL = rawUrl.replace(/\/$/, ''); // Remove barra do final se tiver


// --- COMPONENTE: TOAST (Notificação Flutuante) ---
const Toast = ({ message, type, onClose }) => (
  <motion.div 
    initial={{ opacity: 0, y: 50 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: 20 }}
    className={`toast-notification ${type}`}
  >
    {type === 'error' && <AlertTriangle size={18} />}
    {type === 'info' && <Info size={18} />}
    {type === 'success' && <CheckCircle size={18} />}
    <span>{message}</span>
    <button onClick={onClose}><X size={14}/></button>
  </motion.div>
);

// --- COMPONENTE: TUTORIAL INICIAL ---
const Tutorial = ({ onComplete }) => {
  const [step, setStep] = useState(0);
  const steps = [
    { title: "Lab de Criptografia", desc: "Bem-vindo! Aqui você vai ver e controlar como a segurança da informação funciona de verdade.", icon: <Shield size={32} /> },
    { title: "1. Confidencialidade", desc: "Primeiro, testaremos a Criptografia Básica. Alice usa a Chave Pública de Bob para 'trancar' a mensagem.", icon: <Lock size={32} /> },
    { title: "2. Autenticidade", desc: "Depois, ative o botão 'Assinatura Digital'. Alice usará sua Chave Privada para provar que a mensagem é dela.", icon: <Fingerprint size={32} /> }
  ];

  return (
    <div className="tutorial-overlay">
      <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} className="tutorial-card">
        <div className="tut-icon">{steps[step].icon}</div>
        <h2 className="tut-title">{steps[step].title}</h2>
        <p className="tut-desc">{steps[step].desc}</p>
        <div className="tut-steps">{steps.map((_, i) => <div key={i} className={`dot ${i===step?'active':''}`} />)}</div>
        <button className="btn-primary full-width" onClick={() => step < steps.length - 1 ? setStep(step + 1) : onComplete()}>
          {step < steps.length - 1 ? "Próximo" : "Começar Experiência"} <ArrowRight size={16} />
        </button>
      </motion.div>
    </div>
  );
};

// --- COMPONENTE: MODAL EDUCATIVO DA ASSINATURA ---
const SignatureEducationModal = ({ onClose }) => (
  <div className="tutorial-overlay" style={{zIndex: 110}}>
    <motion.div initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="education-card">
      <div className="edu-header">
        <Fingerprint size={40} className="text-accent" />
        <h2>Modo Assinatura Ativado</h2>
      </div>
      
      <p className="edu-intro">
        Agora, além de cifrar a mensagem, o remetente usará sua <strong>Chave Privada</strong> para criar um selo matemático. Isso garante:
      </p>

      <div className="edu-grid">
        <div className="edu-item">
          <div className="edu-icon"><Feather size={20}/></div>
          <div>
            <strong>Autenticidade</strong>
            <p>Prova que <em>Alice é realmente Alice</em>. Só ela tem a chave privada.</p>
          </div>
        </div>
        <div className="edu-item">
          <div className="edu-icon"><Shield size={20}/></div>
          <div>
            <strong>Integridade</strong>
            <p>Se a mensagem for alterada no caminho, o selo "quebra" na verificação.</p>
          </div>
        </div>
        <div className="edu-item">
          <div className="edu-icon"><CheckCircle size={20}/></div>
          <div>
            <strong>Não Repúdio</strong>
            <p>O remetente não pode negar a autoria depois de assinar.</p>
          </div>
        </div>
      </div>

      <button className="btn-primary full-width" onClick={onClose}>
        Entendi, vamos testar!
      </button>
    </motion.div>
  </div>
);

// --- COMPONENTE: CELULAR ---
const Phone = ({ user, messages, onSend, onDecrypt, keysReady, onInputClick }) => {
  const [text, setText] = useState('');
  const chatRef = useRef(null);

  useEffect(() => { chatRef.current?.scrollTo({ top: chatRef.current.scrollHeight, behavior: 'smooth' }); }, [messages]);

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      if (!keysReady) { onInputClick(); return; }
      onSend(text);
      setText('');
    }
  };

  return (
    <div className="device-wrapper">
      <div className="phone-case">
        <div className="notch"></div>
        <div className="screen-content">
          <div className="chat-header">
            <div className="avatar" style={{background: user === 'Alice' ? '#ec4899' : '#3b82f6'}}>{user[0]}</div>
            <div className="user-info"><h3>{user}</h3><p>{keysReady ? '● Conexão Segura' : '○ Offline'}</p></div>
          </div>

          <div className="messages-list" ref={chatRef} onClick={() => !keysReady && onInputClick()}>
            <AnimatePresence>
              {messages.map((msg) => {
                const isMe = msg.sender === user;
                const showContent = isMe || msg.decrypted;
                return (
                  <motion.div key={msg.id} initial={{opacity:0, y:10}} animate={{opacity:1, y:0}} className={`bubble ${isMe?'me':'other'}`}>
                    {showContent ? (
                      <div>
                        <div className="msg-content">{msg.content}</div>
                        {msg.verified === true && <div className="security-badge valid"><Fingerprint size={10}/> Assinado por {msg.sender}</div>}
                        {msg.verified === false && <div className="security-badge invalid"><AlertTriangle size={10}/> Assinatura Falsa!</div>}
                        {msg.decrypted && !msg.signatureData && !isMe && <div className="security-badge warning"><Lock size={10}/> Apenas Confidencial</div>}
                      </div>
                    ) : (
                      <div className="locked-content" onClick={() => onDecrypt(msg)}>
                        <div className="lock-icon"><Lock size={16} /></div>
                        <div>
                          <div className="hex-preview">HEX: {msg.hex ? msg.hex.substring(0, 6) : '...'}...</div>
                          {msg.signatureData ? <div className="signature-hint"><Feather size={10}/> Pacote Assinado</div> : <span className="unlock-hint">Toque para ler</span>}
                        </div>
                      </div>
                    )}
                  </motion.div>
                );
              })}
            </AnimatePresence>
          </div>

          <div className="input-area" onClick={() => !keysReady && onInputClick()}>
            <input value={text} onChange={e => setText(e.target.value)} 
              placeholder={keysReady ? "Digite aqui..." : "Gere chaves primeiro 🔒"} 
              disabled={!keysReady}
              onKeyPress={handleKeyPress}
              style={{cursor: keysReady ? 'text' : 'not-allowed'}}
            />
            <button className="send-btn" disabled={!text||!keysReady} onClick={() => {onSend(text); setText('')}}>
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="white" d="m12.2 13l-.9.9q-.275.275-.275.7t.275.7t.7.275t.7-.275l2.6-2.6q.3-.3.3-.7t-.3-.7l-2.6-2.6q-.275-.275-.7-.275t-.7.275t-.275.7t.275.7l.9.9H9q-.425 0-.712.288T8 12t.288.713T9 13zm-.2 9q-2.075 0-3.9-.788t-3.175-2.137T2.788 15.9T2 12t.788-3.9t2.137-3.175T8.1 2.788T12 2t3.9.788t3.175 2.137T21.213 8.1T22 12t-.788 3.9t-2.137 3.175t-3.175 2.138T12 22m0-2q3.35 0 5.675-2.325T20 12t-2.325-5.675T12 4T6.325 6.325T4 12t2.325 5.675T12 20m0-8"/></svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

// --- APP PRINCIPAL ---
export default function App() {
  const [showTutorial, setShowTutorial] = useState(true);
  const [useGlobalSig, setUseGlobalSig] = useState(false);
  const [showSigEdu, setShowSigEdu] = useState(false);
  const [toast, setToast] = useState(null);
  
  const [chat, setChat] = useState([]); 
  const [logs, setLogs] = useState([]);
  const [keysReady, setKeysReady] = useState(false);
  const [keysDisplay, setKeysDisplay] = useState({ Alice: null, Bob: null });
  const logEndRef = useRef(null);

  useEffect(() => { logEndRef.current?.scrollIntoView({ behavior: "smooth" }); }, [logs]);
  
  const addLog = (text, type='info') => {
    const time = new Date().toLocaleTimeString('pt-BR', { hour:'2-digit', minute:'2-digit', second:'2-digit' });
    setLogs(prev => [...prev, {time, text, type}]);
  };

  const showToast = (msg, type='info') => { setToast({ msg, type }); setTimeout(() => setToast(null), 4000); };
  
  const handleNoKeysClick = () => { 
    showToast("⚠️ Gere as chaves primeiro!", "error"); 
    const btn = document.getElementById('start-btn'); 
    if(btn) { 
        btn.style.transform = "scale(1.1)"; 
        setTimeout(() => btn.style.transform = "scale(1)", 200); 
    } 
  };

  const toggleGlobalSig = () => {
      const newState = !useGlobalSig;
      if (newState) { setShowSigEdu(true); addLog("--- MODO ASSINATURA ATIVADO ---", "system"); } 
      else { showToast("Modo Simples: Apenas confidencialidade.", "info"); addLog("--- MODO SIMPLES ---", "system"); }
      setUseGlobalSig(newState);
  };

  const generateKeys = async () => {
    try {
      addLog("Iniciando motor criptográfico RSA...", "system");
      addLog("Buscando números primos grandes aleatórios...", "math");
      const res = await axios.post(`${API_URL}/generate_keys`);
      setKeysDisplay(res.data); setKeysReady(true); setChat([]); 
      addLog("Chaves prontas. Sistema Online.", "secure");
      showToast("Sistema Online!", "success");
    } catch (e) { alert("Backend Offline"); }
  };

  const handleSend = async (sender, text) => {
    const receiver = sender === 'Alice' ? 'Bob' : 'Alice';
    const tempId = Date.now();
    setChat(prev => [...prev, { id: tempId, sender, receiver, content: text, decrypted: false, time: new Date().toLocaleTimeString() }]);
    
    addLog(`[${sender}] Enviando...`, "info");

    try {
      const res = await axios.post(`${API_URL}/encrypt`, { 
          sender, receiver, message: text, with_signature: useGlobalSig 
      });
      
      // MOSTRA OS LOGS DETALHADOS QUE VIERAM DO PYTHON
      if (res.data.detailed_logs) {
          res.data.detailed_logs.forEach(log => {
              addLog(log, "math");
          });
      }
      
      setChat(prev => prev.map(m => m.id === tempId ? { ...m, encryptedData: res.data.encrypted_data, signatureData: res.data.signature_data, hex: res.data.hex_view } : m));
      addLog(`✓ Pacote transmitido.`, "system");
    } catch (e) { console.error(e); addLog("Erro envio", "error"); }
  };

  const handleDecrypt = async (msg) => {
    addLog(`[${msg.receiver}] Lendo...`, "info");
    
    try {
      const res = await axios.post(`${API_URL}/decrypt`, {
        receiver: msg.receiver, sender: msg.sender,
        encrypted_data: msg.encryptedData, signature_data: msg.signatureData
      });

      // MOSTRA OS LOGS DETALHADOS QUE VIERAM DO PYTHON
      if (res.data.detailed_logs) {
          res.data.detailed_logs.forEach(log => {
              let type = "math";
              if (log.includes("SUCESSO")) type = "secure";
              if (log.includes("FALHA") || log.includes("ERRO")) type = "error";
              addLog(log, type);
          });
      }

      setChat(prev => prev.map(m => m.id === msg.id ? { ...m, decrypted: true, content: res.data.original_message, verified: res.data.is_valid } : m));
    } catch (e) { addLog("Erro leitura", "error"); }
  };

  return (
    <div className="app-container">
      {showTutorial && <Tutorial onComplete={() => setShowTutorial(false)} />}
      {showSigEdu && <SignatureEducationModal onClose={() => setShowSigEdu(false)} />}
      <AnimatePresence>{toast && <Toast message={toast.msg} type={toast.type} onClose={() => setToast(null)} />}</AnimatePresence>

      <header className="app-header">
        <div className="logo"><Shield size={28} color="#3b82f6"/><div><h1>CryptoLab</h1><span>Simulador RSA</span></div></div>
        <div className="header-actions">
          <div className={`toggle-container ${useGlobalSig ? 'active' : ''}`} onClick={toggleGlobalSig} title={useGlobalSig ? "Desativar Assinatura" : "Ativar Assinatura"}>
              <div className="toggle-label"><span className="toggle-title">Assinatura Digital</span><span className="toggle-status">{useGlobalSig?'LIGADO':'DESLIGADO'}</span></div>
              <div className="toggle-switch"><div className="toggle-knob">{useGlobalSig?<Fingerprint size={12}/>:<Lock size={12}/>}</div></div>
          </div>
          <div className="divider"></div>
          <button className="btn btn-ghost" onClick={() => setShowTutorial(true)}><BookOpen size={18}/> Tutorial</button>
          <button id="start-btn" className={`btn ${keysReady ? 'btn-outline' : 'btn-primary'}`} onClick={generateKeys}>
            {keysReady ? <RefreshCw size={18}/> : <Play size={18}/>} {keysReady ? 'Resetar' : 'Iniciar'}
          </button>
        </div>
      </header>

      <div className="workspace">
        <div className="simulator-area">
          <Phone user="Alice" messages={chat.filter(m => m.sender==='Alice'||m.receiver==='Alice')} 
            onSend={(text) => handleSend('Alice', text)} 
            onDecrypt={handleDecrypt} keysReady={keysReady} onInputClick={handleNoKeysClick} />
          <div style={{display:'flex',flexDirection:'column',alignItems:'center',gap:'8px',opacity:0.5}}>
            <div style={{width:2,height:50,background:'#3f3f46'}}></div>{useGlobalSig ? <Fingerprint size={32} color="#30d158"/> : <Lock size={24} color="#666"/>}<div style={{width:2,height:50,background:'#3f3f46'}}></div>
          </div>
          <Phone user="Bob" messages={chat.filter(m => m.sender==='Bob'||m.receiver==='Bob')} 
            onSend={(text) => handleSend('Bob', text)} 
            onDecrypt={handleDecrypt} keysReady={keysReady} onInputClick={handleNoKeysClick} />
        </div>
        <div className="sidebar"><div className="sidebar-header"><Terminal size={16} style={{marginRight:8}} /> PROCESSAMENTO REAL</div>
          <div className="log-stream">
            {logs.length === 0 && <div style={{textAlign:'center', marginTop:40, opacity:0.3, fontSize:12}}>Aguardando início...</div>}
            {logs.map((log, i) => <div key={i} className="log-item"><span className="log-time">{log.time}</span><span className={`log-msg ${log.type}`}>{log.text}</span></div>)}
            <div ref={logEndRef} />
          </div>
          {keysReady && (
              <div className="sidebar-footer" style={{padding:15, background:'#27272a', borderTop:'1px solid #3f3f46', fontSize:10, color:'#a1a1aa', display:'flex', justifyContent:'space-between'}}>
                  <div style={{fontFamily:'monospace'}}><strong>Alice Pub:</strong> {keysDisplay.Alice?.e.substring(0,6)}...</div>
                  <div style={{fontFamily:'monospace'}}><strong>Bob Pub:</strong> {keysDisplay.Bob?.e.substring(0,6)}...</div>
              </div>
          )}
        </div>
      </div>
    </div>
  );
}