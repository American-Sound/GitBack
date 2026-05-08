python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

$version = if ($env:APP_VERSION) { $env:APP_VERSION } else { "0.0.0-dev" }
Set-Content -Path src/version.py -Value "__version__ = '$version'"

pyinstaller `
    --onefile `
    --noconfirm `
    --windowed `
    --name "GitBack" `
    --add-data "res;res" `
    --paths "src" `
    --contents-directory "." `
    --collect-binaries "python311" `
    src/main.py