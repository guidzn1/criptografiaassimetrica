import random
import math
import hashlib
from typing import Tuple, List

class RSA:
    def __init__(self, key_size: int = 64):  
        self.key_size = key_size
        self.p = None
        self.q = None
        self.n = None
        self.phi = None
        self.e = None
        self.d = None
    
    # ... (Mantenha is_prime, generate_prime, extended_gcd, mod_inverse, generate_keypair IGUAIS) ...
    # Se quiser, copie e cole as funções matemáticas básicas do arquivo anterior aqui.
    # Vou focar nas funções de Criptografia e Assinatura que mudaram.

    def is_prime(self, n: int, k: int = 5) -> bool:
        if n <= 1: return False
        if n <= 3: return True
        if n % 2 == 0: return False
        r, d = 0, n - 1
        while d % 2 == 0: r += 1; d //= 2
        for _ in range(k):
            a = random.randint(2, n - 2)
            x = pow(a, d, n)
            if x == 1 or x == n - 1: continue
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1: break
            else: return False
        return True
    
    def generate_prime(self) -> int:
        while True:
            num = random.getrandbits(self.key_size // 2)
            num |= (1 << (self.key_size // 2 - 1)) | 1
            if self.is_prime(num): return num

    def extended_gcd(self, a: int, b: int) -> Tuple[int, int, int]:
        if a == 0: return b, 0, 1
        gcd, x1, y1 = self.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1; y = x1
        return gcd, x, y

    def mod_inverse(self, a: int, m: int) -> int:
        gcd, x, _ = self.extended_gcd(a, m)
        if gcd != 1: raise ValueError("Inverso modular não existe")
        return (x % m + m) % m

    def generate_keypair(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        self.p = self.generate_prime()
        self.q = self.generate_prime()
        while self.p == self.q: self.q = self.generate_prime()
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = 65537
        while math.gcd(self.e, self.phi) != 1: self.e = random.randint(2, self.phi - 1)
        self.d = self.mod_inverse(self.e, self.phi)
        return ((self.e, self.n), (self.d, self.n))
    
    # --- CRIPTOGRAFIA (Confidencialidade) ---
    def encrypt(self, message: str, public_key: Tuple[int, int]) -> Tuple[list, List[str]]:
        e, n = public_key
        encrypted = []
        logs = []
        logs.append(f"🔒 CRIPTOGRAFIA: Iniciando para '{message}'...")
        for char in message:
            m = ord(char)
            c = pow(m, e, n)
            encrypted.append(c)
        logs.append(f"   Mensagem cifrada com sucesso (c = m^{e} mod n)")
        return encrypted, logs

    def decrypt(self, encrypted_message: list, private_key: Tuple[int, int]) -> Tuple[str, List[str]]:
        d, n = private_key
        decrypted_chars = []
        logs = []
        logs.append(f"🔓 DESCRIPTOGRAFIA: Usando chave privada...")
        for c in encrypted_message:
            m = pow(c, d, n)
            decrypted_chars.append(chr(m))
        msg = ''.join(decrypted_chars)
        logs.append(f"   Mensagem recuperada: '{msg}'")
        return msg, logs

    # --- ASSINATURA DIGITAL COM HASH (Autenticidade + Integridade) ---
    def sign(self, message: str, private_key: Tuple[int, int]) -> Tuple[list, List[str]]:
        d, n = private_key
        logs = []
        
        # 1. HASHING (O Resumo)
        message_hash = hashlib.sha256(message.encode()).hexdigest()
        logs.append(f"📝 HASHING: Gerando 'Digital Fingerprint' (SHA-256)")
        logs.append(f"   Hash da mensagem '{message}': {message_hash[:10]}...")
        
        # 2. ASSINATURA (Cifra o Hash com a Privada)
        signature = []
        logs.append(f"✍️ ASSINATURA: Cifrando o Hash com chave Privada (d={d})")
        for char in message_hash: # Assina o HASH, não a mensagem
            m = ord(char)
            s = pow(m, d, n)
            signature.append(s)
            
        return signature, logs

    def verify_sign(self, message: str, signature: list, public_key: Tuple[int, int]) -> Tuple[bool, List[str]]:
        e, n = public_key
        logs = []
        logs.append(f"🔍 VERIFICAÇÃO: Iniciando auditoria de integridade...")
        
        try:
            # 1. RECUPERAR O HASH DA ASSINATURA
            recovered_hash_chars = []
            for s in signature:
                m_prime = pow(s, e, n)
                recovered_hash_chars.append(chr(m_prime))
            recovered_hash = ''.join(recovered_hash_chars)
            logs.append(f"   Hash recuperado da assinatura: {recovered_hash[:10]}...")
            
            # 2. CALCULAR HASH DA MENSAGEM RECEBIDA
            calculated_hash = hashlib.sha256(message.encode()).hexdigest()
            logs.append(f"   Hash calculado da mensagem atual: {calculated_hash[:10]}...")
            
            # 3. COMPARAR
            is_valid = (recovered_hash == calculated_hash)
            
            if is_valid:
                logs.append(f"✅ SUCESSO: Os Hashes coincidem! Integridade e Autoria confirmadas.")
            else:
                logs.append(f"❌ ALERTA DE PERIGO: Hashes diferentes! A mensagem foi alterada.")
                
            return is_valid, logs
        except Exception as ex:
            logs.append(f"❌ ERRO: Falha na verificação: {str(ex)}")
            return False, logs