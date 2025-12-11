#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практикалық жұмыс 5: Мультимедиялық файлдарда жасырын хабарларды табу және шығару
Сурет, аудио, бейне файлдарда жасырын хабарларды табу
"""

from PIL import Image
import numpy as np
import cv2
from pydub import AudioSegment
import wave
import os

class MultimediaSteganalysis:
    def __init__(self):
        pass
    
    def analyze_image_lsb(self, image_path):
        """Суретте LSB талдау"""
        print(f"\n{'='*60}")
        print(f"Сурет LSB Талдауы: {image_path}")
        print(f"{'='*60}")
        
        try:
            img = Image.open(image_path).convert('RGB')
            arr = np.array(img)
            
            print(f"\nСурет өлшемі: {arr.shape}")
            print(f"Формат: {img.format}")
            
            # LSB биттерді есептеу
            lsb_zeros = 0
            lsb_ones = 0
            
            for channel in range(3):  # R, G, B
                channel_data = arr[:, :, channel]
                lsb = channel_data & 1
                lsb_zeros += np.sum(lsb == 0)
                lsb_ones += np.sum(lsb == 1)
            
            total = lsb_zeros + lsb_ones
            zero_ratio = lsb_zeros / total if total > 0 else 0
            one_ratio = lsb_ones / total if total > 0 else 0
            
            print(f"\nLSB Статистикасы:")
            print(f"  0 биттер: {lsb_zeros} ({zero_ratio*100:.2f}%)")
            print(f"  1 биттер: {lsb_ones} ({one_ratio*100:.2f}%)")
            
            # Теңгерім тексеру
            if abs(zero_ratio - 0.5) < 0.05:
                print("  ⚠ Күдікті: LSB теңгерім тым жақсы (жасырын хабар болуы мүмкін)")
            else:
                print("  ✓ LSB таралуы қалыпты")
            
            # LSB-ден мәтін шығаруға тырысу
            try:
                from stegano import lsb
                message = lsb.reveal(image_path)
                if message:
                    print(f"\n✓ Жасырын хабар табылды: {message[:100]}...")
                    return message
                else:
                    print("\n✗ Жасырын хабар табылмады")
            except:
                print("\n✗ stegano кітапханасымен хабар табылмады")
            
            return None
            
        except Exception as e:
            print(f"Қате: {e}")
            return None
    
    def analyze_audio(self, audio_path):
        """Аудио файлды талдау"""
        print(f"\n{'='*60}")
        print(f"Аудио Талдауы: {audio_path}")
        print(f"{'='*60}")
        
        try:
            if audio_path.endswith('.wav'):
                audio = AudioSegment.from_wav(audio_path)
            else:
                print("Тек WAV формат қолдауда")
                return None
            
            print(f"\nАудио параметрлері:")
            print(f"  Ұзақтығы: {len(audio)/1000:.2f} секунд")
            print(f"  Частота: {audio.frame_rate} Hz")
            print(f"  Каналдар: {audio.channels}")
            print(f"  Бит тереңдігі: {audio.sample_width * 8} бит")
            
            # LSB талдау
            samples = np.array(audio.get_array_of_samples())
            if audio.channels == 2:
                samples = samples.reshape((-1, 2)).mean(axis=1)
            
            lsb = samples & 1
            zeros = np.sum(lsb == 0)
            ones = np.sum(lsb == 1)
            
            print(f"\nLSB Статистикасы:")
            print(f"  0 биттер: {zeros} ({zeros/len(lsb)*100:.2f}%)")
            print(f"  1 биттер: {ones} ({ones/len(lsb)*100:.2f}%)")
            
            # FFT спектрлік талдау
            if len(samples) > 44100:
                fft = np.fft.fft(samples[:44100])
                freqs = np.abs(fft)
                max_freq_idx = np.argmax(freqs[1:]) + 1
                print(f"\nСпектрлік талдау:")
                print(f"  Ең жоғары жиілік: {max_freq_idx} Hz")
            
            return samples
            
        except Exception as e:
            print(f"Қате: {e}")
            return None
    
    def analyze_video(self, video_path):
        """Бейне файлды талдау"""
        print(f"\n{'='*60}")
        print(f"Бейне Талдауы: {video_path}")
        print(f"{'='*60}")
        
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                print("Бейне файлын ашу мүмкін емес")
                return None
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            print(f"\nБейне параметрлері:")
            print(f"  Кадрлар саны: {frame_count}")
            print(f"  FPS: {fps}")
            print(f"  Өлшемі: {width}x{height}")
            print(f"  Ұзақтығы: {frame_count/fps:.2f} секунд")
            
            # Алғашқы кадрды алу
            ret, frame = cap.read()
            if ret:
                cv2.imwrite('5/first_frame.png', frame)
                print(f"\n✓ Алғашқы кадр сақталды: first_frame.png")
                
                # Кадрдан LSB талдау
                self.analyze_image_lsb('5/first_frame.png')
            
            cap.release()
            return True
            
        except Exception as e:
            print(f"Қате: {e}")
            return None
    
    def compare_files(self, original_path, stego_path):
        """Екі файлды салыстыру"""
        print(f"\n{'='*60}")
        print("Файлдарды Салыстыру")
        print(f"{'='*60}")
        
        try:
            orig_size = os.path.getsize(original_path)
            stego_size = os.path.getsize(stego_path)
            
            print(f"\nӨлшемдер:")
            print(f"  Бастапқы: {orig_size} байт")
            print(f"  Стего: {stego_size} байт")
            print(f"  Айырмашылық: {stego_size - orig_size} байт")
            
            if stego_size > orig_size:
                print("  ⚠ Стего файл үлкенірек - жасырын дерек болуы мүмкін")
            
            # Суреттер үшін визуалды салыстыру
            if original_path.endswith(('.png', '.jpg', '.bmp')):
                orig_img = Image.open(original_path)
                stego_img = Image.open(stego_path)
                
                orig_arr = np.array(orig_img)
                stego_arr = np.array(stego_img)
                
                if orig_arr.shape == stego_arr.shape:
                    diff = np.abs(orig_arr.astype(int) - stego_arr.astype(int))
                    max_diff = np.max(diff)
                    mean_diff = np.mean(diff)
                    
                    print(f"\nПиксель айырмашылығы:")
                    print(f"  Максималды: {max_diff}")
                    print(f"  Орташа: {mean_diff:.2f}")
                    
                    if max_diff > 0:
                        print("  ⚠ Пиксельдерде өзгерістер бар")
            
        except Exception as e:
            print(f"Қате: {e}")


def main():
    analyzer = MultimediaSteganalysis()
    
    print("=" * 60)
    print("Мультимедиялық Файлдарда Жасырын Хабарларды Табу")
    print("=" * 60)
    
    # Мысал: сурет талдау
    # analyzer.analyze_image_lsb('sample.png')
    
    # Мысал: аудио талдау
    # analyzer.analyze_audio('sample.wav')
    
    # Мысал: бейне талдау
    # analyzer.analyze_video('sample.mp4')
    
    print("\nҚолдану: Функцияларды шақырыңыз немесе скриптті өзгертіңіз")


if __name__ == "__main__":
    main()

