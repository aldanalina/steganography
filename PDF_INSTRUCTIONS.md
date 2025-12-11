# PDF Файлды Жасау Нұсқаулары

## Әдіс 1: Браузер арқылы (Ең оңай)

1. `Steganography_Practices_Report.html` файлды браузерде ашыңыз
2. **File → Print** (немесе Cmd+P / Ctrl+P)
3. **Destination** ретінде **"Save as PDF"** таңдаңыз
4. **Save** батырмасын басып, `Steganography_Practices_Report.pdf` ретінде сақтаңыз

## Әдіс 2: Скрипт арқылы (macOS)

```bash
./convert_to_pdf.sh
```

## Әдіс 3: Python арқылы (егер weasyprint орнатылған болса)

```bash
pip install weasyprint
python3 -c "from weasyprint import HTML; HTML('Steganography_Practices_Report.html').write_pdf('Steganography_Practices_Report.pdf')"
```

## Әдіс 4: wkhtmltopdf (Linux)

```bash
sudo apt install wkhtmltopdf
wkhtmltopdf Steganography_Practices_Report.html Steganography_Practices_Report.pdf
```

## Ескерту

HTML файл барлық практикалық жұмыстардың есептерін, код мысалдарын және нәтижелерді қамтиды. PDF-ке түрлендіргеннен кейін барлық ақпарат сақталады.

