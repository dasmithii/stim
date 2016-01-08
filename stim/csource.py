from stim import opcode




def from_opcodes(ops):
    r = '''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>

#define BF_INITIAL_CAPACITY 512


static unsigned int max, len;
static unsigned char *dat, *ptr;



// Checks if ptr is at end of allocated array. Doubles
// capacity if so.
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
    ptr = dat;

''' 

    # TODO: make optimizations for special cases.
    for o in ops:
        r += '\n'
        if o[1] == opcode.INCREMENT:
            r += '*ptr+=' + str(o[0]) + ';'
        elif o[1] == opcode.DECREMENT:
            r += '*ptr-=' + str(o[0]) + ';'
        elif o[1] == opcode.RIGHT:
            r += 'ptr+=' + str(o[0]) + '; bf_check_expand();'
        elif o[1] == opcode.LEFT:
            r += 'ptr-=' + str(o[0]) + ';'
        elif o[1] == opcode.OPEN:
            r += 'while(*ptr){'
        elif o[1] == opcode.CLOSE:
            r += '}'
        elif o[1] == opcode.READ:
            if o[0] == 1:
                r += '*ptr=getchar();'
            else:
                r += 'for(int i=0; i<' + str(o[0]) + ';i++){*ptr=getchar();}'
        elif o[1] == opcode.WRITE:
            if o[0] == 1:
                r += 'putchar(*ptr);'
            else:
                r += 'for(int i=0; i<' + str(o[0]) + ';i++){putchar(*ptr);}'
        else:
            raise 'invalid opchar'

    r += 'free(dat);}'

    return r
