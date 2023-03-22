import logging
import settings
from pathlib import Path

class Log(logging.Logger):
    def __init__(self, name: str, level:any = settings.LOG_LEVEL) -> None:
        super().__init__(name, level)

        log_path = "logs"
        Path(log_path).mkdir(parents=True,exist_ok=True)
        handler = logging.FileHandler(f"logs/{name}.log")
        handler.setLevel(level)

        formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s : %(message)s')
        handler.setFormatter(formatter)

        self.setLevel(level)
        self.name = name
        self.addHandler(handler)
