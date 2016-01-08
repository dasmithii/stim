INCREMENT = 0
DECREMENT = 1
LEFT = 2
RIGHT = 3
READ = 4
WRITE = 5 
OPEN = 6
CLOSE = 7


CONTROL_CODES = [OPEN, CLOSE]
MUTATOR_CODES = [INCREMENT, DECREMENT]
SHIFTER_CODES = [LEFT, RIGHT]
IO_CODES = [READ, WRITE]



# Brainfuck character to opcode conversion.
CHAR_OP_TABLE = {
	'+': INCREMENT,
	'-': DECREMENT,
	'<': LEFT,
	'>': RIGHT,
	',': READ,
	'.': WRITE,
	'[': OPEN,
	']': CLOSE,
}
def from_char(c):
	return CHAR_OP_TABLE[c]



# Opcode to name conversion.
OP_NAME_TABLE = ['INCREMENT', 'DECREMENT', 'LEFT', 'RIGHT', 'READ', 'WRITE', 'OPEN', 'CLOSE']
def to_name(n):
	return OP_NAME_TABLE[n]



# Opcode to 
OP_CHAR_TABLE = {v: k for k, v in CHAR_OP_TABLE.items()}
def to_char(o):
	return OP_CHAR_TABLE[o]



CHAR_SET = CHAR_OP_TABLE.keys()





