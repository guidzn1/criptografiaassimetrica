import random
import math
from typing import Tuple
import os
import time

class RSA:
    def __init__(self, key_size: int = 256):  
        self.key_size = key_size
        self.p = None
        self.q = None
        self.n = None
        self.phi = None
        self.e = None
        self.d = None
    
    def is_prime(self, n: int, k: int = 5) -> bool:
        """Teste de primalidade usando Miller-Rabin"""
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0:
            return False
        
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
        
        for _ in range(k):
            a = random.randint(2, n - 2)
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True
    
    def generate_prime(self) -> int:
        """Gerar um número primo grande"""
        print("🔍 Procurando número primo...")
        tentativas = 0
        while True:
            tentativas += 1
            num = random.getrandbits(self.key_size // 2)
            num |= (1 << (self.key_size // 2 - 1)) | 1
            if self.is_prime(num):
                print(f"✓ Primo encontrado após {tentativas} tentativas: {num}")
                return num
    
    def extended_gcd(self, a: int, b: int) -> Tuple[int, int, int]:
        """Algoritmo estendido de Euclides"""
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = self.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    def mod_inverse(self, a: int, m: int) -> int:
        """Calcular inverso modular"""
        print(f"🎯 Calculando inverso modular de {a} mod {m}")
        gcd, x, _ = self.extended_gcd(a, m)
        if gcd != 1:
            raise ValueError("Inverso modular não existe")
        resultado = (x % m + m) % m
        print(f"✓ Inverso modular encontrado: {resultado}")
        return resultado
    
    def generate_keypair(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Gerar par de chaves pública e privada com detalhes"""
        print("\n" + "="*60)
        print("🔑 INICIANDO GERAÇÃO DE CHAVES RSA")
        print("="*60)
        
        # Gerar dois primos grandes
        print("\n📊 PASSO 1: Gerando números primos p e q")
        self.p = self.generate_prime()
        self.q = self.generate_prime()
        
        # Garantir que são diferentes
        while self.p == self.q:
            self.q = self.generate_prime()
        
        print(f"✓ p = {self.p}")
        print(f"✓ q = {self.q}")
        
        # Calcular n e φ(n)
        print("\n📊 PASSO 2: Calculando n = p × q")
        self.n = self.p * self.q
        print(f"✓ n = {self.p} × {self.q} = {self.n}")
        
        print("\n📊 PASSO 3: Calculando φ(n) = (p-1) × (q-1)")
        self.phi = (self.p - 1) * (self.q - 1)
        print(f"✓ φ(n) = ({self.p}-1) × ({self.q}-1) = {self.phi}")
        
        # Escolher e (expoente público)
        print("\n📊 PASSO 4: Escolhendo expoente público e")
        self.e = 65537
        while math.gcd(self.e, self.phi) != 1:
            self.e = random.randint(2, self.phi - 1)
        print(f"✓ e = {self.e} (coprimo com φ(n))")
        
        # Calcular d (expoente privado)
        print("\n📊 PASSO 5: Calculando expoente privado d = e⁻¹ mod φ(n)")
        self.d = self.mod_inverse(self.e, self.phi)
        print(f"✓ d = {self.d}")
        
        print("\n🎉 CHAVES GERADAS COM SUCESSO!")
        print(f"🔓 Chave PÚBLICA: (e={self.e}, n={self.n})")
        print(f"🔐 Chave PRIVADA: (d={self.d}, n={self.n})")
        print("="*60)
        
        return ((self.e, self.n), (self.d, self.n))
    
    def encrypt_character(self, char: str, public_key: Tuple[int, int], show_steps: bool = True) -> int:
        """Criptografar um único caractere mostrando todos os passos"""
        e, n = public_key
        m = ord(char)
        
        if show_steps:
            print(f"\n📨 Criptografando caractere: '{char}' (ASCII: {m})")
            print(f"   Usando chave pública: e={e}, n={n}")
            print(f"   Fórmula: c = mᵉ mod n")
            print(f"   Cálculo: c = {m}^{e} mod {n}")
        
        c = pow(m, e, n)
        
        if show_steps:
            print(f"   Resultado: c = {c}")
        
        return c
    
    def encrypt(self, message: str, public_key: Tuple[int, int], show_steps: bool = True) -> list:
        """Criptografar mensagem com chave pública mostrando todos os passos"""
        if show_steps:
            print("\n" + "🔒"*30)
            print("INICIANDO CRIPTOGRAFIA DA MENSAGEM")
            print("🔒"*30)
            print(f"📝 Mensagem original: '{message}'")
        
        encrypted = []
        for i, char in enumerate(message):
            if show_steps:
                print(f"\n--- Caractere {i+1}/{len(message)} ---")
            c = self.encrypt_character(char, public_key, show_steps)
            encrypted.append(c)
        
        if show_steps:
            print(f"\n🎉 MENSAGEM CRIPTOGRAFADA:")
            print(f"   Texto original: '{message}'")
            print(f"   Texto cifrado: {encrypted}")
            print("🔒"*30)
        
        return encrypted
    
    def decrypt_character(self, c: int, private_key: Tuple[int, int], show_steps: bool = True) -> str:
        """Descriptografar um único caractere mostrando todos os passos"""
        d, n = private_key
        
        if show_steps:
            print(f"\n📨 Descriptografando bloco: {c}")
            print(f"   Usando chave privada: d={d}, n={n}")
            print(f"   Fórmula: m = cᵈ mod n")
            print(f"   Cálculo: m = {c}^{d} mod {n}")
        
        m = pow(c, d, n)
        char = chr(m)
        
        if show_steps:
            print(f"   Resultado: m = {m} → caractere: '{char}'")
        
        return char
    
    def decrypt(self, encrypted_message: list, private_key: Tuple[int, int], show_steps: bool = True) -> str:
        """Descriptografar mensagem com chave privada mostrando todos os passos"""
        if show_steps:
            print("\n" + "🔓"*30)
            print("INICIANDO DESCRIPTOGRAFIA DA MENSAGEM")
            print("🔓"*30)
            print(f"📫 Mensagem criptografada: {encrypted_message}")
        
        decrypted = []
        for i, c in enumerate(encrypted_message):
            if show_steps:
                print(f"\n--- Bloco {i+1}/{len(encrypted_message)} ---")
            char = self.decrypt_character(c, private_key, show_steps)
            decrypted.append(char)
        
        mensagem_final = ''.join(decrypted)
        
        if show_steps:
            print(f"\n🎉 MENSAGEM DESCRIPTOGRAFADA:")
            print(f"   Texto cifrado: {encrypted_message}")
            print(f"   Texto original: '{mensagem_final}'")
            print("🔓"*30)
        
        return mensagem_final

class Usuario:
    def __init__(self, nome: str):
        self.nome = nome
        self.rsa = RSA(128)  # Tamanho pequeno para números mais legíveis
        self.public_key, self.private_key = self.rsa.generate_keypair()
        self.conversas = {}
    
    def enviar_mensagem(self, mensagem: str, destinatario, mostrar_detalhes: bool = True) -> None:
        """Enviar mensagem criptografada para outro usuário"""
        if mostrar_detalhes:
            print(f"\n{'🚀'*20}")
            print(f"{self.nome} ESTÁ ENVIANDO MENSAGEM PARA {destinatario.nome}")
            print(f"{'🚀'*20}")
        
        # Criptografar mensagem
        mensagem_criptografada = self.rsa.encrypt(mensagem, destinatario.public_key, mostrar_detalhes)
        
        if mostrar_detalhes:
            print(f"\n✈️  TRANSMISSÃO: Mensagem criptografada enviada pela rede")
            print(f"   De: {self.nome}")
            print(f"   Para: {destinatario.nome}")
            print(f"   Dados transmitidos: {mensagem_criptografada}")
        
        # Destinatário recebe e descriptografa
        destinatario.receber_mensagem(mensagem_criptografada, self.nome, mensagem, mostrar_detalhes)
        
        # Armazenar na conversa
        if destinatario.nome not in self.conversas:
            self.conversas[destinatario.nome] = []
        self.conversas[destinatario.nome].append({
            'de': self.nome,
            'para': destinatario.nome,
            'mensagem': mensagem,
            'criptografada': mensagem_criptografada,
            'timestamp': time.time()
        })
    
    def receber_mensagem(self, mensagem_criptografada: list, remetente: str, mensagem_original: str, mostrar_detalhes: bool = True) -> None:
        """Receber mensagem"""
        if mostrar_detalhes:
            print(f"\n{'📩'*20}")
            print(f"{self.nome} ESTÁ RECEBENDO MENSAGEM DE {remetente}")
            print(f"{'📩'*20}")
        
        # Descriptografar mensagem
        mensagem_descriptografada = self.rsa.decrypt(mensagem_criptografada, self.private_key, mostrar_detalhes)
        
        # Armazenar na conversa
        if remetente not in self.conversas:
            self.conversas[remetente] = []
        self.conversas[remetente].append({
            'de': remetente,
            'para': self.nome,
            'mensagem': mensagem_original,
            'criptografada': mensagem_criptografada,
            'timestamp': time.time()
        })

def limpar_tela():
    """Limpar a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_resumo_chat(usuario_atual, outro_usuario):
    """Mostrar resumo da conversa"""
    limpar_tela()
    print(f"=== RESUMO DO CHAT: {usuario_atual.nome} ↔ {outro_usuario.nome} ===")
    print("💬 Visualização simplificada da conversa")
    print("-" * 60)
    
    conversa = usuario_atual.conversas.get(outro_usuario.nome, [])
    
    if not conversa:
        print("\n   💭 Nenhuma mensagem ainda...")
        print("   Digite '1' para começar a conversar!")
    else:
        for msg in conversa:
            if msg['de'] == usuario_atual.nome:
                print(f"\n→ [{msg['de']}] para {msg['para']}: {msg['mensagem']}")
            else:
                print(f"\n← [{msg['de']}] para {msg['para']}: {msg['mensagem']}")
    
    print("\n" + "-" * 60)

def chat_detalhado():
    """Chat que mostra TODOS os detalhes da criptografia"""
    limpar_tela()
    print("=== CHAT DETALHADO COM CRIPTOGRAFIA RSA ===")
    print("🔍 Você verá CADA PASSO do processo de criptografia!")
    
    # Criar usuários
    print("\n📋 CRIANDO USUÁRIOS...")
    alice = Usuario("Alice")
    input("\nPressione Enter para criar Bob...")
    bob = Usuario("Bob")
    
    print("\n🎉 USUÁRIOS PRONTOS! AGORA VOCÊ PODE:")
    print("   • Enviar mensagens entre Alice e Bob")
    print("   • Ver TODOS os cálculos matemáticos")
    print("   • Entender cada etapa da criptografia")
    
    input("\nPressione Enter para começar o chat...")
    
    usuario_atual = alice
    outro_usuario = bob
    
    while True:
        mostrar_resumo_chat(usuario_atual, outro_usuario)
        
        print(f"\n💡 Você está atualmente como: {usuario_atual.nome}")
        print(f"💡 Conversando com: {outro_usuario.nome}")
        
        print("\nOpções:")
        print("1. 📝 Enviar mensagem (ver TODOS os detalhes)")
        print("2. 🔄 Trocar de usuário")
        print("3. 📊 Ver informações das chaves")
        print("4. 🚪 Voltar ao menu principal")
        
        opcao = input("\nEscolha uma opção (1-4): ").strip()
        
        if opcao == "1":
            limpar_tela()
            print(f"=== {usuario_atual.nome} ENVIANDO MENSAGEM ===")
            mensagem = input(f"\nDigite a mensagem que {usuario_atual.nome} enviará para {outro_usuario.nome}: ")
            
            if mensagem.strip():
                usuario_atual.enviar_mensagem(mensagem, outro_usuario, mostrar_detalhes=True)
                print(f"\n✅ Mensagem completa processada!")
                input("\nPressione Enter para continuar...")
            else:
                print("❌ Mensagem não pode ser vazia!")
                input("\nPressione Enter para continuar...")
                
        elif opcao == "2":
            # Trocar usuário atual
            usuario_atual, outro_usuario = outro_usuario, usuario_atual
            print(f"✅ Agora você é {usuario_atual.nome}")
            input("\nPressione Enter para continuar...")
            
        elif opcao == "3":
            limpar_tela()
            print("=== INFORMAÇÕES DAS CHAVES RSA ===")
            print(f"\n🔑 {alice.nome}:")
            print(f"   Pública: (e={alice.public_key[0]}, n={alice.public_key[1]})")
            print(f"   Privada: (d={alice.private_key[0]}, n={alice.private_key[1]})")
            
            print(f"\n🔑 {bob.nome}:")
            print(f"   Pública: (e={bob.public_key[0]}, n={bob.public_key[1]})")
            print(f"   Privada: (d={bob.private_key[0]}, n={bob.private_key[1]})")
            
            print(f"\n📚 Lembrete:")
            print("   • Chave PÚBLICA: usada para CRIPTOGRAFAR")
            print("   • Chave PRIVADA: usada para DESCRIPTOGRAFAR")
            print("   • n = p × q (produto de dois primos)")
            print("   • Mensagem → Cifrada com pública do destinatário")
            print("   • Cifrada → Original com privada do destinatário")
            
            input("\nPressione Enter para voltar...")
            
        elif opcao == "4":
            print("\nSaindo do chat detalhado...")
            break
            
        else:
            print("❌ Opção inválida!")
            input("\nPressione Enter para continuar...")

def demonstracao_educativa():
    """Demonstração educativa mostrando o processo completo"""
    limpar_tela()
    print("=== AULA PRÁTICA: CRIPTOGRAFIA RSA ===")
    print("\nVamos acompanhar uma mensagem passo a passo...")
    
    input("\nPressione Enter para começar a demonstração...")
    
    # Criar usuários
    print("\n1. 🏗️  CRIANDO USUÁRIOS E CHAVES...")
    alice = Usuario("Alice")
    bob = Usuario("Bob")
    
    input("\nPressione Enter para ver uma mensagem sendo enviada...")
    
    # Mensagem de demonstração
    mensagem_teste = "Oi"
    print(f"\n2. 📨 ENVIANDO MENSAGEM: '{mensagem_teste}'")
    print(f"   De: Alice | Para: Bob")
    
    alice.enviar_mensagem(mensagem_teste, bob, mostrar_detalhes=True)
    
    print(f"\n🎓 RESUMO DO PROCESSO:")
    print("   1. Alice quer enviar 'Oi' para Bob")
    print("   2. Alice obtém a chave PÚBLICA de Bob")
    print("   3. Cada caractere é convertido para ASCII")
    print("   4. Para cada valor ASCII: c = mᵉ mod n")
    print("   5. Mensagem criptografada é enviada")
    print("   6. Bob recebe e usa sua chave PRIVADA")
    print("   7. Para cada bloco: m = cᵈ mod n")
    print("   8. Bob vê a mensagem original: 'Oi'")
    
    input("\nPressione Enter para voltar ao menu...")

def main():
    """Menu principal"""
    while True:
        limpar_tela()
        print("=== SISTEMA EDUCATIVO DE CRIPTOGRAFIA RSA ===")
        print("\nEscolha o modo de visualização:")
        print("\n1. 🔍 MODO DETALHADO COMPLETO")
        print("   • Veja CADA cálculo matemático")
        print("   • Acompanhe caractere por caractere")
        print("   • Entenda TODAS as etapas")
        print("")
        print("2. 🎓 AULA PRÁTICA")
        print("   • Demonstração guiada passo a passo")
        print("   • Explicações educativas")
        print("   • Perfeito para aprender")
        print("")
        print("3. 🚪 Sair")
        
        opcao = input("\nOpção (1-3): ").strip()
        
        if opcao == "1":
            chat_detalhado()
        elif opcao == "2":
            demonstracao_educativa()
        elif opcao == "3":
            print("\nObrigado por aprender sobre criptografia! 👋")
            break
        else:
            print("❌ Opção inválida!")
            input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()