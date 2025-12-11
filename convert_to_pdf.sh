#!/bin/bash
# HTML-ді PDF-ке түрлендіру скрипті

echo "HTML файлды PDF-ке түрлендіру..."

# macOS үшін (Chrome/Chromium)
if command -v "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" &> /dev/null; then
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
        --headless \
        --disable-gpu \
        --print-to-pdf=Steganography_Practices_Report.pdf \
        --print-to-pdf-no-header \
        file://$(pwd)/Steganography_Practices_Report.html
    echo "✓ PDF жасалды: Steganography_Practices_Report.pdf"
    exit 0
fi

# Linux үшін (Chrome/Chromium)
if command -v chromium-browser &> /dev/null; then
    chromium-browser --headless --disable-gpu \
        --print-to-pdf=Steganography_Practices_Report.pdf \
        file://$(pwd)/Steganography_Practices_Report.html
    echo "✓ PDF жасалды: Steganography_Practices_Report.pdf"
    exit 0
fi

# wkhtmltopdf
if command -v wkhtmltopdf &> /dev/null; then
    wkhtmltopdf Steganography_Practices_Report.html Steganography_Practices_Report.pdf
    echo "✓ PDF жасалды: Steganography_Practices_Report.pdf"
    exit 0
fi

echo "⚠ PDF конвертер табылмады!"
echo "Қолдану:"
echo "1. HTML файлды браузерде ашыңыз"
echo "2. Print -> Save as PDF басыңыз"
echo "3. 'Steganography_Practices_Report.pdf' ретінде сақтаңыз"

