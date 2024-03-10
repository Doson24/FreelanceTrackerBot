import time

from data.kwork import main as run_kwork
from data.habr_freelance import main as run_habr
from bot.main import run_telegram_wrapper as run_telegram


def main():
    while True:
        # run_kwork()
        run_habr()

        run_telegram()
        time.sleep(60 * 5)


if __name__ == "__main__":
    main()
