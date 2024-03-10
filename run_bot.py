import time

from data.kwork import main as run_kwork
from data.habr_freelance import main as run_habr


def main():
    while True:
        # run_kwork()
        run_habr()

        time.sleep(60 * 5)


if __name__ == "__main__":
    main()
