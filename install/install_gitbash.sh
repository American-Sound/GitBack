python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
pyinstaller \
    --onedir \
    --noconfirm \
    --windowed \
    --name "GitBack" \
    --add-data "res/logo.png:res" \
    --paths "src" \
    --contents-directory "." \
    --collect-binaries "python311" \
    src/main.py
