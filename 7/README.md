# Практика 7: Стегоанализ - Жасырын Хабарларды Анықтау

## Мақсаты
Статистикалық, визуалдық әдістер арқылы жасырын хабарларды анықтау

## Қажетті Файлдар
- Күдікті сурет файлы
- Бастапқы сурет (салыстыру үшін, опция)

## Қолдану

```python
from steganalysis_detection import Steganalysis

analyzer = Steganalysis()

# Гистограмма талдауы
analyzer.histogram_analysis('suspect.png')

# LSB талдауы
analyzer.lsb_histogram('suspect.png')

# χ² тесті
analyzer.chi_square_test('suspect.png')

# Энтропия талдауы
analyzer.entropy_analysis('suspect.png')

# Визуалды салыстыру
analyzer.visual_difference('original.png', 'suspect.png')

# DCT талдауы (JPEG)
analyzer.dct_analysis('suspect.jpg')
```

## Нәтиже
- Гистограмма графиктері (`histogram_analysis.png`)
- LSB статистикасы
- χ² тест нәтижелері
- Энтропия мәндері
- Айырмашылық картасы (`difference.png`, `difference_heatmap.png`)

