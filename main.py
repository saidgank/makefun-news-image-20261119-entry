"""Entry program for the news-image-20261119 competition on make.fun.

The entry image is entry.png beside this file: 'The Daily World' front page
summing up Wednesday 19 November 2026 in 35 stories. This program copies it,
byte for byte, to entry.png in the output directory (MAKEFUN_OUTPUT_DIR
stands in for /output outside the grader). Python 3.13, standard library
only; it runs offline and always produces identical bytes.
"""

import os
import shutil
from pathlib import Path


def main() -> None:
    src = Path(__file__).resolve().parent / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, out_dir / "entry.png")


if __name__ == "__main__":
    main()
