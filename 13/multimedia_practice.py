#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практикалық жұмыс 13: Мультимедиялық файлдардағы ақпаратты жасырудың практикасы мен проблемалары
Сурет, аудио, бейне файлдарда жасыру және шығару
"""

from PIL import Image
import numpy as np
import cv2
from stegano import lsb
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import wave
import os

class MultimediaPractice:
    def __init__(self):
        pass
    
    def hide_text_in_image_lsb(self, image_path, message, output_path):
        """Суретке LSB арқылы мәтін енгізу"""
        print(f"\n{'='*60}")
        print("Суретке LSB Арқылы Мәтін Енгізу")
        print(f"{'='*60}")
        
        try:
            secret = lsb.hide(image_path, message)
            secret.save(output_path)
            
            # Өлшемдерді салыстыру
            orig_size = os.path.getsize(image_path)
            stego_size = os.path.getsize(output_path)
            
            print(f"✓ Хабар енгізілді: {output_path}")
            print(f"  Бастапқы өлшем: {orig_size} байт")
            print(f"  Стего өлшем: {stego_size} байт")
            print(f"  Айырмашылық: {stego_size - orig_size} байт")
            
            return True
            
        except Exception as e:
            print(f"Қате: {e}")
            return False
    
    def hide_text_in_image_aes_lsb(self, image_path, message, key, output_path):
        """Суретке AES+LSB арқылы мәтін енгізу"""
        print(f"\n{'='*60}")
        print("Суретке AES+LSB Арқылы Мәтін Енгізу")
        print(f"{'='*60}")
        
        try:
            # AES шифрлау
            cipher = AES.new(key, AES.MODE_EAX)
            nonce = cipher.nonce
            ciphertext, tag = cipher.encrypt_and_digest(message.encode('utf-8'))
            
            # Base64 кодтау
            encrypted_data = base64.b64encode(nonce + ciphertext).decode()
            
            # LSB енгізу
            secret = lsb.hide(image_path, encrypted_data)
            secret.save(output_path)
            
            print(f"✓ Шифрланған хабар енгізілді: {output_path}")
            return True
            
        except Exception as e:
            print(f"Қате: {e}")
            return False
    
    def reveal_from_image(self, image_path, key=None):
        """Суреттен хабарды шығару"""
        print(f"\n{'='*60}")
        print("Суреттен Хабарды Шығару")
        print(f"{'='*60}")
        
        try:
            extracted = lsb.reveal(image_path)
            
            if not extracted:
                print("✗ Хабар табылмады")
                return None
            
            # AES дешифрлеу қажет болса
            if key:
                try:
                    data = base64.b64decode(extracted)
                    nonce = data[:16]
                    ciphertext = data[16:]
                    
                    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
                    plaintext = cipher.decrypt(ciphertext)
                    print(f"✓ Дешифрленген хабар: {plaintext.decode('utf-8')}")
                    return plaintext.decode('utf-8')
                except:
                    pass
            
            print(f"✓ Хабар: {extracted}")
            return extracted
            
        except Exception as e:
            print(f"Қате: {e}")
            return None
    
    def hide_in_audio_wav(self, audio_path, message, output_path):
        """WAV аудиоға LSB арқылы мәтін енгізу"""
        print(f"\n{'='*60}")
        print("WAV Аудиоға LSB Арқылы Мәтін Енгізу")
        print(f"{'='*60}")
        
        try:
            wf = wave.open(audio_path, 'rb')
            params = wf.getparams()
            frames = wf.readframes(wf.getnframes())
            samples = np.frombuffer(frames, dtype=np.int16)
            wf.close()
            
            # Мәтінді биттерге айналдыру
            bits = ''.join(format(b, '08b') for b in message.encode('utf-8')) + '00000000'
            
            if len(bits) > len(samples):
                print("✗ Аудио сыйымдылығы жетпейді")
                return False
            
            # LSB алмастыру
            samples_copy = samples.copy()
            for i, bit in enumerate(bits):
                samples_copy[i] = (samples_copy[i] & ~1) | int(bit)
            
            # Сақтау
            out = wave.open(output_path, 'wb')
            out.setparams(params)
            out.writeframes(samples_copy.tobytes())
            out.close()
            
            print(f"✓ Хабар аудиоға енгізілді: {output_path}")
            return True
            
        except Exception as e:
            print(f"Қате: {e}")
            return False
    
    def reveal_from_audio_wav(self, audio_path):
        """WAV аудиодан хабарды шығару"""
        print(f"\n{'='*60}")
        print("WAV Аудиодан Хабарды Шығару")
        print(f"{'='*60}")
        
        try:
            wf = wave.open(audio_path, 'rb')
            frames = wf.readframes(wf.getnframes())
            samples = np.frombuffer(frames, dtype=np.int16)
            wf.close()
            
            # LSB биттерді жинау
            bits = ''.join(str(samples[i] & 1) for i in range(len(samples)))
            
            # Байтқа топтастыру
            message = ''
            for i in range(0, len(bits), 8):
                byte = bits[i:i+8]
                if len(byte) == 8:
                    char_code = int(byte, 2)
                    if char_code == 0:
                        break
                    message += chr(char_code)
            
            if message:
                print(f"✓ Хабар: {message}")
                return message
            else:
                print("✗ Хабар табылмады")
                return None
                
        except Exception as e:
            print(f"Қате: {e}")
            return None
    
    def hide_in_video_frame(self, video_path, message, output_path):
        """Бейне кадрына мәтін енгізу"""
        print(f"\n{'='*60}")
        print("Бейне Кадрына Мәтін Енгізу")
        print(f"{'='*60}")
        
        try:
            cap = cv2.VideoCapture(video_path)
            ret, frame = cap.read()
            
            if not ret:
                print("Бейне файлын ашу мүмкін емес")
                return False
            
            # Алғашқы кадрды PNG ретінде сақтау
            cv2.imwrite('13/first_frame.png', frame)
            
            # Кадрға LSB енгізу
            secret = lsb.hide('13/first_frame.png', message)
            secret.save('13/first_frame_stego.png')
            
            print(f"✓ Хабар кадрға енгізілді: first_frame_stego.png")
            cap.release()
            return True
            
        except Exception as e:
            print(f"Қате: {e}")
            return False
    
    def test_format_robustness(self, stego_image_path):
        """Формат тұрақтылығын тексеру"""
        print(f"\n{'='*60}")
        print("Формат Тұрақтылығын Тексеру")
        print(f"{'='*60}")
        
        try:
            # PNG-ден JPEG-ке ауыстыру
            img = Image.open(stego_image_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            jpeg_path = stego_image_path.replace('.png', '_test.jpg')
            img.save(jpeg_path, 'JPEG', quality=85)
            
            # Хабарды шығаруға тырысу
            try:
                message = lsb.reveal(jpeg_path)
                if message:
                    print("✓ JPEG-тен хабар шығарылды")
                else:
                    print("✗ JPEG-тен хабар шығарылмады (сығу LSB-ті жойды)")
            except:
                print("✗ JPEG-тен хабар шығарылмады")
            
            return True
            
        except Exception as e:
            print(f"Қате: {e}")
            return False


def main():
    practice = MultimediaPractice()
    
    print("=" * 60)
    print("Мультимедиялық Файлдарда Жасыру Практикасы")
    print("=" * 60)
    
    # Мысал: Суретке мәтін енгізу
    # practice.hide_text_in_image_lsb('cover.png', 'Secret message', 'stego.png')
    # practice.reveal_from_image('stego.png')
    
    print("\nҚолдану: Функцияларды шақырыңыз немесе скриптті өзгертіңіз")


if __name__ == "__main__":
    main()

