import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inputfile", help="Input file", required=True)
parser.add_argument("-o", "--outputfile", help="Output file", default="out.nasm")
parser.add_argument("-b", help="Base assembly file", default="base.nasm")
parser.add_argument("-c", help="character substitution list as json", default="meanings.json")
parser.add_argument("-q", help="quiet", action='store_true')
parser.add_argument("-l", help="Length of the bytearray the turing machine uses", default=1024)
parser.add_argument("-O1", help="Optimisation level 1", action='store_true')

args = parser.parse_args()


if args.q:
    def debug(*args):
        pass
else:
    def debug(*args):
        print(*args)

if args.O1:
    if args.b == "base.nasm":
        args.b = "base-O1.nasm"
    if args.c == "meanings.json":
        args.c = "meanings-O1.json"

debug(args.outputfile)

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


debug(code)
stack = []
counter = Counter()
asm = ""
counters = {
    "<" : 0,
    ">" : 0,
    "+" : 0,
    "-" : 0,
    "" : 0
}
last_active = ""

for cha in code:
    if cha in character_substitution.keys():
        if args.O1:
            if cha == last_active:
                counters[last_active] += 1
                continue
            
            asm += character_substitution[last_active].format(number = counters[last_active])
            counters[last_active] = 0

            if cha in list("<>+-"):
                last_active = cha
                counters[last_active] += 1
                continue

        if cha == "[":
            stack.append(counter.next())
            asm += character_substitution[cha].format(stack = stack[-1])
        elif cha == "]":
            asm += character_substitution[cha].format(stack = stack.pop())
        
        else:
            asm += character_substitution[cha]

length = int(args.l)
values = {
    "length" : length,
    "length-1": length-1,
    "asm": asm
}
out = base_assembly.format_map( values).format_map(values)
debug(out)

with open(args.outputfile, "w") as f:
    f.write(out)