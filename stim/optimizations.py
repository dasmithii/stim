from stim import csource
from stim import opcode



class Matcher:

	def __init__(self, code_generator, recognizer):
		self._rec = recognizer
		if type(code_generator) == str:
			def g(vs):
				return code_generator
			self._gen = g
		else:
			self._gen = code_generator


	def len(self):
		return len(self._rec)

	def match(self, ops):
		vs = {}
		if len(ops) < self.len():
			return '', ops
		for i, part in enumerate(self._rec):
			op = ops[i]
			if op[1] != part[1]:
				return '', ops
			if type(part[0]) == str:
				vn = part[0]
				if vn not in vs:
					vs[vn] = op[0]
				elif vs[vn] != op[0]:
					return '', ops
			elif op[0] != part[0]:
				return '', ops
		return self._gen(vs), ops[self.len():]




zero = Matcher(csource.SET(0), [(1,opcode.OPEN), (1,opcode.DEC), (1,opcode.CLOSE)])
set_to = Matcher(lambda v: csource.SET(v['n']), [(1,opcode.OPEN), (1,opcode.DEC), (1,opcode.CLOSE), ('n', opcode.INC)])






each = [zero, set_to]



static = [
    (csource.SET(0), [(1, opcode.OPEN), (1,opcode.DEC), (1,opcode.CLOSE)]),
    ()
]