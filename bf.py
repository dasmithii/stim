class Op:
	inc = 0
	dec = 1
	left = 2
	right = 3
	read = 4
	write = 5 
	open = 6
	close = 7


charOp = {
	'+': Op.inc,
	'-': Op.dec,
	'<': Op.left,
	'>': Op.right,
	',': Op.read,
	'.': Op.write,
	'[': Op.open,
	']': Op.close,
}


opName = ['INC', 'DEC', 'LEFT', 'RIGHT', 'READ', 'WRITE', 'OPEN', 'CLOSE']


opChar = {v: k for k, v in charOp.items()}



def optimized(code):
	o = []
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
			o.append((n,charOp[code[0]]))
			code = code[1:]
		else:
			raise 'invalid code!!!!'
	return o



def expand(code):
	return ''.join(op[0]*opChar[op[1]] for op in optimized(code))




def optimize(code):
	code = ''.join(c for c in code if c in '+-<>.,[]')
	o = []
	while len(code) > 0:
		plen = len(code)
		c = code[0]
		if c in '<>':
			i = 0
			while len(code) > 0 and code[0] in '<>':
				tmp = code.lstrip('<')
				i -= len(code) - len(tmp)
				code = tmp
				tmp = code.lstrip('>')
				i += len(code) - len(tmp)
				code = tmp
			if i < 0:
				o.append((-i, Op.left))
			elif i > 0:
				o.append((i, Op.right))
		elif c in '+-':
			i = 0
			while len(code) > 0 and code[0] in '+-':
				tmp = code.lstrip('-')
				i -= len(code) - len(tmp)
				code = tmp
				tmp = code.lstrip('+')
				i += len(code) - len(tmp)
				code = tmp
			if i < 0:
				o.append((-i, Op.dec))
			elif i > 0:
				o.append((i, Op.inc))
		else:
			o.append((1, charOp[c]))
			code = code[1:]
	return o




def compile(ops):
	r = '''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>

#define INITIAL_CAPACITY 512


unsigned int max, len;
unsigned char *dat, *ptr;



// Checks if ptr is at end of allocated array. Doubles
// capacity if so.
void check_expand(){
	if(ptr - dat > max){
		size_t targ = 2*max;
		if(ptr >= dat + targ){
			targ = ptr - dat + 15;
		}
		unsigned char *tmp = realloc(dat, targ);
		ptr += tmp - dat;
		dat = tmp;
		for(int i = max; i < targ; i++)
			ptr[i] = 0;
		max = targ;
	}
}


#define INC(x)    *ptr += x;
#define DEC(x)    *ptr -= x;
#define LEFT(x)    ptr -= x; 
#define RIGHT(x)   ptr += x; check_expand();

#define OPEN(x)   while(*ptr){
#define CLOSE(x)  }
#define READ(x)   *ptr=getchar();
#define WRITE(x)  putchar(*ptr);






int main(){
	max = INITIAL_CAPACITY;
	dat = malloc(max);
	memset(dat, 0, max);
	ptr = dat;

'''
	for op in ops:
		r += opName[op[1]] + '(' + str(op[0]) + ')\n'
	
	r += '''

	free(dat);
}
'''
	return r
