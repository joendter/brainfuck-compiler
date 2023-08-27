# brainfuck-compiler
A cursed impelemntation of a brainfuck compiler for linux

# How to use it?
Run `python3 main.py file.bf` to generate nasm code corresponding to the brainfuck code in `file.bf`
Piggyback off of nasm to convert it to x86 using `bash compile.sh`
