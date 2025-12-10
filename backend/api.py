from flask import Flask, request, jsonify
from flask_cors import CORS
from assimetry import RSA
import time

app = Flask(__name__)
CORS(app)

keys_db = {
    'Alice': {'public': None, 'private': None},
    'Bob': {'public': None, 'private': None}
}
rsa_engines = {'Alice': None, 'Bob': None}

def safe_int(val):
    try: return int(str(val).split('.')[0])
    except: raise ValueError(f"Valor inválido: {val}")

@app.route('/generate_keys', methods=['POST'])
def generate():
    try:
        for name in ['Alice', 'Bob']:
            engine = RSA(key_size=64) # Chaves pequenas para números legíveis
            pub, priv = engine.generate_keypair()
            rsa_engines[name] = engine
            keys_db[name] = {'public': pub, 'private': priv}
        
        return jsonify({
            'Alice': {'e': str(keys_db['Alice']['public'][0]), 'n': str(keys_db['Alice']['public'][1])},
            'Bob': {'e': str(keys_db['Bob']['public'][0]), 'n': str(keys_db['Bob']['public'][1])}
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/encrypt', methods=['POST'])
def encrypt_message():
    data = request.json
    try:
        sender = data.get('sender')
        receiver = data.get('receiver')
        message = data.get('message')
        with_signature = data.get('with_signature', False)
        
        all_logs = [] # Lista para acumular todos os passos

        # 1. CRIPTOGRAFIA
        rec_pub_key = keys_db[receiver]['public']
        if not rec_pub_key: return jsonify({'error': 'Chaves não geradas'}), 400
        
        engine = rsa_engines[sender]
        pub_key_clean = (safe_int(rec_pub_key[0]), safe_int(rec_pub_key[1]))
        
        # Recebe (dados, logs)
        encrypted_ints, enc_logs = engine.encrypt(message, pub_key_clean)
        all_logs.extend(enc_logs) # Adiciona logs de criptografia

        signature_ints = []
        
        # 2. ASSINATURA (Se ativada)
        if with_signature:
            sender_priv_key = keys_db[sender]['private']
            sig_ints, sig_logs = engine.sign(message, sender_priv_key)
            signature_ints = sig_ints
            all_logs.extend(sig_logs) # Adiciona logs de assinatura

        return jsonify({
            'encrypted_data': [str(x) for x in encrypted_ints],
            'signature_data': [str(x) for x in signature_ints] if with_signature else None,
            'hex_view': ' '.join([hex(x)[2:].upper() for x in encrypted_ints]),
            'detailed_logs': all_logs # ENVIA OS LOGS REAIS PARA O FRONT
        })
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/decrypt', methods=['POST'])
def decrypt_message():
    data = request.json
    try:
        receiver = data.get('receiver')
        sender = data.get('sender')
        encrypted_data = [safe_int(x) for x in data.get('encrypted_data')]
        signature_raw = data.get('signature_data')
        signature_data = [safe_int(x) for x in signature_raw] if signature_raw else None
        
        all_logs = []

        # 1. DESCRIPTOGRAFAR
        rec_priv_key = keys_db[receiver]['private']
        engine = rsa_engines[receiver]
        original_msg, dec_logs = engine.decrypt(encrypted_data, rec_priv_key)
        all_logs.extend(dec_logs)
        
        is_valid = None

        # 2. VERIFICAR ASSINATURA
        if signature_data:
            sender_pub_key = keys_db[sender]['public']
            sender_pub_clean = (safe_int(sender_pub_key[0]), safe_int(sender_pub_key[1]))
            is_valid, ver_logs = engine.verify_sign(original_msg, signature_data, sender_pub_clean)
            all_logs.extend(ver_logs)
        
        return jsonify({
            'original_message': original_msg,
            'is_valid': is_valid,
            'detailed_logs': all_logs # ENVIA OS LOGS REAIS
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)