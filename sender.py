import os
import sys
import time
import random
import OneTile
from multiprocessing import Pool




def randomTester(path):
    OneTile.main(path, "live_mz")
    return


def main(path):
    randomTester(path)
    return

if __name__ == "__main__":
    main(sys.argv[1])


