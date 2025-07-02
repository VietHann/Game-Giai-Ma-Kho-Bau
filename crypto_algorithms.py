import base64
import hashlib
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import logging

class CryptoEngine:
   
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def caesar_encrypt(self, text, shift):
        result = ""
        for char in text:
            if char.isalpha():
                ascii_offset = 65 if char.isupper() else 97
                shifted = (ord(char) - ascii_offset + shift) % 26
                result += chr(shifted + ascii_offset)
            else:
                result += char
        return result
    
    def caesar_decrypt(self, text, shift):
        return self.caesar_encrypt(text, -shift)
    
    def vigenere_encrypt(self, text, keyword):
        result = ""
        keyword = keyword.upper()
        keyword_index = 0
        
        for char in text:
            if char.isalpha():
                ascii_offset = 65 if char.isupper() else 97
                char_upper = char.upper()
                key_char = keyword[keyword_index % len(keyword)]
                shift = ord(key_char) - 65
                
                encrypted_char = chr((ord(char_upper) - 65 + shift) % 26 + 65)
                result += encrypted_char if char.isupper() else encrypted_char.lower()
                keyword_index += 1
            else:
                result += char
        return result
    
    def vigenere_decrypt(self, text, keyword):
        result = ""
        keyword = keyword.upper()
        keyword_index = 0
        
        for char in text:
            if char.isalpha():
                ascii_offset = 65 if char.isupper() else 97
                char_upper = char.upper()
                key_char = keyword[keyword_index % len(keyword)]
                shift = ord(key_char) - 65
                
                decrypted_char = chr((ord(char_upper) - 65 - shift) % 26 + 65)
                result += decrypted_char if char.isupper() else decrypted_char.lower()
                keyword_index += 1
            else:
                result += char
        return result
    
    def gcd(self, a, b):
        while b:
            a, b = b, a % b
        return a
    
    def mod_inverse(self, a, m):
        if self.gcd(a, m) != 1:
            return None
        
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        _, x, _ = extended_gcd(a % m, m)
        return (x % m + m) % m
    
    def is_prime(self, n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_rsa_keys(self, bit_size=8):
        primes = [p for p in range(50, 200) if self.is_prime(p)]
        p = random.choice(primes)
        q = random.choice([x for x in primes if x != p])
        
        n = p * q
        phi = (p - 1) * (q - 1)
        
        e = 65537
        while e < phi and self.gcd(e, phi) != 1:
            e += 2
        
        if e >= phi:
            e = 3
        
        d = self.mod_inverse(e, phi)
        
        if d is None:
            return self.generate_rsa_keys(bit_size)
        
        return {
            'public': (n, e),
            'private': (n, d),
            'p': p, 'q': q
        }
    
    def rsa_encrypt_number(self, message_num, public_key):
        n, e = public_key
        return pow(message_num, e, n)
    
    def rsa_decrypt_number(self, cipher_num, private_key):
        n, d = private_key
        return pow(cipher_num, d, n)
    
    def rsa_encrypt(self, message, public_key):
        encrypted_chars = []
        for char in message:
            char_num = ord(char)
            encrypted_num = self.rsa_encrypt_number(char_num, public_key)
            encrypted_chars.append(str(encrypted_num))
        return ','.join(encrypted_chars)
    
    def rsa_decrypt(self, encrypted_message, private_key):
        try:
            encrypted_chars = encrypted_message.split(',')
            decrypted_chars = []
            for encrypted_char in encrypted_chars:
                encrypted_num = int(encrypted_char.strip())
                decrypted_num = self.rsa_decrypt_number(encrypted_num, private_key)
                decrypted_chars.append(chr(decrypted_num))
            return ''.join(decrypted_chars)
        except Exception as e:
            self.logger.error(f"RSA decryption error: {e}")
            raise
    
    def aes_encrypt(self, message, key):
        key = hashlib.sha256(key).digest()
        
        cipher = AES.new(key, AES.MODE_CBC)
        padded_message = pad(message.encode(), AES.block_size)
        encrypted = cipher.encrypt(padded_message)
        
        result = base64.b64encode(cipher.iv + encrypted).decode()
        return result
    
    def aes_decrypt(self, encrypted_message, key):
        try:
            key = hashlib.sha256(key).digest()
            
            encrypted_data = base64.b64decode(encrypted_message)
            iv = encrypted_data[:16]  
            encrypted = encrypted_data[16:]
            
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
            
            return decrypted.decode()
        except Exception as e:
            self.logger.error(f"AES decryption error: {e}")
            raise
