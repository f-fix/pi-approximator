#include <stdint.h>

typedef struct {
    uint8_t ram[65536];
    uint8_t vram[131072];
    uint8_t slot_bufs[4][4][4][16384];
    uint8_t slot_kind[4][4][4]; /* 0=empty, 1=rom, 2=ram16, 3=ram8_mirror, 4=mapper, 5=diskrom */
    uint8_t mapper_segs[32][16384];
    uint8_t mapper_n_segs;
    uint8_t mapper_slot;
    uint8_t expanded[4];
    uint8_t ffff_regs[4];
    uint8_t slot_reg_a8;
    uint8_t mapper_seg[4];
    uint8_t mv, is_r800, strict_enaslt, vdp_latch_valid, vdp_latch;
    uint16_t vdp_addr;
    uint8_t vdp_r14, fdc_touched, pal_writes[256];
    int pal_count;
    uint8_t watch_mode, digit_pgt[0x1800];
    int watch_err;
    uint16_t watch_err_addr;
    uint8_t watch_err_val;
    uint16_t guard_lo, guard_hi;
    uint32_t vram_min_calc, vram_max_calc;
    uint8_t track_vram;
    uint8_t a, f, b, c, d, e, h, l;
    uint8_t a2, f2, b2, c2, d2, e2, h2, l2;
    uint16_t ix, iy, sp, pc;
    uint8_t iff, ei_delay;
    uint64_t irq_period, steps, irq_cnt;
    int stop_reason;
    uint8_t bad_op;
    uint16_t bad_pc;
} MSXState;

static inline void active_slot(MSXState *s, int page, int *pri, int *sub) {
    *pri = (s->slot_reg_a8 >> (page * 2)) & 3;
    *sub = s->expanded[*pri] ? ((s->ffff_regs[*pri] >> (page * 2)) & 3) : 0;
}

static inline uint8_t read8(MSXState *s, uint16_t addr) {
    if (addr >= 0xC000) {
        if (addr == 0xFFFF) {
            int pri = (s->slot_reg_a8 >> 6) & 3;
            if (s->expanded[pri]) return (~s->ffff_regs[pri]) & 0xFF;
        }
        return s->ram[addr];
    }
    int page = addr >> 14; uint16_t off = addr & 0x3FFF;
    if (page == 2 && s->ram[0xFC49] <= 0xA0) {
        int pri, sub; active_slot(s, 2, &pri, &sub);
        if (pri == ((s->slot_reg_a8 >> 6) & 3) && off >= (s->ram[0xFC49] == 0xA0 ? 0x2000 : 0))
            return s->ram[addr];
    }
    int pri, sub; active_slot(s, page, &pri, &sub);
    uint8_t kind = s->slot_kind[pri][sub][page];
    if (kind == 0) return 0xFF;
    if (kind == 2) return s->slot_bufs[pri][sub][page][off];
    if (kind == 3) return s->slot_bufs[pri][sub][page][off & 0x1FFF];
    if (kind == 4) return s->mapper_segs[s->mapper_seg[page] % s->mapper_n_segs][off];
    if (kind == 5) { if (off >= 0x3FF8) s->fdc_touched = 1; return s->slot_bufs[pri][sub][page][off]; }
    return s->slot_bufs[pri][sub][page][off];
}

static inline void write8(MSXState *s, uint16_t addr, uint8_t val) {
    if (s->guard_lo && addr >= s->guard_lo && addr <= s->guard_hi) {
        s->watch_err = 99; s->watch_err_addr = addr; s->watch_err_val = val;
    }
    if (addr >= 0xC000) {
        if (addr == 0xFFFF) {
            int pri = (s->slot_reg_a8 >> 6) & 3;
            if (s->expanded[pri]) s->ffff_regs[pri] = val;
            return;
        }
        s->ram[addr] = val; return;
    }
    int page = addr >> 14; uint16_t off = addr & 0x3FFF;
    if (page == 2 && s->ram[0xFC49] <= 0xA0) {
        int pri, sub; active_slot(s, 2, &pri, &sub);
        if (pri == ((s->slot_reg_a8 >> 6) & 3) && off >= (s->ram[0xFC49] == 0xA0 ? 0x2000 : 0)) {
            s->ram[addr] = val; return;
        }
    }
    int pri, sub; active_slot(s, page, &pri, &sub);
    uint8_t kind = s->slot_kind[pri][sub][page];
    if (kind == 2) s->slot_bufs[pri][sub][page][off] = val;
    else if (kind == 3) s->slot_bufs[pri][sub][page][off & 0x1FFF] = val;
    else if (kind == 4) s->mapper_segs[s->mapper_seg[page] % s->mapper_n_segs][off] = val;
    else if (kind == 5) { if (off >= 0x3FF8) s->fdc_touched = 1; }
}

