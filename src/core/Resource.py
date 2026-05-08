import sys
from pathlib import Path



def resource_path(relative: str) -> Path:
    base = Path(getattr(sys, '_MEIPASS', Path(__file__).parent.parent.parent))
    return base / relative
