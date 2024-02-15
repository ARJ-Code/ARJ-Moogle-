from news.recomendation import build_dataset
import sys

cant_lines = -1

try:
    cant_lines = int(sys.argv[1])
except:
    pass

build_dataset(cant_lines)
