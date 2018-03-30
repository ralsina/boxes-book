"""
Usage:
    boxes <input> <output>
    boxes --version
"""

from docopt import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Boxes 0')
    print(arguments)
