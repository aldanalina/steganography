#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практикалық жұмыс 9: Текст және суретке жасырын хабар енгізу және оны жою
LSB, бос орындар және кодтау принциптері
"""

from PIL import Image
import numpy as np
from stegano import lsb
import os

class TextImageSteganography:
    def __init__(self):
        pass
    
    def hide_in_image_lsb(self, image_path, message, output_path):
        """Суретке LSB арқылы хабар енгізу"""
        print(f"\n{'='*60}")
        print("Суретке LSB Арқылы Хабар Енгізу")
        print(f"{'='*60}")
        
        try:
            secret = lsb.hide(image_path, message)
            secret.save(output_path)
            print(f"✓ Жасырын хабар енгізілді: {output_path}")
            return True
        except Exception as e:
            print(f"Қате: {e}")
            return False
    
    def reveal_from_image(self, image_path):
        """Суреттен хабарды шығару"""
        print(f"\n{'='*60}")
        print("Суреттен Хабарды Шығару")
        print(f"{'='*60}")
        
        try:
            message = lsb.reveal(image_path)
            if message:
                print(f"✓ Жасырын хабар: {message}")
                return message
            else:
                print("✗ Жасырын хабар табылмады")
                return None
        except Exception as e:
            print(f"Қате: {e}")
            return None
    
    def remove_stego_from_image(self, stego_image_path, output_path, method='recompress'):
        """Суреттен жасырын хабарды жою"""
        print(f"\n{'='*60}")
        print("Суреттен Жасырын Хабарды Жою")
        print(f"{'='*60}")
        
        try:
            img = Image.open(stego_image_path)
            
            if method == 'recompress':
                # JPEG-ке ауыстыру (сығу LSB-ті жояды)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img.save(output_path, 'JPEG', quality=85)
                print(f"✓ Файл қайта сығылды: {output_path}")
            
            elif method == 'resize':
                # Өлшемін өзгерту
                width, height = img.size
                new_size = (width - 1, height - 1)
                img_resized = img.resize(new_size, Image.LANCZOS)
                img_resized = img_resized.resize((width, height), Image.LANCZOS)
                img_resized.save(output_path)
                print(f"✓ Файл өлшемі өзгертілді: {output_path}")
            
            elif method == 'filter':
                # Фильтр қолдану
                from PIL import ImageFilter
                img_filtered = img.filter(ImageFilter.BLUR)
                img_filtered.save(output_path)
                print(f"✓ Фильтр қолданылды: {output_path}")
            
            return True
            
        except Exception as e:
            print(f"Қате: {e}")
            return False
    
    def hide_in_text_zerowidth(self, text, secret_message):
        """Текстке zero-width символдар арқылы хабар енгізу"""
        print(f"\n{'='*60}")
        print("Текстке Zero-Width Символдар Арқылы Хабар Енгізу")
        print(f"{'='*60}")
        
        def text_to_binary(msg):
            return ''.join(format(ord(c), '08b') for c in msg)
        
        binary = text_to_binary(secret_message)
        encoded = ''
        
        for i, char in enumerate(text):
            if i < len(binary):
                encoded += char
                # Zero-width space (0x200B) = 0, Zero-width non-joiner (0x200C) = 1
                if binary[i] == '0':
                    encoded += '\u200b'
                else:
                    encoded += '\u200c'
            else:
                encoded += char
        
        print(f"✓ Хабар енгізілді ({len(binary)} бит)")
        return encoded
    
    def reveal_from_text_zerowidth(self, encoded_text):
        """Тексттен zero-width символдардан хабарды шығару"""
        print(f"\n{'='*60}")
        print("Тексттен Zero-Width Символдардан Хабарды Шығару")
        print(f"{'='*60}")
        
        bits = ''
        for char in encoded_text:
            if char == '\u200b':
                bits += '0'
            elif char == '\u200c':
                bits += '1'
        
        # Биттерді байтқа топтастыру
        message = ''
        for i in range(0, len(bits), 8):
            if i + 8 <= len(bits):
                byte = bits[i:i+8]
                message += chr(int(byte, 2))
        
        if message:
            print(f"✓ Жасырын хабар: {message}")
            return message
        else:
            print("✗ Жасырын хабар табылмады")
            return None
    
    def remove_stego_from_text(self, stego_text):
        """Тексттен жасырын хабарды жою (copy-paste арқылы)"""
        print(f"\n{'='*60}")
        print("Тексттен Жасырын Хабарды Жою")
        print(f"{'='*60}")
        
        # Zero-width символдарды алып тастау
        cleaned = ''.join(ch for ch in stego_text if ch not in ['\u200b', '\u200c'])
        print(f"✓ Zero-width символдар алып тасталды")
        print(f"  Бастапқы ұзындық: {len(stego_text)}")
        print(f"  Тазартылған ұзындық: {len(cleaned)}")
        return cleaned
    
    def compare_images(self, original_path, stego_path):
        """Суреттерді салыстыру"""
        print(f"\n{'='*60}")
        print("Суреттерді Салыстыру")
        print(f"{'='*60}")
        
        try:
            orig_img = Image.open(original_path)
            stego_img = Image.open(stego_path)
            
            orig_arr = np.array(orig_img)
            stego_arr = np.array(stego_img)
            
            if orig_arr.shape != stego_arr.shape:
                print("⚠ Суреттердің өлшемдері әртүрлі")
                return
            
            diff = np.abs(orig_arr.astype(int) - stego_arr.astype(int))
            max_diff = np.max(diff)
            mean_diff = np.mean(diff)
            
            print(f"Максималды айырмашылық: {max_diff}")
            print(f"Орташа айырмашылық: {mean_diff:.2f}")
            
            if max_diff > 0:
                print("⚠ Пиксельдерде өзгерістер бар")
            else:
                print("✓ Пиксельдер бірдей")
                
        except Exception as e:
            print(f"Қате: {e}")


def main():
    stego = TextImageSteganography()
    
    print("=" * 60)
    print("Текст және Суретке Жасырын Хабар Енгізу және Жою")
    print("=" * 60)
    
    # Мысал: Текстке zero-width енгізу
    base_text = "Бұл тексеру үшін қолданылатын мәтін."
    secret = "Сәлем"
    encoded_text = stego.hide_in_text_zerowidth(base_text, secret)
    
    with open('9/encoded_text.txt', 'w', encoding='utf-8') as f:
        f.write(encoded_text)
    
    revealed = stego.reveal_from_text_zerowidth(encoded_text)
    cleaned = stego.remove_stego_from_text(encoded_text)
    
    print("\n" + "=" * 60)
    print("Тест аяқталды!")
    print("=" * 60)


if __name__ == "__main__":
    main()

