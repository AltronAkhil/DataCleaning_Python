import subprocess
import time

try:
    print("Starting App...")

    backend = subprocess.Popen(
        ["python", "app.py"], 
        cwd="app"
    )
    time.sleep(2)
except Exception as e:
    print(f"Error starting App: {e}")

