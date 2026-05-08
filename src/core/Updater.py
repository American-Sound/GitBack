import sys
import json
import urllib.request
import os
import subprocess
import tempfile



try:
    from version import __version__
except ImportError:
    __version__ = "0.0.0-dev"



VERSION_URL = "https://github.com/american-sound/GitBack/releases/latest/download/version.json"
TIMEOUT = 5



def check_for_update():
    try:
        with urllib.request.urlopen(VERSION_URL, timeout=TIMEOUT) as r:
            data = json.loads(r.read())
        return data if data["version"] != __version__ else None
    except Exception:
        return None



def get_download_url(update_info):
    if sys.platform == "win32":
        return update_info["windows_installer"]
    elif sys.platform == "linux":
        return update_info["linux_binary"]



def download_update(url):
    suffix = ".exe" if sys.platform == "win32" else ".tar.gz"
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    urllib.request.urlretrieve(url, tmp.name)
    return tmp.name



def apply_update(downloaded_path):
    if sys.platform == "win32":
        _apply_windows(downloaded_path)
    else:
        _apply_linux(downloaded_path)



def _apply_windows(installer_path):
    subprocess.Popen([installer_path, "/SILENT"])
    sys.exit(0)



def _apply_linux(tar_path):
    import tarfile
    install_dir = os.path.dirname(sys.executable)
    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(install_dir)
    os.remove(tar_path)
    os.execv(sys.executable, [sys.executable] + sys.argv)