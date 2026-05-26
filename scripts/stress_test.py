#!/usr/bin/env python3
import os
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build" / "stress"
LETTERS = list("ABCDEGHIJKLM")

def run(cmd, inp, timeout=5):
    p = subprocess.run(cmd, input=inp.encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.decode(errors="ignore"))
    return p.stdout.decode()

def compile_one(letter, kind):
    exe = BUILD / f"{letter}_{kind}.exe"
    src = ROOT / "solutions" / letter / f"{kind}.cpp"
    subprocess.check_call(["g++", "-std=c++17", "-O2", str(src), "-o", str(exe)])
    return exe

def gen(letter):
    if letter == "A":
        n=random.randint(1,12); a=[random.randint(1,5) for _ in range(n)]
        return f"{n}\n{' '.join(map(str,a))}\n"
    if letter == "B":
        return ""
    if letter == "C":
        n=random.randint(2,12); q=random.randint(1,20); edges=[]
        for v in range(2,n+1):
            u=random.randint(1,v-1); w=random.randint(-10,10); edges.append((u,v,w))
        qs=[(random.randint(1,n),random.randint(1,n)) for _ in range(q)]
        return f"{n} {q}\n"+"\n".join(f"{u} {v} {w}" for u,v,w in edges)+"\n"+"\n".join(f"{x} {y}" for x,y in qs)+"\n"
    if letter == "D":
        n=random.randint(2,15); k=random.randint(0,n-2); s="".join(random.choice("abc") for _ in range(n))
        return f"{n} {k} {s}\n"
    if letter == "E":
        return f"{random.randint(2,18)}\n"
    if letter == "G":
        n=random.randint(2,10); m=n-1; q=random.randint(1,12)
        a=[random.randint(1,20) for _ in range(n)]
        edges=[(i,i+1,random.randint(1,20)) for i in range(1,n)]
        ops=[]
        for _ in range(q):
            if random.random()<0.4:
                ops.append(f"1 {random.randint(1,n)} {random.randint(1,20)}")
            else:
                ops.append(f"2 {random.randint(1,n)}")
        return f"{n} {m} {q}\n{' '.join(map(str,a))}\n"+"\n".join(f"{u} {v} {d}" for u,v,d in edges)+"\n"+"\n".join(ops)+"\n"
    if letter == "H":
        n=random.randint(1,30); q=random.randint(1,20); s="".join(random.choice("abc") for _ in range(n))
        qs=[] 
        for _ in range(q):
            l=random.randint(1,n); r=random.randint(l,n); qs.append((l,r))
        return f"{n} {q}\n{s}\n"+"\n".join(f"{l} {r}" for l,r in qs)+"\n"
    if letter == "I":
        n=random.randint(1,10); m=random.randint(1,100); t=[random.randint(1,20) for _ in range(n)]
        return f"{n} {m}\n{' '.join(map(str,t))}\n"
    if letter == "J":
        n=random.randint(1,10); M=random.randint(1,200); rows=[(random.randint(1,30),random.randint(1,200)) for _ in range(n)]
        return f"{n} {M}\n"+"\n".join(f"{a} {b}" for a,b in rows)+"\n"
    if letter == "K":
        n=random.randint(3,25); cuts=sorted(random.sample(range(1,n),2)); r=random.randint(0,n); g=random.randint(0,n-r); b=n-r-g
        return f"1\n{n} 1 {r} {g} {b}\n1 {max(2,min(n-1,cuts[1]))}\n"
    if letter == "L":
        n=random.randint(1,20); k=random.randint(1,n); pts=[]
        for _ in range(n):
            x=y=0
            while x==0 and y==0: x=random.randint(-10,10); y=random.randint(-10,10)
            pts.append((x,y))
        return f"1\n{n} {k}\n"+"\n".join(f"{x} {y}" for x,y in pts)+"\n"
    if letter == "M":
        return "1\n3 3\nS..\n.R.\n..E\n"
    raise ValueError(letter)

def main():
    random.seed(20260526)
    BUILD.mkdir(parents=True, exist_ok=True)
    for letter in LETTERS:
        std=compile_one(letter,"std")
        brute=compile_one(letter,"brute")
        for case in range(50):
            inp=gen(letter)
            a=run([str(std)], inp)
            b=run([str(brute)], inp)
            if letter=="L":
                av=[float(x) for x in a.split()]
                bv=[float(x) for x in b.split()]
                if len(av)!=len(bv) or any(abs(x-y)>1e-8 for x,y in zip(av,bv)):
                    print("Mismatch", letter, case, inp, a, b); return 1
            elif a!=b:
                print("Mismatch", letter, case)
                print(inp)
                print("std:",a)
                print("brute:",b)
                return 1
        print(f"{letter}: ok")
    return 0

if __name__ == "__main__":
    sys.exit(main())
