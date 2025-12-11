#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практикалық жоба 15: Ақпаратты жасырын пайдалану және оны қорғау стратегиясы жасау
Толық цикл: жасау → сақтау → тасымалдау → қорғау → анықтау
"""

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
from stegano import lsb
import os
import json
from datetime import datetime

class InformationProtectionStrategy:
    def __init__(self):
        self.key_storage = "15/keys"
        self.data_storage = "15/data"
        self.logs_storage = "15/logs"
        
        # Қалталарды жасау
        for dir_path in [self.key_storage, self.data_storage, self.logs_storage]:
            os.makedirs(dir_path, exist_ok=True)
    
    def create_message(self, message, metadata=None):
        """Хабарламаны жасау"""
        print(f"\n{'='*60}")
        print("Хабарламаны Жасау")
        print(f"{'='*60}")
        
        message_data = {
            'content': message,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        
        message_file = os.path.join(self.data_storage, f"message_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        with open(message_file, 'w', encoding='utf-8') as f:
            json.dump(message_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Хабарлама сақталды: {message_file}")
        return message_file
    
    def encrypt_message(self, message_file, key=None):
        """Хабарламаны шифрлау"""
        print(f"\n{'='*60}")
        print("Хабарламаны Шифрлау")
        print(f"{'='*60}")
        
        # Кілтті жасау немесе қолдану
        if key is None:
            key = get_random_bytes(16)
            key_file = os.path.join(self.key_storage, f"key_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bin")
            with open(key_file, 'wb') as f:
                f.write(key)
            print(f"✓ Жаңа кілт сақталды: {key_file}")
        
        # Хабарламаны оқу
        with open(message_file, 'r', encoding='utf-8') as f:
            message_data = json.load(f)
        
        message_content = message_data['content']
        
        # AES шифрлау
        cipher = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(message_content.encode('utf-8'))
        
        encrypted_data = base64.b64encode(nonce + ciphertext).decode()
        
        encrypted_file = message_file.replace('.txt', '_encrypted.txt')
        with open(encrypted_file, 'w', encoding='utf-8') as f:
            f.write(encrypted_data)
        
        print(f"✓ Хабарлама шифрланды: {encrypted_file}")
        return encrypted_file, key
    
    def hide_in_image(self, encrypted_file, cover_image_path, output_path):
        """Шифрланған хабарламаны суретке енгізу"""
        print(f"\n{'='*60}")
        print("Шифрланған Хабарламаны Суретке Енгізу")
        print(f"{'='*60}")
        
        # Шифрланған деректі оқу
        with open(encrypted_file, 'r', encoding='utf-8') as f:
            encrypted_data = f.read()
        
        # LSB арқылы енгізу
        secret_img = lsb.hide(cover_image_path, encrypted_data)
        secret_img.save(output_path)
        
        print(f"✓ Хабарлама суретке енгізілді: {output_path}")
        return output_path
    
    def extract_and_decrypt(self, stego_image_path, key):
        """Суреттен шығару және дешифрлеу"""
        print(f"\n{'='*60}")
        print("Суреттен Шығару және Дешифрлеу")
        print(f"{'='*60}")
        
        # LSB-ден шығару
        extracted = lsb.reveal(stego_image_path)
        
        if not extracted:
            print("✗ Жасырын хабар табылмады")
            return None
        
        # Base64 декодтау
        data = base64.b64decode(extracted)
        nonce = data[:16]
        ciphertext = data[16:]
        
        # AES дешифрлеу
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)
        
        print(f"✓ Хабарлама қалпына келтірілді: {plaintext.decode('utf-8')}")
        return plaintext.decode('utf-8')
    
    def log_operation(self, operation, details):
        """Операцияны логтау"""
        log_file = os.path.join(self.logs_storage, f"log_{datetime.now().strftime('%Y%m%d')}.txt")
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'details': details
        }
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    def create_protection_strategy(self):
        """Қорғау стратегиясын жасау"""
        strategy = """
Ақпаратты Қорғау Стратегиясы

1. Техникалық Деңгей:
   - Шифрлау: AES-256
   - Стеганография: LSB (PNG/BMP)
   - Кілт басқару: Бөлек сақтау
   - Логтау: Барлық операциялар

2. Ұйымдық Деңгей:
   - Ақпараттық қауіпсіздік саясаты
   - Деректерді жіберу/қабылдау логтары
   - Құпия деректермен жұмыс тәртібі
   - Оқыту және аудит

3. Қалпына Келтіру:
   - Резервтік көшірме сақтау
   - Бақылау және инцидентке әрекет ету жоспары
   - Хабар жоғалған жағдайда қалпына келтіру процедурасы

4. Қауіптер мен Қарсы Шаралар:
   - Файл сығылуы: Lossless формат пайдалану
   - Кілт ұрлануы: Кілтті бөлек тасымалдау
   - Анықтау: Шифрланған дерек + Random padding
   - Бұлттағы бұзылу: 2FA және шифрланған контейнерлер
"""
        
        strategy_file = os.path.join(self.data_storage, "protection_strategy.txt")
        with open(strategy_file, 'w', encoding='utf-8') as f:
            f.write(strategy)
        
        print(f"✓ Қорғау стратегиясы сақталды: {strategy_file}")
        return strategy_file


def main():
    strategy = InformationProtectionStrategy()
    
    print("=" * 60)
    print("Ақпаратты Жасыру және Қорғау Стратегиясы")
    print("=" * 60)
    
    # Толық цикл мысалы
    message = "Жасырын мәлімет: ProjectKey=AI2030"
    
    # 1. Хабарламаны жасау
    message_file = strategy.create_message(message, {'author': 'Test', 'priority': 'high'})
    
    # 2. Шифрлау
    encrypted_file, key = strategy.encrypt_message(message_file)
    
    # 3. Суретке енгізу (мысал - файл болса)
    # stego_file = strategy.hide_in_image(encrypted_file, 'cover.png', 'stego.png')
    
    # 4. Логтау
    strategy.log_operation('encrypt', {'file': encrypted_file})
    
    # 5. Стратегияны жасау
    strategy.create_protection_strategy()
    
    print("\n" + "=" * 60)
    print("Жоба аяқталды!")
    print("=" * 60)


if __name__ == "__main__":
    main()

