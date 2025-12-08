# Setup Guide - AI Document Processing Workflow

## Quick Setup (One Command)

Simply run:
```bash
python setup.py
```

That's it! The script will automatically:
1. ✅ Create necessary directories (`data/input`, `data/output`, `log`)
2. ✅ Create/use Python virtual environment (`venv`)
3. ✅ Install all packages from `requirements.txt`
4. ✅ Create config files from templates (`config.json`, `secrets.toml`)
5. ✅ Check for Tesseract OCR installation
6. ✅ Verify API key configuration

## After Setup

### 1. Activate Virtual Environment

**Windows:**
```powershell
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 2. Configure API Keys (REQUIRED)

Edit `config/secrets.toml` and add your API keys:
- OpenAI/Azure OpenAI endpoint and key
- Azure Document Intelligence endpoint and key

### 3. Run the Project

```bash
python main.py --mode all
```

## Manual Installation (If setup.py fails)

If `setup.py` encounters issues, you can install manually:

1. **Create/activate virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac
   ```

2. **Install packages:**
   ```bash
   pip install -r requirements.txt
   ```

## What setup.py Does

- **Creates directories:** `data/input`, `data/output`, `log`
- **Sets up venv:** Creates virtual environment if it doesn't exist
- **Installs dependencies:** Automatically runs `pip install -r requirements.txt` in the venv
- **Config setup:** Copies template files to actual config files
- **Validation:** Checks Tesseract OCR and API key configuration

## Troubleshooting

### Packages not installing?
- Make sure you're using Python 3.11 or 3.12 (Python 3.13 may have compatibility issues)
- Check internet connection
- Try manual installation: `venv\Scripts\python.exe -m pip install -r requirements.txt`

### "Module not found" errors?
- Make sure venv is activated
- Verify packages are installed: `pip list`
- Re-run setup.py or manually install requirements.txt

### Tesseract not found?
- Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
- Mac: `brew install tesseract`
- Linux: `sudo apt-get install tesseract-ocr`

## Notes

- **You only need to run `setup.py` once** (or when requirements.txt changes)
- **Always activate venv** before running the project
- **setup.py installs requirements.txt automatically** - you don't need to run pip install separately
- The script is smart - it won't recreate existing venv or overwrite existing config files

