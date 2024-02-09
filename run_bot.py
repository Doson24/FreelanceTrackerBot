import time

from data.kwork import main as run_kwork
from bot.main import run_telegram_wrapper as run_telegram


def main():
    while True:
        run_kwork()
        time.sleep(60 * 5)


if __name__ == "__main__":
    main()
