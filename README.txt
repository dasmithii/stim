OVERVIEW:

    stim is an optimizing brainfuck-to-C transpiler.



QUICK START:

    Get rolling:              python3 setup.py install
    Test:                     python3 bin/test

    Compile to C:             stim input.bf output.c
    Compile to executable:    stim input.bf output
    Run file directly:        stim input.bf
    Run string:               stim ">>>>>++++"



BRAINFUCK DIALECT:

    Comments are C-style.
    You can input code with positive integers before brainfuck
    commands to indicate that the command should be repeated n times.