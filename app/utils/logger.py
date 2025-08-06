import logging
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def log_to_console(user_id: str, raw_response: str):
    """
    Log the full raw response to the console.
    """
    logging.info(f"[USER: {user_id}] {raw_response}")