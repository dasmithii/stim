from stim import csource
from stim import opcode
from stim import optimizations

import tempfile
import os
import subprocess
import sys
import re

import random
import string



def compile_to_C(code):
    code = lint(code)
    ops = join_sisters(code)
    c = ''
    while len(ops) > 0:
        p = len(ops)
        for optimization in optimizations.each:
            s, ops = optimization.match(ops)
            c += s
        if p == len(ops):
            c += csource.convert_one(ops[0])
            ops = ops[1:]
    return csource.boilerplate.soround(c)


def compile_to_executable(code, output):
    c_path = _random_c_path()
    with open(c_path, 'w') as c_file:
        c_file.write(compile_to_C(code))
    x_path = c_path[0:-2]
    rc = subprocess.call(['make', x_path],stdout=sys.stdout,stderr=sys.stderr)
    if rc != 0:
        raise Exception('C-to-executable compilation failed.')
    else:
        subprocess.call(['mv', x_path, output], stderr=sys.stderr)
    os.remove(c_path)


def execute(code):
    c_path = _random_c_path()
    c_file = open(c_path, 'w')
    with open(c_path, 'w') as c_file:
        c_file.write(compile_to_C(code))

    x_path = c_path[0:-2]
    rc = subprocess.call(['make', x_path, '-s'])
    if rc != 0:
        print('C-to-executable compilation failed.', file=sys.stderr)
    else:
        try:
            s = subprocess.check_output([x_path]).decode('utf-8')
        except KeyboardInterrupt:
            pass # ignore CTRL-C
        if rc != 0:
            raise ValueError('Error in .bf program execution.')
        else:
            subprocess.call(['rm', x_path])

    os.remove(c_path)
    return s




def lint(code):
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
            raise ValueError("invalid brainfuck character: '" + c + "'")

    return code



def join_sisters(code):
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
            raise ValueError('invalid code!!!! FUCK FUCK FUCK')

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
                n = ops[0][0] if o1 == opcode.INC else -ops[0][0]
                n += ops[1][0] if o1 == opcode.DEC else -ops[1][0]
                ops[1] = (n,opcode.INC) if n > 0 else (-n,opcode.DEC)
        old = ops
        ops = list(filter(lambda x: x[0] > 0, ops))
        if len(ops) == len(old):
            break

    return ops


def _random_c_path():
    return '/tmp/stim_' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25)) + '.c'


