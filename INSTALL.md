# Орнату Нұсқаулары

## 1. Python Орнату

### Windows:
1. [Python.org](https://www.python.org/downloads/) сайтынан Python 3.7+ жүктеңіз
2. Орнату кезінде "Add Python to PATH" опциясын таңдаңыз
3. Терминалда тексеріңіз:
```bash
python --version
```

### Linux/Mac:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# Mac (Homebrew)
brew install python3
```

## 2. Кітапханаларды Орнату

### Негізгі кітапханалар:
```bash
pip install -r requirements.txt
```

### Бөлек орнату (егер қате туындаса):
```bash
pip install Pillow numpy scipy matplotlib
pip install stegano
pip install pycryptodome
pip install opencv-python
pip install pydub
pip install qrcode[pil]
```

## 3. Қосымша Құралдар

### FFmpeg (аудио/бейне өңдеу үшін):

**Windows:**
1. [FFmpeg.org](https://ffmpeg.org/download.html) сайтынан жүктеңіз
2. PATH-қа қосыңыз

**Linux:**
```bash
sudo apt install ffmpeg
```

**Mac:**
```bash
brew install ffmpeg
```

### StegExpose (Java):

**Windows/Linux/Mac:**
1. Java орнатыңыз: `sudo apt install openjdk-11-jre` (Linux)
2. [GitHub](https://github.com/b3dk7/StegExpose/releases) сайтынан StegExpose.jar жүктеңіз

### zsteg (Ruby):

**Linux/Mac:**
```bash
sudo apt install ruby  # Linux
brew install ruby      # Mac
sudo gem install zsteg
```

## 4. Тестілеу

Орнатуды тексеру:
```bash
python -c "import PIL; import numpy; import stegano; print('OK')"
```

Егер "OK" шықса, орнату сәтті!

## 5. Мәселелерді Шешу

### "ModuleNotFoundError":
```bash
pip install <module_name>
```

### "Permission denied":
```bash
pip install --user <module_name>
```

### Windows-та pip табылмады:
```bash
python -m pip install -r requirements.txt
```

