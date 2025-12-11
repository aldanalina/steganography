#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практикалық жұмыс 10: Қауіпті ақпаратты жасырын сақтау үшін кеңейтілген қолдану тәсілдері
Криптостеганография, контейнерлер, QR-код
"""

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
from stegano import lsb
import qrcode
from PIL import Image
import zipfile
import os

class AdvancedSteganography:
    def __init__(self):
        pass
    
    def crypto_steganography(self, image_path, message, key, output_path):
        """Криптостеганография: AES шифрлау + LSB енгізу"""
        print(f"\n{'='*60}")
        print("Криптостеганография: AES + LSB")
        print(f"{'='*60}")
        
        try:
            # 1. AES шифрлау
            cipher = AES.new(key, AES.MODE_EAX)
            nonce = cipher.nonce
            ciphertext, tag = cipher.encrypt_and_digest(message.encode('utf-8'))
            
            # 2. Біріктіру және Base64 кодтау
            encrypted_data = base64.b64encode(nonce + ciphertext).decode()
            print(f"✓ Хабар шифрланды ({len(encrypted_data)} таңба)")
            
            # 3. LSB арқылы суретке енгізу
            secret_img = lsb.hide(image_path, encrypted_data)
            secret_img.save(output_path)
            print(f"✓ Шифрланған хабар суретке енгізілді: {output_path}")
            
            return True
            
        except Exception as e:
            print(f"Қате: {e}")
            return False
    
    def crypto_steganography_reveal(self, stego_image_path, key):
        """Криптостеганографиядан хабарды шығару және дешифрлеу"""
        print(f"\n{'='*60}")
        print("Криптостеганографиядан Хабарды Шығару")
        print(f"{'='*60}")
        
        try:
            # 1. LSB-ден шығару
            encrypted_data = lsb.reveal(stego_image_path)
            if not encrypted_data:
                print("✗ Жасырын хабар табылмады")
                return None
            
            # 2. Base64 декодтау
            data = base64.b64decode(encrypted_data)
            nonce = data[:16]
            ciphertext = data[16:]
            
            # 3. AES дешифрлеу
            cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
            plaintext = cipher.decrypt(ciphertext)
            
            print(f"✓ Хабар дешифрленді: {plaintext.decode('utf-8')}")
            return plaintext.decode('utf-8')
            
        except Exception as e:
            print(f"Қате: {e}")
            return None
    
    def create_qr_code(self, data, output_path):
        """QR-код жасау"""
        print(f"\n{'='*60}")
        print("QR-код Жасау")
        print(f"{'='*60}")
        
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(output_path)
            print(f"✓ QR-код сақталды: {output_path}")
            return True
            
        except Exception as e:
            print(f"Қате: {e}")
            return False
    
    def hide_qr_in_image(self, qr_path, cover_image_path, output_path):
        """QR-кодты суретке енгізу"""
        print(f"\n{'='*60}")
        print("QR-кодты Суретке Енгізу")
        print(f"{'='*60}")
        
        try:
            qr_img = Image.open(qr_path)
            cover_img = Image.open(cover_image_path)
            
            # QR-кодты суретке орналастыру
            qr_resized = qr_img.resize((200, 200))
            cover_img.paste(qr_resized, (10, 10))
            cover_img.save(output_path)
            
            print(f"✓ QR-код суретке енгізілді: {output_path}")
            return True
            
        except Exception as e:
            print(f"Қате: {e}")
            return False
    
    def create_container(self, secret_file_path, container_path):
        """Контейнер жасау (ZIP)"""
        print(f"\n{'='*60}")
        print("Контейнер Жасау (ZIP)")
        print(f"{'='*60}")
        
        try:
            with zipfile.ZipFile(container_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(secret_file_path, os.path.basename(secret_file_path))
            
            print(f"✓ Контейнер жасалды: {container_path}")
            print(f"  Өлшемі: {os.path.getsize(container_path)} байт")
            return True
            
        except Exception as e:
            print(f"Қате: {e}")
            return False
    
    def extract_from_container(self, container_path, extract_dir):
        """Контейнерден файлды шығару"""
        print(f"\n{'='*60}")
        print("Контейнерден Файлды Шығару")
        print(f"{'='*60}")
        
        try:
            os.makedirs(extract_dir, exist_ok=True)
            
            with zipfile.ZipFile(container_path, 'r') as zipf:
                zipf.extractall(extract_dir)
            
            print(f"✓ Файлдар шығарылды: {extract_dir}")
            return True
            
        except Exception as e:
            print(f"Қате: {e}")
            return False
    
    def secure_delete(self, file_path, passes=3):
        """Қауіпсіз жою (shred)"""
        print(f"\n{'='*60}")
        print("Қауіпсіз Жою")
        print(f"{'='*60}")
        
        try:
            file_size = os.path.getsize(file_path)
            
            with open(file_path, 'ba+', buffering=0) as f:
                for _ in range(passes):
                    f.seek(0)
                    f.write(os.urandom(file_size))
                    f.flush()
                    os.fsync(f.fileno())
            
            os.remove(file_path)
            print(f"✓ Файл қауіпсіз жойылды ({passes} рет қайта жазылды)")
            return True
            
        except Exception as e:
            print(f"Қате: {e}")
            return False


def main():
    advanced = AdvancedSteganography()
    
    print("=" * 60)
    print("Кеңейтілген Стеганография")
    print("=" * 60)
    
    # Мысал: Криптостеганография
    key = get_random_bytes(16)
    message = "Құпия код: 5482-XZ"
    
    # Кілтті сақтау
    with open('10/key.bin', 'wb') as f:
        f.write(key)
    print(f"✓ Кілт сақталды: key.bin")
    
    # Мысал: QR-код
    advanced.create_qr_code("SecretKey=AI4567", "10/secret_qr.png")
    
    # Мысал: Контейнер
    test_file = "10/test_secret.txt"
    with open(test_file, 'w') as f:
        f.write("Confidential data")
    
    advanced.create_container(test_file, "10/secret_container.zip")
    
    print("\n" + "=" * 60)
    print("Тест аяқталды!")
    print("=" * 60)


if __name__ == "__main__":
    main()

