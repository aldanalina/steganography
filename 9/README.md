# Практика 9: Текст және Суретке Жасырын Хабар Енгізу және Жою

## Мақсаты
Текст пен сурет файлдарына ақпаратты жасырын енгізу және жою

## Қажетті Файлдар
- PNG сурет (LSB үшін)
- Мәтін файлы

## Қолдану

```python
from text_image_steganography import TextImageSteganography

stego = TextImageSteganography()

# Суретке LSB енгізу
stego.hide_in_image_lsb('cover.png', 'Secret message', 'hidden.png')

# Суреттен шығару
stego.reveal_from_image('hidden.png')

# Суреттен жою
stego.remove_stego_from_image('hidden.png', 'cleaned.jpg', method='recompress')

# Текстке zero-width енгізу
encoded = stego.hide_in_text_zerowidth('Base text', 'Secret')
revealed = stego.reveal_from_text_zerowidth(encoded)
cleaned = stego.remove_stego_from_text(encoded)
```

## Нәтиже
- `hidden.png` - жасырын хабар енгізілген сурет
- `cleaned.jpg` - жасырын хабар жойылған сурет
- `encoded_text.txt` - zero-width символдар енгізілген мәтін

