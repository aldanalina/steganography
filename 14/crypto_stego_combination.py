#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практикалық жұмыс 14: Криптографиялық және стеганографиялық әдістерді біріктіру практикасы
AES шифрлау + LSB енгізу
"""

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
from stegano import lsb
from PIL import Image
import numpy as np
import os

class CryptoStegoCombination:
    def __init__(self):
        pass
    
    def encrypt_and_hide(self, image_path, message, key, output_path):
        """AES шифрлау + LSB енгізу"""
        print(f"\n{'='*60}")
        print("AES Шифрлау + LSB Енгізу")
        print(f"{'='*60}")
        
        try:
            # 1. AES шифрлау
            cipher = AES.new(key, AES.MODE_EAX)
            plaintext = message.encode('utf-8')
            nonce = cipher.nonce
            ciphertext, tag = cipher.encrypt_and_digest(plaintext)
            
            print(f"✓ Хабар шифрланды")
            print(f"  Бастапқы ұзындық: {len(plaintext)} байт")
            print(f"  Шифрланған ұзындық: {len(ciphertext)} байт")
            
            # 2. Base64 кодтау
            encrypted_data = base64.b64encode(nonce + ciphertext).decode()
            print(f"  Base64 ұзындығы: {len(encrypted_data)} таңба")
            
            # 3. LSB арқылы суретке енгізу
            secret_img = lsb.hide(image_path, encrypted_data)
            secret_img.save(output_path)
            
            # Өлшемдерді салыстыру
            orig_size = os.path.getsize(image_path)
            stego_size = os.path.getsize(output_path)
            
            print(f"✓ Шифрланған хабар суретке енгізілді: {output_path}")
            print(f"  Бастапқы өлшем: {orig_size} байт")
            print(f"  Стего өлшем: {stego_size} байт")
            print(f"  Айырмашылық: {stego_size - orig_size} байт")
            
            return True
            
        except Exception as e:
            print(f"Қате: {e}")
            return False
    
    def extract_and_decrypt(self, stego_image_path, key):
        """LSB-ден шығару + AES дешифрлеу"""
        print(f"\n{'='*60}")
        print("LSB Шығару + AES Дешифрлеу")
        print(f"{'='*60}")
        
        try:
            # 1. LSB-ден шығару
            extracted = lsb.reveal(stego_image_path)
            
            if not extracted:
                print("✗ Жасырын хабар табылмады")
                return None
            
            print(f"✓ Дерек LSB-ден шығарылды ({len(extracted)} таңба)")
            
            # 2. Base64 декодтау
            data = base64.b64decode(extracted)
            nonce = data[:16]
            ciphertext = data[16:]
            
            print(f"✓ Base64 декодталды")
            print(f"  Nonce: {len(nonce)} байт")
            print(f"  Ciphertext: {len(ciphertext)} байт")
            
            # 3. AES дешифрлеу
            cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
            plaintext = cipher.decrypt(ciphertext)
            
            print(f"✓ Хабар дешифрленді: {plaintext.decode('utf-8')}")
            return plaintext.decode('utf-8')
            
        except Exception as e:
            print(f"Қате: {e}")
            return None
    
    def compare_methods(self, image_path, message):
        """Әдістерді салыстыру"""
        print(f"\n{'='*60}")
        print("Әдістерді Салыстыру")
        print(f"{'='*60}")
        
        # 1. Тек LSB
        print("\n1. Тек LSB:")
        try:
            secret1 = lsb.hide(image_path, message)
            secret1.save('14/lsb_only.png')
            lsb_size = os.path.getsize('14/lsb_only.png')
            print(f"  Өлшем: {lsb_size} байт")
        except Exception as e:
            print(f"  Қате: {e}")
        
        # 2. AES + LSB
        print("\n2. AES + LSB:")
        key = get_random_bytes(16)
        try:
            cipher = AES.new(key, AES.MODE_EAX)
            nonce = cipher.nonce
            ciphertext, tag = cipher.encrypt_and_digest(message.encode('utf-8'))
            encrypted_data = base64.b64encode(nonce + ciphertext).decode()
            
            secret2 = lsb.hide(image_path, encrypted_data)
            secret2.save('14/aes_lsb.png')
            aes_lsb_size = os.path.getsize('14/aes_lsb.png')
            print(f"  Өлшем: {aes_lsb_size} байт")
            print(f"  Қауіпсіздік: Екі қабат қорғау (шифрлау + жасыру)")
        except Exception as e:
            print(f"  Қате: {e}")
    
    def test_key_security(self, stego_image_path, correct_key, wrong_key):
        """Кілт қауіпсіздігін тексеру"""
        print(f"\n{'='*60}")
        print("Кілт Қауіпсіздігін Тексеру")
        print(f"{'='*60}")
        
        # Дұрыс кілтпен
        print("\n1. Дұрыс кілтпен:")
        result1 = self.extract_and_decrypt(stego_image_path, correct_key)
        
        # Қате кілтпен
        print("\n2. Қате кілтпен:")
        try:
            result2 = self.extract_and_decrypt(stego_image_path, wrong_key)
            if result2:
                print("  ⚠ Қате кілтпен де ашылды (қауіпсіздік мәселесі!)")
            else:
                print("  ✓ Қате кілтпен ашылмады (қауіпсіз)")
        except Exception as e:
            print(f"  ✓ Қате кілтпен ашылмады: {e}")
    
    def analyze_entropy(self, original_path, stego_path):
        """Энтропия талдауы"""
        print(f"\n{'='*60}")
        print("Энтропия Талдауы")
        print(f"{'='*60}")
        
        def calculate_entropy(data):
            counts = np.bincount(data.flatten())
            probs = counts[counts > 0] / len(data.flatten())
            return -np.sum(probs * np.log2(probs))
        
        orig_img = Image.open(original_path).convert('RGB')
        stego_img = Image.open(stego_path).convert('RGB')
        
        orig_arr = np.array(orig_img)
        stego_arr = np.array(stego_img)
        
        orig_entropy = np.mean([calculate_entropy(orig_arr[:, :, i]) for i in range(3)])
        stego_entropy = np.mean([calculate_entropy(stego_arr[:, :, i]) for i in range(3)])
        
        print(f"Бастапқы энтропия: {orig_entropy:.4f}")
        print(f"Стего энтропия: {stego_entropy:.4f}")
        print(f"Айырмашылық: {stego_entropy - orig_entropy:.4f}")
        
        if stego_entropy > orig_entropy + 0.5:
            print("⚠ Энтропия артты (шифрланған/жасырылған дерек белгісі)")


def main():
    combo = CryptoStegoCombination()
    
    print("=" * 60)
    print("Криптография + Стеганография Біріктіру")
    print("=" * 60)
    
    # Мысал
    key = get_random_bytes(16)
    message = "Құпия хабар: ExamCode#4821"
    
    # Кілтті сақтау
    with open('14/key.bin', 'wb') as f:
        f.write(key)
    print(f"✓ Кілт сақталды: key.bin")
    
    # Мысал қолдану:
    # combo.encrypt_and_hide('cover.png', message, key, 'stego.png')
    # combo.extract_and_decrypt('stego.png', key)
    
    print("\nҚолдану: Функцияларды шақырыңыз немесе скриптті өзгертіңіз")


if __name__ == "__main__":
    main()

