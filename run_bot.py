import time

from loguru import logger
from data.habr_freelance import main as run_habr
from data.FLru import main as run_flru

# Настройка логирования
logger.add("logfile.log", rotation="500 MB", level="INFO")


def main():
    from data.kwork import main as run_kwork

    while True:
        # run_kwork()
        run_habr()
        run_flru()

        time.sleep(30)


if __name__ == "__main__":
    main()
