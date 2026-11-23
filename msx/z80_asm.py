import re

R8 = ["B", "C", "D", "E", "H", "L", "(HL)", "A"]
R16_SP = ["BC", "DE", "HL", "SP"]
R16_AF = ["BC", "DE", "HL", "AF"]
ALU = ["ADD A,", "ADC A,", "SUB", "SBC A,", "AND", "XOR", "OR", "CP"]
CC = ["NZ", "Z", "NC", "C", "PO", "PE", "P", "M"]
ROT = ["RLC", "RRC", "RL", "RR", "SLA", "SRA", "SLL", "SRL"]

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

def disasm_insn(buf: bytes, pc: int, base: int, rel_set: set[int]):
    op = buf[pc]; gpc = base + pc
    def u8(off): return buf[pc + off]
    def s8(off): v = buf[pc + off]; return v - 256 if v >= 128 else v
    def u16(off): return buf[pc + off] | (buf[pc + off + 1] << 8)
    def fmt16(off):
        val = u16(off)
        if (pc + off) in rel_set: return f"R(0x{val:04X})", val, pc + off
        return f"0x{val:04X}", None, None

    if op == 0x00: return 1, "NOP", None, None
    if op == 0x07: return 1, "RLCA", None, None
    if op == 0x08: return 1, "EX AF, AF'", None, None
    if op == 0x0F: return 1, "RRCA", None, None
    if op == 0x10: t = gpc + 2 + s8(1); return 2, f"DJNZ L_{t:04X}", t, None
    if op == 0x17: return 1, "RLA", None, None
    if op == 0x18: t = gpc + 2 + s8(1); return 2, f"JR L_{t:04X}", t, None
    if op == 0x1F: return 1, "RRA", None, None
    if op in (0x20, 0x28, 0x30, 0x38): t = gpc + 2 + s8(1); return 2, f"JR {CC[(op-0x20)>>3]}, L_{t:04X}", t, None
    if op == 0x22: s, t, r = fmt16(1); return 3, f"LD ({s}), HL", t, r
    if op == 0x27: return 1, "DAA", None, None
    if op == 0x2A: s, t, r = fmt16(1); return 3, f"LD HL, ({s})", t, r
    if op == 0x2F: return 1, "CPL", None, None
    if op == 0x32: s, t, r = fmt16(1); return 3, f"LD ({s}), A", t, r
    if op == 0x37: return 1, "SCF", None, None
    if op == 0x3A: s, t, r = fmt16(1); return 3, f"LD A, ({s})", t, r
    if op == 0x3F: return 1, "CCF", None, None
    if op in (0x01, 0x11, 0x21, 0x31): s, t, r = fmt16(1); return 3, f"LD {R16_SP[op>>4]}, {s}", t, r
    if op in (0x02, 0x12): return 1, f"LD ({R16_SP[op>>4]}), A", None, None
    if op in (0x0A, 0x1A): return 1, f"LD A, ({R16_SP[op>>4]})", None, None
    if op in (0x03, 0x13, 0x23, 0x33): return 1, f"INC {R16_SP[op>>4]}", None, None
    if op in (0x0B, 0x1B, 0x2B, 0x3B): return 1, f"DEC {R16_SP[op>>4]}", None, None
    if op in (0x09, 0x19, 0x29, 0x39): return 1, f"ADD HL, {R16_SP[op>>4]}", None, None
    if (op & 0xC7) == 0x04: return 1, f"INC {R8[(op>>3)&7]}", None, None
    if (op & 0xC7) == 0x05: return 1, f"DEC {R8[(op>>3)&7]}", None, None
    if (op & 0xC7) == 0x06: return 2, f"LD {R8[(op>>3)&7]}, 0x{u8(1):02X}", None, None
    if op == 0x76: return 1, "HALT", None, None
    if (op & 0xC0) == 0x40: return 1, f"LD {R8[(op>>3)&7]}, {R8[op&7]}", None, None
    if (op & 0xC0) == 0x80: return 1, f"{ALU[(op>>3)&7]} {R8[op&7]}", None, None
    if (op & 0xC7) == 0xC0: return 1, f"RET {CC[(op>>3)&7]}", None, None
    if (op & 0xCF) == 0xC1: return 1, f"POP {R16_AF[(op>>4)&3]}", None, None
    if (op & 0xC7) == 0xC2: s, t, r = fmt16(1); return 3, f"JP {CC[(op>>3)&7]}, {s}", t, r
    if op == 0xC3: s, t, r = fmt16(1); return 3, f"JP {s}", t, r
    if (op & 0xC7) == 0xC4: s, t, r = fmt16(1); return 3, f"CALL {CC[(op>>3)&7]}, {s}", t, r
    if (op & 0xCF) == 0xC5: return 1, f"PUSH {R16_AF[(op>>4)&3]}", None, None
    if (op & 0xC7) == 0xC6: return 2, f"{ALU[(op>>3)&7]} 0x{u8(1):02X}", None, None
    if (op & 0xC7) == 0xC7: return 1, f"RST 0x{op&0x38:02X}", None, None
    if op == 0xC9: return 1, "RET", None, None
    if op == 0xCD: s, t, r = fmt16(1); return 3, f"CALL {s}", t, r
    if op == 0xD3: return 2, f"OUT (0x{u8(1):02X}), A", None, None
    if op == 0xD9: return 1, "EXX", None, None
    if op == 0xDB: return 2, f"IN A, (0x{u8(1):02X})", None, None
    if op == 0xE3: return 1, "EX (SP), HL", None, None
    if op == 0xE9: return 1, "JP (HL)", None, None
    if op == 0xEB: return 1, "EX DE, HL", None, None
    if op == 0xF3: return 1, "DI", None, None
    if op == 0xF9: return 1, "LD SP, HL", None, None
    if op == 0xFB: return 1, "EI", None, None
    if op == 0xCB:
        op2 = u8(1); r = R8[op2 & 7]; b = (op2 >> 3) & 7
        if op2 < 0x40: return 2, f"{ROT[b]} {r}", None, None
        if op2 < 0x80: return 2, f"BIT {b}, {r}", None, None
        if op2 < 0xC0: return 2, f"RES {b}, {r}", None, None
        return 2, f"SET {b}, {r}", None, None
    if op == 0xED:
        op2 = u8(1)
        if op2 in (0x42,0x52,0x62,0x72): return 2, f"SBC HL, {R16_SP[(op2>>4)&3]}", None, None
        if op2 in (0x4A,0x5A,0x6A,0x7A): return 2, f"ADC HL, {R16_SP[(op2>>4)&3]}", None, None
        if op2 in (0x43,0x53,0x63,0x73): s, t, r = fmt16(2); return 4, f"LD ({s}), {R16_SP[(op2>>4)&3]}", t, r
        if op2 in (0x4B,0x5B,0x6B,0x7B): s, t, r = fmt16(2); return 4, f"LD {R16_SP[(op2>>4)&3]}, ({s})", t, r
        if op2 == 0xB0: return 2, "LDIR", None, None
        if op2 == 0xC3: return 2, "MULUW HL, BC", None, None
        raise ValueError(f"ED {op2:02X} at {gpc:04X}")
    if op in (0xDD, 0xFD):
        idx = "IX" if op == 0xDD else "IY"; op2 = u8(1)
        if op2 == 0x09: return 2, f"ADD {idx}, BC", None, None
        if op2 == 0x19: return 2, f"ADD {idx}, DE", None, None
        if op2 == 0x29: return 2, f"ADD {idx}, {idx}", None, None
        if op2 == 0x39: return 2, f"ADD {idx}, SP", None, None
        if op2 == 0x21: s, t, r = fmt16(2); return 4, f"LD {idx}, {s}", t, r
        if op2 == 0x22: s, t, r = fmt16(2); return 4, f"LD ({s}), {idx}", t, r
        if op2 == 0x2A: s, t, r = fmt16(2); return 4, f"LD {idx}, ({s})", t, r
        if op2 == 0x23: return 2, f"INC {idx}", None, None
        if op2 == 0x2B: return 2, f"DEC {idx}", None, None
        if op2 == 0xE1: return 2, f"POP {idx}", None, None
        if op2 == 0xE5: return 2, f"PUSH {idx}", None, None
        if op2 == 0xE9: return 2, f"JP ({idx})", None, None
        if op2 == 0x60: return 2, f"LD {idx}H, B", None, None
        if op2 == 0x67: return 2, f"LD {idx}H, A", None, None
        if op2 == 0x6F: return 2, f"LD {idx}L, A", None, None
        if op2 == 0x7C: return 2, f"LD A, {idx}H", None, None
        if op2 == 0x7D: return 2, f"LD A, {idx}L", None, None
        if op2 == 0x36: return 4, f"LD ({idx}{s8(2):+d}), 0x{u8(3):02X}", None, None
        if (op2 & 0xC7) == 0x46: return 3, f"LD {R8[(op2>>3)&7]}, ({idx}{s8(2):+d})", None, None
        if (op2 & 0xF8) == 0x70 and op2 != 0x76: return 3, f"LD ({idx}{s8(2):+d}), {R8[op2&7]}", None, None
        if op2 == 0xCB:
            d = s8(2); op3 = u8(3); b = (op3 >> 3) & 7
            if 0x40 <= op3 < 0x80: return 4, f"BIT {b}, ({idx}{d:+d})", None, None
            raise ValueError(f"{idx} CB {op3:02X} at {gpc:04X}")
        raise ValueError(f"{idx} {op2:02X} at {gpc:04X}")
    raise ValueError(f"OP {op:02X} at {gpc:04X}")

