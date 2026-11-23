import ctypes, subprocess
from pathlib import Path

class MSXState(ctypes.Structure):
    _fields_ = [
        ("ram", ctypes.c_uint8 * 65536), ("vram", ctypes.c_uint8 * 131072),
        ("slot_bufs", (((ctypes.c_uint8 * 16384) * 4) * 4) * 4),
        ("slot_kind", ((ctypes.c_uint8 * 4) * 4) * 4),
        ("mapper_segs", (ctypes.c_uint8 * 16384) * 32),
        ("mapper_n_segs", ctypes.c_uint8), ("mapper_slot", ctypes.c_uint8),
        ("expanded", ctypes.c_uint8 * 4), ("ffff_regs", ctypes.c_uint8 * 4),
        ("slot_reg_a8", ctypes.c_uint8), ("mapper_seg", ctypes.c_uint8 * 4),
        ("mv", ctypes.c_uint8), ("is_r800", ctypes.c_uint8), ("strict_enaslt", ctypes.c_uint8),
        ("vdp_latch_valid", ctypes.c_uint8), ("vdp_latch", ctypes.c_uint8),
        ("vdp_addr", ctypes.c_uint16), ("vdp_r14", ctypes.c_uint8), ("fdc_touched", ctypes.c_uint8),
        ("pal_writes", ctypes.c_uint8 * 256), ("pal_count", ctypes.c_int),
        ("watch_mode", ctypes.c_uint8), ("digit_pgt", ctypes.c_uint8 * 0x1800),
        ("watch_err", ctypes.c_int), ("watch_err_addr", ctypes.c_uint16), ("watch_err_val", ctypes.c_uint8),
        ("guard_lo", ctypes.c_uint16), ("guard_hi", ctypes.c_uint16),
        ("vram_min_calc", ctypes.c_uint32), ("vram_max_calc", ctypes.c_uint32), ("track_vram", ctypes.c_uint8),
        ("a", ctypes.c_uint8), ("f", ctypes.c_uint8), ("b", ctypes.c_uint8), ("c", ctypes.c_uint8),
        ("d", ctypes.c_uint8), ("e", ctypes.c_uint8), ("h", ctypes.c_uint8), ("l", ctypes.c_uint8),
        ("a2", ctypes.c_uint8), ("f2", ctypes.c_uint8), ("b2", ctypes.c_uint8), ("c2", ctypes.c_uint8),
        ("d2", ctypes.c_uint8), ("e2", ctypes.c_uint8), ("h2", ctypes.c_uint8), ("l2", ctypes.c_uint8),
        ("ix", ctypes.c_uint16), ("iy", ctypes.c_uint16), ("sp", ctypes.c_uint16), ("pc", ctypes.c_uint16),
        ("iff", ctypes.c_uint8), ("ei_delay", ctypes.c_uint8),
        ("irq_period", ctypes.c_uint64), ("steps", ctypes.c_uint64), ("irq_cnt", ctypes.c_uint64),
        ("stop_reason", ctypes.c_int), ("bad_op", ctypes.c_uint8), ("bad_pc", ctypes.c_uint16),
    ]

_here = Path(__file__).resolve().parent
_so = _here / "z80_fast.so"
if not _so.exists():
    subprocess.run(["gcc", "-O2", "-shared", "-fPIC", str(_here / "z80_fast.c"), "-o", str(_so)], cwd=str(_here), check=True)
_lib = ctypes.CDLL(str(_so))
_lib.run_usr_c.argtypes = [ctypes.POINTER(MSXState), ctypes.c_uint16, ctypes.c_int16, ctypes.c_uint64]
_lib.run_usr_c.restype = ctypes.c_int

