import subprocess, pathlib, sys
root=pathlib.Path(r'C:\sam5440files\code\HBCPC')
ch=sys.argv[1]
exe=root/'subagents'/'agent1'/(ch+'.exe')
d=root/'data'/ch
ins=sorted(d.glob('*.in'))
ok=0; bad=[]
for inf in ins:
    stem=inf.stem; ansf=inf.with_suffix('.ans')
    try:
        p=subprocess.run([str(exe)], input=inf.read_bytes(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=2)
        if p.returncode!=0:
            bad.append((stem,'RE',p.stderr.decode(errors='ignore')[:60])); continue
        out=p.stdout.decode(errors='ignore').strip().split()
        exp=ansf.read_text(errors='ignore').strip().split()
        if ch=='L':
            good=len(out)==len(exp)
            if good:
                for a,b in zip(out,exp):
                    try:
                        x=float(a); y=float(b)
                        if abs(x-y)>1e-9+1e-9*abs(y): good=False; break
                    except: good=False; break
        else: good=(out==exp)
        if good: ok+=1
        else: bad.append((stem,'WA',f'out={" ".join(out[:4])} exp={" ".join(exp[:4])}'))
    except subprocess.TimeoutExpired:
        bad.append((stem,'TLE','>2s'))
    print(f'{ch} {stem} done', flush=True)
print(f'{ch} {ok}/{len(ins)}')
for x in bad: print('\t'.join(x))
