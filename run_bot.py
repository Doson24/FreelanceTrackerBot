import time

from data.kwork import main as run_kwork
from data.habr_freelance import main as run_habr
from data.FLru import main as run_flru


def main():
    while True:
        # run_kwork()
        # run_habr()
        run_flru()

        time.sleep(60 * 5)


if __name__ == "__main__":
    main()
