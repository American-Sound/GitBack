python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

VERSION=${APP_VERSION#v}
VERSION=${APP_VERSION:-"0.0.0-dev"}
echo "__version__ = '$VERSION'" > src/version.py

pyinstaller \
    --onefile \
    --noconfirm \
    --windowed \
    --name "GitBack" \
    --add-data "res:res" \
    --paths "src" \
    --contents-directory "." \
    --collect-binaries "python311" \
    src/main.py