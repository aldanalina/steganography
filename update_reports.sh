#!/bin/bash
# Барлық есептерді жаңарту және PDF жасау
# Барлық суреттер HTML және PDF ішінде сақталады - бір файлмен бөлісуге болады

echo "📝 HTML есепті жаңарту (суреттерді base64 форматта қосу)..."
python3 generate_html_report.py

echo ""
echo "📄 PDF файлды жасау (суреттер PDF ішінде сақталады)..."
if [ -f "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]; then
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
        --headless --disable-gpu \
        --print-to-pdf=Steganography_Practices_Report.pdf \
        --print-to-pdf-no-header \
        "file://$(pwd)/Steganography_Practices_Report.html" 2>&1 | grep -v "ERROR"
    
    if [ -f "Steganography_Practices_Report.pdf" ]; then
        pdf_size=$(du -h Steganography_Practices_Report.pdf | cut -f1)
        echo "✅ PDF жасалды: Steganography_Practices_Report.pdf (өлшемі: $pdf_size)"
        echo "✅ Барлық суреттер PDF ішінде сақталған - бір файлмен бөлісуге болады!"
    fi
else
    echo "⚠ Chrome табылмады."
    echo "📖 Браузерде HTML файлды ашып, Print -> Save as PDF қолданыңыз"
    echo "   Барлық суреттер PDF-ке де қосылады!"
fi

echo ""
echo "✅ Дайын! Барлық суреттер HTML және PDF ішінде сақталған."
echo "📤 Енді бір файлмен бөлісуге болады:"
echo "   - Steganography_Practices_Report.html (барлық суреттер ішінде)"
echo "   - Steganography_Practices_Report.pdf (барлық суреттер ішінде)"