static inline uint16_t read16(MSXState *s, uint16_t a) { return (uint16_t)read8(s, a) | ((uint16_t)read8(s, a+1) << 8); }
static inline void write16(MSXState *s, uint16_t a, uint16_t v) { write8(s, a, v & 0xFF); write8(s, a+1, (v >> 8) & 0xFF); }
static inline void push16(MSXState *s, uint16_t v) { s->sp -= 2; write16(s, s->sp, v); }
static inline uint16_t pop16(MSXState *s) { uint16_t v = read16(s, s->sp); s->sp += 2; return v; }

static inline void port_out(MSXState *s, uint8_t p, uint8_t v) {
    if (p == 0x99) {
        if (!s->vdp_latch_valid) { s->vdp_latch = v; s->vdp_latch_valid = 1; }
        else {
            if (v & 0x80) { if ((v & 0x3F) == 14) s->vdp_r14 = s->vdp_latch & 7; }
            else s->vdp_addr = s->vdp_latch | ((uint16_t)(v & 0x3F) << 8);
            s->vdp_latch_valid = 0;
        }
    } else if (p == 0x98) {
        uint32_t fa = (s->mv >= 1) ? (((uint32_t)(s->vdp_r14 & 7) << 14) | (s->vdp_addr & 0x3FFF)) : (s->vdp_addr & 0x3FFF);
        s->vram[fa] = v;
        if (s->track_vram) { if (fa < s->vram_min_calc) s->vram_min_calc = fa; if (fa > s->vram_max_calc) s->vram_max_calc = fa; }
        if (s->watch_mode) {
            if (fa >= 0x1800 && fa <= 0x1B03) { s->watch_err = 1; s->watch_err_addr = fa; s->watch_err_val = v; }
            else if (s->watch_mode == 1) {
                if (fa < 0x1800 && s->digit_pgt[fa]) { s->watch_err = 2; s->watch_err_addr = fa; s->watch_err_val = v; }
                else if (fa >= 0x2000 && fa < 0x3800 && v != 0x33 && v != 0xFF) { s->watch_err = 3; s->watch_err_addr = fa; s->watch_err_val = v; }
            } else if (s->watch_mode == 2) {
                if (fa < 0x1800) s->digit_pgt[fa] = 1;
                else if (fa >= 0x2000 && fa < 0x3800 && v != 0x13 && v != 0x6F) { s->watch_err = 4; s->watch_err_addr = fa; s->watch_err_val = v; }
            }
        }
        s->vdp_addr = (s->vdp_addr + 1) & 0x3FFF;
    } else if (p == 0x9A) { if (s->pal_count < 256) s->pal_writes[s->pal_count++] = v; }
    else if (p >= 0xFC && p <= 0xFF) { s->mapper_seg[p - 0xFC] = v; }
    else if (p == 0xA8) { s->slot_reg_a8 = v; }
}

static inline uint8_t port_in(MSXState *s, uint8_t p) {
    if (p == 0x99) { s->vdp_latch_valid = 0; return 0x80; }
    if (p == 0x98) {
        uint32_t fa = (s->mv >= 1) ? (((uint32_t)(s->vdp_r14 & 7) << 14) | (s->vdp_addr & 0x3FFF)) : (s->vdp_addr & 0x3FFF);
        uint8_t v = s->vram[fa]; s->vdp_addr = (s->vdp_addr + 1) & 0x3FFF; return v;
    }
    if (p == 0xA8) return s->slot_reg_a8;
    return 0xFF;
}

