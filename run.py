
import subprocess
import webbrowser
import time
import sys
import threading

URL = "http://127.0.0.1:8000"

def open_browser():
    time.sleep(5)
    webbrowser.open(URL)

threading.Thread(target=open_browser, daemon=True).start()

subprocess.run([
    sys.executable,
    "-m", "uvicorn",
    "app.main:app",
    "--reload",
    "--host", "127.0.0.1",
    "--port", "8000"
])
