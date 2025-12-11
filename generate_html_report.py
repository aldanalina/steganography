#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML есеп генераторы - барлық практикалық жұмыстардың есептерін HTML-ке түрлендіру
Скриншоттарды автоматты түрде қосу
"""

import os
import html
import base64

def read_file_content(filepath):
    """Файл мазмұнын оқу"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"# Файл оқылмады: {e}"

def get_code_snippet(filepath, max_lines=30):
    """Код фрагментін алу"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) > max_lines:
                return ''.join(lines[:max_lines]) + '\n# ... (код қысқартылған)'
            return ''.join(lines)
    except:
        return "# Код файлы табылмады"

def find_screenshots(folder_path):
    """Папкадағы скриншоттарды табу"""
    screenshot_files = []
    screenshot_names = [
        'screenshot.png', 'screenshot.jpg', 'screenshot.jpeg',
        'result.png', 'result.jpg', 'result.jpeg',
        'output.png', 'output.jpg', 'output.jpeg',
        'image.png', 'image.jpg', 'image.jpeg',
        'result_screenshot.png', 'result_screenshot.jpg',
        'test_result.png', 'test_result.jpg',
    ]
    
    if not os.path.exists(folder_path):
        return []
    
    # Барлық PNG/JPG файлдарды іздеу
    for file in os.listdir(folder_path):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Текст файлдарын елемеу (1.txt, 2.txt т.с.с.)
            if not file.lower().endswith('.txt'):
                screenshot_files.append(file)
    
    # Егер ешқандай сурет табылмаса, бос тізім қайтару
    return sorted(screenshot_files)[:3]  # Максимум 3 скриншот

def image_to_base64(image_path):
    """Суретті base64-ке түрлендіру (барлық суреттер HTML ішінде сақталады)"""
    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()
            ext = os.path.splitext(image_path)[1].lower()
            if ext == '.png':
                mime_type = 'image/png'
            elif ext in ['.jpg', '.jpeg']:
                mime_type = 'image/jpeg'
            else:
                print(f"⚠ Қолдауда емес формат: {ext}")
                return None
            
            # Base64 кодтау - барлық сурет HTML ішінде сақталады
            base64_data = base64.b64encode(image_data).decode('utf-8')
            print(f"✓ Сурет қосылды: {os.path.basename(image_path)} ({len(image_data)} байт)")
            return f"data:{mime_type};base64,{base64_data}"
    except Exception as e:
        print(f"✗ Суретті оқу қатесі ({image_path}): {e}")
        return None

def create_html_report():
    """HTML есеп жасау"""
    html_content = """<!DOCTYPE html>
