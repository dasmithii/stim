from stim import opcode



def INC(n):
    return '*ptr+=' + str(n) + ';'
def DEC(n):
    return '*ptr-=' + str(n) + ';'
def RIGHT(n):
    return 'ptr+=' + str(n) + ';bf_check_expand();'
def LEFT(n):
    return 'ptr-=' + str(n) + ';'
def OPEN(): 
    return 'while(*ptr){'
def CLOSE():
    return '}'
def READ(n=1):
    return 'for(int i=0; i < ' + str(n) + '; i++) *ptr=getchar();'
def WRITE(n=1):
    return 'for(int i=0; i < ' + str(n) + '; i++) putchar(*ptr);'

def SET(n):
    return '*ptr=' + str(n) + ';'



def convert_one(op):
    if op[1] == opcode.INC:
        return INC(op[0])
    elif op[1] == opcode.DEC:
        return DEC(op[0])
    elif op[1] == opcode.RIGHT:
        return RIGHT(op[0])
    elif op[1] == opcode.LEFT:
        return LEFT(op[0])
    elif op[1] == opcode.OPEN:
        return OPEN()
    elif op[1] == opcode.CLOSE:
        return CLOSE()
    elif op[1] == opcode.READ:
        return READ(op[0])
    elif op[1] == opcode.WRITE:
        return WRITE(op[0])
    raise ValueError('invalid op')


def convert(ops):
    return ''.join(convert_one(op) for op in ops)



class boilerplate:
    def soround(text):
        return boilerplate.top + text + boilerplate.bottom
    bottom = 'free(dat);}'
    top = '''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>

#define BF_INITIAL_CAPACITY 512
static unsigned int max, len;
static unsigned char *dat, *ptr;

void bf_check_expand(){
    if(ptr - dat > max){
        size_t targ = 2*max;
        if(ptr >= dat + targ){
            targ = ptr - dat + 15;
        }
        unsigned char *tmp = realloc(dat, targ);
        ptr += tmp - dat;
        dat = tmp;
        for(int i = max; i < targ; i++){
            ptr[i] = 0;
        }
        max = targ;
    }
}

int main(){
    max = BF_INITIAL_CAPACITY;
    dat = malloc(max);
    memset(dat, 0, max);
    ptr = dat;'''



