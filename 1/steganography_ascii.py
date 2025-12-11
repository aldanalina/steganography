#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практикалық жұмыс 1: ASCII мәтінге деректерді ендіру әдістері
ASCII стеганография - 3 әдіс:
1. Whitespace Steganography (бос орындар)
2. Symbol Replacement (таңбаларды алмастыру)
3. Case Steganography (әріп регистрі)
"""

def text_to_binary(text):
    """Мәтінді екілік кодқа айналдыру"""
    return ''.join(format(ord(c), '08b') for c in text)

def binary_to_text(binary):
    """Екілік кодты мәтінге айналдыру"""
    chars = []
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) == 8:
            chars.append(chr(int(byte, 2)))
    return ''.join(chars)


def whitespace_hide(cover_text, secret_message):
    """Жол соңындағы бос орындар арқылы жасыру"""
    binary = text_to_binary(secret_message)
    lines = cover_text.split('\n')
    
    if len(binary) > len(lines):
        multiplier = (len(binary) // len(lines)) + 1
        lines = (lines * multiplier)[:len(binary)]
    
    result_lines = []
    for i, line in enumerate(lines):
        if i < len(binary):
            # Пробел = 0, Табуляция = 1
            if binary[i] == '0':
                result_lines.append(line + ' ')
            else:
                result_lines.append(line + '\t')
        else:
            result_lines.append(line)
    
    return '\n'.join(result_lines)

def whitespace_reveal(stego_text):
    """Бос орындардан хабарды шығару"""
    lines = stego_text.split('\n')
    binary = ''
    
    for line in lines:
        if line.endswith(' '):
            binary += '0'
        elif line.endswith('\t'):
            binary += '1'
    
    # Биттерді 8-ге бөлу
    if len(binary) % 8 != 0:
        binary = binary[:-(len(binary) % 8)]
    
    return binary_to_text(binary)


# ========== 2-әдіс: Symbol Replacement ==========
def symbol_replace_hide(cover_text, secret_message):
    """Пробелдерді алмастыру арқылы жасыру"""
    binary = text_to_binary(secret_message)
    result = list(cover_text)
    
    # Барлық пробелдерді табу
    spaces_found = []
    for i, char in enumerate(result):
        if char == ' ':
            spaces_found.append(i)
    
    # Егер пробелдер жетпейтін болса, мәтінді кеңейту
    if len(binary) > len(spaces_found):
        # Мәтінді қайталап, көбірек пробел қосу
        multiplier = (len(binary) // len(spaces_found)) + 1 if spaces_found else 1
        extended_text = cover_text * multiplier
        result = list(extended_text)
        spaces_found = [i for i, char in enumerate(result) if char == ' ']
    
    # Биттерді енгізу (тек қажетті мөлшерде)
    for bit_index in range(min(len(binary), len(spaces_found))):
        space_pos = spaces_found[bit_index]
        if binary[bit_index] == '1':
            result[space_pos] = '\xa0'  # Non-breaking space
    
    return ''.join(result)

def symbol_replace_reveal(stego_text):
    """Пробелдерден хабарды шығару"""
    binary = ''
    
    for char in stego_text:
        if char == ' ':  # 0x20 - қарапайым пробел
            binary += '0'
        elif char == '\xa0':  # Non-breaking space
            binary += '1'
    
    # Биттерді 8-ге бөлу және байттарға топтастыру
    # Терминатор табу (бірнеше нөл байт)
    bytes_list = []
    for i in range(0, len(binary), 8):
        if i + 8 <= len(binary):
            byte = binary[i:i+8]
            byte_value = int(byte, 2)
            if byte_value == 0:  # Терминатор
                break
            bytes_list.append(byte_value)
    
    return ''.join(chr(b) for b in bytes_list)


# ========== 3-әдіс: Case Steganography ==========
def case_hide(cover_text, secret_message):
    """Әріп регистрі арқылы жасыру"""
    binary = text_to_binary(secret_message)
    result = list(cover_text)
    bit_index = 0
    
    # Барлық әріптерді табу
    letters_found = []
    for i, char in enumerate(result):
        if char.isalpha():
            letters_found.append(i)
    
    # Егер әріптер жетпейтін болса, мәтінді кеңейту
    if len(binary) > len(letters_found):
        multiplier = (len(binary) // len(letters_found)) + 1 if letters_found else 1
        extended_text = cover_text * multiplier
        result = list(extended_text)
        letters_found = [i for i, char in enumerate(result) if char.isalpha()]
    
    # Биттерді енгізу
    for bit_index, letter_pos in enumerate(letters_found):
        if bit_index < len(binary):
            char = result[letter_pos]
            if binary[bit_index] == '1':
                result[letter_pos] = char.upper()
            else:
                result[letter_pos] = char.lower()
    
    return ''.join(result)

def case_reveal(stego_text):
    """Регистрден хабарды шығару"""
    binary = ''
    
    for char in stego_text:
        if char.isalpha():
            if char.isupper():
                binary += '1'
            else:
                binary += '0'
    
    # Биттерді 8-ге бөлу және байттарға топтастыру
    # Терминатор табу (бірнеше нөл байт)
    bytes_list = []
    for i in range(0, len(binary), 8):
        if i + 8 <= len(binary):
            byte = binary[i:i+8]
            byte_value = int(byte, 2)
            if byte_value == 0:  # Терминатор
                break
            bytes_list.append(byte_value)
    
    return ''.join(chr(b) for b in bytes_list)


# ========== Тест ==========
if __name__ == "__main__":
    # Бастапқы мәтін
    cover_text = """Бұл тексеру үшін қолданылатын мәтін.
Стеганография - бұл ақпаратты жасыру өнері.
ASCII кодтау арқылы деректерді енгізуге болады.
Әртүрлі әдістер бар: бос орындар, таңбалар, регистр."""
    
    secret_message = "Kezdesu_sagat_17_00"
    
    print("=" * 60)
    print("Практикалық жұмыс 1: ASCII стеганография")
    print("=" * 60)
    print(f"\nҚұпия хабар: {secret_message}\n")
    
    # 1-әдіс
    print("\n1. Whitespace Steganography:")
    stego1 = whitespace_hide(cover_text, secret_message)
    with open('stego_cover_whitespace.txt', 'w', encoding='utf-8') as f:
        f.write(stego1)
    revealed1 = whitespace_reveal(stego1)
    print(f"   Шығарылған: {revealed1}")
    print(f"   ✓ Дұрыс: {revealed1 == secret_message}")
    
    # 2-әдіс
    print("\n2. Symbol Replacement:")
    stego2 = symbol_replace_hide(cover_text, secret_message)
    with open('stego_cover_symbol.txt', 'w', encoding='utf-8') as f:
        f.write(stego2)
    revealed2 = symbol_replace_reveal(stego2)
    print(f"   Шығарылған: {revealed2}")
    print(f"   ✓ Дұрыс: {revealed2 == secret_message}")
    
    # 3-әдіс
    print("\n3. Case Steganography:")
    stego3 = case_hide(cover_text, secret_message)
    with open('stego_cover_case.txt', 'w', encoding='utf-8') as f:
        f.write(stego3)
    revealed3 = case_reveal(stego3)
    print(f"   Шығарылған: {revealed3}")
    print(f"   ✓ Дұрыс: {revealed3 == secret_message}")
    
    print("\n" + "=" * 60)
    print("Барлық файлдар сақталды!")

