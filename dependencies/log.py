import os, logging
from datetime import datetime


class Log:
    def __init__(self, path):
        # create logs folder in current path
        current_path = os.path.dirname(os.path.abspath(__file__))
        log_dir = os.path.join(current_path, f"../{path}")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # create log file for current session
        current_time = datetime.now()
        self.log_file = os.path.join(log_dir, f"{current_time}.log")

    def log(self, message, level="INFO"):
        # Configure logging (optional for basic usage)
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format="[%(asctime)s] [%(levelname)s] %(message)s",
        )

        # Validate log level
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if level not in valid_levels:
            raise ValueError(
                f"Invalid log level: '{level}'. Valid levels are: {', '.join(valid_levels)}"
            )

        # Log the message using the logging module
        log_text = f"{message}"
        print(f"{level+': ' if level!='INFO' else ''}{log_text}")
        logging.log(getattr(logging, level.upper()), log_text)
