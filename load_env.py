# Load .env file to os environment variables
import os

file = ".env"
if os.path.exists(file):
    with open(file) as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value
                print(f"Loaded env variable: {key}")
