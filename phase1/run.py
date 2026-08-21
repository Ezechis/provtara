"""python run.py  →  http://127.0.0.1:5055  (Render/Railway: $PORT, 0.0.0.0)"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT.parent / "phase0" / "src"))

from phase1.web import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5055"))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug, threaded=True, use_reloader=debug)