static inline void set_z_szp(MSXState *s, uint8_t val, int carry) {
    uint8_t f = (carry < 0) ? (s->f & 1) : (carry ? 1 : 0);
    if (val & 0x80) f |= 0x80;
    if (val == 0) f |= 0x40;
    s->f = f;
}
static inline uint16_t add16(MSXState *s, uint16_t a, uint16_t b) { uint32_t r=(uint32_t)a+b; s->f=(s->f&0x40)|(r>0xFFFF?1:0); return (uint16_t)r; }
static inline uint16_t adc16(MSXState *s, uint16_t a, uint16_t b) { uint32_t r=(uint32_t)a+b+(s->f&1); uint16_t r16=r; s->f=(r>0xFFFF?1:0)|(r16==0?0x40:0)|((r16&0x8000)?0x80:0); return r16; }
static inline uint16_t sbc16(MSXState *s, uint16_t a, uint16_t b) { int32_t r=(int32_t)a-(int32_t)b-(s->f&1); uint16_t r16=r; s->f=(r<0?3:2)|(r16==0?0x40:0)|((r16&0x8000)?0x80:0); return r16; }
static inline uint8_t add8(MSXState *s, uint8_t a, uint8_t b, uint8_t cy) { uint16_t r=(uint16_t)a+b+cy; uint8_t r8=r; s->f=(r>255?1:0)|(r8==0?0x40:0)|((r8&0x80)?0x80:0); return r8; }
static inline uint8_t sub8(MSXState *s, uint8_t a, uint8_t b, uint8_t cy) { int16_t r=(int16_t)a-(int16_t)b-cy; uint8_t r8=r; s->f=2|(r<0?1:0)|(r8==0?0x40:0)|((r8&0x80)?0x80:0); return r8; }
static inline uint8_t get_r(MSXState *s, int i) { switch(i){case 0:return s->b;case 1:return s->c;case 2:return s->d;case 3:return s->e;case 4:return s->h;case 5:return s->l;case 6:return read8(s,((uint16_t)s->h<<8)|s->l);default:return s->a;} }
static inline void set_r(MSXState *s, int i, uint8_t v) { switch(i){case 0:s->b=v;break;case 1:s->c=v;break;case 2:s->d=v;break;case 3:s->e=v;break;case 4:s->h=v;break;case 5:s->l=v;break;case 6:write8(s,((uint16_t)s->h<<8)|s->l,v);break;case 7:s->a=v;break;} }

