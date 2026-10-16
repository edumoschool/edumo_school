import re, json, sys
txt = open(sys.argv[1], encoding='utf-8').read().replace('​','').replace(' ',' ').replace('\f','\n')
HEAD = {'Countries','Numbers 1–10','Numbers 11–100','Days of the week','Months','Ordinal numbers'}
skip = re.compile(r'^(Name|Photocopiable.*|Here is a list.*|Words marked.*|adj = .*|adv = .*|\d+|˛)$')
units={}; cur=None; section=None; pending=None; last=None
POS = r'(?:n pl|n|v|adj|adv|prep|pron, pl|pron|det|conj|phr v|phr|exclamation|pl)'
ENTRY = re.compile(r'^(.+?)\s+(?:('+POS+r')\s+)?(/[^/]+/)\s*(.*)$')
for line in txt.split('\n'):
    line=re.sub(r'\s+',' ',line).strip()
    if not line: continue
    m = re.match(r'A\d Wordlist Unit (\d+)$', line)
    if m:
        u=int(m.group(1))
        if u!=cur: cur=u; section=None; last=None; units.setdefault(u, [])
        continue
    if skip.match(line): continue
    if line in HEAD: section=line; continue
    if line.startswith('/') and pending is not None:
        line = pending+' '+line; pending=None
    elif pending is not None:
        pending += ' '+line; continue
    m = ENTRY.match(line)
    if m:
        last=dict(word=m.group(1).strip(), pos=(m.group(2) or '').strip(), ipa=m.group(3), ex=m.group(4).strip(), section=section)
        units[cur].append(last); continue
    if last is not None and last['ex']=='' and last['section'] is None and not re.search(r'(^|\s)/', line):
        last['ex']=line; continue
    ends = last is None or last['ex']=='' or re.search(r'[.!?’]$', last['ex'])
    if not re.search(r'(^|\s)/', line) and ends and not re.search(r'[.!?’]$', line):
        pending=line; continue
    if last is not None:
        last['ex']=(last['ex']+' '+line).strip()
    else:
        print('ORPHAN',cur,line)
json.dump(units, open(sys.argv[2],'w'), ensure_ascii=False, indent=0)
tot=0
for u,ws in units.items():
    tot+=len(ws); print(u, len(ws))
print(tot)
