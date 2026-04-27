import subprocess

try:
    print("Starting App...")

    backend = subprocess.Popen(
        ["python", "app.py"], 
        cwd="app"
    )

except Exception as e:
    print(f"Error starting app: {e}")
