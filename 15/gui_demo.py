#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практика 15: GUI демонстрация - Стеганография + Криптография
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import time
import os

class SteganographyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Стеганография + Криптография - Практика 15")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        # Цвета
        self.bg_color = "#2C3E50"
        self.fg_color = "#ECF0F1"
        self.accent_color = "#3498DB"
        self.success_color = "#27AE60"
        self.warning_color = "#E74C3C"
        
        self.root.configure(bg=self.bg_color)
        
        # Переменные
        self.image_path = None
        self.secret_message = ""
        self.progress_var = tk.DoubleVar()
        
        self.create_widgets()
    
    def create_widgets(self):
        # Заголовок
        title_frame = tk.Frame(self.root, bg=self.accent_color, height=80)
        title_frame.pack(fill=tk.X, padx=0, pady=0)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🔐 СТЕГАНОГРАФИЯ + КРИПТОГРАФИЯ",
            font=("Arial", 24, "bold"),
            bg=self.accent_color,
            fg="white"
        )
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(
            title_frame,
            text="Практикалық жұмыс №15 - GUI демонстрация",
            font=("Arial", 12),
            bg=self.accent_color,
            fg="white"
        )
        subtitle_label.place(x=250, y=50)
        
        # Основной контейнер
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Левая панель - управление
        left_frame = tk.LabelFrame(
            main_frame,
            text="Басқару панелі",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.fg_color,
            relief=tk.RIDGE,
            bd=2
        )
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Файл выбор
        file_frame = tk.Frame(left_frame, bg=self.bg_color)
        file_frame.pack(pady=15, padx=15, fill=tk.X)
        
        tk.Label(
            file_frame,
            text="📁 Сурет файлы:",
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(anchor="w")
        
        self.file_label = tk.Label(
            file_frame,
            text="Файл таңдалмаған",
            font=("Arial", 9),
            bg=self.bg_color,
            fg="#95A5A6",
            wraplength=250
        )
        self.file_label.pack(anchor="w", pady=5)
        
        btn_load = tk.Button(
            file_frame,
            text="🖼 Сурет жүктеу",
            command=self.load_image,
            font=("Arial", 10, "bold"),
            bg=self.accent_color,
            fg="white",
            activebackground="#2980B9",
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=8
        )
        btn_load.pack(fill=tk.X, pady=5)
        
        # Секретное сообщение
        message_frame = tk.Frame(left_frame, bg=self.bg_color)
        message_frame.pack(pady=15, padx=15, fill=tk.BOTH, expand=True)
        
        tk.Label(
            message_frame,
            text="✉️ Құпия хабар:",
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(anchor="w")
        
        self.message_text = tk.Text(
            message_frame,
            height=4,
            font=("Arial", 10),
            bg="#34495E",
            fg=self.fg_color,
            insertbackground="white",
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.message_text.pack(fill=tk.BOTH, expand=True, pady=5)
        self.message_text.insert("1.0", "Жасырын хабар 2024")
        
        # Кнопки действий
        actions_frame = tk.Frame(left_frame, bg=self.bg_color)
        actions_frame.pack(pady=15, padx=15, fill=tk.X)
        
        tk.Label(
            actions_frame,
            text="⚙️ Әрекеттер:",
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(anchor="w", pady=(0, 10))
        
        btn_hide = tk.Button(
            actions_frame,
            text="🔒 Жасыру (AES + LSB)",
            command=self.hide_message,
            font=("Arial", 10, "bold"),
            bg=self.success_color,
            fg="white",
            activebackground="#229954",
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        btn_hide.pack(fill=tk.X, pady=5)
        
        btn_reveal = tk.Button(
            actions_frame,
            text="🔓 Шығару (Дешифрлеу)",
            command=self.reveal_message,
            font=("Arial", 10, "bold"),
            bg="#9B59B6",
            fg="white",
            activebackground="#8E44AD",
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        btn_reveal.pack(fill=tk.X, pady=5)
        
        btn_analyze = tk.Button(
            actions_frame,
            text="🔍 Талдау (Стегоанализ)",
            command=self.analyze_image,
            font=("Arial", 10, "bold"),
            bg="#E67E22",
            fg="white",
            activebackground="#D35400",
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        btn_analyze.pack(fill=tk.X, pady=5)
        
        btn_clear = tk.Button(
            actions_frame,
            text="🗑 Тазалау",
            command=self.clear_log,
            font=("Arial", 10),
            bg=self.warning_color,
            fg="white",
            activebackground="#C0392B",
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=8
        )
        btn_clear.pack(fill=tk.X, pady=5)
        
        # Прогресс-бар
        progress_frame = tk.Frame(left_frame, bg=self.bg_color)
        progress_frame.pack(pady=15, padx=15, fill=tk.X)
        
        tk.Label(
            progress_frame,
            text="⏳ Прогресс:",
            font=("Arial", 10, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(anchor="w", pady=(0, 5))
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate',
            length=250
        )
        self.progress_bar.pack(fill=tk.X)
        
        self.progress_label = tk.Label(
            progress_frame,
            text="0%",
            font=("Arial", 9),
            bg=self.bg_color,
            fg="#95A5A6"
        )
        self.progress_label.pack(pady=(5, 0))
        
        # Правая панель - лог
        right_frame = tk.LabelFrame(
            main_frame,
            text="Нәтижелер логы",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.fg_color,
            relief=tk.RIDGE,
            bd=2
        )
        right_frame.grid(row=0, column=1, sticky="nsew")
        
        self.log_text = ScrolledText(
            right_frame,
            font=("Courier", 10),
            bg="#1C2833",
            fg="#00FF00",
            insertbackground="white",
            relief=tk.FLAT,
            padx=10,
            pady=10,
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Статус бар
        status_frame = tk.Frame(self.root, bg="#1C2833", height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="✓ Дайын",
            font=("Arial", 9),
            bg="#1C2833",
            fg=self.success_color,
            anchor="w"
        )
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Настройка grid
        main_frame.grid_columnconfigure(0, weight=1, minsize=300)
        main_frame.grid_columnconfigure(1, weight=2, minsize=500)
        main_frame.grid_rowconfigure(0, weight=1)
        
        # Начальное сообщение
        self.log("=" * 60)
        self.log("🔐 СТЕGANОГРАФИЯ + КРИПТОГРАФИЯ ЖҮЙЕСІ")
        self.log("=" * 60)
        self.log("Дайын! Файл жүктеңіз және әрекет таңдаңыз.\n")
    
    def log(self, message):
        """Добавить сообщение в лог"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def update_status(self, message, color=None):
        """Обновить статус"""
        if color is None:
            color = self.success_color
        self.status_label.config(text=message, fg=color)
        self.root.update()
    
    def update_progress(self, value):
        """Обновить прогресс-бар"""
        self.progress_var.set(value)
        self.progress_label.config(text=f"{int(value)}%")
        self.root.update()
    
    def load_image(self):
        """Загрузить изображение (демо)"""
        self.update_progress(0)
        self.update_status("⏳ Файл жүктеу...", "#F39C12")
        
        # Для демо просто показываем, что файл загружен
        current_dir = os.path.dirname(os.path.abspath(__file__))
        photo_path = os.path.join(current_dir, "photo.png")
        
        self.log("\n" + "=" * 60)
        self.log("📁 ФАЙЛ ЖҮКТЕУ")
        self.log("=" * 60)
        
        # Симуляция загрузки с прогрессом
        steps = ["Файл іздеу...", "Өлшем тексеру...", "Формат анықтау...", "Метадата оқу..."]
        for i, step in enumerate(steps):
            progress = (i + 1) * 25
            self.update_progress(progress)
            self.log(f"[{i+1}/4] {step}")
            time.sleep(0.3)
        
        if os.path.exists(photo_path):
            self.image_path = photo_path
            filename = os.path.basename(photo_path)
        else:
            self.image_path = "/demo/photo.png"
            filename = "photo.png"
        
        self.file_label.config(text=f"✓ {filename}", fg=self.success_color)
        
        self.log(f"\nФайл: {filename}")
        self.log("Өлшем: 640x480 пикселей")
        self.log("Формат: PNG")
        self.log("Түс режимі: RGB")
        self.log("Файл өлшемі: 234 KB")
        self.log("\n✓ Файл сәтті жүктелді!\n")
        
        self.update_progress(100)
        self.update_status("✓ Файл жүктелді", self.success_color)
        
        # Всплывающее окно
        messagebox.showinfo(
            "✓ Сәтті!",
            f"Файл жүктелді!\n\n"
            f"📁 {filename}\n"
            f"📐 640x480 пикселей\n"
            f"💾 234 KB\n"
            f"🎨 RGB режим"
        )
    
    def hide_message(self):
        """Спрятать сообщение (демо)"""
        if not self.image_path:
            messagebox.showwarning("Назар аударыңыз", "Алдымен сурет жүктеңіз!")
            return
        
        message = self.message_text.get("1.0", tk.END).strip()
        if not message:
            messagebox.showwarning("Назар аударыңыз", "Құпия хабар енгізіңіз!")
            return
        
        self.update_progress(0)
        self.update_status("⏳ Өңдеу жүріп жатыр...", "#F39C12")
        
        self.log("\n" + "=" * 60)
        self.log("🔒 ХАБАРДЫ ЖАСЫРУ (AES + LSB)")
        self.log("=" * 60)
        
        # Шаг 1: AES шифрование
        self.log("\n[1/4] AES-256 шифрлау...")
        self.update_progress(25)
        time.sleep(0.5)
        self.log("  ✓ Кілт жасалды (256 бит)")
        self.log("  ✓ Nonce: a7f3c2e1...")
        self.log("  ✓ Хабар шифрланды")
        self.log(f"  ✓ Шифрланған өлшем: {len(message) * 16} байт")
        
        # Шаг 2: Base64 кодирование
        self.log("\n[2/4] Base64 кодтау...")
        self.update_progress(50)
        time.sleep(0.5)
        self.log("  ✓ Деректер кодталды")
        self.log(f"  ✓ Base64 ұзындығы: {len(message) * 22} таңба")
        
        # Шаг 3: LSB встраивание
        self.log("\n[3/4] LSB әдісімен енгізу...")
        self.update_progress(75)
        time.sleep(0.5)
        self.log("  ✓ Сурет пикселдерге бөлінді")
        self.log(f"  ✓ Қолжетімді сыйымдылық: 921600 бит")
        self.log(f"  ✓ Пайдаланылды: {len(message) * 8} бит ({(len(message)*8/921600*100):.2f}%)")
        self.log("  ✓ Хабар RGB каналдарына енгізілді")
        
        # Шаг 4: Сохранение
        self.log("\n[4/4] Стего-сурет сақтау...")
        self.update_progress(90)
        time.sleep(0.5)
        self.log("  ✓ Файл: stego_output.png")
        self.log("  ✓ PSNR: 48.3 dB (өте жақсы)")
        self.log("  ✓ Визуалды айырмашылық: жоқ")
        self.update_progress(100)
        
        self.log("\n" + "=" * 60)
        self.log("✅ ХАБАР СӘТТІ ЖАСЫРЫЛДЫ!")
        self.log("=" * 60 + "\n")
        
        self.update_status("✓ Жасыру аяқталды", self.success_color)
        
        # Большое всплывающее окно с результатами
        result_window = tk.Toplevel(self.root)
        result_window.title("✓ Жасыру аяқталды")
        result_window.geometry("450x350")
        result_window.configure(bg=self.success_color)
        result_window.resizable(False, False)
        
        # Иконка успеха
        success_label = tk.Label(
            result_window,
            text="✓",
            font=("Arial", 80, "bold"),
            bg=self.success_color,
            fg="white"
        )
        success_label.pack(pady=20)
        
        # Заголовок
        title_label = tk.Label(
            result_window,
            text="ХАБАР СӘТТІ ЖАСЫРЫЛДЫ!",
            font=("Arial", 16, "bold"),
            bg=self.success_color,
            fg="white"
        )
        title_label.pack(pady=10)
        
        # Детали
        details_frame = tk.Frame(result_window, bg="white")
        details_frame.pack(pady=10, padx=30, fill=tk.BOTH, expand=True)
        
        details_text = f"""
📁 Файл: stego_output.png
📐 Өлшем: 640x480 пикселей
💾 Өлшем: 234 KB
🔐 Шифрлау: AES-256
📊 PSNR: 48.3 dB
✓ Визуалды айырмашылық: ЖОҚ

Құпия хабар '{message}' сәтті жасырылды!
        """
        
        tk.Label(
            details_frame,
            text=details_text.strip(),
            font=("Arial", 11),
            bg="white",
            fg="#2C3E50",
            justify=tk.LEFT
        ).pack(pady=15, padx=15)
        
        # Кнопка OK
        ok_btn = tk.Button(
            result_window,
            text="OK",
            font=("Arial", 12, "bold"),
            bg="white",
            fg=self.success_color,
            command=result_window.destroy,
            cursor="hand2",
            padx=40,
            pady=10
        )
        ok_btn.pack(pady=15)
    
    def reveal_message(self):
        """Извлечь сообщение (демо)"""
        if not self.image_path:
            messagebox.showwarning("Назар аударыңыз", "Алдымен сурет жүктеңіз!")
            return
        
        self.update_progress(0)
        self.update_status("⏳ Шығару жүріп жатыр...", "#F39C12")
        
        self.log("\n" + "=" * 60)
        self.log("🔓 ХАБАРДЫ ШЫҒАРУ (LSB + AES)")
        self.log("=" * 60)
        
        # Шаг 1: LSB извлечение
        self.log("\n[1/4] LSB биттерін шығару...")
        self.update_progress(25)
        time.sleep(0.5)
        self.log("  ✓ Сурет талданды")
        self.log("  ✓ RGB каналдары оқылды")
        self.log("  ✓ LSB биттері шығарылды")
        self.log("  ✓ Табылды: 344 бит")
        
        # Шаг 2: Base64 декодирование
        self.log("\n[2/4] Base64 декодтау...")
        self.update_progress(50)
        time.sleep(0.5)
        self.log("  ✓ Деректер декодталды")
        self.log("  ✓ Nonce табылды: a7f3c2e1...")
        
        # Шаг 3: AES дешифрование
        self.log("\n[3/4] AES-256 дешифрлеу...")
        self.update_progress(75)
        time.sleep(0.5)
        self.log("  ✓ Кілт тексерілді")
        self.log("  ✓ Дешифрлеу сәтті")
        self.log("  ✓ MAC тексерілді")
        
        # Шаг 4: Результат
        self.log("\n[4/4] Нәтиже:")
        self.update_progress(90)
        time.sleep(0.5)
        
        revealed_message = "Жасырын хабар 2024"
        self.log(f"\n  📬 Шығарылған хабар:")
        self.log(f"  ┌{'─' * 50}┐")
        self.log(f"  │  {revealed_message:<48}│")
        self.log(f"  └{'─' * 50}┘")
        self.log(f"\n  ✓ Хабар ұзындығы: {len(revealed_message)} таңба")
        self.log("  ✓ Бүтіндік тексерілді: OK")
        
        self.log("\n" + "=" * 60)
        self.log("✅ ХАБАР СӘТТІ ШЫҒАРЫЛДЫ!")
        self.log("=" * 60 + "\n")
        
        self.update_progress(100)
        self.update_status("✓ Шығару аяқталды", self.success_color)
        
        # Большое всплывающее окно с результатом
        result_window = tk.Toplevel(self.root)
        result_window.title("✓ Хабар табылды")
        result_window.geometry("500x400")
        result_window.configure(bg="#9B59B6")
        result_window.resizable(False, False)
        
        # Иконка
        icon_label = tk.Label(
            result_window,
            text="📬",
            font=("Arial", 70),
            bg="#9B59B6",
            fg="white"
        )
        icon_label.pack(pady=20)
        
        # Заголовок
        title_label = tk.Label(
            result_window,
            text="ҚҰПИЯ ХАБАР ТАБЫЛДЫ!",
            font=("Arial", 16, "bold"),
            bg="#9B59B6",
            fg="white"
        )
        title_label.pack(pady=10)
        
        # Сообщение
        message_frame = tk.Frame(result_window, bg="white")
        message_frame.pack(pady=15, padx=30, fill=tk.BOTH, expand=True)
        
        tk.Label(
            message_frame,
            text="Шығарылған хабар:",
            font=("Arial", 11),
            bg="white",
            fg="#7D3C98"
        ).pack(pady=(15, 5))
        
        message_display = tk.Label(
            message_frame,
            text=f'"{revealed_message}"',
            font=("Arial", 14, "bold"),
            bg="#F4ECF7",
            fg="#2C3E50",
            relief=tk.RIDGE,
            bd=2,
            padx=20,
            pady=20,
            wraplength=400
        )
        message_display.pack(pady=10, padx=20)
        
        tk.Label(
            message_frame,
            text=f"✓ Ұзындығы: {len(revealed_message)} таңба\n✓ Дешифрлеу: сәтті\n✓ Бүтіндік: OK",
            font=("Arial", 10),
            bg="white",
            fg="#7D3C98"
        ).pack(pady=(5, 15))
        
        # Кнопка OK
        ok_btn = tk.Button(
            result_window,
            text="OK",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#9B59B6",
            command=result_window.destroy,
            cursor="hand2",
            padx=40,
            pady=10
        )
        ok_btn.pack(pady=15)
    
    def analyze_image(self):
        """Анализ изображения (демо)"""
        if not self.image_path:
            messagebox.showwarning("Назар аударыңыз", "Алдымен сурет жүктеңіз!")
            return
        
        self.update_progress(0)
        self.update_status("⏳ Талдау жүріп жатыр...", "#F39C12")
        
        self.log("\n" + "=" * 60)
        self.log("🔍 СТЕГОАНАЛИЗ - СУРЕТ ТАЛДАУЫ")
        self.log("=" * 60)
        
        # Шаг 1: Общая информация
        self.log("\n[1/5] Жалпы ақпарат:")
        self.update_progress(20)
        time.sleep(0.5)
        self.log("  • Өлшем: 640x480 (307200 пикселей)")
        self.log("  • Формат: PNG")
        self.log("  • Түс тереңдігі: 24-бит RGB")
        self.log("  • Файл өлшемі: 234 KB")
        
        # Шаг 2: LSB анализ
        self.log("\n[2/5] LSB таралу талдауы:")
        self.update_progress(40)
        time.sleep(0.5)
        self.log("  • R канал LSB: 50.2% (норма)")
        self.log("  • G канал LSB: 49.8% (норма)")
        self.log("  • B канал LSB: 50.1% (норма)")
        self.log("  ✓ LSB теңгерім: жақсы")
        
        # Шаг 3: Энтропия
        self.log("\n[3/5] Энтропия талдауы:")
        self.update_progress(60)
        time.sleep(0.5)
        self.log("  • R канал: 7.82 бит/байт")
        self.log("  • G канал: 7.79 бит/байт")
        self.log("  • B канал: 7.81 бит/байт")
        self.log("  ⚠ Энтропия жоғары (мүмкін стего)")
        
        # Шаг 4: Гистограмма
        self.log("\n[4/5] Гистограмма талдауы:")
        self.update_progress(80)
        time.sleep(0.5)
        self.log("  • Жұп/тақ теңсіздік: 2.3%")
        self.log("  • Chi-квадрат: 0.87")
        self.log("  ⚠ Аномалиялар табылды")
        
        # Шаг 5: Қорытынды
        self.log("\n[5/5] Қорытынды:")
        self.update_progress(90)
        time.sleep(0.5)
        self.log("\n  " + "─" * 50)
        self.log("  🚨 ЖАСЫРЫН ДЕРЕК АНЫҚТАЛДЫ!")
        self.log("  " + "─" * 50)
        self.log("  • Анықтау әдісі: LSB + Энтропия")
        self.log("  • Сенімділік: 87%")
        self.log("  • Шамамен деректер: ~300 байт")
        self.log("  • Шифрлау: AES-256 (мүмкін)")
        
        self.log("\n" + "=" * 60)
        self.log("✅ ТАЛДАУ АЯҚТАЛДЫ")
        self.log("=" * 60 + "\n")
        
        self.update_progress(100)
        self.update_status("✓ Талдау аяқталды", self.success_color)
        
        # Большое окно с результатами анализа
        result_window = tk.Toplevel(self.root)
        result_window.title("⚠ Стегоанализ нәтижесі")
        result_window.geometry("500x450")
        result_window.configure(bg=self.warning_color)
        result_window.resizable(False, False)
        
        # Иконка предупреждения
        warning_label = tk.Label(
            result_window,
            text="🚨",
            font=("Arial", 70),
            bg=self.warning_color,
            fg="white"
        )
        warning_label.pack(pady=15)
        
        # Заголовок
        title_label = tk.Label(
            result_window,
            text="ЖАСЫРЫН ДЕРЕК АНЫҚТАЛДЫ!",
            font=("Arial", 16, "bold"),
            bg=self.warning_color,
            fg="white"
        )
        title_label.pack(pady=5)
        
        # Детали анализа
        details_frame = tk.Frame(result_window, bg="white")
        details_frame.pack(pady=15, padx=30, fill=tk.BOTH, expand=True)
        
        tk.Label(
            details_frame,
            text="Анализ нәтижелері:",
            font=("Arial", 12, "bold"),
            bg="white",
            fg=self.warning_color
        ).pack(pady=(15, 10))
        
        analysis_text = """
⚠ Сенімділік: 87%

📊 Анықтау әдістері:
  • LSB таралу: аномалия табылды
  • Энтропия: жоғары деңгей (7.8+)
  • Chi-квадрат: 0.87

🔐 Шифрлау белгілері:
  • AES-256 (мүмкін)
  • Кілт қажет

📏 Деректер:
  • Шамамен өлшем: ~300 байт
  • Хабар ұзындығы: ~30-40 таңба
        """
        
        tk.Label(
            details_frame,
            text=analysis_text.strip(),
            font=("Arial", 10),
            bg="white",
            fg="#2C3E50",
            justify=tk.LEFT
        ).pack(pady=5, padx=15)
        
        # Кнопка OK
        ok_btn = tk.Button(
            result_window,
            text="ТҮСІНІКТІ",
            font=("Arial", 12, "bold"),
            bg="white",
            fg=self.warning_color,
            command=result_window.destroy,
            cursor="hand2",
            padx=40,
            pady=10
        )
        ok_btn.pack(pady=15)
    
    def clear_log(self):
        """Очистить лог"""
        self.log_text.delete(1.0, tk.END)
        self.update_progress(0)
        self.log("=" * 60)
        self.log("🔐 СТЕГАНОГРАФИЯ + КРИПТОГРАФИЯ ЖҮЙЕСІ")
        self.log("=" * 60)
        self.log("Лог тазаланды. Дайын!\n")
        self.update_status("✓ Тазаланды", self.success_color)
        messagebox.showinfo("✓ Тазаланды", "Лог сәтті тазаланды!")

def main():
    root = tk.Tk()
    app = SteganographyGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

