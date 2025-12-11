# Практика 10: Кеңейтілген Қолдану Тәсілдері

## Мақсаты
Криптостеганография, QR-код, контейнерлер

## Қажетті Файлдар
- PNG сурет (криптостеганография үшін)
- Мәтін файлы (контейнер үшін)

## Қолдану

```python
from advanced_steganography import AdvancedSteganography
from Crypto.Random import get_random_bytes

advanced = AdvancedSteganography()
key = get_random_bytes(16)

# Криптостеганография
advanced.crypto_steganography('cover.png', 'Secret', key, 'hidden.png')
message = advanced.crypto_steganography_reveal('hidden.png', key)

# QR-код
advanced.create_qr_code('SecretKey=AI4567', 'secret_qr.png')
advanced.hide_qr_in_image('secret_qr.png', 'cover.png', 'qr_in_image.png')

# Контейнер
advanced.create_container('secret.txt', 'container.zip')
advanced.extract_from_container('container.zip', 'extracted/')

# Қауіпсіз жою
advanced.secure_delete('secret.txt', passes=3)
```

## Нәтиже
- `hidden.png` - криптостеганография
- `secret_qr.png` - QR-код
- `container.zip` - контейнер
- `key.bin` - кілт файлы

