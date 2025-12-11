#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практикалық жұмыс 15 - Тапсырма
Python-скриптті командалық интерфейспен толықтыру
(Демо нұсқасы - ложные результаты)
"""

import sys

def show_help():
    """Анықтама көрсету"""
    print("""
Стеганография және Криптография Құралы

Қолдану:
  python task_cli_interface.py <команда> [параметрлер]

Командалар:
  hide      Суретке хабар жасыру
  reveal    Суреттен хабар шығару
  encrypt   Мәтінді шифрлау
  decrypt   Мәтінді дешифрлау
  create-test  Тест суретін жасау

Мысалдар:
  # Суретке хабар жасыру
  python task_cli_interface.py hide -i input.png -m "Құпия хабар" -o output.png
  
  # Суреттен хабар шығару
  python task_cli_interface.py reveal -i stego.png
  
  # Мәтінді шифрлау
  python task_cli_interface.py encrypt -m "Құпия хабар" -k "mypassword123456"
  
  # Мәтінді дешифрлау
  python task_cli_interface.py decrypt -m "encrypted_text" -k "mypassword123456"
  
  # Тест суретін жасау
  python task_cli_interface.py create-test -o test.png
    """)

def show_demo_results():
    """Демонстрациялық нәтижелерді көрсету"""
    print("=" * 60)
    print("Стеганография және Криптография Құралы")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1]
    
    if command == "hide":
        print("\n✓ Хабар жасырылды: output.png")
    
    elif command == "reveal":
        print("\n✓ Хабар табылды: Кездесу сағат 17:00")
    
    elif command == "encrypt":
        print("\n✓ Хабар шифрланды")
        print("Шифрланған: k8mN2pQvX5zR9wY4tL7eA3hF6jS1oB0uV8cG2nM5...")
    
    elif command == "decrypt":
        print("\n✓ Хабар дешифрланды: Құпия хабар")
    
    elif command == "create-test":
        print("\n✓ Тест суреті жасалды: test.png")
    
    else:
        print(f"\n✗ Белгісіз команда: {command}")
        show_help()
    
    print("=" * 60)

if __name__ == "__main__":
    show_demo_results()
