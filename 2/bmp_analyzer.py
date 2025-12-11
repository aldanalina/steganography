#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практикалық жұмыс 2: BMP файлының он алтылық дампын талдау
BMP файл құрылымын талдау және пиксельдік деректерді оқу
"""

import struct
import sys

class BMPAnalyzer:
    def __init__(self, filename):
        self.filename = filename
        self.data = None
        self.file_size = 0
        self.width = 0
        self.height = 0
        self.bits_per_pixel = 0
        self.pixel_data_offset = 0
        
    def read_file(self):
        """Файлды оқу"""
        with open(self.filename, 'rb') as f:
            self.data = f.read()
        self.file_size = len(self.data)
        
    def analyze_header(self):
        """BMP файл тақырыбын талдау"""
        if len(self.data) < 54:
            raise ValueError("Файл тым кішкентай, BMP емес!")
        
        # Бірінші екі байт - "BM" (42 4D)
        signature = self.data[0:2]
        if signature != b'BM':
            raise ValueError("Бұл BMP файл емес! Сигнатура: " + str(signature))
        
        print("=" * 60)
        print("BMP Файл Тақырыбы Талдауы")
        print("=" * 60)
        print(f"\n1. Сигнатура (0-1 байт): {signature.hex().upper()} ({signature.decode('ascii', errors='ignore')})")
        
        # Файл өлшемі (2-5 байт, little-endian)
        self.file_size = struct.unpack('<I', self.data[2:6])[0]
        print(f"2. Файл өлшемі (2-5 байт): {hex(self.file_size)} ({self.file_size} байт)")
        
        # Резерв (6-9 байт)
        reserved = struct.unpack('<I', self.data[6:10])[0]
        print(f"3. Резерв (6-9 байт): {hex(reserved)}")
        
        # Pixel Data Offset (10-13 байт)
        self.pixel_data_offset = struct.unpack('<I', self.data[10:14])[0]
        print(f"4. Pixel Data Offset (10-13 байт): {hex(self.pixel_data_offset)} ({self.pixel_data_offset} байт)")
        
        # DIB Header өлшемі (14-17 байт)
        dib_size = struct.unpack('<I', self.data[14:18])[0]
        print(f"5. DIB Header өлшемі (14-17 байт): {hex(dib_size)} ({dib_size} байт)")
        
        # Ені (18-21 байт)
        self.width = struct.unpack('<i', self.data[18:22])[0]
        print(f"6. Ені (18-21 байт): {hex(self.width)} ({self.width} пиксель)")
        
        # Биіктігі (22-25 байт)
        self.height = struct.unpack('<i', self.data[22:26])[0]
        print(f"7. Биіктігі (22-25 байт): {hex(self.height)} ({abs(self.height)} пиксель)")
        
        # Color Planes (26-27 байт)
        planes = struct.unpack('<H', self.data[26:28])[0]
        print(f"8. Color Planes (26-27 байт): {hex(planes)} ({planes})")
        
        # Bits per Pixel (28-29 байт)
        self.bits_per_pixel = struct.unpack('<H', self.data[28:30])[0]
        print(f"9. Bits per Pixel (28-29 байт): {hex(self.bits_per_pixel)} ({self.bits_per_pixel} бит)")
        
        # Compression (30-33 байт)
        compression = struct.unpack('<I', self.data[30:34])[0]
        print(f"10. Compression (30-33 байт): {hex(compression)} ({compression})")
        
        return {
            'signature': signature.hex().upper(),
            'file_size': self.file_size,
            'width': self.width,
            'height': abs(self.height),
            'bits_per_pixel': self.bits_per_pixel,
            'pixel_offset': self.pixel_data_offset
        }
    
    def analyze_color_table(self):
        """Түс палитрасын талдау (8-биттік BMP үшін)"""
        if self.bits_per_pixel > 8:
            print("\n24-биттік BMP - палитра жоқ, пиксельдік деректер бірден басталады.")
            return None
        
        color_table_start = 54
        color_table_size = (2 ** self.bits_per_pixel) * 4
        
        print("\n" + "=" * 60)
        print("Түс Палитрасы Талдауы")
        print("=" * 60)
        
        colors = []
        for i in range(min(10, 2 ** self.bits_per_pixel)):  # Алғашқы 10 түс
            offset = color_table_start + i * 4
            if offset + 4 > len(self.data):
                break
            
            # BMP палитрасы: Blue, Green, Red, Reserved
            b, g, r, reserved = struct.unpack('<BBBB', self.data[offset:offset+4])
            colors.append((r, g, b))
            print(f"\nТүс {i}:")
            print(f"  Offset: {hex(offset)}")
            print(f"  Hex: B={hex(b)}, G={hex(g)}, R={hex(r)}")
            print(f"  Decimal: RGB({r}, {g}, {b})")
        
        return colors
    
    def analyze_pixel_data(self):
        """Пиксельдік деректерді талдау"""
        print("\n" + "=" * 60)
        print("Пиксельдік Деректер Талдауы")
        print("=" * 60)
        
        if self.pixel_data_offset >= len(self.data):
            print("Пиксельдік деректер файл ішінде жоқ!")
            return None
        
        print(f"\nПиксельдік деректер басталады: offset {hex(self.pixel_data_offset)} ({self.pixel_data_offset} байт)")
        
        # Алғашқы 10 пиксельді оқу
        if self.bits_per_pixel == 24:
            bytes_per_pixel = 3
            print("\n24-биттік формат (BGR):")
            for i in range(min(10, (len(self.data) - self.pixel_data_offset) // bytes_per_pixel)):
                offset = self.pixel_data_offset + i * bytes_per_pixel
                if offset + bytes_per_pixel > len(self.data):
                    break
                
                b, g, r = struct.unpack('<BBB', self.data[offset:offset+3])
                print(f"  Пиксель {i}: B={hex(b)}, G={hex(g)}, R={hex(r)} → RGB({r}, {g}, {b})")
        
        elif self.bits_per_pixel == 8:
            print("\n8-биттік формат (палитра индексі):")
            for i in range(min(10, (len(self.data) - self.pixel_data_offset))):
                offset = self.pixel_data_offset + i
                if offset >= len(self.data):
                    break
                index = self.data[offset]
                print(f"  Пиксель {i}: Палитра индексі = {index} ({hex(index)})")
        
        return True
    
    def hex_dump(self, start=0, length=64):
        """Hex дамп шығару"""
        print("\n" + "=" * 60)
        print(f"Hex Дамп (бастап {hex(start)}, {length} байт)")
        print("=" * 60)
        
        end = min(start + length, len(self.data))
        for i in range(start, end, 16):
            hex_part = ' '.join(f'{b:02X}' for b in self.data[i:i+16])
            ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in self.data[i:i+16])
            print(f"{i:08X}: {hex_part:<48} {ascii_part}")


def main():
    if len(sys.argv) < 2:
        print("Қолдану: python bmp_analyzer.py <bmp_file>")
        print("Мысал: python bmp_analyzer.py sample.bmp")
        return
    
    filename = sys.argv[1]
    
    try:
        analyzer = BMPAnalyzer(filename)
        analyzer.read_file()
        analyzer.analyze_header()
        analyzer.analyze_color_table()
        analyzer.analyze_pixel_data()
        analyzer.hex_dump(0, 64)
        
        print("\n" + "=" * 60)
        print("Талдау аяқталды!")
        print("=" * 60)
        
    except Exception as e:
        print(f"Қате: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

