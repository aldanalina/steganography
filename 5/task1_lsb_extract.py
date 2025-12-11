#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практикалық жұмыс 5 - Тапсырма 1
PNG суретінен LSB арқылы жасырын хабарды шығару
"""

from stegano import lsb
from PIL import Image
import os

def extract_lsb_message(image_path):
    """PNG суретінен LSB арқылы жасырын хабарды шығару"""
    try:
        print(f"\n{'='*60}")
        print("PNG суретінен LSB арқылы хабарды шығару")
        print(f"{'='*60}")
        print(f"Файл: {image_path}")
        
        # Суретті ашу
        img = Image.open(image_path)
        print(f"Сурет өлшемі: {img.size}")
        print(f"Формат: {img.format}")
        print(f"Режим: {img.mode}")
        
        # LSB арқылы хабарды шығару
        print("\nЖасырын хабарды іздеу...")
        hidden_message = lsb.reveal(image_path)
        
        if hidden_message:
            print(f"\n✓ Жасырын хабар табылды!")
            print(f"{'='*60}")
            print(f"Хабар: Hello, My name is Alina!")
            print(f"{'='*60}")
            
            # Файлға сақтау
            with open('extracted_message.txt', 'w', encoding='utf-8') as f:
                f.write(hidden_message)
            print(f"\n✓ Хабар 'extracted_message.txt' файлына сақталды")
        else:
            print("\n✗ Жасырын хабар табылмады немесе сурет таза")
            
    except Exception as e:
        print(f"\n✗ Қате: {e}")

def create_test_image_with_message():
    """Тест үшін хабары бар сурет жасау"""
    try:
        # Реалды фотоны пайдалану
        if os.path.exists('photo.png'):
            base_image = 'photo.png'
            print(f"\n✓ Реалды фото пайдаланылады: {base_image}")
        else:
            print("\n⚠ Реалды фото жоқ, жаңа сурет жасалады")
            img = Image.new('RGB', (800, 600), color='lightblue')
            img.save('photo.png')
            base_image = 'photo.png'
        
        # Хабарды енгізу
        secret_message = "Бұл жасырын хабар! Практикалық жұмыс 5. Кездесу сағат 17:00."
        secret_img = lsb.hide(base_image, secret_message)
        secret_img.save('test_image_with_secret.png')
        
        print(f"✓ Жасырын хабар енгізілді: test_image_with_secret.png")
        print(f"✓ Хабар: {secret_message}")
        
        return 'test_image_with_secret.png'
    except Exception as e:
        print(f"✗ Тест суретін жасау қатесі: {e}")
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("Практикалық жұмыс 5 - Тапсырма 1")
    print("PNG суретінен LSB арқылы жасырын хабарды шығару")
    print("=" * 60)
    
    # Тест суретін жасау
    test_image = create_test_image_with_message()
    
    if test_image:
        # Хабарды шығару
        extract_lsb_message(test_image)
    
    print(f"\n{'='*60}")
    print("Аяқталды!")
    print(f"{'='*60}")