int run_usr_c(MSXState *s, uint16_t entry, int16_t arg_i16, uint64_t max_steps) {
    write16(s, 0xF7F8, (uint16_t)arg_i16); s->a = 2; push16(s, 0xFFFF); s->pc = entry;
    s->stop_reason = 0; s->watch_err = 0;
    uint64_t steps = 0;
    while (s->pc != 0xFFFF) {
        if (s->watch_err) { s->stop_reason = 4; return 0; }
        if (++steps > max_steps) { s->stop_reason = 1; s->steps += steps; return 0; }
        if (s->ei_delay) s->ei_delay = 0;
        else if (s->iff && s->irq_period && (steps % s->irq_period == 0)) { s->iff = 0; push16(s, s->pc); s->pc = 0x0038; s->irq_cnt++; }
        if (s->pc == 0x0024) {
            int page = (s->h >> 6) & 3;
            if (s->strict_enaslt && page == 0) { s->stop_reason = 3; return 0; }
            int pri = s->a & 3;
            if (s->a & 0x80) { int sub = (s->a >> 2) & 3; uint8_t ns = (s->ffff_regs[pri] & ~(3<<(page*2))) | (sub<<(page*2)); s->ffff_regs[pri] = ns; s->ram[0xFCC5+pri] = ns; }
            s->slot_reg_a8 = (s->slot_reg_a8 & ~(3<<(page*2))) | (pri<<(page*2)); s->iff = 1;
            if (s->strict_enaslt) { s->b=0xAA;s->c=0x55;s->d=0xBB;s->e=0x66;s->h=0xCC;s->l=0x77;s->ix=0xDEAD;s->iy=0xBEEF; }
            s->pc = pop16(s); continue;
        }
        uint8_t op = read8(s, s->pc++);
        if (op == 0x00) {} else if (op == 0xF3) { s->iff = 0; s->ei_delay = 0; } else if (op == 0xFB) { s->iff = 1; s->ei_delay = 1; }
        else if (op == 0xAF) { s->a = 0; s->f = 0x40; } else if (op == 0x37) { s->f |= 1; }
        else if (op == 0x3F) { s->f = (s->f & 0xC4) | ((s->f & 1) ^ 1); } else if (op == 0x2F) { s->a ^= 0xFF; s->f |= 2; }
        else if (op == 0xC9) { s->pc = pop16(s); }
        else if (op == 0x17) { uint8_t c=(s->a>>7)&1; s->a=(s->a<<1)|(s->f&1); s->f=(s->f&0xC0)|c; }
        else if (op == 0x07) { uint8_t c=(s->a>>7)&1; s->a=(s->a<<1)|c; s->f=(s->f&0xC0)|c; }
        else if (op == 0x0F) { uint8_t c=s->a&1; s->a=(s->a>>1)|(c<<7); s->f=(s->f&0xC0)|c; }
        else if (op == 0x1F) { uint8_t c=s->a&1; s->a=(s->a>>1)|((s->f&1)<<7); s->f=(s->f&0xC0)|c; }
        else if (op == 0xD9) { uint8_t t; t=s->b;s->b=s->b2;s->b2=t;t=s->c;s->c=s->c2;s->c2=t;t=s->d;s->d=s->d2;s->d2=t;t=s->e;s->e=s->e2;s->e2=t;t=s->h;s->h=s->h2;s->h2=t;t=s->l;s->l=s->l2;s->l2=t; }
        else if (op == 0xEB) { uint8_t t=s->d;s->d=s->h;s->h=t;t=s->e;s->e=s->l;s->l=t; }
        else if (op == 0xE3) { uint16_t t=read16(s,s->sp);write16(s,s->sp,((uint16_t)s->h<<8)|s->l);s->h=t>>8;s->l=t&255; }
        else if (op == 0xE9) { s->pc = ((uint16_t)s->h<<8)|s->l; }
        else if (op==0xC5||op==0xD5||op==0xE5||op==0xF5) { push16(s,(op==0xC5)?(((uint16_t)s->b<<8)|s->c):(op==0xD5)?(((uint16_t)s->d<<8)|s->e):(op==0xE5)?(((uint16_t)s->h<<8)|s->l):(((uint16_t)s->a<<8)|s->f)); }
        else if (op==0xC1||op==0xD1||op==0xE1||op==0xF1) { uint16_t v=pop16(s);if(op==0xC1){s->b=v>>8;s->c=v&255;}else if(op==0xD1){s->d=v>>8;s->e=v&255;}else if(op==0xE1){s->h=v>>8;s->l=v&255;}else{s->a=v>>8;s->f=v&255;} }
        else if (op==0x01||op==0x11||op==0x21||op==0x31) { uint16_t v=read16(s,s->pc);s->pc+=2;if(op==0x01){s->b=v>>8;s->c=v&255;}else if(op==0x11){s->d=v>>8;s->e=v&255;}else if(op==0x21){s->h=v>>8;s->l=v&255;}else s->sp=v; }
        else if (op==0x09||op==0x19||op==0x29||op==0x39) { uint16_t rr=(op==0x09)?(((uint16_t)s->b<<8)|s->c):(op==0x19)?(((uint16_t)s->d<<8)|s->e):(op==0x29)?(((uint16_t)s->h<<8)|s->l):s->sp;uint16_t r=add16(s,((uint16_t)s->h<<8)|s->l,rr);s->h=r>>8;s->l=r&255; }
        else if (op==0x03||op==0x13||op==0x23||op==0x33) { if(op==0x03){uint16_t v=(((uint16_t)s->b<<8)|s->c)+1;s->b=v>>8;s->c=v&255;}else if(op==0x13){uint16_t v=(((uint16_t)s->d<<8)|s->e)+1;s->d=v>>8;s->e=v&255;}else if(op==0x23){uint16_t v=(((uint16_t)s->h<<8)|s->l)+1;s->h=v>>8;s->l=v&255;}else s->sp++; }
        else if (op==0x0B||op==0x1B||op==0x2B||op==0x3B) { if(op==0x0B){uint16_t v=(((uint16_t)s->b<<8)|s->c)-1;s->b=v>>8;s->c=v&255;}else if(op==0x1B){uint16_t v=(((uint16_t)s->d<<8)|s->e)-1;s->d=v>>8;s->e=v&255;}else if(op==0x2B){uint16_t v=(((uint16_t)s->h<<8)|s->l)-1;s->h=v>>8;s->l=v&255;}else s->sp--; }
        else if ((op&0xC7)==0x06) { set_r(s,(op>>3)&7,read8(s,s->pc++)); }
        else if ((op&0xC0)==0x40&&op!=0x76) { set_r(s,(op>>3)&7,get_r(s,op&7)); }
        else if ((op&0xC7)==0x04) { int i=(op>>3)&7;uint8_t v=get_r(s,i)+1;set_r(s,i,v);set_z_szp(s,v,-1); }
        else if ((op&0xC7)==0x05) { int i=(op>>3)&7;uint8_t v=get_r(s,i)-1;set_r(s,i,v);set_z_szp(s,v,-1); }
        else if (op==0x22) { uint16_t a=read16(s,s->pc);s->pc+=2;write16(s,a,((uint16_t)s->h<<8)|s->l); }
        else if (op==0x2A) { uint16_t a=read16(s,s->pc);s->pc+=2;uint16_t v=read16(s,a);s->h=v>>8;s->l=v&255; }
        else if (op==0x32) { uint16_t a=read16(s,s->pc);s->pc+=2;write8(s,a,s->a); }
        else if (op==0x3A) { uint16_t a=read16(s,s->pc);s->pc+=2;s->a=read8(s,a); }
        else if (op==0x0A||op==0x1A) { s->a=read8(s,(op==0x0A)?(((uint16_t)s->b<<8)|s->c):(((uint16_t)s->d<<8)|s->e)); }
        else if (op==0x02||op==0x12) { write8(s,(op==0x02)?(((uint16_t)s->b<<8)|s->c):(((uint16_t)s->d<<8)|s->e),s->a); }
        else if ((op&0xF8)==0x80) { s->a=add8(s,s->a,get_r(s,op&7),0); }
        else if ((op&0xF8)==0x88) { s->a=add8(s,s->a,get_r(s,op&7),s->f&1); }
        else if ((op&0xF8)==0x90) { s->a=sub8(s,s->a,get_r(s,op&7),0); }
        else if ((op&0xF8)==0x98) { s->a=sub8(s,s->a,get_r(s,op&7),s->f&1); }
        else if ((op&0xF8)==0xA0) { s->a&=get_r(s,op&7);set_z_szp(s,s->a,0); }
        else if ((op&0xF8)==0xA8) { s->a^=get_r(s,op&7);set_z_szp(s,s->a,0); }
        else if ((op&0xF8)==0xB0) { s->a|=get_r(s,op&7);set_z_szp(s,s->a,0); }
        else if ((op&0xF8)==0xB8) { sub8(s,s->a,get_r(s,op&7),0); }
        else if (op==0xC6) { s->a=add8(s,s->a,read8(s,s->pc++),0); }
        else if (op==0xCE) { s->a=add8(s,s->a,read8(s,s->pc++),s->f&1); }
        else if (op==0xD6) { s->a=sub8(s,s->a,read8(s,s->pc++),0); }
        else if (op==0xE6) { s->a&=read8(s,s->pc++);set_z_szp(s,s->a,0); }
        else if (op==0xEE) { s->a^=read8(s,s->pc++);set_z_szp(s,s->a,0); }
        else if (op==0xF6) { s->a|=read8(s,s->pc++);set_z_szp(s,s->a,0); }
        else if (op==0xFE) { sub8(s,s->a,read8(s,s->pc++),0); }
        else if (op==0x18) { int8_t o=(int8_t)read8(s,s->pc++);s->pc+=o; }
        else if (op==0x10) { int8_t o=(int8_t)read8(s,s->pc++);if(--s->b!=0)s->pc+=o; }
        else if (op==0x20||op==0x28||op==0x30||op==0x38) { int8_t o=(int8_t)read8(s,s->pc++);if((op==0x20)?!(s->f&0x40):(op==0x28)?(s->f&0x40):(op==0x30)?!(s->f&1):(s->f&1))s->pc+=o; }
        else if (op==0xC3) { s->pc=read16(s,s->pc); }
        else if (op==0xC2||op==0xCA||op==0xD2||op==0xDA) { uint16_t a=read16(s,s->pc);s->pc+=2;if((op==0xC2)?!(s->f&0x40):(op==0xCA)?(s->f&0x40):(op==0xD2)?!(s->f&1):(s->f&1))s->pc=a; }
        else if ((op&0xC7)==0xC0) { int cc=(op>>3)&7;if((cc==0)?!(s->f&0x40):(cc==1)?(s->f&0x40):(cc==2)?!(s->f&1):(cc==3)?(s->f&1):(cc==6)?!(s->f&0x80):(cc==7)?(s->f&0x80):0)s->pc=pop16(s); }
        else if (op==0xCD) { uint16_t a=read16(s,s->pc);push16(s,s->pc+2);s->pc=a; }
        else if (op==0xD3) { port_out(s,read8(s,s->pc++),s->a); }
        else if (op==0xDB) { s->a=port_in(s,read8(s,s->pc++)); }
        else if (op==0xCB) { uint8_t op2=read8(s,s->pc++);uint8_t r=get_r(s,op2&7);int b=(op2>>3)&7;if(op2<0x40){int cy=0;if(b==0){cy=(r>>7)&1;r=(r<<1)|cy;}else if(b==1){cy=r&1;r=(r>>1)|(cy<<7);}else if(b==2){cy=(r>>7)&1;r=(r<<1)|(s->f&1);}else if(b==3){cy=r&1;r=(r>>1)|((s->f&1)<<7);}else if(b==4){cy=(r>>7)&1;r<<=1;}else if(b==6){cy=(r>>7)&1;r=(r<<1)|1;}else if(b==7){cy=r&1;r>>=1;}set_r(s,op2&7,r);set_z_szp(s,r,cy);}else if(op2<0x80)s->f=(s->f&1)|(!(r&(1<<b))?0x40:0);else if(op2<0xC0)set_r(s,op2&7,r&~(1<<b));else set_r(s,op2&7,r|(1<<b)); }
        else if (op==0xED) { uint8_t op2=read8(s,s->pc++);if(op2==0x4B){uint16_t a=read16(s,s->pc);s->pc+=2;uint16_t v=read16(s,a);s->b=v>>8;s->c=v&255;}else if(op2==0x5B){uint16_t a=read16(s,s->pc);s->pc+=2;uint16_t v=read16(s,a);s->d=v>>8;s->e=v&255;}else if(op2==0x43){uint16_t a=read16(s,s->pc);s->pc+=2;write16(s,a,((uint16_t)s->b<<8)|s->c);}else if(op2==0x53){uint16_t a=read16(s,s->pc);s->pc+=2;write16(s,a,((uint16_t)s->d<<8)|s->e);}else if(op2==0x4A||op2==0x5A||op2==0x6A||op2==0x7A){uint16_t rr=(op2==0x4A)?(((uint16_t)s->b<<8)|s->c):(op2==0x5A)?(((uint16_t)s->d<<8)|s->e):(op2==0x6A)?(((uint16_t)s->h<<8)|s->l):s->sp;uint16_t v=adc16(s,((uint16_t)s->h<<8)|s->l,rr);s->h=v>>8;s->l=v&255;}else if(op2==0x42||op2==0x52||op2==0x62||op2==0x72){uint16_t rr=(op2==0x42)?(((uint16_t)s->b<<8)|s->c):(op2==0x52)?(((uint16_t)s->d<<8)|s->e):(op2==0x62)?(((uint16_t)s->h<<8)|s->l):s->sp;uint16_t v=sbc16(s,((uint16_t)s->h<<8)|s->l,rr);s->h=v>>8;s->l=v&255;}else if(op2==0xB0){uint16_t hl=((uint16_t)s->h<<8)|s->l,de=((uint16_t)s->d<<8)|s->e,bc=((uint16_t)s->b<<8)|s->c;do{write8(s,de++,read8(s,hl++));bc--;}while(bc!=0);s->h=hl>>8;s->l=hl&255;s->d=de>>8;s->e=de&255;s->b=0;s->c=0;}else if(op2==0xC3){if(s->is_r800){uint32_t res=(uint32_t)(((uint16_t)s->h<<8)|s->l)*(uint32_t)(((uint16_t)s->b<<8)|s->c);s->h=(res>>8)&255;s->l=res&255;s->d=(res>>24)&255;s->e=(res>>16)&255;}}else{s->stop_reason=2;s->bad_op=op2;s->bad_pc=s->pc-2;return 0;} }
        else if (op==0xDD||op==0xFD) { int is_ix=(op==0xDD);uint16_t idx=is_ix?s->ix:s->iy;uint8_t op2=read8(s,s->pc++);if(op2==0xE5)push16(s,idx);else if(op2==0xE1)idx=pop16(s);else if(op2==0x21){idx=read16(s,s->pc);s->pc+=2;}else if(op2==0x22){uint16_t a=read16(s,s->pc);s->pc+=2;write16(s,a,idx);}else if(op2==0x2A){uint16_t a=read16(s,s->pc);s->pc+=2;idx=read16(s,a);}else if(op2==0x23)idx++;else if(op2==0x2B)idx--;else if(op2==0x09)idx=add16(s,idx,((uint16_t)s->b<<8)|s->c);else if(op2==0x19)idx=add16(s,idx,((uint16_t)s->d<<8)|s->e);else if(op2==0x29)idx=add16(s,idx,idx);else if(op2==0x60)idx=((uint16_t)s->b<<8)|(idx&0xFF);else if(op2==0x67)idx=((uint16_t)s->a<<8)|(idx&0xFF);else if(op2==0x6F)idx=(idx&0xFF00)|s->a;else if(op2==0x7C)s->a=(idx>>8)&255;else if(op2==0x7D)s->a=idx&255;else if(op2==0x36){int8_t d=(int8_t)read8(s,s->pc);uint8_t n=read8(s,s->pc+1);s->pc+=2;write8(s,idx+d,n);}else if((op2&0xC7)==0x46){int8_t d=(int8_t)read8(s,s->pc++);set_r(s,(op2>>3)&7,read8(s,idx+d));}else if((op2&0xF8)==0x70&&op2!=0x76){int8_t d=(int8_t)read8(s,s->pc++);write8(s,idx+d,get_r(s,op2&7));}else if(op2==0xCB){int8_t d=(int8_t)read8(s,s->pc);uint8_t op3=read8(s,s->pc+1);s->pc+=2;uint8_t v=read8(s,idx+d);int b=(op3>>3)&7;if(op3>=0x40&&op3<0x80)s->f=(s->f&1)|(!(v&(1<<b))?0x40:0);else{s->stop_reason=2;s->bad_op=op3;s->bad_pc=s->pc-4;return 0;}}else{s->stop_reason=2;s->bad_op=op2;s->bad_pc=s->pc-2;return 0;}if(is_ix)s->ix=idx;else s->iy=idx; }
        else { s->stop_reason=2; s->bad_op=op; s->bad_pc=s->pc-1; return 0; }
    }
    if (s->watch_err) { s->stop_reason = 4; return 0; }
    s->steps += steps;
    return (int)(int16_t)read16(s, 0xF7F8);
}