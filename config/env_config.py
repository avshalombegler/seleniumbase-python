import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://the-internet.herokuapp.com/")
BROWSER = os.getenv("BROWSER", "chrome")
SHORT_TIMEOUT = int(os.getenv("SHORT_TIMEOUT", 3))
LONG_TIMEOUT = int(os.getenv("LONG_TIMEOUT", 10))
HEADLESS = os.getenv("HEADLESS", "True").lower() == "true"
MAXIMIZED = os.getenv("MAXIMIZED", "False").lower() == "true"
USERNAME = os.getenv("USERNAME", "tomsmith")
PASSWORD = os.getenv("PASSWORD", "SuperSecretPassword!")