class FastMSXSim:
    def __init__(self, mv=0, bottom=0x8000, basic_slot=0x03, expanded_slots=None, is_r800=False, irq_period=400, strict=True, mapper_segs=0, mapper_slot=3, mapper_sub=0):
        self.s = MSXState()
        st = self.s; st.mv = mv; st.is_r800 = int(is_r800); st.strict_enaslt = int(strict); st.irq_period = irq_period
        st.ram[0x002D] = mv; st.ram[0xFC48] = bottom & 0xFF; st.ram[0xFC49] = (bottom >> 8) & 0xFF
        exp = set(expanded_slots or [])
        for s_idx in range(4):
            st.expanded[s_idx] = 1 if s_idx in exp else 0
            st.ram[0xFCC1 + s_idx] = 0x80 if s_idx in exp else 0x00
            st.ram[0xFCC5 + s_idx] = 0x00
        st.slot_kind[0][0][0] = 1; st.slot_kind[0][0][1] = 1
        if strict:
            for i in range(0x0038): st.slot_bufs[0][0][0][i] = (0xA5 ^ (i * 13)) & 0xFF
            st.slot_bufs[0][0][0][0x002D] = mv
        for i, b in enumerate([0xF5,0xE5,0xDB,0x99,0x21,0x9E,0xFC,0x34,0xE1,0xF1,0xFB,0xC9]):
            st.slot_bufs[0][0][0][0x0038 + i] = b
        b_pri = basic_slot & 3; b_sub = (basic_slot >> 2) & 3 if (basic_slot & 0x80) else 0
        st.slot_reg_a8 = (b_pri << 6) | ((b_pri if bottom <= 0xA000 else 0) << 4)
        if basic_slot & 0x80:
            st.ffff_regs[b_pri] = (b_sub << 6) | ((b_sub if bottom <= 0xA000 else 0) << 4)
            st.ram[0xFCC5 + b_pri] = st.ffff_regs[b_pri]
        for i, seg in enumerate([3, 2, 1, 0]): st.mapper_seg[i] = seg
        st.vram[0x1B00] = 0xD0; st.sp = 0xF000; st.iff = 1
        if mapper_segs > 0:
            st.mapper_n_segs = mapper_segs; st.mapper_slot = mapper_slot
            st.slot_kind[mapper_slot][mapper_sub][0] = 4
            st.slot_kind[mapper_slot][mapper_sub][1] = 4
            st.slot_kind[mapper_slot][mapper_sub][2] = 4

    def set_slot_ram(self, pri, sub, page, kind='ram16'):
        self.s.slot_kind[pri][sub][page] = {'rom':1,'ram16':2,'ram8_mirror':3,'mapper':4,'diskrom':5}[kind]

    def load_bytes(self, addr, data):
        for i, b in enumerate(data): self.write8(addr + i, b)

    def read8(self, addr):
        addr &= 0xFFFF
        if addr >= 0xC000: return self.s.ram[addr]
        page = addr >> 14; off = addr & 0x3FFF
        if page == 2 and self.s.ram[0xFC49] <= 0xA0:
            pri = (self.s.slot_reg_a8 >> 4) & 3
            if pri == ((self.s.slot_reg_a8 >> 6) & 3) and off >= (0x2000 if self.s.ram[0xFC49] == 0xA0 else 0):
                return self.s.ram[addr]
        pri = (self.s.slot_reg_a8 >> (page * 2)) & 3
        sub = ((self.s.ffff_regs[pri] >> (page * 2)) & 3) if self.s.expanded[pri] else 0
        k = self.s.slot_kind[pri][sub][page]
        if k == 0: return 0xFF
        if k == 4: return self.s.mapper_segs[self.s.mapper_seg[page] % self.s.mapper_n_segs][off]
        if k == 3: return self.s.slot_bufs[pri][sub][page][off & 0x1FFF]
        return self.s.slot_bufs[pri][sub][page][off]

    def write8(self, addr, val):
        addr &= 0xFFFF; val &= 0xFF
        if addr >= 0xC000: self.s.ram[addr] = val; return
        page = addr >> 14; off = addr & 0x3FFF
        if page == 2 and self.s.ram[0xFC49] <= 0xA0:
            pri = (self.s.slot_reg_a8 >> 4) & 3
            if pri == ((self.s.slot_reg_a8 >> 6) & 3) and off >= (0x2000 if self.s.ram[0xFC49] == 0xA0 else 0):
                self.s.ram[addr] = val; return
        pri = (self.s.slot_reg_a8 >> (page * 2)) & 3
        sub = ((self.s.ffff_regs[pri] >> (page * 2)) & 3) if self.s.expanded[pri] else 0
        k = self.s.slot_kind[pri][sub][page]
        if k == 2: self.s.slot_bufs[pri][sub][page][off] = val
        elif k == 3: self.s.slot_bufs[pri][sub][page][off & 0x1FFF] = val
        elif k == 4: self.s.mapper_segs[self.s.mapper_seg[page] % self.s.mapper_n_segs][off] = val

    def run_usr(self, entry, arg_i16, max_steps=100_000_000):
        res = _lib.run_usr_c(ctypes.byref(self.s), entry & 0xFFFF, arg_i16, max_steps)
        if self.s.stop_reason != 0:
            raise RuntimeError(f"stop={self.s.stop_reason} op={self.s.bad_op:02X} pc={self.s.bad_pc:04X} werr={self.s.watch_err} addr={self.s.watch_err_addr:04X}")
        return res