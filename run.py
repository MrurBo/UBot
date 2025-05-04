import subprocess
import sys
import time


def run_bot():
    subprocess.Popen([sys.executable, "main.py"])


def run_api():
    subprocess.Popen([sys.executable, "api.py"])


if __name__ == "__main__":
    run_bot()
    run_api()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down both processes...")
        