import re, hashlib
import mpmath
from pathlib import Path
from msx_tools import tok_sz, decode_bas_sec, parse_reloc
from fast_sim import FastMSXSim

def load_bas(path):
    txt = Path(path).read_text()
    lines = txt.splitlines()
    lmap = {int(m.group(1)): m.group(2) for l in lines if (m := re.match(r'^(\d+)\s+(.*)$', l))}
    return lines, lmap, hashlib.sha256(txt.encode('ascii')).hexdigest()

def relocate(sec_bytes, code_len, base_addr):
    out = bytearray(sec_bytes[:code_len])
    for off in parse_reloc(sec_bytes[code_len:]):
        v16 = (out[off] | (out[off+1] << 8)) + base_addr
        out[off] = v16 & 0xFF; out[off+1] = (v16 >> 8) & 0xFF
    return bytes(out)

def write16(sim, addr, val):
    sim.write8(addr, val & 0xFF); sim.write8(addr + 1, (val >> 8) & 0xFF)

def main():
    mpmath.mp.dps = 1500
    PI = str(mpmath.mp.pi).replace('.', '')

    piv_lines, piv_map, piv_sha = load_bas("PIV13.BAS")
    mk_lines, mk_map, mk_sha = load_bas("MKPI8K.BAS")
    assert max(len(x) for x in piv_lines) <= 253
    assert max(len(x) for x in mk_lines) <= 253
    piv_tsz = sum(tok_sz(x) for x in piv_lines)
    print(f"PIV13.BAS: {len(piv_lines)} lines, tok_sz={piv_tsz}B, sha256={piv_sha}")
    print(f"MKPI8K.BAS: {len(mk_lines)} lines, sha256={mk_sha}")

    for dm in (True, False):
        prog = dict(piv_map); prog.update(mk_map)
        for ln_k in sorted(mk_map):
            if 50 <= ln_k <= 76 and 'DELETE' in mk_map[ln_k]:
                if dm and 73 <= ln_k <= 76: continue
                if (not dm) and 69 <= ln_k <= 72: continue
                m = re.search(r'DELETE(\d+)(?:-(\d+))?', mk_map[ln_k])
                lo = int(m.group(1)); hi = int(m.group(2) or lo)
                assert lo in prog and hi in prog, f"missing DELETE endpoint {lo}-{hi}"
                for k in list(prog):
                    if lo <= k <= hi: del prog[k]
        for k in list(prog):
            if 1 <= k <= 90: del prog[k]
        tsz = sum(tok_sz(f"{k} {prog[k]}") for k in sorted(prog))
        print(f"  PI8K ({'Disk' if dm else 'Tape'}): {len(prog)} lines, tok_sz={tsz}B")

    s0 = decode_bas_sec(piv_map, 1840, 1860)
    s1 = decode_bas_sec(piv_map, 1900, 1981)
    s2 = decode_bas_sec(piv_map, 1990, 2000)
    s3 = decode_bas_sec(piv_map, 2010, 2070)
    assert (len(s0), len(s1), len(s2), len(s3)) == (582, 1913, 438, 1353)
    r1 = parse_reloc(s1[1782:])
    assert {o: s1[o]|(s1[o+1]<<8) for o in r1 if (s1[o]|(s1[o+1]<<8)) >= 2150} == {345: 2653, 390: 2580, 428: 2653, 1159: 2309, 1655: 2189}

    for C_d in (40, 45, 1392):
        sim = FastMSXSim(mv=0, bottom=0xE000, basic_slot=0x03)
        A = 0xEC04; sim.s.sp = 0xEB00
        sim.load_bytes(A, relocate(s1, 1782, A))
        C_v = 65535 if C_d <= 40 else 151
        T4 = 4 if (C_v < 65535 and (-((-C_d)//4)*14 > 151 + 1662)) else 0
        write16(sim, A+3, A+1610); write16(sim, A+5, 151); write16(sim, A+7, C_v)
        write16(sim, A+9, A); write16(sim, A+11, C_d); sim.write8(A+15, 0)
        sim.s.guard_lo = A + 1912; sim.s.guard_hi = 0xF600
        sim.run_usr(A+1610, T4)
        D = -((-C_d)//4); sim.run_usr(A, -D)
        digs = []
        for step in range(D, 0, -1):
            sim.s.watch_mode = 1; T1 = sim.run_usr(A, step)
            sim.s.watch_mode = 2; sim.run_usr(A+1085, T1)
            digs.append(T1)
        assert "".join(f"{x:04d}" for x in digs)[:C_d] == PI[:C_d]
        print(f"  [8K Guard+Watch16K] C={C_d} PASS")

    for label, mv, r800, msegs, B_w, T3, C_d, T4, nsteps in [
        ("MSX2 SCREEN5 T3=1", 1, False, 16, 50, 1, 403, 1, 101),
        ("MSX2 SCREEN6p1 T3=1", 1, False, 16, 50, 1, 403, 3, 101),
        ("turboR R800 10752d", 3, True, 32, 0, 1, 10752, 3, 5),
        ("MSX2 64K VRAM 10752d", 1, False, 0, 9000, 0, 10752, 3, 5),
    ]:
        sim = FastMSXSim(mv=mv, bottom=0x8000, basic_slot=0x03, is_r800=r800, mapper_segs=msegs)
        A = 0xA000; sim.s.sp = 0x9E00
        sim.load_bytes(A, relocate(s1, 1782, A))
        sim.load_bytes(A+1782, relocate(s2, 407, A))
        sim.load_bytes(A+2189, relocate(s3, 1245, A))
        sim.run_usr(A+2694, 0)
        C_v = B_w if (T3 == 0 and C_d > B_w // 14 * 4) else 65535
        write16(sim, A+3, A+(3302 if B_w > 0 else 2694)); write16(sim, A+5, B_w); write16(sim, A+7, C_v)
        write16(sim, A+9, A+2694); write16(sim, A+11, C_d); sim.write8(A+15, T3)
        sim.write8(A+2134, 0); sim.write8(A+2149, 3)
        sim.run_usr(A+1610, T4)
        D = -((-C_d)//4); sim.run_usr(A, -D)
        digs = [sim.run_usr(A, s) for s in range(D, D-nsteps, -1)]
        for t1 in digs: sim.run_usr(A+1085, t1)
        got = "".join(f"{x:04d}" for x in digs)[:min(C_d, nsteps*4)]
        assert got == PI[:len(got)]
        print(f"  [{label}] C={C_d} checked={len(got)}d PASS")

if __name__ == "__main__":
    main()