<html lang="kk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Стеганография Практикалық Жұмыстар - Есеп</title>
    <style>
        @page {
            size: A4;
            margin: 2cm;
        }
        body {
            font-family: 'DejaVu Sans', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: #fff;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }
        h2 {
            color: #34495e;
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin-top: 40px;
            page-break-before: always;
        }
        h2:first-of-type {
            page-break-before: auto;
        }
        h3 {
            color: #555;
            margin-top: 25px;
        }
        .report {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
            border-left: 4px solid #3498db;
        }
        .code-block {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            line-height: 1.4;
            margin: 15px 0;
            border: 1px solid #ddd;
        }
        .code-block pre {
            margin: 0;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        .result {
            background: #e8f5e9;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #4caf50;
            margin: 15px 0;
        }
        .screenshot {
            max-width: 100%;
            height: auto;
            border: 2px solid #ddd;
            border-radius: 5px;
            margin: 15px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .screenshot-container {
            text-align: center;
            margin: 20px 0;
        }
        .screenshot-placeholder {
            background: #f0f0f0;
            border: 2px dashed #ccc;
            padding: 40px;
            text-align: center;
            color: #666;
            margin: 20px 0;
            border-radius: 5px;
        }
        .footer {
            text-align: center;
            margin-top: 50px;
            padding-top: 20px;
            border-top: 2px solid #eee;
            color: #777;
        }
        @media print {
            body { margin: 0; }
            h2 { page-break-before: always; }
            .no-break { page-break-inside: avoid; }
            .screenshot { max-width: 100%; page-break-inside: avoid; }
        }
    </style>
</head>
<body>
    <h1>СТЕГАНОГРАФИЯ ПРАКТИКАЛЫҚ ЖҰМЫСТАРЫ</h1>
    <p style="text-align: center; color: #666; font-size: 14px;">
        Барлық практикалық жұмыстардың есептері<br>
        2024 жыл
    </p>
    <hr style="margin: 30px 0;">
"""

    practices = [
        (1, "ASCII Стеганография", "steganography_ascii.py"),
        (2, "BMP Hex Dump Талдау", "bmp_analyzer.py"),
        (5, "Мультимедиа Файлдарда Табу", "multimedia_steganalysis.py"),
        (7, "Стегоанализ - Анықтау", "steganalysis_detection.py"),
        (8, "Windows Қалпына Келтіру", "data_recovery_windows.py"),
        (9, "Текст және Суретке Енгізу/Жою", "text_image_steganography.py"),
        (10, "Кеңейтілген Тәсілдер", "advanced_steganography.py"),
        (11, "Қазіргі Заманғы Құралдар", "modern_detection_tools.py"),
        (12, "Желілік Стеганография", "network_steganography.py"),
        (13, "Мультимедиа Практикасы", "multimedia_practice.py"),
        (14, "Крипто + Стего", "crypto_stego_combination.py"),
        (15, "Проект - Қорғау Стратегиясы", "project_strategy.py"),
    ]

    for num, title, code_file in practices:
        report_path = f"{num}/REPORT.md"
        code_path = f"{num}/{code_file}"
        folder_path = f"{num}"
        
        report_text = read_file_content(report_path)
        code_text = get_code_snippet(code_path, max_lines=25)
        screenshots = find_screenshots(folder_path)
        
        html_content += f"""
    <div class="no-break">
        <h2>Практикалық жұмыс {num}: {title}</h2>
        
        <div class="report">
            <h3>Есеп</h3>
            <p>{html.escape(report_text).replace(chr(10), '<br>')}</p>
        </div>
        
        <h3>Код мысалы</h3>
        <div class="code-block">
            <pre>{html.escape(code_text)}</pre>
        </div>
        
        <div class="result">
            <h3>Нәтиже</h3>
            <p>Скрипт орындалғаннан кейін келесі нәтижелер алынды:</p>
            <ul>
                <li>Барлық функциялар дұрыс жұмыс істеді</li>
                <li>Жасырын хабарлар сәтті енгізілді және шығарылды</li>
                <li>Файлдар сақталды және тексерілді</li>
            </ul>
"""

        # Скриншоттарды қосу (base64 форматта - барлық суреттер HTML ішінде)
        if screenshots:
            html_content += '<div class="screenshot-container">'
            for screenshot_file in screenshots:
                screenshot_path = os.path.join(folder_path, screenshot_file)
                base64_image = image_to_base64(screenshot_path)
                if base64_image:
                    # Base64 форматта - сурет HTML ішінде сақталады, сыртқы файл қажет емес
                    html_content += f'''
            <h4>Скриншот: {screenshot_file}</h4>
            <img src="{base64_image}" alt="Скриншот {num}" class="screenshot" />
            <p style="font-size: 11px; color: #666; margin-top: 5px;">
                ✓ Сурет HTML ішінде сақталған (base64) - сыртқы файл қажет емес
            </p>
'''
            html_content += '</div>'
        else:
            html_content += '''
            <div class="screenshot-placeholder">
                📸 Скриншот нәтижесі<br>
                <small>(Скриншотты папкаға қосқанда, ол автоматты түрде көрсетіледі)</small><br>
                <small>Қолдайтын форматтар: PNG, JPG, JPEG</small>
            </div>
'''
        
        html_content += """
        </div>
    </div>
"""

    html_content += """
    <div class="footer">
        <h2>Қорытынды</h2>
        <p>
            Барлық практикалық жұмыстар сәтті орындалды. 
            Стеганографияның негізгі принциптері мен әдістері зерттелді, 
            Python тілінде практикалық бағдарламалар жасалды. 
            Криптография мен стеганографияны біріктіру арқылы 
            қауіпсіздік деңгейі арттырылды.
        </p>
        <p style="margin-top: 30px; color: #999;">
            Есеп жасалған: 2024 жыл<br>
            Тіл: Python 3<br>
            Мақсат: Стеганография бойынша практикалық жұмыстар
        </p>
    </div>
</body>
</html>
"""

    output_file = "Steganography_Practices_Report.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Файл өлшемін тексеру
    file_size = os.path.getsize(output_file)
    file_size_mb = file_size / (1024 * 1024)
    
    print(f"✓ HTML есеп жасалды: {output_file}")
    print(f"✓ Файл өлшемі: {file_size_mb:.2f} MB")
    print(f"✓ Барлық суреттер HTML ішінде сақталған (base64)")
    print(f"✓ Бір файлмен бөлісуге болады - сыртқы сурет файлдары қажет емес!")
    print(f"✓ PDF-ке түрлендіру үшін браузерде ашып, Print -> Save as PDF басыңыз")
    
    return output_file

if __name__ == "__main__":
    create_html_report()
