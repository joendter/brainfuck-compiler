import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inputfile", help="Input file", required=True)
parser.add_argument("-o", "--outputfile", help="Output file", default="out.nasm")
parser.add_argument("-b", help="Base assembly file", default="base.nasm")
parser.add_argument("-c", help="character substitution list as json", default="basic.json")
parser.add_argument("-q", help="quiet", action='store_true')
parser.add_argument("-l", help="Length of the bytearray the turing machine uses", default=1024)

args = parser.parse_args()


if args.q:
    def print(*args):
        pass

print(args.outputfile)

with open(args.inputfile,"r") as f:
    code = f.read()

with open(args.b, "r") as f:
    base_assembly = f.read()

with open(args.c, "r") as f:
    character_substitution = json.load(f)

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
    if cha in character_substitution.keys():
        if cha == "[":
            stack.append(counter.next())
            asm += character_substitution[cha].format(stack = stack[-1])
        elif cha == "]":
            asm += character_substitution[cha].format(stack = stack.pop())
        else:
            asm += character_substitution[cha]

length = args.l
values = {
    "length" : length,
    "length-1": length-1,
    "asm": asm
}
out = base_assembly.format_map( values)
print(out)

with open(args.outputfile, "w") as f:
    f.write(out)