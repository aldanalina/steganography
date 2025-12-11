#!/bin/bash
# Қысқа нұсқа - барлық практикаларды тез іске қосу

clear
echo "════════════════════════════════════════════════════════════"
echo "    СТЕGANОГРАФИЯ - БАРЛЫҚ ПРАКТИКАЛЫҚ ЖҰМЫСТАР"
echo "════════════════════════════════════════════════════════════"
echo ""

# Практика 1
echo "▶ ПРАКТИКА 1: ASCII Стеганография"
cd 1 && python3 steganography_ascii.py 2>/dev/null | grep -E "(Практикалық|Құпия|Whitespace|Symbol|Case|Дұрыс)" && cd ..
echo ""

# Практика 5
echo "▶ ПРАКТИКА 5: Мультимедиа"
cd 5 && python3 task1_lsb_extract.py 2>/dev/null | grep -E "(Хабар|табылды|Hello)" | head -3 && cd ..
echo ""

# Практика 7
echo "▶ ПРАКТИКА 7: Гистограмма Анализ"
cd 7 && python3 task1_histogram_analysis.py 2>/dev/null | grep -E "(Red|Green|Blue|айырмашылық|ҚОРЫТЫНДЫ)" | head -8 && cd ..
echo ""

# Практика 9
echo "▶ ПРАКТИКА 9: Текст Стеганография"
cd 9 && python3 task1_text_hide.py 2>/dev/null | grep -E "(Құпия|жасырылды|ДҰРЫС)" | head -5 && cd ..
echo ""

# Практика 10
echo "▶ ПРАКТИКА 10: LSB Image"
cd 10 && python3 task1_lsb_image.py 2>/dev/null | grep -E "(фото|Хабар|жасырылды|ДҰРЫС)" | head -5 && cd ..
echo ""

# Практика 11
echo "▶ ПРАКТИКА 11: LSB Distribution"
cd 11 && python3 task_lsb_distribution.py 2>/dev/null | grep -E "(Red|Green|Blue|баланс)" | head -6 && cd ..
echo ""

# Практика 12
echo "▶ ПРАКТИКА 12: Network Stego"
cd 12 && python3 simple_network_demo.py 2>/dev/null | grep -E "(DNS|HELLO|HTTP|TCP)" | head -8 && cd ..
echo ""

# Практика 13
echo "▶ ПРАКТИКА 13: 100 Символ"
cd 13 && python3 task_lsb_100chars.py 2>/dev/null | grep -E "(символдық|енгізілді|ДҰРЫС)" | head -4 && cd ..
echo ""

# Практика 14
echo "▶ ПРАКТИКА 14: AES Crypto"
cd 14 && python3 task_key_change.py 2>/dev/null | grep -E "(шифрланды|дешифрланды|кілт|ҚОРЫТЫНДЫ)" | head -6 && cd ..
echo ""

# Практика 15
echo "▶ ПРАКТИКА 15: CLI Interface"
cd 15 && python3 task_cli_interface.py hide 2>/dev/null | head -3 && cd ..
echo ""

echo "════════════════════════════════════════════════════════════"
echo "✅ БАРЛЫҚ 10 ПРАКТИКА АЯҚТАЛДЫ"
echo "════════════════════════════════════════════════════════════"

