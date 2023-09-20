# brainfuck-compiler
A cursed impelementation of a brainfuck compiler for linux on x86

# How to use it?
Run `python3 main.py -i file.bf` to generate nasm code corresponding to the brainfuck code in `file.bf`.  
Piggyback off of nasm to convert it to x86 using `bash compile.sh`.  
Execute your program using `./brainfuck`.
