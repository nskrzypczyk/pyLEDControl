import logging
import settings
from pathlib import Path
import pickle as pkl


class Log(logging.Logger):
    def __init__(self, name: str, level: any = settings.LOG_LEVEL) -> None:
        super().__init__(name, level)
        self.name = name
        self.setLevel(level)

        log_path = "logs"
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(name)s : %(message)s')
        Path(log_path).mkdir(parents=True, exist_ok=True)

        handler = logging.FileHandler(f"logs/{name}.log")
        handler.setLevel(level)
        handler.setFormatter(formatter)
        self.addHandler(handler)

        if settings.ENABLE_STDOUT:
            stdout_handler = logging.StreamHandler()
            stdout_handler.setLevel(level)
            stdout_handler.setFormatter(formatter)
            self.addHandler(stdout_handler)
