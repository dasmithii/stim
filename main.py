"""stim (brainfuck-to-C compiler).

Usage:
  main.py <path> [-p | -o | -e]
  main.py (-h | --help)
  main.py (-v | --version)

Options:
  -h --help        Display this text.
  -v --version     Check version.
  <path>           Path to code.
  -p               Note that input is pre-optimized.
  -e               Expand optimized code to regular brainfuck.

"""
from docopt import docopt
import bf

if __name__ == '__main__':
    args = docopt(__doc__, version='stg-python 0.0.1')

    with open(args['<path>']) as ifile:
    	code = ifile.read()
    	if args['-p']:
    		print(bf.compile(bf.optimized(code)))
    	elif args['-e']:
    		print(bf.expand(code))
    	else:
    		print(bf.compile(bf.optimize(code)))