def assemble(lines: list[str], base: int = 0) -> tuple[bytes, bytes]:
    labels = {}; parsed = []; pc = base
    def eval_val(expr: str, cur_labels: dict, allow_missing=False):
        expr = expr.strip(); is_rel = False
        if expr.startswith("R(") and expr.endswith(")"): is_rel = True; expr = expr[2:-1].strip()
        def repl(m):
            tok = m.group(0)
            if tok.startswith(("0x","0X")): return str(int(tok, 16))
            if tok in cur_labels: return str(cur_labels[tok])
            if allow_missing: return "0"
            raise KeyError(f"Unknown symbol: {tok}")
        ev = re.sub(r'\b0[xX][0-9a-fA-F]+\b|\b[A-Za-z_][A-Za-z0-9_]*\b', repl, expr)
        return int(eval(ev, {"__builtins__": {}})) & 0xFFFF, is_rel

    def enc_insn(mnem: str, cur_pc: int, pass2: bool):
        mnem = mnem.strip(); out = bytearray()
        parts = mnem.split(None, 1); op = parts[0].upper()
        ops = [x.strip() for x in parts[1].split(",")] if len(parts) > 1 else []
        ops_u = [x.upper() for x in ops]
        simple = {"NOP":0x00,"RLCA":0x07,"EX AF, AF'":0x08,"RRCA":0x0F,"RLA":0x17,"RRA":0x1F,"DAA":0x27,"CPL":0x2F,"SCF":0x37,"CCF":0x3F,"HALT":0x76,"RET":0xC9,"EXX":0xD9,"EX (SP), HL":0xE3,"JP (HL)":0xE9,"EX DE, HL":0xEB,"DI":0xF3,"LD SP, HL":0xF9,"EI":0xFB}
        norm = f"{op} {', '.join(ops)}" if ops else op
        if norm.upper() in simple: return bytes([simple[norm.upper()]]), None
        if op == "EX":
            if ops_u == ["AF", "AF'"]: return bytes([0x08]), None
            if ops_u == ["(SP)", "HL"]: return bytes([0xE3]), None
            if ops_u == ["DE", "HL"]: return bytes([0xEB]), None
        if op == "LDIR": return bytes([0xED, 0xB0]), None
        if op == "MULUW" and ops_u == ["HL", "BC"]: return bytes([0xED, 0xC3]), None
        if op == "DB":
            for it in ops: v_i, _ = eval_val(it, labels, not pass2); out.append(v_i & 0xFF)
            return bytes(out), None
        if op == "DW":
            ro = []
            for it in ops:
                v_i, is_r = eval_val(it, labels, not pass2)
                if is_r: ro.append(cur_pc + len(out) - base)
                out.extend([v_i & 0xFF, (v_i >> 8) & 0xFF])
            return bytes(out), ro
        if op in ("PUSH", "POP"):
            if ops_u[0] in R16_AF: return bytes([(0xC5 if op=="PUSH" else 0xC1) | (R16_AF.index(ops_u[0]) << 4)]), None
            if ops_u[0] in ("IX", "IY"): return bytes([0xDD if ops_u[0]=="IX" else 0xFD, 0xE5 if op=="PUSH" else 0xE1]), None
        if op == "RET" and len(ops) == 1: return bytes([0xC0 | (CC.index(ops_u[0]) << 3)]), None
        if op == "RST": v_i, _ = eval_val(ops[0], labels, not pass2); return bytes([0xC7 | (v_i & 0x38)]), None
        if op == "OUT" and ops_u[1] == "A": v_i, _ = eval_val(ops[0][1:-1], labels, not pass2); return bytes([0xD3, v_i & 0xFF]), None
        if op == "IN" and ops_u[0] == "A": v_i, _ = eval_val(ops[1][1:-1], labels, not pass2); return bytes([0xDB, v_i & 0xFF]), None
        if op == "DJNZ":
            tgt, _ = eval_val(ops[0], labels, not pass2)
            d = ((tgt - (cur_pc + 2)) & 0xFF) if pass2 else 0
            if pass2: assert -128 <= (tgt - (cur_pc + 2)) <= 127
            return bytes([0x10, d]), None
        if op == "JR":
            if len(ops) == 1:
                tgt, _ = eval_val(ops[0], labels, not pass2); d = ((tgt - (cur_pc + 2)) & 0xFF) if pass2 else 0
                if pass2: assert -128 <= (tgt - (cur_pc + 2)) <= 127
                return bytes([0x18, d]), None
            cc_i = ["NZ","Z","NC","C"].index(ops_u[0]); tgt, _ = eval_val(ops[1], labels, not pass2)
            d = ((tgt - (cur_pc + 2)) & 0xFF) if pass2 else 0
            if pass2: assert -128 <= (tgt - (cur_pc + 2)) <= 127
            return bytes([0x20 + cc_i * 8, d]), None
        if op == "JP":
            if ops_u == ["(HL)"]: return bytes([0xE9]), None
            if ops_u == ["(IX)"]: return bytes([0xDD, 0xE9]), None
            if ops_u == ["(IY)"]: return bytes([0xFD, 0xE9]), None
            if len(ops) == 1: v_i, is_r = eval_val(ops[0], labels, not pass2); return bytes([0xC3, v_i & 0xFF, v_i >> 8]), ([cur_pc + 1 - base] if is_r else None)
            cc_i = CC.index(ops_u[0]); v_i, is_r = eval_val(ops[1], labels, not pass2)
            return bytes([0xC2 | (cc_i << 3), v_i & 0xFF, v_i >> 8]), ([cur_pc + 1 - base] if is_r else None)
        if op == "CALL":
            if len(ops) == 1: v_i, is_r = eval_val(ops[0], labels, not pass2); return bytes([0xCD, v_i & 0xFF, v_i >> 8]), ([cur_pc + 1 - base] if is_r else None)
            cc_i = CC.index(ops_u[0]); v_i, is_r = eval_val(ops[1], labels, not pass2)
            return bytes([0xC4 | (cc_i << 3), v_i & 0xFF, v_i >> 8]), ([cur_pc + 1 - base] if is_r else None)
        if op in ("INC", "DEC"):
            if ops_u[0] in R8: return bytes([(0x04 if op=="INC" else 0x05) | (R8.index(ops_u[0]) << 3)]), None
            if ops_u[0] in R16_SP: return bytes([(0x03 if op=="INC" else 0x0B) | (R16_SP.index(ops_u[0]) << 4)]), None
            if ops_u[0] in ("IX", "IY"): return bytes([0xDD if ops_u[0]=="IX" else 0xFD, 0x23 if op=="INC" else 0x2B]), None
        if op == "ADD":
            if ops_u[0] == "HL": return bytes([0x09 | (R16_SP.index(ops_u[1]) << 4)]), None
            if ops_u[0] in ("IX", "IY"):
                return bytes([0xDD if ops_u[0]=="IX" else 0xFD, {"BC":0x09,"DE":0x19,ops_u[0]:0x29,"SP":0x39}[ops_u[1]]]), None
            if ops_u[0] == "A":
                if ops_u[1] in R8: return bytes([0x80 | R8.index(ops_u[1])]), None
                v_i, _ = eval_val(ops[1], labels, not pass2); return bytes([0xC6, v_i & 0xFF]), None
        if op in ("ADC", "SBC"):
            if ops_u[0] == "HL": return bytes([0xED, (0x4A if op=="ADC" else 0x42) | (R16_SP.index(ops_u[1]) << 4)]), None
            if ops_u[0] == "A":
                if ops_u[1] in R8: return bytes([(0x88 if op=="ADC" else 0x98) | R8.index(ops_u[1])]), None
                v_i, _ = eval_val(ops[1], labels, not pass2); return bytes([0xCE if op=="ADC" else 0xDE, v_i & 0xFF]), None
        if op in ("SUB", "AND", "XOR", "OR", "CP"):
            idx = ["SUB","AND","XOR","OR","CP"].index(op); arg = ops[0] if len(ops)==1 else ops[1]
            if arg.upper() in R8: return bytes([[0x90,0xA0,0xA8,0xB0,0xB8][idx] | R8.index(arg.upper())]), None
            v_i, _ = eval_val(arg, labels, not pass2); return bytes([[0xD6,0xE6,0xEE,0xF6,0xFE][idx], v_i & 0xFF]), None
        if op in ROT: return bytes([0xCB, (ROT.index(op) << 3) | R8.index(ops_u[0])]), None
        if op in ("BIT", "RES", "SET"):
            b = int(ops[0]); base_cb = {"BIT":0x40,"RES":0x80,"SET":0xC0}[op]
            m_idx = re.match(r'^\((IX|IY)([+-]\d+)\)$', ops_u[1])
            if m_idx: return bytes([0xDD if m_idx.group(1)=="IX" else 0xFD, 0xCB, int(m_idx.group(2)) & 0xFF, base_cb | (b << 3) | 6]), None
            return bytes([0xCB, base_cb | (b << 3) | R8.index(ops_u[1])]), None
        if op == "LD":
            dst, src = ops[0], ops[1]; du, su = ops_u[0], ops_u[1]
            if du in R8 and su in R8 and not (du=="(HL)" and su=="(HL)"): return bytes([0x40 | (R8.index(du) << 3) | R8.index(su)]), None
            if du in ("IXH","IXL","IYH","IYL") and su in ("A","B"): return bytes([0xDD if du.startswith("IX") else 0xFD, {("H","B"):0x60,("H","A"):0x67,("L","A"):0x6F}[(du[2],su)]]), None
            if du == "A" and su in ("IXH","IXL","IYH","IYL"): return bytes([0xDD if su.startswith("IX") else 0xFD, 0x7C if su[2]=="H" else 0x7D]), None
            m_dst = re.match(r'^\((IX|IY)([+-]\d+)\)$', du)
            if m_dst:
                px = 0xDD if m_dst.group(1)=="IX" else 0xFD; d = int(m_dst.group(2)) & 0xFF
                if su in R8 and su != "(HL)": return bytes([px, 0x70 | R8.index(su), d]), None
                v_i, _ = eval_val(src, labels, not pass2); return bytes([px, 0x36, d, v_i & 0xFF]), None
            m_src = re.match(r'^\((IX|IY)([+-]\d+)\)$', su)
            if m_src and du in R8 and du != "(HL)":
                return bytes([0xDD if m_src.group(1)=="IX" else 0xFD, 0x46 | (R8.index(du) << 3), int(m_src.group(2)) & 0xFF]), None
            if du in R8:
                if du == "A" and su in ("(BC)", "(DE)"): return bytes([0x0A if su=="(BC)" else 0x1A]), None
                if du == "A" and su.startswith("(") and su.endswith(")"):
                    v_i, is_r = eval_val(src[1:-1], labels, not pass2); return bytes([0x3A, v_i & 0xFF, v_i >> 8]), ([cur_pc + 1 - base] if is_r else None)
                v_i, _ = eval_val(src, labels, not pass2); return bytes([0x06 | (R8.index(du) << 3), v_i & 0xFF]), None
            if du in ("(BC)", "(DE)") and su == "A": return bytes([0x02 if du=="(BC)" else 0x12]), None
            if du.startswith("(") and du.endswith(")"):
                v_i, is_r = eval_val(dst[1:-1], labels, not pass2)
                if su == "A": return bytes([0x32, v_i & 0xFF, v_i >> 8]), ([cur_pc + 1 - base] if is_r else None)
                if su == "HL": return bytes([0x22, v_i & 0xFF, v_i >> 8]), ([cur_pc + 1 - base] if is_r else None)
                if su in ("IX", "IY"): return bytes([0xDD if su=="IX" else 0xFD, 0x22, v_i & 0xFF, v_i >> 8]), ([cur_pc + 2 - base] if is_r else None)
                if su in R16_SP: return bytes([0xED, 0x43 | (R16_SP.index(su) << 4), v_i & 0xFF, v_i >> 8]), ([cur_pc + 2 - base] if is_r else None)
            if du in R16_SP or du in ("IX", "IY"):
                if su.startswith("(") and su.endswith(")"):
                    v_i, is_r = eval_val(src[1:-1], labels, not pass2)
                    if du == "HL": return bytes([0x2A, v_i & 0xFF, v_i >> 8]), ([cur_pc + 1 - base] if is_r else None)
                    if du in ("IX", "IY"): return bytes([0xDD if du=="IX" else 0xFD, 0x2A, v_i & 0xFF, v_i >> 8]), ([cur_pc + 2 - base] if is_r else None)
                    return bytes([0xED, 0x4B | (R16_SP.index(du) << 4), v_i & 0xFF, v_i >> 8]), ([cur_pc + 2 - base] if is_r else None)
                v_i, is_r = eval_val(src, labels, not pass2)
                if du in ("IX", "IY"): return bytes([0xDD if du=="IX" else 0xFD, 0x21, v_i & 0xFF, v_i >> 8]), ([cur_pc + 2 - base] if is_r else None)
                return bytes([0x01 | (R16_SP.index(du) << 4), v_i & 0xFF, v_i >> 8]), ([cur_pc + 1 - base] if is_r else None)
        raise ValueError(f"Cannot assemble: {mnem}")

    for raw_ln in lines:
        ln = raw_ln.split(";", 1)[0].strip()
        if not ln: continue
        if ":" in ln:
            lbl, rest = ln.split(":", 1); labels[lbl.strip()] = pc; ln = rest.strip()
            if not ln: continue
        if ln.upper().startswith("ORG "): pc = int(ln.split()[1], 0); continue
        bs, _ = enc_insn(ln, pc, False); parsed.append((pc, ln)); pc += len(bs)
    out_bin = bytearray(); rel_offs = []
    for cur_pc, ln in parsed:
        bs, ro = enc_insn(ln, cur_pc, True); out_bin.extend(bs)
        if ro: rel_offs.extend(ro)
    return bytes(out_bin), encode_reloc(rel_offs)