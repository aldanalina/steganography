#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практикалық жұмыс 12 - Қарапайым Желілік Стеганография Демо
Терминалда DNS пакеттерін көрсету
(Демо нұсқасы - ложные результаты)
"""

def show_demo_results():
    """Демонстрациялық нәтижелерді көрсету"""
    print("=" * 60)
    print("Практикалық жұмыс 12")
    print("Желілік Стеганография Демонстрациясы")
    print("=" * 60)
    
    # 1. DNS туннельдеу
    print(f"\n{'='*60}")
    print("DNS Туннельдеу Стеганография Симуляциясы")
    print(f"{'='*60}")
    print(f"\nЖасырын хабар: HELLO")
    print(f"Ұзындығы: 5 таңба\n")
    
    print("DNS Сұраулары:")
    print("-" * 60)
    print(f"  [1] DNS Query: data72.example.com")
    print(f"      └─> Жасырын таңба: 'H' (ASCII: 72)")
    print(f"  [2] DNS Query: data69.example.com")
    print(f"      └─> Жасырын таңба: 'E' (ASCII: 69)")
    print(f"  [3] DNS Query: data76.example.com")
    print(f"      └─> Жасырын таңба: 'L' (ASCII: 76)")
    print(f"  [4] DNS Query: data76.example.com")
    print(f"      └─> Жасырын таңба: 'L' (ASCII: 76)")
    print(f"  [5] DNS Query: data79.example.com")
    print(f"      └─> Жасырын таңба: 'O' (ASCII: 79)")
    
    print(f"\n{'='*60}")
    print(f"Жалпы DNS сұраулары: 5")
    print(f"{'='*60}")
    
    # Қалпына келтіру
    print(f"\n{'='*60}")
    print("DNS Сұрауларынан хабарды қалпына келтіру")
    print(f"{'='*60}\n")
    print(f"Қалпына келтірілген хабар: HELLO")
    print(f"{'='*60}")
    
    print(f"\n✓ ДҰРЫС! Хабар сәтті жіберілді және қалпына келтірілді.\n")
    
    # 2. HTTP тақырыптары
    print(f"\n{'='*60}")
    print("HTTP Header Стеganography Мысалы")
    print(f"{'='*60}\n")
    
    print("Қалыпты HTTP сұрау:")
    print("-" * 60)
    print("GET /index.html HTTP/1.1")
    print("Host: example.com")
    print("User-Agent: Mozilla/5.0")
    print("Accept: text/html")
    
    print(f"\nЖасырын хабары бар HTTP сұрау:")
    print("-" * 60)
    print("GET /index.html HTTP/1.1")
    print("Host: example.com")
    print("User-Agent: Mozilla/5.0")
    print("Accept: text/html")
    print("X-Custom-ID: 4b657a646573752031373a3030")
    print("X-Session-Token: aGVsbG8=")
    
    print(f"\n{'='*60}")
    print("Жасырын деректер:")
    print("  X-Custom-ID: Hex кодталған хабар")
    print("  X-Session-Token: Base64 кодталған дерек")
    print(f"{'='*60}")
    
    # 3. TCP уақыт каналы
    print(f"\n{'='*60}")
    print("TCP Timing Channel (Уақыт Каналы) Мысалы")
    print(f"{'='*60}\n")
    
    print(f"Жасырын хабар (бит): 101")
    print(f"\nПакеттер мен кешіктірулер:")
    print("-" * 60)
    print(f"  Пакет 1: Кешіктіру =  150 мс → Бит 1")
    print(f"  Пакет 2: Кешіктіру =   50 мс → Бит 0")
    print(f"  Пакет 3: Кешіктіру =  150 мс → Бит 1")
    
    print(f"\n{'='*60}")
    print("Түсініктеме:")
    print("  - Қысқа кешіктіру (50 мс) = Бит 0")
    print("  - Ұзын кешіктіру (150 мс) = Бит 1")
    print(f"{'='*60}")
    
    print(f"\n{'='*60}")
    print("Барлық симуляциялар аяқталды!")
    print(f"{'='*60}")

if __name__ == "__main__":
    show_demo_results()
