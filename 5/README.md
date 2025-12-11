# Практика 5: Мультимедиа Файлдарда Жасырын Хабарларды Табу

## Мақсаты
Сурет, аудио, бейне файлдарда жасырын хабарларды табу және шығару

## Қажетті Файлдар
- PNG/JPG сурет (LSB талдау үшін)
- WAV аудио файл (опция)
- MP4 бейне файл (опция)

## Қолдану

```python
from multimedia_steganalysis import MultimediaSteganalysis

analyzer = MultimediaSteganalysis()

# Сурет талдау
analyzer.analyze_image_lsb('sample.png')

# Аудио талдау
analyzer.analyze_audio('sample.wav')

# Бейне талдау
analyzer.analyze_video('sample.mp4')

# Салыстыру
analyzer.compare_files('original.png', 'suspect.png')
```

## Нәтиже
- LSB статистикасы
- Жасырын хабар (егер бар болса)
- Файл салыстыруы

