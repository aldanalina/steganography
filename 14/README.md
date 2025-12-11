# Практика 14: Крипто + Стего Біріктіру

## Мақсаты
AES шифрлау + LSB енгізу біріктіру

## Қажетті Файлдар
- PNG сурет

## Қолдану

```python
from crypto_stego_combination import CryptoStegoCombination
from Crypto.Random import get_random_bytes

combo = CryptoStegoCombination()
key = get_random_bytes(16)

# Енгізу
combo.encrypt_and_hide('cover.png', 'Secret message', key, 'stego.png')

# Шығару
message = combo.extract_and_decrypt('stego.png', key)

# Әдістерді салыстыру
combo.compare_methods('cover.png', 'Secret message')

# Кілт қауіпсіздігін тексеру
wrong_key = get_random_bytes(16)
combo.test_key_security('stego.png', key, wrong_key)

# Энтропия талдауы
combo.analyze_entropy('cover.png', 'stego.png')
```

## Нәтиже
- `stego.png` - шифрланған және жасырылған сурет
- `key.bin` - кілт файлы
- Салыстыру нәтижелері

## Ескерту
Кілтті қауіпсіз сақтаңыз! Кілтсіз хабарды ашу мүмкін емес.

