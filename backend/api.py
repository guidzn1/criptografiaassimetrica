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

@app.route('/', methods=['GET'])
def home():
    return jsonify({'status': 'Online', 'message': 'CryptoLab API Running'})

@app.route('/generate_keys', methods=['POST'])
def generate():
    try:
        for name in ['Alice', 'Bob']:
            engine = RSA(key_size=64)
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
        if not data: return jsonify({'error': 'Sem dados'}), 400
        
        sender = data.get('sender')
        receiver = data.get('receiver')
        message = data.get('message')
        with_signature = data.get('with_signature', False)
        
        # VERIFICAÇÃO DE CHAVES (Evita erro 500 se o servidor reiniciou)
        if not keys_db[receiver]['public'] or not rsa_engines[sender]:
            return jsonify({'error': 'SERVIDOR REINICIOU: Gere as chaves novamente!'}), 400
            
        rec_pub_key = keys_db[receiver]['public']
        engine = rsa_engines[sender]
        pub_key_clean = (safe_int(rec_pub_key[0]), safe_int(rec_pub_key[1]))
        
        all_logs = []
        
        # 1. Criptografar
        encrypted_ints, enc_logs = engine.encrypt(message, pub_key_clean)
        all_logs.extend(enc_logs)

        # 2. Assinar
        signature_ints = []
        if with_signature:
            sender_priv_key = keys_db[sender]['private']
            sig_ints, sig_logs = engine.sign(message, sender_priv_key)
            signature_ints = sig_ints
            all_logs.extend(sig_logs)

        return jsonify({
            'encrypted_data': [str(x) for x in encrypted_ints],
            'signature_data': [str(x) for x in signature_ints] if with_signature else None,
            'hex_view': ' '.join([hex(x)[2:].upper() for x in encrypted_ints]),
            'detailed_logs': all_logs
        })
    except Exception as e:
        print(f"Erro no encrypt: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/hack_attack', methods=['POST'])
def hack_attack():
    data = request.json
    try:
        receiver = data.get('receiver')
        if not keys_db[receiver]['public']:
             return jsonify({'error': 'Chaves perdidas. Gere novamente.'}), 400

        fake_message = "MENSAGEM ALTERADA POR EVE!"
        original_signature = data.get('original_signature')
        
        all_logs = ["⚠️ ALERTA: 'Eve' interceptou o pacote!", f"⚠️ HACK: Trocando conteúdo por '{fake_message}'..."]
        
        rec_pub_key = keys_db[receiver]['public']
        engine = RSA(key_size=64)
        pub_key_clean = (safe_int(rec_pub_key[0]), safe_int(rec_pub_key[1]))
        
        encrypted_fake, _ = engine.encrypt(fake_message, pub_key_clean)
        all_logs.append(f"⚠️ HACK: Criptografando falso com chave de {receiver}.")

        return jsonify({
            'encrypted_data': [str(x) for x in encrypted_fake],
            'signature_data': original_signature,
            'hex_view': 'DEAD BEEF 0000',
            'detailed_logs': all_logs
        })
    except Exception as e: return jsonify({'error': str(e)}), 500

@app.route('/decrypt', methods=['POST'])
def decrypt_message():
    data = request.json
    try:
        # PROTEÇÃO CONTRA DADOS VAZIOS
        if not data or 'encrypted_data' not in data:
            return jsonify({'error': 'Dados inválidos'}), 400

        receiver = data.get('receiver')
        sender = data.get('sender')
        
        # VERIFICAÇÃO DE CHAVES (O Pulo do Gato para o erro 400)
        if not keys_db[receiver]['private'] or not rsa_engines[receiver]:
            return jsonify({'error': 'SERVIDOR REINICIOU: As chaves sumiram da memória. Por favor, clique em INICIAR novamente.'}), 400

        encrypted_data = [safe_int(x) for x in data.get('encrypted_data')]
        signature_raw = data.get('signature_data')
        signature_data = [safe_int(x) for x in signature_raw] if signature_raw else None
        
        all_logs = []
        rec_priv_key = keys_db[receiver]['private']
        engine = rsa_engines[receiver]
        
        # 1. Descriptografar
        original_msg, dec_logs = engine.decrypt(encrypted_data, rec_priv_key)
        all_logs.extend(dec_logs)
        
        is_valid = None
        # 2. Verificar
        if signature_data:
            if not keys_db[sender]['public']: # Proteção extra
                 return jsonify({'error': 'Chave pública do remetente perdida.'}), 400
                 
            sender_pub_key = keys_db[sender]['public']
            sender_pub_clean = (safe_int(sender_pub_key[0]), safe_int(sender_pub_key[1]))
            is_valid, ver_logs = engine.verify_sign(original_msg, signature_data, sender_pub_clean)
            all_logs.extend(ver_logs)
        
        return jsonify({
            'original_message': original_msg,
            'is_valid': is_valid,
            'detailed_logs': all_logs
        })
    except Exception as e:
        print(f"Erro no decrypt: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)