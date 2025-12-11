#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практикалық жұмыс 7: Жасырын хабарларды бұзу (стегонализ) және анықтау тәсілдері
Стегоанализ - статистикалық, визуалдық және құралдық тәсілдер
"""

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import cv2

class Steganalysis:
    def __init__(self):
        pass
    
    def histogram_analysis(self, image_path):
        """Гистограмма талдауы"""
        print(f"\n{'='*60}")
        print(f"Гистограмма Талдауы: {image_path}")
        print(f"{'='*60}")
        
        img = Image.open(image_path).convert('RGB')
        arr = np.array(img)
        
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        colors = ['red', 'green', 'blue']
        channels = ['R', 'G', 'B']
        
        for i, (col, ch) in enumerate(zip(colors, channels)):
            channel = arr[:, :, i].flatten()
            axes[i].hist(channel, bins=256, color=col, alpha=0.7, edgecolor='black')
            axes[i].set_title(f'{ch} канал гистограммасы')
            axes[i].set_xlabel('Пиксель мәні')
            axes[i].set_ylabel('Жиілік')
        
        plt.tight_layout()
        plt.savefig('7/histogram_analysis.png', dpi=150)
        print("✓ Гистограмма сақталды: histogram_analysis.png")
        plt.close()
        
        return arr
    
    def lsb_histogram(self, image_path):
        """LSB бит таралуын тексеру"""
        print(f"\n{'='*60}")
        print(f"LSB Талдауы: {image_path}")
        print(f"{'='*60}")
        
        img = Image.open(image_path).convert('RGB')
        arr = np.array(img)
        
        lsb_counts = {0: 0, 1: 0}
        
        for i in range(3):  # R, G, B каналдары
            channel = arr[:, :, i].flatten()
            lsb = channel & 1
            lsb_counts[0] += int(np.sum(lsb == 0))
            lsb_counts[1] += int(np.sum(lsb == 1))
        
        total = lsb_counts[0] + lsb_counts[1]
        zero_ratio = lsb_counts[0] / total if total > 0 else 0
        one_ratio = lsb_counts[1] / total if total > 0 else 0
        
        print(f"\nLSB Статистикасы:")
        print(f"  0 биттер: {lsb_counts[0]} ({zero_ratio*100:.2f}%)")
        print(f"  1 биттер: {lsb_counts[1]} ({one_ratio*100:.2f}%)")
        
        # Теңгерім тексеру
        if abs(zero_ratio - 0.5) < 0.05:
            print("  ⚠ Күдікті: LSB теңгерім тым жақсы (жасырын хабар болуы мүмкін)")
            return True
        else:
            print("  ✓ LSB таралуы қалыпты")
            return False
    
    def chi_square_test(self, image_path):
        """χ² тесті"""
        print(f"\n{'='*60}")
        print(f"χ² Тесті: {image_path}")
        print(f"{'='*60}")
        
        img = Image.open(image_path).convert('RGB')
        arr = np.array(img)
        
        # Бір канал үшін (R)
        channel = arr[:, :, 0].flatten()
        
        # Жұп және тақ мәндерді санау
        even = np.sum((channel & 1) == 0)
        odd = np.sum((channel & 1) == 1)
        
        observed = [even, odd]
        expected = [len(channel) / 2, len(channel) / 2]
        
        chi2, p_value = stats.chisquare(observed, expected)
        
        print(f"\nχ² нәтижелері:")
        print(f"  χ² мәні: {chi2:.4f}")
        print(f"  p-мәні: {p_value:.6f}")
        
        if p_value < 0.05:
            print("  ⚠ Күдікті: Статистикалық маңызды айырмашылық (p < 0.05)")
            return True
        else:
            print("  ✓ Статистикалық айырмашылық жоқ")
            return False
    
    def visual_difference(self, original_path, suspect_path):
        """Визуалды айырмашылық талдауы"""
        print(f"\n{'='*60}")
        print("Визуалды Айырмашылық Талдауы")
        print(f"{'='*60}")
        
        img1 = cv2.imread(original_path)
        img2 = cv2.imread(suspect_path)
        
        if img1 is None or img2 is None:
            print("Суреттерді ашу мүмкін емес")
            return None
        
        # Айырмашылық картасы
        diff = cv2.absdiff(img1, img2)
        cv2.imwrite('7/difference.png', diff)
        print("✓ Айырмашылық картасы сақталды: difference.png")
        
        # Heatmap
        diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        plt.figure(figsize=(10, 8))
        plt.imshow(diff_gray, cmap='hot', interpolation='nearest')
        plt.colorbar()
        plt.title('Айырмашылық Heatmap')
        plt.savefig('7/difference_heatmap.png', dpi=150)
        print("✓ Heatmap сақталды: difference_heatmap.png")
        plt.close()
        
        return diff
    
    def entropy_analysis(self, image_path):
        """Энтропия талдауы"""
        print(f"\n{'='*60}")
        print(f"Энтропия Талдауы: {image_path}")
        print(f"{'='*60}")
        
        img = Image.open(image_path).convert('RGB')
        arr = np.array(img)
        
        def calculate_entropy(data):
            """Энтропияны есептеу"""
            counts = np.bincount(data.flatten())
            probs = counts[counts > 0] / len(data.flatten())
            entropy = -np.sum(probs * np.log2(probs))
            return entropy
        
        entropies = []
        for i in range(3):
            entropy = calculate_entropy(arr[:, :, i])
            entropies.append(entropy)
            print(f"  {['R', 'G', 'B'][i]} канал энтропиясы: {entropy:.4f}")
        
        avg_entropy = np.mean(entropies)
        print(f"\nОрташа энтропия: {avg_entropy:.4f}")
        
        # Жоғары энтропия - кодталған/жасырылған дерек белгісі
        if avg_entropy > 7.5:
            print("  ⚠ Күдікті: Энтропия тым жоғары (кодталған дерек болуы мүмкін)")
            return True
        else:
            print("  ✓ Энтропия қалыпты")
            return False
    
    def dct_analysis(self, image_path):
        """DCT талдауы (JPEG)"""
        print(f"\n{'='*60}")
        print(f"DCT Талдауы: {image_path}")
        print(f"{'='*60}")
        
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        if img is None:
            print("Суретті ашу мүмкін емес")
            return None
        
        # 8x8 блокқа бөлу
        h, w = img.shape
        h = (h // 8) * 8
        w = (w // 8) * 8
        img = img[:h, :w]
        
        # Алғашқы блокты DCT-ке түрлендіру
        block = img[0:8, 0:8].astype(np.float32) - 128
        dct = cv2.dct(block)
        
        print("\nDCT коэффициенттері (алғашқы 8x8 блок):")
        print(dct)
        
        # Коэффициенттердің таралуын талдау
        dct_flat = dct.flatten()
        print(f"\nDCT статистикасы:")
        print(f"  Минимум: {np.min(dct_flat):.2f}")
        print(f"  Максимум: {np.max(dct_flat):.2f}")
        print(f"  Орташа: {np.mean(dct_flat):.2f}")
        print(f"  Стандартты ауытқу: {np.std(dct_flat):.2f}")
        
        return dct


def main():
    analyzer = Steganalysis()
    
    print("=" * 60)
    print("Стегоанализ - Жасырын Хабарларды Анықтау")
    print("=" * 60)
    
    # Мысал қолдану:
    # analyzer.histogram_analysis('suspect.png')
    # analyzer.lsb_histogram('suspect.png')
    # analyzer.chi_square_test('suspect.png')
    # analyzer.entropy_analysis('suspect.png')
    # analyzer.visual_difference('original.png', 'suspect.png')
    
    print("\nҚолдану: Функцияларды шақырыңыз немесе скриптті өзгертіңіз")


if __name__ == "__main__":
    main()

