from datetime import datetime


class Logger:
    def info(self, message):
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] [INFO] {message}"
        )

    def warning(self, message):
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] [WARNING] {message}"
        )

    def error(self, message):
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] [ERROR] {message}"
        )