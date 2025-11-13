from flask import Flask, request, jsonify
from flask_cors import CORS
from assimetry import RSA
import math

app = Flask(__name__)
CORS(app)

# Estado em memória
keys_db = {
    'Alice': {'public': None, 'private': None},
    'Bob': {'public': None, 'private': None}
}
rsa_engines = {'Alice': None, 'Bob': None}

def safe_int(val):
    """Converte seguramente para int, evitando erros de tipo"""
    try:
        return int(str(val).split('.')[0]) # Remove casas decimais se houver
    except:
        raise ValueError(f"Não foi possível converter para inteiro: {val}")

@app.route('/generate_keys', methods=['POST'])
def generate():
    try:
        # Gerando chaves de 64 bits (rápido e visualmente curto o suficiente)
        for name in ['Alice', 'Bob']:
            engine = RSA(key_size=64)
            pub, priv = engine.generate_keypair()
            rsa_engines[name] = engine
            keys_db[name] = {'public': pub, 'private': priv}
        
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/encrypt', methods=['POST'])
def encrypt_msg():
    data = request.json
    try:
        sender = data.get('sender')
        receiver = data.get('receiver')
        message = data.get('message')
        
        if not keys_db[receiver]['public']:
            return jsonify({'error': 'Chaves não geradas'}), 400

        # Pega a chave pública do DESTINATÁRIO
        e_key, n_key = keys_db[receiver]['public']
        pub_key_clean = (safe_int(e_key), safe_int(n_key))
        
        # Usa a engine do remetente apenas para chamar o método (matemática é agnóstica)
        # Mas na prática RSA, a criptografia usa apenas a chave pública do destino.
        engine = rsa_engines[sender]
        
        encrypted_ints = engine.encrypt(message, pub_key_clean, show_steps=False)
        
        # Retorna TUDO como string para não quebrar no JS
        return jsonify({
            'encrypted_data': [str(x) for x in encrypted_ints],
            'hex_view': ' '.join([hex(x)[2:].upper() for x in encrypted_ints])
        })
    except Exception as e:
        print(f"Erro encrypt: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/decrypt', methods=['POST'])
def decrypt_msg():
    data = request.json
    try:
        receiver = data.get('receiver')
        encrypted_data = data.get('encrypted_data') # Lista de Strings
        
        if not keys_db[receiver]['private']:
            return jsonify({'error': 'Chaves perdidas. Reinicie.'}), 400
            
        # Converte Strings -> Inteiros Python
        encrypted_ints = [safe_int(x) for x in encrypted_data]
        
        d_key, n_key = keys_db[receiver]['private']
        priv_key_clean = (safe_int(d_key), safe_int(n_key))
        
        engine = rsa_engines[receiver]
        original_msg = engine.decrypt(encrypted_ints, priv_key_clean, show_steps=False)
        
        return jsonify({'original_message': original_msg})
    except Exception as e:
        print(f"Erro decrypt: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)