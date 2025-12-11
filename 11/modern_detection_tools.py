#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практикалық жұмыс 11: Қазіргі заманғы құралдарды қолдану арқылы жасырын хабарды анықтау
StegExpose, zsteg, StegDetect сияқты құралдарды симуляциялау
"""

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os

class ModernDetectionTools:
    def __init__(self):
        pass
    
    def stegexpose_simulation(self, image_path):
        """StegExpose симуляциясы - LSB және визуалды талдау"""
        print(f"\n{'='*60}")
        print(f"StegExpose Симуляциясы: {image_path}")
        print(f"{'='*60}")
        
        try:
            img = Image.open(image_path).convert('RGB')
            arr = np.array(img)
            
            # LSB талдау
            lsb_scores = []
            for i in range(3):
                channel = arr[:, :, i].flatten()
                lsb = channel & 1
                zeros = np.sum(lsb == 0)
                ones = np.sum(lsb == 1)
                total = zeros + ones
                
                if total > 0:
                    balance = abs(zeros - ones) / total
                    lsb_scores.append(balance)
            
            avg_balance = np.mean(lsb_scores)
            print(f"\nLSB теңгерім коэффициенті: {avg_balance:.4f}")
            
            # Энтропия
            def entropy(data):
                counts = np.bincount(data.flatten())
                probs = counts[counts > 0] / len(data.flatten())
                return -np.sum(probs * np.log2(probs))
            
            entropies = [entropy(arr[:, :, i]) for i in range(3)]
            avg_entropy = np.mean(entropies)
            print(f"Орташа энтропия: {avg_entropy:.4f}")
            
            # Нәтиже
            suspicion_score = 0
            if avg_balance < 0.1:
                suspicion_score += 50
                print("⚠ LSB теңгерім тым жақсы")
            
            if avg_entropy > 7.5:
                suspicion_score += 50
                print("⚠ Энтропия тым жоғары")
            
            print(f"\nКүдіктілік баллы: {suspicion_score}/100")
            
            if suspicion_score >= 50:
                print("⚠ КҮДІКТІ: Жасырын хабар болуы мүмкін")
                return True
            else:
                print("✓ ТАЗА: Жасырын хабар белгілері жоқ")
                return False
                
        except Exception as e:
            print(f"Қате: {e}")
            return False
    
    def zsteg_simulation(self, image_path):
        """zsteg симуляциясы - PNG/BMP LSB, palette, alpha-channel"""
        print(f"\n{'='*60}")
        print(f"zsteg Симуляциясы: {image_path}")
        print(f"{'='*60}")
        
        try:
            img = Image.open(image_path)
            
            # Формат тексеру
            print(f"Формат: {img.format}")
            print(f"Режим: {img.mode}")
            
            if img.mode == 'RGBA':
                print("\nAlpha канал талдауы:")
                arr = np.array(img)
                alpha = arr[:, :, 3]
                lsb_alpha = alpha & 1
                zeros = np.sum(lsb_alpha == 0)
                ones = np.sum(lsb_alpha == 1)
                print(f"  Alpha LSB: 0={zeros}, 1={ones}")
            
            # RGB каналдары
            if img.mode in ['RGB', 'RGBA']:
                arr = np.array(img.convert('RGB'))
                for i, ch in enumerate(['R', 'G', 'B']):
                    channel = arr[:, :, i]
                    lsb = channel & 1
                    zeros = np.sum(lsb == 0)
                    ones = np.sum(lsb == 1)
                    print(f"  {ch} канал LSB: 0={zeros}, 1={ones}")
            
            # LSB-ден мәтін іздеу
            try:
                from stegano import lsb
                message = lsb.reveal(image_path)
                if message:
                    print(f"\n✓ Жасырын хабар табылды: {message[:50]}...")
                    return message
            except:
                pass
            
            print("\n✗ Жасырын хабар табылмады")
            return None
            
        except Exception as e:
            print(f"Қате: {e}")
            return None
    
    def stegdetect_simulation(self, image_path):
        """StegDetect симуляциясы - JPEG стеганография"""
        print(f"\n{'='*60}")
        print(f"StegDetect Симуляциясы: {image_path}")
        print(f"{'='*60}")
        
        try:
            img = Image.open(image_path)
            
            if img.format != 'JPEG':
                print("StegDetect тек JPEG файлдар үшін")
                return None
            
            # JPEG DCT талдауы
            import cv2
            img_cv = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            
            if img_cv is None:
                print("Суретті ашу мүмкін емес")
                return None
            
            # DCT коэффициенттерін талдау
            h, w = img_cv.shape
            h = (h // 8) * 8
            w = (w // 8) * 8
            img_cv = img_cv[:h, :w]
            
            # Бірнеше блокты талдау
            anomalies = 0
            for y in range(0, min(64, h-8), 8):
                for x in range(0, min(64, w-8), 8):
                    block = img_cv[y:y+8, x:x+8].astype(np.float32) - 128
                    dct = cv2.dct(block)
                    
                    # Коэффициенттердің симметриясын тексеру
                    if np.abs(dct[0, 0]) > 1000:  # DC коэффициент
                        anomalies += 1
            
            print(f"\nDCT аномалиялар саны: {anomalies}")
            
            if anomalies > 10:
                print("⚠ КҮДІКТІ: DCT стеганография белгілері бар")
                return True
            else:
                print("✓ ТАЗА: DCT талдауы қалыпты")
                return False
                
        except Exception as e:
            print(f"Қате: {e}")
            return False
    
    def batch_analysis(self, image_dir):
        """Бірнеше файлды талдау"""
        print(f"\n{'='*60}")
        print(f"Batch Талдау: {image_dir}")
        print(f"{'='*60}")
        
        results = []
        
        for filename in os.listdir(image_dir):
            if filename.lower().endswith(('.png', '.jpg', '.bmp')):
                filepath = os.path.join(image_dir, filename)
                print(f"\nТалдау: {filename}")
                
                result = {
                    'file': filename,
                    'stegexpose': self.stegexpose_simulation(filepath),
                    'zsteg': self.zsteg_simulation(filepath),
                    'stegdetect': self.stegdetect_simulation(filepath) if filename.lower().endswith('.jpg') else None
                }
                results.append(result)
        
        # Нәтижелерді көрсету
        print(f"\n{'='*60}")
        print("Нәтижелер:")
        print(f"{'='*60}")
        for r in results:
            print(f"\n{r['file']}:")
            print(f"  StegExpose: {'Күдікті' if r['stegexpose'] else 'Таза'}")
            if r['zsteg']:
                print(f"  zsteg: Хабар табылды")
            if r['stegdetect'] is not None:
                print(f"  StegDetect: {'Күдікті' if r['stegdetect'] else 'Таза'}")
        
        return results
    
    def create_report(self, results, output_path):
        """Есеп жасау"""
        print(f"\n{'='*60}")
        print("Есеп Жасау")
        print(f"{'='*60}")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("Стегоанализ Есебі\n")
            f.write("=" * 60 + "\n\n")
            
            for r in results:
                f.write(f"Файл: {r['file']}\n")
                f.write(f"  StegExpose: {'Күдікті' if r['stegexpose'] else 'Таза'}\n")
                if r['zsteg']:
                    f.write(f"  zsteg: Хабар табылды\n")
                if r['stegdetect'] is not None:
                    f.write(f"  StegDetect: {'Күдікті' if r['stegdetect'] else 'Таза'}\n")
                f.write("\n")
        
        print(f"✓ Есеп сақталды: {output_path}")


def main():
    detector = ModernDetectionTools()
    
    print("=" * 60)
    print("Қазіргі Заманғы Анықтау Құралдары")
    print("=" * 60)
    
    # Мысал қолдану:
    # detector.stegexpose_simulation('suspect.png')
    # detector.zsteg_simulation('suspect.png')
    # detector.stegdetect_simulation('suspect.jpg')
    
    print("\nҚолдану: Функцияларды шақырыңыз немесе скриптті өзгертіңіз")


if __name__ == "__main__":
    main()

