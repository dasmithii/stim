from stim import csource
from stim import opcode

import tempfile
import os
import subprocess
import sys
import re

import random
import string




def compile_to_C(code, output=None):
    # Remove C-style block comments.
    code = re.sub('/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/', '', code)

    # Remove C-style line comments.
    def line_decomment(x):
        i = x.find('//')
        return x if i == -1 else x[0:i]
    code = ''.join(map(line_decomment, code.split('\n')))

    # Remove whitespace.
    code = ''.join(code.split())

    # Check for invalid characters.
    for c in code:
        if (not c.isdigit()) and c not in opcode.CHAR_SET:
            raise 'invalid brainfuck character'

    # Read in operations. Kill code variable. TODO: improve.
    ops = []
    while len(code) > 0:
        c = code[0]
        n = 1
        if c.isdigit():
            ns = ''
            while len(code) > 1 and code[0].isdigit():
                ns += code[0]
                code = code[1:]
            n = int(ns)
        if code[0] in '+-<>.,[]':
            ops.append((n,opcode.from_char(code[0])))
            code = code[1:]
        else:
            raise 'invalid code!!!!'

    # Combine neighboring sister operations until no more can be
    # combined.
    while True:
        change = False
        for i in range(len(ops)-1):
            o1 = ops[i][1]
            o2 = ops[i+1][1]
            if o1 in opcode.CONTROL_CODES:
                continue
            elif o1 == o2 and o1 not in opcode.CONTROL_CODES:
                ops[i+1] = (ops[i+1][0] + ops[i][0], ops[i+1][1])
                ops[i] = (0, ops[i][1])
            elif o1 in opcode.SHIFTER_CODES and o2 in opcode.SHIFTER_CODES:
                n = ops[0][0] if o1 == opcode.RIGHT else -ops[0][0]
                n += ops[1][0] if o1 == opcode.RIGHT else -ops[1][0]
                ops[1][0] = (n,opcode.RIGHT) if n > 0 else (-n,opcode.LEFT)
            elif o1 in opcode.MUTATOR_CODES and o2 in opcode.MUTATOR_CODES:
                n = ops[0][0] if o1 == opcode.INCREMENT else -ops[0][0]
                n += ops[1][0] if o1 == opcode.DECREMENT else -ops[1][0]
                ops[1] = (n,opcode.INCREMENT) if n > 0 else (-n,opcode.DECREMENT)
        old = ops
        ops = list(filter(lambda x: x[0] > 0, ops))
        if len(ops) == len(old):
            break

    #Generate C code.
    compiled = csource.from_opcodes(ops)

    if output:
        with open(output, 'w') as ofile:
            ofile.write(compiled)

    return compiled



def _random_c_path():
    return '/tmp/stim_' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25)) + '.c'


def compile_to_executable(code, output):
    c_path = _random_c_path()
    c_file = open(c_path, 'w')

    c_file.write(compile_to_C(code))

    c_file.close()

    x_path = c_path[0:-2]
    rc = subprocess.call(['make', x_path],stdout=sys.stdout,stderr=sys.stderr)
    if rc != 0:
        print('C-to-executable compilation failed.', file=sys.stderr)
    else:
        rc = subprocess.call(['mv', x_path, output], stderr=sys.stderr)
    os.remove(c_path)


def execute(code):
    c_path = _random_c_path()
    c_file = open(c_path, 'w')

    c_file.write(compile_to_C(code))

    c_file.close()

    x_path = c_path[0:-2]
    rc = subprocess.call(['make', x_path],stderr=sys.stderr)
    if rc != 0:
        print('C-to-executable compilation failed.', file=sys.stderr)
    else:
        try:
            rc = subprocess.call([x_path],stdin=sys.stdin, stdout=sys.stdout,stderr=sys.stderr)
        except KeyboardInterrupt:
            pass # ignore CTRL-C
        if rc != 0:
            print('Error in .bf program execution.', file=sys.stderr)
        else:
            rc = subprocess.call(['rm', x_path],stderr=sys.stderr)

    os.remove(c_path)



