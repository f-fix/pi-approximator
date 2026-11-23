import re

TOKENS = {
    'END':129,'FOR':130,'NEXT':131,'DATA':132,'INPUT':133,'DIM':134,'READ':135,'LET':136,'GOTO':137,
    'RUN':138,'IF':139,'RESTORE':140,'GOSUB':141,'RETURN':142,'REM':143,'STOP':144,'PRINT':145,
    'CLEAR':146,'LIST':147,'NEW':148,'ON':149,'WAIT':150,'DEF':151,'POKE':152,'CONT':153,'CSAVE':154,
    'CLOAD':155,'OUT':156,'LPRINT':157,'LLIST':158,'WIDTH':159,'ELSE':161,'TRON':162,'TROFF':163,
    'SWAP':164,'ERASE':165,'EDIT':166,'ERROR':167,'RESUME':168,'DELETE':169,'AUTO':170,'RENUM':171,
    'DEFSTR':172,'DEFINT':173,'DEFSNG':174,'DEFDBL':175,'LINE':176,'CALL':186,'SCREEN':197,
    'COLOR':198,'CLS':199,'SET':212,'VDP':200,'TIME':203,'USING':190,'USR':221,'OR':247,'AND':246,
    'NOT':224,'STEP':220,'TO':217,'THEN':218,'MOD':251,'LEFT$':255,'RIGHT$':255,'MID$':255,
    'CHR$':255,'STR$':255,'ASC':255,'LEN':255,'VAL':255,'PEEK':255,'INT':255,'FRE':255,'INSTR':229,
    'VARPTR':231,'INKEY$':236,'BLOAD':207,'BSAVE':208,'SAVE':183,'MERGE':182,
}

def tok_sz(line: str) -> int:
    m = re.match(r'^\s*(\d+)\s+(.*)$', line)
    body = m.group(2); i = 0; out = bytearray()
    while i < len(body):
        if body[i] == '"':
            j = body.find('"', i+1); j = len(body)-1 if j == -1 else j
            out.extend(body[i:j+1].encode('ascii')); i = j + 1; continue
        if body[i] == ':':
            if body[i:i+5].upper() == ':ELSE': out.extend([0x3A, 0xA1]); i += 5; continue
            out.append(0x3A); i += 1; continue
        matched = next((kw for kw in sorted(TOKENS, key=len, reverse=True) if body[i:i+len(kw)].upper() == kw), None)
        if matched:
            t = TOKENS[matched]; out.extend([255,0x80] if t==255 else [t]); i += len(matched); continue
        if body[i:i+2].upper() == '&H':
            j = i+2
            while j < len(body) and body[j] in '0123456789ABCDEFabcdef': j += 1
            out.extend([0x0C,0,0]); i = j; continue
        if body[i].isdigit() or (body[i]=='.' and i+1<len(body) and body[i+1].isdigit()):
            j = i
            while j < len(body) and (body[j].isdigit() or body[j] in '.eEdD+-!#'):
                if body[j] in '+-' and body[j-1] not in 'eEdD': break
                j += 1
            lit = body[i:j]
            if '#' in lit or ('.' in lit and len(lit)>7): out.extend([0x1F]+[0]*8)
            elif '!' in lit or '.' in lit or 'E' in lit.upper(): out.extend([0x1D]+[0]*4)
            else:
                v_i = int(lit)
                if 0<=v_i<=9: out.append(0x11+v_i)
                elif v_i<=255: out.extend([0x0F, v_i])
                elif v_i<=32767: out.extend([0x1C, v_i&255, v_i>>8])
                else: out.extend([0x1D]+[0]*4)
            i = j; continue
        out.append(ord(body[i])); i += 1
    return 5 + len(out)

def parse_reloc(rel_bytes: bytes) -> list[int]:
    pos = -1; offs = []
    for b in rel_bytes:
        if b == 0: break
        if b == 255: pos += 255; continue
        pos += b; offs.append(pos)
    return offs

def encode_reloc(offs: list[int]) -> bytes:
    out = bytearray(); prev = -1
    for o in sorted(offs):
        d = o - prev
        while d >= 255: out.append(255); d -= 255
        out.append(d); prev = o
    out.append(0)
    return bytes(out)

def decode_bas_sec(line_map: dict[int, str], start_ln: int, end_ln: int) -> bytes:
    out = bytearray(); total = 0
    for ln in sorted(k for k in line_map if start_ln <= k <= end_ln):
        h = re.match(r'^DATA\s+"(.*)"$', line_map[ln]).group(1)
        t3 = h.index("~"); g = 0; t4 = 0; z = 0
        while t4 < t3:
            t5 = ord(h[t4])
            if t5 == 46: z = 1; break
            if t5 >= 121:
                t6 = ord(h[t4+1]) - 35
                if t6 == 85: t6 -= 74
                for _ in range(t5 - 118): b = out[-t6 - 1]; out.append(b); g += b
                t4 += 2
            else:
                d = 0
                for k in range(5):
                    t6 = ord(h[t4+k]) - 35
                    if t6 == 85: t6 -= 74
                    d = d * 85 + t6
                bs = d.to_bytes(4, 'big'); out.extend(bs); g += sum(bs); t4 += 5
        assert (g & 0xFFFF) == int(h[t3+1:t3+5], 16)
        total += g
        if z: assert (total & 0xFFFF) == int(h[t4+1:t4+5], 16)
    return bytes(out)

def enc_d(d: int) -> str: return 'x' if d == 11 else chr(35 + d)
def enc_b85_4(bs: bytes) -> str:
    val = int.from_bytes(bs, 'big'); chars = []
    for _ in range(5): chars.append(enc_d(val % 85)); val //= 85
    return ''.join(reversed(chars))

def encode_data(raw: bytes, max_line_payload=236) -> list[str]:
    n = len(raw); INF = 10**9; dp = [INF]*(n+1); choice = [None]*(n+1); dp[n] = 0
    for i in range(n-1, -1, -1):
        if i+4 <= n and 5 + dp[i+4] < dp[i]: dp[i] = 5 + dp[i+4]; choice[i] = ('b85', 4)
        for L in range(min(7, n-i), 2, -1):
            sub = raw[i:i+L]
            for j in range(i-1, max(0, i-85)-1, -1):
                if all(raw[j+k] == sub[k] for k in range(L)):
                    if 2 + dp[i+L] < dp[i]: dp[i] = 2 + dp[i+L]; choice[i] = ('lz', L, i-j-1)
                    break
    assert dp[0] < INF, "Tail cannot be encoded without padding"
    tokens = []; i = 0
    while i < n:
        ch = choice[i]
        if ch[0] == 'b85': bs = raw[i:i+4]; tokens.append((enc_b85_4(bs), sum(bs))); i += 4
        else: _, L, off = ch; bs = raw[i:i+L]; tokens.append((chr(118+L)+enc_d(off), sum(bs))); i += L
    lines = []; cur = ""; cur_sum = 0; tot_sum = 0
    for idx, (tok, s) in enumerate(tokens):
        limit = max_line_payload - (5 if idx == len(tokens)-1 else 0)
        if len(cur) + len(tok) > limit and cur:
            lines.append(f"{cur}~{cur_sum & 0xFFFF:04X}"); cur = ""; cur_sum = 0
        cur += tok; cur_sum += s; tot_sum += s
    lines.append(f"{cur}.{tot_sum & 0xFFFF:04X}~{cur_sum & 0xFFFF:04X}")
    return lines