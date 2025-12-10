import random
import math
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
    
    # ... (Mantenha os métodos is_prime, generate_prime, extended_gcd e mod_inverse iguais) ...
    def is_prime(self, n: int, k: int = 5) -> bool:
        if n <= 1: return False
        if n <= 3: return True
        if n % 2 == 0: return False
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
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
        x = y1 - (b // a) * x1
        y = x1
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
        while math.gcd(self.e, self.phi) != 1:
            self.e = random.randint(2, self.phi - 1)
        self.d = self.mod_inverse(self.e, self.phi)
        return ((self.e, self.n), (self.d, self.n))
    
    # --- CRIPTOGRAFIA DETALHADA ---
    def encrypt(self, message: str, public_key: Tuple[int, int]) -> Tuple[list, List[str]]:
        e, n = public_key
        encrypted = []
        logs = []
        
        logs.append(f"🔐 INICIANDO CRIPTOGRAFIA (Chave e={e}, n={n})")
        for char in message:
            m = ord(char) # Converte para ASCII
            # Fórmula: c = m^e mod n
            c = pow(m, e, n)
            encrypted.append(c)
            logs.append(f"   Caractere '{char}' (ASCII {m}) -> {m}^{e} mod {n} = {c}")
            
        return encrypted, logs

    def decrypt(self, encrypted_message: list, private_key: Tuple[int, int]) -> Tuple[str, List[str]]:
        d, n = private_key
        decrypted_chars = []
        logs = []
        
        logs.append(f"🔓 INICIANDO DESCRIPTOGRAFIA (Chave d={d}, n={n})")
        for c in encrypted_message:
            # Fórmula: m = c^d mod n
            m = pow(c, d, n)
            char = chr(m)
            decrypted_chars.append(char)
            logs.append(f"   Bloco {c} -> {c}^{d} mod {n} = {m} ('{char}')")
            
        return ''.join(decrypted_chars), logs

    # --- ASSINATURA DETALHADA ---
    def sign(self, message: str, private_key: Tuple[int, int]) -> Tuple[list, List[str]]:
        d, n = private_key
        signature = []
        logs = []
        
        logs.append(f"✍️ GERANDO ASSINATURA (Chave Privada d={d})")
        for char in message:
            m = ord(char)
            # Fórmula: s = m^d mod n
            s = pow(m, d, n)
            signature.append(s)
            logs.append(f"   Assinando '{char}' (ASCII {m}) -> {m}^{d} mod {n} = {s}")
            
        return signature, logs

    def verify_sign(self, message: str, signature: list, public_key: Tuple[int, int]) -> Tuple[bool, List[str]]:
        e, n = public_key
        logs = []
        logs.append(f"🔍 VERIFICANDO ASSINATURA (Chave Pública e={e})")
        
        try:
            recovered_chars = []
            for i, s in enumerate(signature):
                # Fórmula: m' = s^e mod n
                m_prime = pow(s, e, n)
                char = chr(m_prime)
                recovered_chars.append(char)
                logs.append(f"   Verificando bloco {s} -> {s}^{e} mod {n} = {m_prime} ('{char}')")
            
            recovered_msg = ''.join(recovered_chars)
            is_valid = (recovered_msg == message)
            
            if is_valid:
                logs.append(f"✅ SUCESSO: Mensagem recuperada '{recovered_msg}' bate com original.")
            else:
                logs.append(f"❌ FALHA: Mensagem recuperada '{recovered_msg}' NÃO bate com '{message}'.")
                
            return is_valid, logs
        except Exception as ex:
            logs.append(f"❌ ERRO MATEMÁTICO: {str(ex)}")
            return False, logs