import re
from pathlib import Path
from msx_tools import decode_bas_sec
from z80_asm import disasm_insn, assemble, parse_reloc

SECTIONS = [
    ("s0", 1840, 1860, 531, 0,    [(521, 531)]),
    ("s1", 1900, 1981, 1782, 0,   [(3, 17), (1379, 1451)]),
    ("s2", 1990, 2000, 407, 1782, [(345, 369)]),
    ("s3", 2010, 2070, 1245, 2189,[(375, 391), (1215, 1223)]),
]

lmap = {
    int(m.group(1)): m.group(2)
    for l in Path("PIV13.BAS").read_text().splitlines()
    if (m := re.match(r'^(\d+)\s+(.*)$', l))
}

for name, lo_ln, hi_ln, clen, base, dr in SECTIONS:
    blob = decode_bas_sec(lmap, lo_ln, hi_ln)
    raw, rel = blob[:clen], blob[clen:]
    rel_set = set(parse_reloc(rel))
    def in_data(off): return next(((lo, hi) for lo, hi in dr if lo <= off < hi), None)

    insns = []; targets = set(); pc = 0
    while pc < len(raw):
        d = in_data(pc)
        if d:
            lo, hi = d; insns.append((pc, raw[pc:hi], None, None)); pc = hi
        else:
            ln, mn, tgt, ro = disasm_insn(raw, pc, base, rel_set)
            insns.append((pc, raw[pc:pc+ln], mn, ro))
            if tgt is not None: targets.add(tgt)
            pc += ln

    asm_lines = [f"ORG 0x{base:04X}"]
    for pc, chunk, mn, ro in insns:
        gpc = base + pc
        if gpc in targets: asm_lines.append(f"L_{gpc:04X}:")
        if mn is None:
            for i in range(0, len(chunk), 8):
                asm_lines.append("    DB " + ", ".join(f"0x{b:02X}" for b in chunk[i:i+8]))
        else:
            asm_lines.append(f"    {mn} ; {gpc:04X}: {chunk.hex()}")

    Path(f"{name}.asm").write_text("\n".join(asm_lines))
    ab, ar = assemble(asm_lines, base=base)
    assert ab == raw and ar == rel
    print(f"{name}: {len(asm_lines)} lines -> {len(ab)}B code + {len(ar)}B reloc EXACT MATCH")