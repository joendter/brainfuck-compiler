import sys
args = sys.argv
with open(args[1],"r") as f:
    code = f.read()
with open("base.nasm", "r") as f:
    base_assembly = f.read()

#syntax checking
counter = 0
for cha in code:
    if cha == "[":
        counter += 1
    if cha == "]":
        counter -= 1
    if counter < 0:
        print("invalid syntax")
        exit(10)

class Counter():
    count = 0
    def next(self):
        self.count += 1
        return self.count


print(code)
stack = []
counter = Counter()
asm = ""

for cha in code:
    if cha == "+":
        asm += "    call increment\n"
    if cha == "-":
        asm += "    call decrement\n"
    if cha == "<":
        asm += "    call move_left\n"
    if cha == ">":
        asm += "    call move_right\n"
    if cha == "]":
        asm += f"""
    mov al, byte [ecx]
    test al, al
    jnz a{stack.pop()}
"""
    if cha == "[":
        stack.append(counter.next())
        asm += f"   a{stack[-1]}:\n"

    if cha == ".":
        asm += "    call print\n"
    if cha == ",":
        asm += "    call read\n"

length = 1024
values = {
    "length" : length,
    "length-1": length-1,
    "asm": asm
}
out = base_assembly.format_map( values)
print(out)

with open("out.nasm", "w") as f:
    f.write(out)