# PIV13.BAS Disassembled & Round-Trip Verified Z80/R800 Machine Code

Source: `PIV13.BAS` (`sha256: 90929cf746ebfd9f4f64bc8aaa84faa1441aeaa6bb4b385a4d2c2c999c60280b`)

Every `.asm` listing below was generated from `PIV13.BAS` `DATA` lines (`1840..2070`), annotated with entry-point, register, MSX BIOS/I/O, and data-table comments, and verified via `z80_asm.py` to re-assemble to the **exact same machine-code bytes and relocation tables**.

> **Syntax note:** `R(0xNNNN)` marks a 16-bit operand belonging to the section's delta-encoded relocation table (adjusted by `A!` at load time in BASIC lines `1095..1105`).

## `s0.asm` (531 B code + 51 B reloc = 582 B)

```asm
ORG 0x0000
; === s0: MSX1 Slot/RAM Probe (runs once at A!, overwritten by s1) ===
    DI ; 0000: f3
    PUSH AF ; 0001: f5
    PUSH BC ; 0002: c5
    PUSH DE ; 0003: d5
    PUSH HL ; 0004: e5
    PUSH IX ; 0005: dde5
    PUSH IY ; 0007: fde5
    IN A, (0xA8) ; 0009: dba8 [PPI slot select]
    LD (R(0x0209)), A ; 000B: 320902
    LD A, 0xFF ; 000E: 3eff
    LD (R(0x0210)), A ; 0010: 321002
    LD (R(0x0211)), A ; 0013: 321102
    LD (R(0x0212)), A ; 0016: 321202
    IN A, (0xA8) ; 0019: dba8 [PPI slot select]
    RLCA ; 001B: 07
    RLCA ; 001C: 07
    AND 0x03 ; 001D: e603
    LD B, 0x06 ; 001F: 0606
    CALL R(0x01DF) ; 0021: cddf01
    LD (R(0x020F)), A ; 0024: 320f02
    LD A, (0xFCC1) ; 0027: 3ac1fc [EXPTBL]
    AND 0x80 ; 002A: e680
    LD (R(0x020B)), A ; 002C: 320b02
    LD A, (R(0x0209)) ; 002F: 3a0902
    RRCA ; 0032: 0f
    RRCA ; 0033: 0f
    AND 0x03 ; 0034: e603
    LD B, 0x02 ; 0036: 0602
    CALL R(0x01DF) ; 0038: cddf01
    LD (R(0x020C)), A ; 003B: 320c02
    LD A, (0xFC49) ; 003E: 3a49fc
    CP 0xA1 ; 0041: fea1
    JR C, L_004D ; 0043: 3808
    LD A, 0x02 ; 0045: 3e02
    CALL R(0x006D) ; 0047: cd6d00
    LD (R(0x0210)), A ; 004A: 321002
L_004D:
    LD A, 0x01 ; 004D: 3e01
    CALL R(0x006D) ; 004F: cd6d00
    LD (R(0x0211)), A ; 0052: 321102
    LD A, 0x00 ; 0055: 3e00
    CALL R(0x006D) ; 0057: cd6d00
    LD (R(0x0212)), A ; 005A: 321202
    LD HL, 0x0000 ; 005D: 210000
    LD (0xF7F8), HL ; 0060: 22f8f7 [BASIC USR arg/ret]
    POP IY ; 0063: fde1
    POP IX ; 0065: dde1
    POP HL ; 0067: e1
    POP DE ; 0068: d1
    POP BC ; 0069: c1
    POP AF ; 006A: f1
    EI ; 006B: fb
    RET ; 006C: c9
L_006D:
    LD (R(0x020A)), A ; 006D: 320a02
    LD A, 0xFF ; 0070: 3eff
    LD (R(0x020D)), A ; 0072: 320d02
    LD A, (R(0x020F)) ; 0075: 3a0f02
    CALL R(0x00B2) ; 0078: cdb200
    JR NC, L_00AE ; 007B: 3031
    LD C, 0x00 ; 007D: 0e00
L_007F:
    LD HL, 0xFCC1 ; 007F: 21c1fc [EXPTBL]
    LD A, C ; 0082: 79
    ADD A, L ; 0083: 85
    LD L, A ; 0084: 6f
    JR NC, L_0088 ; 0085: 3001
    INC H ; 0087: 24
L_0088:
    LD A, (HL) ; 0088: 7e
    BIT 7, A ; 0089: cb7f
    JR NZ, L_0095 ; 008B: 2008
    LD A, C ; 008D: 79
    CALL R(0x00B2) ; 008E: cdb200
    JR NC, L_00AE ; 0091: 301b
    JR L_00A8 ; 0093: 1813
L_0095:
    LD B, 0x00 ; 0095: 0600
L_0097:
    LD A, B ; 0097: 78
    RLCA ; 0098: 07
    RLCA ; 0099: 07
    OR C ; 009A: b1
    OR 0x80 ; 009B: f680
    CALL R(0x00B2) ; 009D: cdb200
    JR NC, L_00AE ; 00A0: 300c
    INC B ; 00A2: 04
    LD A, B ; 00A3: 78
    CP 0x04 ; 00A4: fe04
    JR NZ, L_0097 ; 00A6: 20ef
L_00A8:
    INC C ; 00A8: 0c
    LD A, C ; 00A9: 79
    CP 0x04 ; 00AA: fe04
    JR NZ, L_007F ; 00AC: 20d1
L_00AE:
    LD A, (R(0x020D)) ; 00AE: 3a0d02
    RET ; 00B1: c9
L_00B2:
    PUSH BC ; 00B2: c5
    PUSH DE ; 00B3: d5
    PUSH HL ; 00B4: e5
    LD (R(0x020E)), A ; 00B5: 320e02
    LD D, A ; 00B8: 57
    LD A, (R(0x020A)) ; 00B9: 3a0a02
    OR A ; 00BC: b7
    JR NZ, L_00F4 ; 00BD: 2035
    LD A, (R(0x020B)) ; 00BF: 3a0b02
    CP D ; 00C2: ba
    JP Z, R(0x0188) ; 00C3: ca8801
    BIT 7, D ; 00C6: cb7a
    JR Z, L_00D3 ; 00C8: 2809
    LD A, (R(0x020F)) ; 00CA: 3a0f02
    XOR D ; 00CD: aa
    AND 0x03 ; 00CE: e603
    JP NZ, R(0x0188) ; 00D0: c28801
L_00D3:
    LD A, D ; 00D3: 7a
    BIT 7, A ; 00D4: cb7f
    JR Z, L_00E7 ; 00D6: 280f
    RRCA ; 00D8: 0f
    RRCA ; 00D9: 0f
    AND 0x03 ; 00DA: e603
    LD B, A ; 00DC: 47
    LD A, (0xFFFF) ; 00DD: 3affff [SLTSL subslot reg]
    CPL ; 00E0: 2f
    AND 0xFC ; 00E1: e6fc
    OR B ; 00E3: b0
    LD (0xFFFF), A ; 00E4: 32ffff [SLTSL subslot reg]
L_00E7:
    LD A, D ; 00E7: 7a
    AND 0x03 ; 00E8: e603
    LD B, A ; 00EA: 47
    IN A, (0xA8) ; 00EB: dba8 [PPI slot select]
    AND 0xFC ; 00ED: e6fc
    OR B ; 00EF: b0
    OUT (0xA8), A ; 00F0: d3a8 [PPI slot select]
    JR L_0111 ; 00F2: 181d
L_00F4:
    CP 0x01 ; 00F4: fe01
    JR NZ, L_0106 ; 00F6: 200e
    LD A, (R(0x020B)) ; 00F8: 3a0b02
    CP D ; 00FB: ba
    JP Z, R(0x0188) ; 00FC: ca8801
    LD A, (R(0x020C)) ; 00FF: 3a0c02
    CP D ; 0102: ba
    JP Z, R(0x0188) ; 0103: ca8801
L_0106:
    LD A, (R(0x020A)) ; 0106: 3a0a02
    RRCA ; 0109: 0f
    RRCA ; 010A: 0f
    LD H, A ; 010B: 67
    LD A, D ; 010C: 7a
    CALL 0x0024 ; 010D: cd2400 [BIOS ENASLT]
    DI ; 0110: f3
L_0111:
    LD A, (R(0x020A)) ; 0111: 3a0a02
    RRCA ; 0114: 0f
    RRCA ; 0115: 0f
    LD H, A ; 0116: 67
    LD L, 0x00 ; 0117: 2e00
    LD A, (HL) ; 0119: 7e
    CP 0x41 ; 011A: fe41
    JR NZ, L_0126 ; 011C: 2008
    INC HL ; 011E: 23
    LD A, (HL) ; 011F: 7e
    DEC HL ; 0120: 2b
    CP 0x42 ; 0121: fe42
    JP Z, R(0x0185) ; 0123: ca8501
L_0126:
    LD A, (HL) ; 0126: 7e
    CP 0x43 ; 0127: fe43
    JR NZ, L_0133 ; 0129: 2008
    INC HL ; 012B: 23
    LD A, (HL) ; 012C: 7e
    DEC HL ; 012D: 2b
    CP 0x44 ; 012E: fe44
    JP Z, R(0x0185) ; 0130: ca8501
L_0133:
    PUSH HL ; 0133: e5
    LD B, 0x10 ; 0134: 0610
L_0136:
    LD A, (HL) ; 0136: 7e
    LD C, A ; 0137: 4f
    CPL ; 0138: 2f
    LD (HL), A ; 0139: 77
    CP (HL) ; 013A: be
    LD (HL), C ; 013B: 71
    JR NZ, L_0184 ; 013C: 2046
    LD A, H ; 013E: 7c
    ADD A, 0x04 ; 013F: c604
    LD H, A ; 0141: 67
    DJNZ L_0136 ; 0142: 10f2
    POP HL ; 0144: e1
    PUSH HL ; 0145: e5
    LD A, H ; 0146: 7c
    OR 0x3E ; 0147: f63e
    LD H, A ; 0149: 67
    LD A, (HL) ; 014A: 7e
    LD C, A ; 014B: 4f
    CPL ; 014C: 2f
    LD (HL), A ; 014D: 77
    CP (HL) ; 014E: be
    LD (HL), C ; 014F: 71
    POP HL ; 0150: e1
    JP NZ, R(0x0185) ; 0151: c28501
    INC H ; 0154: 24
    LD A, (HL) ; 0155: 7e
    PUSH AF ; 0156: f5
    LD DE, 0x2000 ; 0157: 110020
    CALL R(0x01C4) ; 015A: cdc401
    JR C, L_017F ; 015D: 3820
    LD DE, 0x1000 ; 015F: 110010
    CALL R(0x01C4) ; 0162: cdc401
    JR C, L_017F ; 0165: 3818
    LD DE, 0x0800 ; 0167: 110008
    CALL R(0x01C4) ; 016A: cdc401
    JR C, L_017F ; 016D: 3810
    POP AF ; 016F: f1
    LD (HL), A ; 0170: 77
    LD A, (R(0x020E)) ; 0171: 3a0e02
    LD (R(0x020D)), A ; 0174: 320d02
    CALL R(0x018D) ; 0177: cd8d01
    POP HL ; 017A: e1
    POP DE ; 017B: d1
    POP BC ; 017C: c1
    OR A ; 017D: b7
    RET ; 017E: c9
L_017F:
    POP AF ; 017F: f1
    LD (HL), A ; 0180: 77
    JP R(0x0185) ; 0181: c38501
L_0184:
    POP HL ; 0184: e1
L_0185:
    CALL R(0x018D) ; 0185: cd8d01
L_0188:
    POP HL ; 0188: e1
    POP DE ; 0189: d1
    POP BC ; 018A: c1
    SCF ; 018B: 37
    RET ; 018C: c9
L_018D:
    LD A, (R(0x020A)) ; 018D: 3a0a02
    OR A ; 0190: b7
    JR NZ, L_01AC ; 0191: 2019
    LD A, (R(0x020B)) ; 0193: 3a0b02
    OR A ; 0196: b7
    JR Z, L_01A5 ; 0197: 280c
    LD A, (0xFFFF) ; 0199: 3affff [SLTSL subslot reg]
    CPL ; 019C: 2f
    AND 0xFC ; 019D: e6fc
    LD (0xFFFF), A ; 019F: 32ffff [SLTSL subslot reg]
    LD (0xFCC5), A ; 01A2: 32c5fc [SLTTBL]
L_01A5:
    IN A, (0xA8) ; 01A5: dba8 [PPI slot select]
    AND 0xFC ; 01A7: e6fc
    OUT (0xA8), A ; 01A9: d3a8 [PPI slot select]
    RET ; 01AB: c9
L_01AC:
    CP 0x01 ; 01AC: fe01
    JR NZ, L_01BA ; 01AE: 200a
    LD A, (R(0x020C)) ; 01B0: 3a0c02
    LD H, 0x40 ; 01B3: 2640
    CALL 0x0024 ; 01B5: cd2400 [BIOS ENASLT]
    DI ; 01B8: f3
    RET ; 01B9: c9
L_01BA:
    LD A, (R(0x020F)) ; 01BA: 3a0f02
    LD H, 0x80 ; 01BD: 2680
    CALL 0x0024 ; 01BF: cd2400 [BIOS ENASLT]
    DI ; 01C2: f3
    RET ; 01C3: c9
L_01C4:
    PUSH HL ; 01C4: e5
    ADD HL, DE ; 01C5: 19
    EX (SP), HL ; 01C6: e3
    LD (HL), 0x55 ; 01C7: 3655
    EX (SP), HL ; 01C9: e3
    LD A, (HL) ; 01CA: 7e
    EX (SP), HL ; 01CB: e3
    CP 0x55 ; 01CC: fe55
    JR NZ, L_01DC ; 01CE: 200c
    LD (HL), 0xAA ; 01D0: 36aa
    EX (SP), HL ; 01D2: e3
    LD A, (HL) ; 01D3: 7e
    EX (SP), HL ; 01D4: e3
    CP 0xAA ; 01D5: feaa
    JR NZ, L_01DC ; 01D7: 2003
    POP DE ; 01D9: d1
    SCF ; 01DA: 37
    RET ; 01DB: c9
L_01DC:
    POP DE ; 01DC: d1
    OR A ; 01DD: b7
    RET ; 01DE: c9
L_01DF:
    LD C, A ; 01DF: 4f
    LD HL, 0xFCC1 ; 01E0: 21c1fc [EXPTBL]
    ADD A, L ; 01E3: 85
    LD L, A ; 01E4: 6f
    JR NC, L_01E8 ; 01E5: 3001
    INC H ; 01E7: 24
L_01E8:
    LD A, (HL) ; 01E8: 7e
    BIT 7, A ; 01E9: cb7f
    JR Z, L_0207 ; 01EB: 281a
    LD HL, 0xFCC5 ; 01ED: 21c5fc [SLTTBL]
    LD A, C ; 01F0: 79
    ADD A, L ; 01F1: 85
    LD L, A ; 01F2: 6f
    JR NC, L_01F6 ; 01F3: 3001
    INC H ; 01F5: 24
L_01F6:
    LD A, (HL) ; 01F6: 7e
L_01F7:
    INC B ; 01F7: 04
    DEC B ; 01F8: 05
    JR Z, L_01FF ; 01F9: 2804
    RRCA ; 01FB: 0f
    DEC B ; 01FC: 05
    JR L_01F7 ; 01FD: 18f8
L_01FF:
    AND 0x03 ; 01FF: e603
    RLCA ; 0201: 07
    RLCA ; 0202: 07
    OR C ; 0203: b1
    OR 0x80 ; 0204: f680
    RET ; 0206: c9
L_0207:
    LD A, C ; 0207: 79
    RET ; 0208: c9
; Scratch + output slot table: +527=O (BASIC), +528=R (p2), +529=Q (p1), +530=P (p0)
L_0209:
    DB 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ; 0209
    DB 0x00, 0x00 ; 0211
```

## `s1.asm` (1782 B code + 131 B reloc = 1913 B)

```asm
ORG 0x0000
; === s1: Core Pi Spigot + MSX1 Display + GFX + Speed Loop ===
    JP R(0x0011) ; 0000: c31100
; 14-byte header: +3=B!, +5=B, +7=C!, +9=A_ext, +11=C, +13=S_disp, +15=T3, +16=CPU
L_0003:
    DB 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0x00 ; 0003
    DB 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ; 000B
; spigot_entry: USR(D): D<0 initializes array (returns 0), D>0 runs 1 block of 4 digits
L_0011:
    DI ; 0011: f3
    PUSH AF ; 0012: f5
    PUSH BC ; 0013: c5
    PUSH DE ; 0014: d5
    PUSH HL ; 0015: e5
    PUSH IX ; 0016: dde5
    PUSH IY ; 0018: fde5
    LD A, (0x002D) ; 001A: 3a2d00 [BIOS MSXVER]
    LD (R(0x03F6)), A ; 001D: 32f603
    LD BC, (0xF7F8) ; 0020: ed4bf8f7 [BASIC USR arg/ret]
    PUSH BC ; 0024: c5
    LD A, (R(0x000F)) ; 0025: 3a0f00
    OR A ; 0028: b7
    JR Z, L_0045 ; 0029: 281a
    CALL R(0x075E) ; 002B: cd5e07
    LD A, (R(0x0856)) ; 002E: 3a5608
    OR A ; 0031: b7
    JR Z, L_0045 ; 0032: 2811
    LD HL, 0x0038 ; 0034: 213800
    LD (HL), 0xC3 ; 0037: 36c3
    INC HL ; 0039: 23
    LD DE, R(0x0802) ; 003A: 110208
    LD (HL), E ; 003D: 73
    INC HL ; 003E: 23
    LD (HL), D ; 003F: 72
    LD A, 0xC9 ; 0040: 3ec9
    LD (0x0066), A ; 0042: 326600
L_0045:
    EI ; 0045: fb
    POP BC ; 0046: c1
    BIT 7, B ; 0047: cb78
    JP Z, R(0x00FE) ; 0049: cafe00
    XOR A ; 004C: af
    SUB C ; 004D: 91
    LD C, A ; 004E: 4f
    SBC A, A ; 004F: 9f
    SUB B ; 0050: 90
    LD B, A ; 0051: 47
    CALL R(0x02B4) ; 0052: cdb402
    LD HL, 0x0000 ; 0055: 210000
    LD (R(0x0430)), HL ; 0058: 223004
    LD (R(0x0432)), HL ; 005B: 223204
    LD A, (R(0x000F)) ; 005E: 3a0f00
    OR A ; 0061: b7
    JR NZ, L_00BC ; 0062: 2058
    PUSH BC ; 0064: c5
    LD H, B ; 0065: 60
    LD L, C ; 0066: 69
    OR A ; 0067: b7
    LD DE, (R(0x0007)) ; 0068: ed5b0700
    SBC HL, DE ; 006C: ed52
    JR C, L_0074 ; 006E: 3804
    LD BC, (R(0x0007)) ; 0070: ed4b0700
L_0074:
    LD HL, (R(0x0003)) ; 0074: 2a0300
    LD (HL), 0xD0 ; 0077: 36d0
    INC HL ; 0079: 23
    LD (HL), 0x07 ; 007A: 3607
    DEC HL ; 007C: 2b
    LD D, H ; 007D: 54
    LD E, L ; 007E: 5d
    INC DE ; 007F: 13
    INC DE ; 0080: 13
    SLA C ; 0081: cb21
    RL B ; 0083: cb10
    DEC BC ; 0085: 0b
    DEC BC ; 0086: 0b
    LD A, B ; 0087: 78
    OR C ; 0088: b1
    JR Z, L_008D ; 0089: 2802
    LDIR ; 008B: edb0
L_008D:
    POP BC ; 008D: c1
    LD H, B ; 008E: 60
    LD L, C ; 008F: 69
    OR A ; 0090: b7
    LD DE, (R(0x0007)) ; 0091: ed5b0700
    SBC HL, DE ; 0095: ed52
    JR C, L_00AE ; 0097: 3815
    JR Z, L_00AE ; 0099: 2813
    LD B, H ; 009B: 44
    LD C, L ; 009C: 4d
    LD HL, (R(0x0007)) ; 009D: 2a0700
L_00A0:
    PUSH BC ; 00A0: c5
    LD BC, 0x07D0 ; 00A1: 01d007
    CALL R(0x0411) ; 00A4: cd1104
    POP BC ; 00A7: c1
    INC HL ; 00A8: 23
    DEC BC ; 00A9: 0b
    LD A, B ; 00AA: 78
    OR C ; 00AB: b1
    JR NZ, L_00A0 ; 00AC: 20f2
L_00AE:
    LD HL, 0x0000 ; 00AE: 210000
    LD (0xF7F8), HL ; 00B1: 22f8f7 [BASIC USR arg/ret]
    LD A, 0x02 ; 00B4: 3e02
    LD (0xF663), A ; 00B6: 3263f6
    JP R(0x0288) ; 00B9: c38802
L_00BC:
    BIT 7, B ; 00BC: cb78
    JR Z, L_00CF ; 00BE: 280f
    PUSH BC ; 00C0: c5
    LD HL, (R(0x0009)) ; 00C1: 2a0900
    LD (HL), 0x00 ; 00C4: 3600
    LD D, H ; 00C6: 54
    LD E, L ; 00C7: 5d
    INC DE ; 00C8: 13
    LD BC, 0x025F ; 00C9: 015f02
    LDIR ; 00CC: edb0
    POP BC ; 00CE: c1
L_00CF:
    LD HL, 0x0000 ; 00CF: 210000
L_00D2:
    PUSH HL ; 00D2: e5
    OR A ; 00D3: b7
    LD DE, (R(0x0007)) ; 00D4: ed5b0700
    SBC HL, DE ; 00D8: ed52
    POP HL ; 00DA: e1
    JR C, L_00E7 ; 00DB: 380a
    PUSH BC ; 00DD: c5
    LD BC, 0x07D0 ; 00DE: 01d007
    CALL R(0x0411) ; 00E1: cd1104
    POP BC ; 00E4: c1
    JR L_00F6 ; 00E5: 180f
L_00E7:
    PUSH BC ; 00E7: c5
    PUSH HL ; 00E8: e5
    CALL R(0x06F6) ; 00E9: cdf606
    LD (IX+0), 0xD0 ; 00EC: dd3600d0
    LD (IX+1), 0x07 ; 00F0: dd360107
    POP HL ; 00F4: e1
    POP BC ; 00F5: c1
L_00F6:
    INC HL ; 00F6: 23
    DEC BC ; 00F7: 0b
    LD A, B ; 00F8: 78
    OR C ; 00F9: b1
    JR NZ, L_00D2 ; 00FA: 20d6
    JR L_00AE ; 00FC: 18b0
L_00FE:
    CALL R(0x02B4) ; 00FE: cdb402
    DEC BC ; 0101: 0b
    PUSH BC ; 0102: c5
    POP IY ; 0103: fde1
    PUSH IY ; 0105: fde5
    POP HL ; 0107: e1
    OR A ; 0108: b7
    LD DE, (R(0x0007)) ; 0109: ed5b0700
    SBC HL, DE ; 010D: ed52
    JR NC, L_012A ; 010F: 3019
    LD A, (R(0x000F)) ; 0111: 3a0f00
    OR A ; 0114: b7
    JR NZ, L_0124 ; 0115: 200d
    LD H, B ; 0117: 60
    LD L, C ; 0118: 69
    ADD HL, HL ; 0119: 29
    LD DE, (R(0x0003)) ; 011A: ed5b0300
    ADD HL, DE ; 011E: 19
    PUSH HL ; 011F: e5
    POP IX ; 0120: dde1
    JR L_012A ; 0122: 1806
L_0124:
    PUSH IY ; 0124: fde5
    POP HL ; 0126: e1
    CALL R(0x06F6) ; 0127: cdf606
L_012A:
    LD HL, 0x0000 ; 012A: 210000
    LD (R(0x0430)), HL ; 012D: 223004
    LD (R(0x0432)), HL ; 0130: 223204
L_0133:
    PUSH IY ; 0133: fde5
    POP HL ; 0135: e1
    OR A ; 0136: b7
    LD DE, (R(0x0007)) ; 0137: ed5b0700
    SBC HL, DE ; 013B: ed52
    JR C, L_0147 ; 013D: 3808
    PUSH IY ; 013F: fde5
    POP HL ; 0141: e1
    CALL R(0x03F7) ; 0142: cdf703
    JR L_014D ; 0145: 1806
L_0147:
    LD E, (IX+0) ; 0147: dd5e00
    LD D, (IX+1) ; 014A: dd5601
L_014D:
    CALL R(0x0358) ; 014D: cd5803
    LD A, IYH ; 0150: fd7c
    BIT 7, A ; 0152: cb7f
    JR Z, L_0167 ; 0154: 2811
    PUSH HL ; 0156: e5
    PUSH BC ; 0157: c5
    CALL R(0x0A5D) ; 0158: cd5d0a
    AND (HL) ; 015B: a6
    POP BC ; 015C: c1
    POP HL ; 015D: e1
    JR Z, L_0167 ; 015E: 2807
    PUSH HL ; 0160: e5
    LD HL, 0x2710 ; 0161: 211027
    ADD HL, DE ; 0164: 19
    EX DE, HL ; 0165: eb
    POP HL ; 0166: e1
L_0167:
    LD BC, (R(0x0430)) ; 0167: ed4b3004
    ADD HL, BC ; 016B: 09
    EX DE, HL ; 016C: eb
    LD BC, (R(0x0432)) ; 016D: ed4b3204
    ADC HL, BC ; 0171: ed4a
    EX DE, HL ; 0173: eb
    LD A, IYL ; 0174: fd7d
    LD C, A ; 0176: 4f
    LD A, IYH ; 0177: fd7c
    LD B, A ; 0179: 47
    SLA C ; 017A: cb21
    RL B ; 017C: cb10
    INC BC ; 017E: 03
    LD A, IYH ; 017F: fd7c
    BIT 7, A ; 0181: cb7f
    JR Z, L_01C0 ; 0183: 283b
    CALL R(0x0A14) ; 0185: cd140a
    PUSH AF ; 0188: f5
    PUSH DE ; 0189: d5
    PUSH HL ; 018A: e5
    PUSH IY ; 018B: fde5
    POP HL ; 018D: e1
    OR A ; 018E: b7
    LD DE, (R(0x0007)) ; 018F: ed5b0700
    SBC HL, DE ; 0193: ed52
    JR C, L_019F ; 0195: 3808
    PUSH IY ; 0197: fde5
    POP HL ; 0199: e1
    CALL R(0x0411) ; 019A: cd1104
    JR L_01A5 ; 019D: 1806
L_019F:
    LD (IX+0), C ; 019F: dd7100
    LD (IX+1), B ; 01A2: dd7001
L_01A5:
    POP HL ; 01A5: e1
    POP DE ; 01A6: d1
    POP AF ; 01A7: f1
    PUSH HL ; 01A8: e5
    PUSH DE ; 01A9: d5
    PUSH AF ; 01AA: f5
    CALL R(0x0A5D) ; 01AB: cd5d0a
    LD B, A ; 01AE: 47
    POP AF ; 01AF: f1
    OR A ; 01B0: b7
    JR Z, L_01B8 ; 01B1: 2805
    LD A, (HL) ; 01B3: 7e
    OR B ; 01B4: b0
    LD (HL), A ; 01B5: 77
    JR L_01BC ; 01B6: 1804
L_01B8:
    LD A, B ; 01B8: 78
    CPL ; 01B9: 2f
    AND (HL) ; 01BA: a6
    LD (HL), A ; 01BB: 77
L_01BC:
    POP DE ; 01BC: d1
    POP HL ; 01BD: e1
    JR L_01E1 ; 01BE: 1821
L_01C0:
    CALL R(0x02C3) ; 01C0: cdc302
    PUSH DE ; 01C3: d5
    PUSH HL ; 01C4: e5
    PUSH IY ; 01C5: fde5
    POP HL ; 01C7: e1
    OR A ; 01C8: b7
    LD DE, (R(0x0007)) ; 01C9: ed5b0700
    SBC HL, DE ; 01CD: ed52
    JR C, L_01D9 ; 01CF: 3808
    ADD HL, DE ; 01D1: 19
    CALL R(0x0411) ; 01D2: cd1104
    POP HL ; 01D5: e1
    POP DE ; 01D6: d1
    JR L_01E1 ; 01D7: 1808
L_01D9:
    POP HL ; 01D9: e1
    POP DE ; 01DA: d1
    LD (IX+0), C ; 01DB: dd7100
    LD (IX+1), B ; 01DE: dd7001
L_01E1:
    LD A, IYL ; 01E1: fd7d
    LD C, A ; 01E3: 4f
    LD A, IYH ; 01E4: fd7c
    LD B, A ; 01E6: 47
    CALL R(0x02FB) ; 01E7: cdfb02
    LD (R(0x0430)), HL ; 01EA: 223004
    LD (R(0x0432)), DE ; 01ED: ed533204
    DEC IY ; 01F1: fd2b
    LD A, IYL ; 01F3: fd7d
    LD B, A ; 01F5: 47
    LD A, IYH ; 01F6: fd7c
    OR B ; 01F8: b0
    JR Z, L_024C ; 01F9: 2851
    PUSH IY ; 01FB: fde5
    POP HL ; 01FD: e1
    OR A ; 01FE: b7
    LD DE, (R(0x0007)) ; 01FF: ed5b0700
    SBC HL, DE ; 0203: ed52
    JP NC, R(0x0133) ; 0205: d23301
    INC HL ; 0208: 23
    LD A, H ; 0209: 7c
    OR L ; 020A: b5
    JR Z, L_0229 ; 020B: 281c
    LD A, (R(0x000F)) ; 020D: 3a0f00
    OR A ; 0210: b7
    JR NZ, L_021A ; 0211: 2007
    DEC IX ; 0213: dd2b
    DEC IX ; 0215: dd2b
    JP R(0x0133) ; 0217: c33301
L_021A:
    CP 0x02 ; 021A: fe02
    JR Z, L_0229 ; 021C: 280b
    DEC IX ; 021E: dd2b
    DEC IX ; 0220: dd2b
    LD A, IXH ; 0222: dd7c
    BIT 6, A ; 0224: cb77
    JP NZ, R(0x0133) ; 0226: c23301
L_0229:
    LD A, (R(0x000F)) ; 0229: 3a0f00
    OR A ; 022C: b7
    JR NZ, L_023F ; 022D: 2010
    LD HL, (R(0x0007)) ; 022F: 2a0700
    DEC HL ; 0232: 2b
    ADD HL, HL ; 0233: 29
    LD DE, (R(0x0003)) ; 0234: ed5b0300
    ADD HL, DE ; 0238: 19
    PUSH HL ; 0239: e5
    POP IX ; 023A: dde1
    JP R(0x0133) ; 023C: c33301
L_023F:
    PUSH DE ; 023F: d5
    PUSH HL ; 0240: e5
    PUSH IY ; 0241: fde5
    POP HL ; 0243: e1
    CALL R(0x06F6) ; 0244: cdf606
    POP HL ; 0247: e1
    POP DE ; 0248: d1
    JP R(0x0133) ; 0249: c33301
L_024C:
    LD A, (R(0x000F)) ; 024C: 3a0f00
    OR A ; 024F: b7
    JR NZ, L_0258 ; 0250: 2006
    LD IX, (R(0x0003)) ; 0252: dd2a0300
    JR L_025E ; 0256: 1806
L_0258:
    LD HL, 0x0000 ; 0258: 210000
    CALL R(0x06F6) ; 025B: cdf606
L_025E:
    LD E, (IX+0) ; 025E: dd5e00
    LD D, (IX+1) ; 0261: dd5601
    CALL R(0x0358) ; 0264: cd5803
    LD BC, (R(0x0430)) ; 0267: ed4b3004
    ADD HL, BC ; 026B: 09
    EX DE, HL ; 026C: eb
    LD BC, (R(0x0432)) ; 026D: ed4b3204
    ADC HL, BC ; 0271: ed4a
    EX DE, HL ; 0273: eb
    LD BC, 0x2710 ; 0274: 011027
    CALL R(0x02C3) ; 0277: cdc302
    LD (IX+0), C ; 027A: dd7100
    LD (IX+1), B ; 027D: dd7001
    CALL R(0x05D4) ; 0280: cdd405
    LD A, 0x02 ; 0283: 3e02
    LD (0xF663), A ; 0285: 3263f6
L_0288:
    DI ; 0288: f3
    LD A, (R(0x03F6)) ; 0289: 3af603
    OR A ; 028C: b7
    JR Z, L_029E ; 028D: 280f
    LD HL, (R(0x0007)) ; 028F: 2a0700
    INC HL ; 0292: 23
    LD A, H ; 0293: 7c
    OR L ; 0294: b5
    JR Z, L_029E ; 0295: 2807
    XOR A ; 0297: af
    OUT (0x99), A ; 0298: d399 [VDP reg/addr]
    LD A, 0x8E ; 029A: 3e8e
    OUT (0x99), A ; 029C: d399 [VDP reg/addr]
L_029E:
    LD A, (R(0x000F)) ; 029E: 3a0f00
    OR A ; 02A1: b7
    JR Z, L_02A7 ; 02A2: 2803
    CALL R(0x07BC) ; 02A4: cdbc07
L_02A7:
    POP IY ; 02A7: fde1
    POP IX ; 02A9: dde1
    POP HL ; 02AB: e1
    POP DE ; 02AC: d1
    POP BC ; 02AD: c1
    POP AF ; 02AE: f1
    LD HL, 0xF7F8 ; 02AF: 21f8f7 [BASIC USR arg/ret]
    EI ; 02B2: fb
    RET ; 02B3: c9
; VRAM spill array read/write dispatch (dispatches to rev_pgt_spill when T3=0 & V=0)
L_02B4:
    LD H, B ; 02B4: 60
    LD L, C ; 02B5: 69
    ADD HL, HL ; 02B6: 29
    ADD HL, HL ; 02B7: 29
    ADD HL, HL ; 02B8: 29
    ADD HL, HL ; 02B9: 29
    OR A ; 02BA: b7
    SBC HL, BC ; 02BB: ed42
    OR A ; 02BD: b7
    SBC HL, BC ; 02BE: ed42
    LD B, H ; 02C0: 44
    LD C, L ; 02C1: 4d
    RET ; 02C2: c9
L_02C3:
    PUSH BC ; 02C3: c5
    EXX ; 02C4: d9
    POP BC ; 02C5: c1
    LD HL, 0x0000 ; 02C6: 210000
    EXX ; 02C9: d9
    LD A, D ; 02CA: 7a
    OR A ; 02CB: b7
    JR NZ, L_02D6 ; 02CC: 2008
    LD D, E ; 02CE: 53
    LD E, H ; 02CF: 5c
    LD H, L ; 02D0: 65
    LD L, A ; 02D1: 6f
    LD A, 0x18 ; 02D2: 3e18
    JR L_02D8 ; 02D4: 1802
L_02D6:
    LD A, 0x20 ; 02D6: 3e20
L_02D8:
    ADD HL, HL ; 02D8: 29
    RL E ; 02D9: cb13
    RL D ; 02DB: cb12
    EXX ; 02DD: d9
    ADC HL, HL ; 02DE: ed6a
    JR C, L_02EE ; 02E0: 380c
    OR A ; 02E2: b7
    SBC HL, BC ; 02E3: ed42
    JR NC, L_02F1 ; 02E5: 300a
    ADD HL, BC ; 02E7: 09
    EXX ; 02E8: d9
    DEC A ; 02E9: 3d
    JR NZ, L_02D8 ; 02EA: 20ec
    JR L_02F6 ; 02EC: 1808
L_02EE:
    OR A ; 02EE: b7
    SBC HL, BC ; 02EF: ed42
L_02F1:
    EXX ; 02F1: d9
    INC L ; 02F2: 2c
    DEC A ; 02F3: 3d
    JR NZ, L_02D8 ; 02F4: 20e2
L_02F6:
    EXX ; 02F6: d9
    PUSH HL ; 02F7: e5
    EXX ; 02F8: d9
    POP BC ; 02F9: c1
    RET ; 02FA: c9
; div_step / mul_qk: uses R800 MULUW HL,BC if (A!+16)!=0, else Z80 shift-add
L_02FB:
    LD A, D ; 02FB: 7a
    OR E ; 02FC: b3
    JR NZ, L_0327 ; 02FD: 2028
    LD A, (R(0x0010)) ; 02FF: 3a1000
    OR A ; 0302: b7
    JR Z, L_0308 ; 0303: 2803
    MULUW HL, BC ; 0305: edc3 [R800 16x16->32 hardware mul]
    RET ; 0307: c9
L_0308:
    PUSH BC ; 0308: c5
    EXX ; 0309: d9
    POP HL ; 030A: e1
    EXX ; 030B: d9
    LD B, H ; 030C: 44
    LD C, L ; 030D: 4d
    LD HL, 0x0000 ; 030E: 210000
    LD D, H ; 0311: 54
    LD E, L ; 0312: 5d
    LD A, 0x10 ; 0313: 3e10
L_0315:
    ADD HL, HL ; 0315: 29
    RL E ; 0316: cb13
    RL D ; 0318: cb12
    EXX ; 031A: d9
    ADD HL, HL ; 031B: 29
    EXX ; 031C: d9
    JR NC, L_0323 ; 031D: 3004
    ADD HL, BC ; 031F: 09
    JR NC, L_0323 ; 0320: 3001
    INC DE ; 0322: 13
L_0323:
    DEC A ; 0323: 3d
    JR NZ, L_0315 ; 0324: 20ef
    RET ; 0326: c9
L_0327:
    PUSH IX ; 0327: dde5
    LD (R(0x0430)), DE ; 0329: ed533004
    PUSH BC ; 032D: c5
    PUSH HL ; 032E: e5
    POP BC ; 032F: c1
    POP HL ; 0330: e1
    LD IX, 0x0000 ; 0331: dd210000
    LD DE, 0x0000 ; 0335: 110000
    LD A, 0x10 ; 0338: 3e10
L_033A:
    ADD IX, IX ; 033A: dd29
    RL E ; 033C: cb13
    RL D ; 033E: cb12
    ADD HL, HL ; 0340: 29
    JR NC, L_034F ; 0341: 300c
    ADD IX, BC ; 0343: dd09
    EX DE, HL ; 0345: eb
    PUSH BC ; 0346: c5
    LD BC, (R(0x0430)) ; 0347: ed4b3004
    ADC HL, BC ; 034B: ed4a
    POP BC ; 034D: c1
    EX DE, HL ; 034E: eb
L_034F:
    DEC A ; 034F: 3d
    JR NZ, L_033A ; 0350: 20e8
    PUSH IX ; 0352: dde5
    POP HL ; 0354: e1
    POP IX ; 0355: dde1
    RET ; 0357: c9
; mul_10000: DE * 10000 -> DE:HL (R800 MULUW if (A!+16)!=0, else unrolled Z80)
L_0358:
    LD A, (R(0x0010)) ; 0358: 3a1000
    OR A ; 035B: b7
    JR Z, L_0366 ; 035C: 2808
    LD HL, 0x2710 ; 035E: 211027
    LD B, D ; 0361: 42
    LD C, E ; 0362: 4b
    MULUW HL, BC ; 0363: edc3 [R800 16x16->32 hardware mul]
    RET ; 0365: c9
L_0366:
    LD B, D ; 0366: 42
    LD C, E ; 0367: 4b
    LD H, D ; 0368: 62
    LD L, E ; 0369: 6b
    LD DE, 0x0000 ; 036A: 110000
    ADD HL, HL ; 036D: 29
    RL E ; 036E: cb13
    ADD HL, HL ; 0370: 29
    RL E ; 0371: cb13
    ADD HL, HL ; 0373: 29
    RL E ; 0374: cb13
    ADD HL, BC ; 0376: 09
    JR NC, L_037A ; 0377: 3001
    INC DE ; 0379: 13
L_037A:
    ADD HL, HL ; 037A: 29
    RL E ; 037B: cb13
    ADD HL, BC ; 037D: 09
    JR NC, L_0381 ; 037E: 3001
    INC DE ; 0380: 13
L_0381:
    ADD HL, HL ; 0381: 29
    RL E ; 0382: cb13
    ADD HL, BC ; 0384: 09
    JR NC, L_0388 ; 0385: 3001
    INC DE ; 0387: 13
L_0388:
    ADD HL, HL ; 0388: 29
    RL E ; 0389: cb13
    RL D ; 038B: cb12
    ADD HL, HL ; 038D: 29
    RL E ; 038E: cb13
    RL D ; 0390: cb12
    ADD HL, HL ; 0392: 29
    RL E ; 0393: cb13
    RL D ; 0395: cb12
    ADD HL, HL ; 0397: 29
    RL E ; 0398: cb13
    RL D ; 039A: cb12
    ADD HL, BC ; 039C: 09
    JR NC, L_03A0 ; 039D: 3001
    INC DE ; 039F: 13
L_03A0:
    ADD HL, HL ; 03A0: 29
    RL E ; 03A1: cb13
    RL D ; 03A3: cb12
    ADD HL, HL ; 03A5: 29
    RL E ; 03A6: cb13
    RL D ; 03A8: cb12
    ADD HL, HL ; 03AA: 29
    RL E ; 03AB: cb13
    RL D ; 03AD: cb12
    ADD HL, HL ; 03AF: 29
    RL E ; 03B0: cb13
    RL D ; 03B2: cb12
    RET ; 03B4: c9
L_03B5:
    OR A ; 03B5: b7
    LD DE, (R(0x0007)) ; 03B6: ed5b0700
    SBC HL, DE ; 03BA: ed52
    LD A, (R(0x03F6)) ; 03BC: 3af603
    OR A ; 03BF: b7
    JR NZ, L_03E1 ; 03C0: 201f
    LD DE, 0x027E ; 03C2: 117e02
    OR A ; 03C5: b7
    SBC HL, DE ; 03C6: ed52
    JR C, L_03D5 ; 03C8: 380b
    LD A, H ; 03CA: 7c
    SUB 0x04 ; 03CB: d604
    JR C, L_03DA ; 03CD: 380b
    LD H, A ; 03CF: 67
    JP R(0x05AB) ; 03D0: c3ab05
    NOP ; 03D3: 00
    NOP ; 03D4: 00
L_03D5:
    LD DE, 0x2000 ; 03D5: 110020
    JR L_03DD ; 03D8: 1803
L_03DA:
    LD DE, 0x3800 ; 03DA: 110038
L_03DD:
    ADD HL, HL ; 03DD: 29
    ADD HL, DE ; 03DE: 19
    EX DE, HL ; 03DF: eb
    RET ; 03E0: c9
L_03E1:
    LD A, H ; 03E1: 7c
    RLCA ; 03E2: 07
    RLCA ; 03E3: 07
    RLCA ; 03E4: 07
    AND 0x03 ; 03E5: e603
    OR 0x04 ; 03E7: f604
    OUT (0x99), A ; 03E9: d399 [VDP reg/addr]
    LD A, 0x8E ; 03EB: 3e8e
    OUT (0x99), A ; 03ED: d399 [VDP reg/addr]
    LD A, H ; 03EF: 7c
    AND 0x1F ; 03F0: e61f
    LD H, A ; 03F2: 67
    ADD HL, HL ; 03F3: 29
    EX DE, HL ; 03F4: eb
    RET ; 03F5: c9
L_03F6:
    NOP ; 03F6: 00
L_03F7:
    PUSH HL ; 03F7: e5
    DI ; 03F8: f3
    CALL R(0x03B5) ; 03F9: cdb503
    LD A, E ; 03FC: 7b
    OUT (0x99), A ; 03FD: d399 [VDP reg/addr]
    LD A, D ; 03FF: 7a
    AND 0x3F ; 0400: e63f
    OUT (0x99), A ; 0402: d399 [VDP reg/addr]
    EX (SP), HL ; 0404: e3
    EX (SP), HL ; 0405: e3
    IN A, (0x98) ; 0406: db98 [VDP VRAM data]
    LD E, A ; 0408: 5f
    EX (SP), HL ; 0409: e3
    EX (SP), HL ; 040A: e3
    IN A, (0x98) ; 040B: db98 [VDP VRAM data]
    LD D, A ; 040D: 57
    EI ; 040E: fb
    POP HL ; 040F: e1
    RET ; 0410: c9
L_0411:
    PUSH HL ; 0411: e5
    DI ; 0412: f3
    CALL R(0x03B5) ; 0413: cdb503
    LD A, E ; 0416: 7b
    OUT (0x99), A ; 0417: d399 [VDP reg/addr]
    LD A, D ; 0419: 7a
    OR 0x40 ; 041A: f640
    OUT (0x99), A ; 041C: d399 [VDP reg/addr]
    PUSH HL ; 041E: e5
    POP HL ; 041F: e1
    LD A, C ; 0420: 79
    OUT (0x98), A ; 0421: d398 [VDP VRAM data]
    EX (SP), HL ; 0423: e3
    EX (SP), HL ; 0424: e3
    LD A, B ; 0425: 78
    OUT (0x98), A ; 0426: d398 [VDP VRAM data]
    EI ; 0428: fb
    POP HL ; 0429: e1
    RET ; 042A: c9
L_042B:
    OUT (0x99), A ; 042B: d399 [VDP reg/addr]
    PUSH HL ; 042D: e5
    POP HL ; 042E: e1
    RET ; 042F: c9
L_0430:
    NOP ; 0430: 00
    NOP ; 0431: 00
L_0432:
    NOP ; 0432: 00
    NOP ; 0433: 00
L_0434:
    LD A, L ; 0434: 7d
    OUT (0x99), A ; 0435: d399 [VDP reg/addr]
    LD A, H ; 0437: 7c
    OR 0x40 ; 0438: f640
    JR L_042B ; 043A: 18ef
    NOP ; 043C: 00
; K! (A!+1085): Render 4-digit group T1 to VRAM (jumps to 2309 on V>=1; 0x0475 LD E,A tail mask)
    PUSH AF ; 043D: f5
    PUSH BC ; 043E: c5
    PUSH DE ; 043F: d5
    PUSH HL ; 0440: e5
    PUSH IX ; 0441: dde5
    LD HL, (0xF7F8) ; 0443: 2af8f7 [BASIC USR arg/ret]
    LD IX, R(0x0568) ; 0446: dd216805
    LD DE, 0x03E8 ; 044A: 11e803
    CALL R(0x0552) ; 044D: cd5205
    LD DE, 0x0064 ; 0450: 116400
    CALL R(0x0552) ; 0453: cd5205
    LD DE, 0x000A ; 0456: 110a00
    CALL R(0x0552) ; 0459: cd5205
    LD (IX+0), L ; 045C: dd7500
    LD HL, (R(0x000B)) ; 045F: 2a0b00
    LD DE, (R(0x000D)) ; 0462: ed5b0d00
    OR A ; 0466: b7
    SBC HL, DE ; 0467: ed52
    LD A, H ; 0469: 7c
    OR A ; 046A: b7
    JR NZ, L_0482 ; 046B: 2015
    LD A, L ; 046D: 7d
    CP 0x04 ; 046E: fe04
    JR NC, L_0482 ; 0470: 3010
    LD HL, R(0x0568) ; 0472: 216805
    LD E, A ; 0475: 5f
    LD D, 0x00 ; 0476: 1600
    ADD HL, DE ; 0478: 19
    LD A, 0x04 ; 0479: 3e04
    SUB E ; 047B: 93
    LD B, A ; 047C: 47
L_047D:
    LD (HL), 0x0A ; 047D: 360a
    INC HL ; 047F: 23
    DJNZ L_047D ; 0480: 10fb
L_0482:
    LD A, (R(0x0563)) ; 0482: 3a6305
    OR A ; 0485: b7
    JP NZ, R(0x0905) ; 0486: c20509
    LD DE, R(0x0574) ; 0489: 117405
    LD C, 0x00 ; 048C: 0e00
L_048E:
    PUSH BC ; 048E: c5
    PUSH DE ; 048F: d5
    CALL R(0x0528) ; 0490: cd2805
    LD HL, (R(0x0565)) ; 0493: 2a6505
    LD A, L ; 0496: 7d
    ADD A, C ; 0497: 81
    LD L, A ; 0498: 6f
    JR NC, L_049C ; 0499: 3001
    INC H ; 049B: 24
L_049C:
    LD A, L ; 049C: 7d
    AND 0x07 ; 049D: e607
    LD B, A ; 049F: 47
    LD A, L ; 04A0: 7d
    AND 0xF8 ; 04A1: e6f8
    RRCA ; 04A3: 0f
    RRCA ; 04A4: 0f
    RRCA ; 04A5: 0f
    LD H, A ; 04A6: 67
    LD A, (R(0x0564)) ; 04A7: 3a6405
    AND 0xFE ; 04AA: e6fe
    RLCA ; 04AC: 07
    RLCA ; 04AD: 07
    OR B ; 04AE: b0
    LD L, A ; 04AF: 6f
    PUSH HL ; 04B0: e5
    LD HL, R(0x056C) ; 04B1: 216c05
    LD A, (HL) ; 04B4: 7e
    RLCA ; 04B5: 07
    RLCA ; 04B6: 07
    RLCA ; 04B7: 07
    RLCA ; 04B8: 07
    INC HL ; 04B9: 23
    OR (HL) ; 04BA: b6
    LD C, A ; 04BB: 4f
    INC HL ; 04BC: 23
    LD A, (HL) ; 04BD: 7e
    RLCA ; 04BE: 07
    RLCA ; 04BF: 07
    RLCA ; 04C0: 07
    RLCA ; 04C1: 07
    INC HL ; 04C2: 23
    OR (HL) ; 04C3: b6
    LD B, A ; 04C4: 47
    POP HL ; 04C5: e1
    DI ; 04C6: f3
    CALL R(0x0434) ; 04C7: cd3404
    LD A, C ; 04CA: 79
    OUT (0x98), A ; 04CB: d398 [VDP VRAM data]
    LD DE, 0x0008 ; 04CD: 110800
    ADD HL, DE ; 04D0: 19
    CALL R(0x0623) ; 04D1: cd2306
    EI ; 04D4: fb
    NOP ; 04D5: 00
    NOP ; 04D6: 00
    NOP ; 04D7: 00
    POP DE ; 04D8: d1
    POP BC ; 04D9: c1
    LD HL, 0x000B ; 04DA: 210b00
    ADD HL, DE ; 04DD: 19
    EX DE, HL ; 04DE: eb
    INC C ; 04DF: 0c
    LD A, C ; 04E0: 79
    CP 0x05 ; 04E1: fe05
    JR NZ, L_048E ; 04E3: 20a9
    LD HL, (R(0x000D)) ; 04E5: 2a0d00
    LD DE, 0x0004 ; 04E8: 110400
    ADD HL, DE ; 04EB: 19
    LD DE, (R(0x000B)) ; 04EC: ed5b0b00
    OR A ; 04F0: b7
    SBC HL, DE ; 04F1: ed52
    ADD HL, DE ; 04F3: 19
    JR C, L_04F7 ; 04F4: 3801
    EX DE, HL ; 04F6: eb
L_04F7:
    LD (R(0x000D)), HL ; 04F7: 220d00
    LD A, (R(0x0563)) ; 04FA: 3a6305
    CP 0x02 ; 04FD: fe02
    LD B, 0x40 ; 04FF: 0640
    JR C, L_0505 ; 0501: 3802
    LD B, 0x80 ; 0503: 0680
L_0505:
    LD A, (R(0x0564)) ; 0505: 3a6405
    ADD A, 0x04 ; 0508: c604
    CP B ; 050A: b8
    JR C, L_0518 ; 050B: 380b
    XOR A ; 050D: af
    LD HL, (R(0x0565)) ; 050E: 2a6505
    LD DE, 0x0005 ; 0511: 110500
    ADD HL, DE ; 0514: 19
    LD (R(0x0565)), HL ; 0515: 226505
L_0518:
    LD (R(0x0564)), A ; 0518: 326405
    LD HL, 0x0000 ; 051B: 210000
    LD (0xF7F8), HL ; 051E: 22f8f7 [BASIC USR arg/ret]
    POP IX ; 0521: dde1
    POP HL ; 0523: e1
    POP DE ; 0524: d1
    POP BC ; 0525: c1
    POP AF ; 0526: f1
    RET ; 0527: c9
L_0528:
    LD B, 0x04 ; 0528: 0604
    LD IX, R(0x0568) ; 052A: dd216805
    LD HL, R(0x056C) ; 052E: 216c05
L_0531:
    PUSH HL ; 0531: e5
    LD L, (IX+0) ; 0532: dd6e00
    LD H, 0x00 ; 0535: 2600
    ADD HL, DE ; 0537: 19
    LD A, (HL) ; 0538: 7e
    POP HL ; 0539: e1
    LD (HL), A ; 053A: 77
    INC HL ; 053B: 23
    INC IX ; 053C: dd23
    DJNZ L_0531 ; 053E: 10f1
    LD A, C ; 0540: 79
    CP 0x04 ; 0541: fe04
    RET NZ ; 0543: c0
    LD HL, (R(0x000D)) ; 0544: 2a0d00
    LD A, H ; 0547: 7c
    OR L ; 0548: b5
    RET NZ ; 0549: c0
    LD HL, R(0x056C) ; 054A: 216c05
    LD A, (HL) ; 054D: 7e
    OR 0x01 ; 054E: f601
    LD (HL), A ; 0550: 77
    RET ; 0551: c9
L_0552:
    LD B, 0x00 ; 0552: 0600
L_0554:
    OR A ; 0554: b7
    SBC HL, DE ; 0555: ed52
    JR C, L_055C ; 0557: 3803
    INC B ; 0559: 04
    JR L_0554 ; 055A: 18f8
L_055C:
    ADD HL, DE ; 055C: 19
    LD (IX+0), B ; 055D: dd7000
    INC IX ; 0560: dd23
    RET ; 0562: c9
; K! / VDP state vars (17 bytes): 1379=mode_t4, 1380=vdp_latch, 1381=char_cnt, 1383=pgt_flag, 1388=tile_buf[8]
L_0563:
    DB 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ; 0563
    DB 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ; 056B
    DB 0x00, 0x04, 0x04, 0x0C, 0x0C, 0x0A, 0x0E, 0x06 ; 0573
    DB 0x0E, 0x04, 0x04, 0x00, 0x0A, 0x0C, 0x02, 0x02 ; 057B
    DB 0x0A, 0x08, 0x08, 0x02, 0x0A, 0x0A, 0x00, 0x0A ; 0583
    DB 0x04, 0x04, 0x04, 0x0E, 0x0C, 0x0C, 0x04, 0x04 ; 058B
    DB 0x06, 0x00, 0x0A, 0x04, 0x08, 0x02, 0x02, 0x02 ; 0593
    DB 0x0A, 0x04, 0x0A, 0x02, 0x00, 0x04, 0x04, 0x0E ; 059B
    DB 0x0C, 0x02, 0x0C, 0x04, 0x04, 0x04, 0x0C, 0x00 ; 05A3
; rev_pgt_spill (1451): reverses 16K VRAM PGT spill address (0x17FE down to 0x0000)
L_05AB:
    ADD HL, HL ; 05AB: 29
    EX DE, HL ; 05AC: eb
    LD HL, 0x17FE ; 05AD: 21fe17
    OR A ; 05B0: b7
    SBC HL, DE ; 05B1: ed52
    EX DE, HL ; 05B3: eb
    RET ; 05B4: c9
; y_to_inv (1461): maps linear Y row to inverse SCREEN 2 bank/char offset
L_05B5:
    PUSH BC ; 05B5: c5
    LD A, H ; 05B6: 7c
    AND 0x1F ; 05B7: e61f
    RLCA ; 05B9: 07
    RLCA ; 05BA: 07
    RLCA ; 05BB: 07
    LD B, A ; 05BC: 47
    LD A, L ; 05BD: 7d
    AND 0x07 ; 05BE: e607
    OR B ; 05C0: b0
    JR Z, L_05D0 ; 05C1: 280d
    DEC A ; 05C3: 3d
L_05C4:
    SUB 0x0A ; 05C4: d60a
    JR NC, L_05C4 ; 05C6: 30fc
    ADD A, 0x05 ; 05C8: c605
    JR C, L_05D0 ; 05CA: 3804
    LD A, 0xFF ; 05CC: 3eff
    POP BC ; 05CE: c1
    RET ; 05CF: c9
L_05D0:
    LD A, 0x33 ; 05D0: 3e33
    POP BC ; 05D2: c1
    RET ; 05D3: c9
; retire_ct (1492): sweeps SCREEN 2 CT from muted (0x23/0xEF) to invisible/crisp (0x33/0xFF)
L_05D4:
    LD BC, (0xF7F8) ; 05D4: ed4bf8f7 [BASIC USR arg/ret]
    LD (0xF7F8), HL ; 05D8: 22f8f7 [BASIC USR arg/ret]
    LD A, (R(0x03F6)) ; 05DB: 3af603
    OR A ; 05DE: b7
    RET NZ ; 05DF: c0
    LD A, (R(0x0567)) ; 05E0: 3a6705
    OR A ; 05E3: b7
    RET Z ; 05E4: c8
    CALL R(0x02B4) ; 05E5: cdb402
    LD HL, (R(0x0007)) ; 05E8: 2a0700
    LD DE, 0x067E ; 05EB: 117e06
    ADD HL, DE ; 05EE: 19
    RET C ; 05EF: d8
    EX DE, HL ; 05F0: eb
    LD H, B ; 05F1: 60
    LD L, C ; 05F2: 69
    DEC HL ; 05F3: 2b
    LD B, 0x0E ; 05F4: 060e
L_05F6:
    PUSH HL ; 05F6: e5
    OR A ; 05F7: b7
    SBC HL, DE ; 05F8: ed52
    JR NC, L_05FE ; 05FA: 3002
    POP HL ; 05FC: e1
    RET ; 05FD: c9
L_05FE:
    ADD HL, HL ; 05FE: 29
    PUSH DE ; 05FF: d5
    EX DE, HL ; 0600: eb
    LD HL, 0x37FE ; 0601: 21fe37
    SBC HL, DE ; 0604: ed52
    CALL R(0x05B5) ; 0606: cdb505
    LD C, A ; 0609: 4f
    INC L ; 060A: 2c
    CALL R(0x05B5) ; 060B: cdb505
    LD E, A ; 060E: 5f
    DEC L ; 060F: 2d
    DI ; 0610: f3
    CALL R(0x0434) ; 0611: cd3404
    LD A, C ; 0614: 79
    OUT (0x98), A ; 0615: d398 [VDP VRAM data]
    EX (SP), HL ; 0617: e3
    EX (SP), HL ; 0618: e3
    LD A, E ; 0619: 7b
    OUT (0x98), A ; 061A: d398 [VDP VRAM data]
    EI ; 061C: fb
    POP DE ; 061D: d1
    POP HL ; 061E: e1
    DEC HL ; 061F: 2b
    DJNZ L_05F6 ; 0620: 10d4
    RET ; 0622: c9
; k_ct_update (1571): sets printed-digit CT bytes (0x13/0x6F)
L_0623:
    CALL R(0x0434) ; 0623: cd3404
    LD A, B ; 0626: 78
    OUT (0x98), A ; 0627: d398 [VDP VRAM data]
    LD A, (R(0x0567)) ; 0629: 3a6705
    OR A ; 062C: b7
    RET Z ; 062D: c8
    LD A, (R(0x0565)) ; 062E: 3a6505
    RRA ; 0631: 1f
    LD A, 0x13 ; 0632: 3e13
    JR NC, L_0638 ; 0634: 3002
    LD A, 0x6F ; 0636: 3e6f
L_0638:
    LD C, A ; 0638: 4f
    SET 5, H ; 0639: cbec
    CALL R(0x0434) ; 063B: cd3404
    LD A, C ; 063E: 79
    OUT (0x98), A ; 063F: d398 [VDP VRAM data]
    RES 3, L ; 0641: cb9d
    CALL R(0x0434) ; 0643: cd3404
    LD A, C ; 0646: 79
    OUT (0x98), A ; 0647: d398 [VDP VRAM data]
    RET ; 0649: c9
; J! (A!+1610): GFX init (jumps to 2189 on V>=1; SCREEN 2 PNT/CT/PGT setup on V=0)
    PUSH AF ; 064A: f5
    PUSH BC ; 064B: c5
    PUSH DE ; 064C: d5
    PUSH HL ; 064D: e5
    LD A, (0xF7F8) ; 064E: 3af8f7 [BASIC USR arg/ret]
    LD B, A ; 0651: 47
    AND 0x03 ; 0652: e603
    LD (R(0x0563)), A ; 0654: 326305
    LD A, B ; 0657: 78
    AND 0x04 ; 0658: e604
    LD (R(0x0567)), A ; 065A: 326705
    LD HL, 0x0000 ; 065D: 210000
    LD (R(0x000D)), HL ; 0660: 220d00
    XOR A ; 0663: af
    LD (R(0x0564)), A ; 0664: 326405
    LD A, (R(0x0563)) ; 0667: 3a6305
    CP 0x03 ; 066A: fe03
    LD HL, 0x0001 ; 066C: 210100
    JR NZ, L_0672 ; 066F: 2001
    INC HL ; 0671: 23
L_0672:
    LD (R(0x0565)), HL ; 0672: 226505
    OR A ; 0675: b7
    JP NZ, R(0x088D) ; 0676: c28d08
    DI ; 0679: f3
    LD HL, 0x1B00 ; 067A: 21001b
    CALL R(0x0434) ; 067D: cd3404
    LD A, 0xD0 ; 0680: 3ed0
    OUT (0x98), A ; 0682: d398 [VDP VRAM data]
    EI ; 0684: fb
    LD DE, 0x1301 ; 0685: 110113
    LD A, (R(0x0567)) ; 0688: 3a6705
    OR A ; 068B: b7
    JR Z, L_0690 ; 068C: 2802
    LD D, 0x23 ; 068E: 1623
L_0690:
    LD C, 0x18 ; 0690: 0e18
    LD HL, 0x2000 ; 0692: 210020
L_0695:
    PUSH BC ; 0695: c5
    PUSH HL ; 0696: e5
    LD HL, R(0x056C) ; 0697: 216c05
    LD B, 0x08 ; 069A: 0608
L_069C:
    LD (HL), D ; 069C: 72
    INC HL ; 069D: 23
    DEC E ; 069E: 1d
    JR NZ, L_06AF ; 069F: 200e
    LD E, 0x05 ; 06A1: 1e05
    LD A, (R(0x0567)) ; 06A3: 3a6705
    OR A ; 06A6: b7
    LD A, 0x7C ; 06A7: 3e7c
    JR Z, L_06AD ; 06A9: 2802
    LD A, 0xCC ; 06AB: 3ecc
L_06AD:
    XOR D ; 06AD: aa
    LD D, A ; 06AE: 57
L_06AF:
    DJNZ L_069C ; 06AF: 10eb
    POP HL ; 06B1: e1
    POP BC ; 06B2: c1
    DI ; 06B3: f3
    CALL R(0x0434) ; 06B4: cd3404
    PUSH HL ; 06B7: e5
    PUSH DE ; 06B8: d5
    LD E, 0x20 ; 06B9: 1e20
L_06BB:
    LD HL, R(0x056C) ; 06BB: 216c05
    LD B, 0x08 ; 06BE: 0608
L_06C0:
    LD A, (HL) ; 06C0: 7e
    OUT (0x98), A ; 06C1: d398 [VDP VRAM data]
    INC HL ; 06C3: 23
    DJNZ L_06C0 ; 06C4: 10fa
    DEC E ; 06C6: 1d
    JR NZ, L_06BB ; 06C7: 20f2
    POP DE ; 06C9: d1
    POP HL ; 06CA: e1
    EI ; 06CB: fb
    INC H ; 06CC: 24
    DEC C ; 06CD: 0d
    JR NZ, L_0695 ; 06CE: 20c5
; J!_exit (1744): clears USR return arg & restores regs
    LD HL, 0x0000 ; 06D0: 210000
    LD (0xF7F8), HL ; 06D3: 22f8f7 [BASIC USR arg/ret]
    POP HL ; 06D6: e1
    POP DE ; 06D7: d1
    POP BC ; 06D8: c1
    POP AF ; 06D9: f1
    RET ; 06DA: c9
; spd_loop (A!+1755): 27-byte CPU speed calibrator over 20 VDP frames
    DI ; 06DB: f3
    IN A, (0x99) ; 06DC: db99 [VDP reg/addr]
L_06DE:
    IN A, (0x99) ; 06DE: db99 [VDP reg/addr]
    RLCA ; 06E0: 07
    JR NC, L_06DE ; 06E1: 30fb
    LD DE, 0x0000 ; 06E3: 110000
L_06E6:
    LD B, 0x14 ; 06E6: 0614
L_06E8:
    DJNZ L_06E8 ; 06E8: 10fe
    INC DE ; 06EA: 13
    IN A, (0x99) ; 06EB: db99 [VDP reg/addr]
    RLCA ; 06ED: 07
    JR NC, L_06E6 ; 06EE: 30f6
    LD (0xF7F8), DE ; 06F0: ed53f8f7 [BASIC USR arg/ret]
    EI ; 06F4: fb
    RET ; 06F5: c9
```

## `s2.asm` (407 B code + 31 B reloc = 438 B)

```asm
ORG 0x06F6
; === s2: Multi-Slot / Mapper Array Access + s2_helper (at A!+1782) ===
    PUSH DE ; 06F6: d5
    PUSH BC ; 06F7: c5
    OR A ; 06F8: b7
    LD DE, (R(0x0005)) ; 06F9: ed5b0500
    SBC HL, DE ; 06FD: ed52
    JR NC, L_070E ; 06FF: 300d
    ADD HL, DE ; 0701: 19
    ADD HL, HL ; 0702: 29
    LD DE, (R(0x0003)) ; 0703: ed5b0300
    ADD HL, DE ; 0707: 19
    PUSH HL ; 0708: e5
    POP IX ; 0709: dde1
    POP BC ; 070B: c1
    POP DE ; 070C: d1
    RET ; 070D: c9
L_070E:
    LD A, (R(0x000F)) ; 070E: 3a0f00
    CP 0x01 ; 0711: fe01
    JR Z, L_0739 ; 0713: 2824
    LD A, H ; 0715: 7c
    RLCA ; 0716: 07
    RLCA ; 0717: 07
    RLCA ; 0718: 07
    AND 0x03 ; 0719: e603
    LD E, A ; 071B: 5f
    LD D, 0x00 ; 071C: 1600
    PUSH HL ; 071E: e5
    LD HL, R(0x0861) ; 071F: 216108
    ADD HL, DE ; 0722: 19
    LD B, (HL) ; 0723: 46
    POP HL ; 0724: e1
    LD A, H ; 0725: 7c
    AND 0x1F ; 0726: e61f
    LD H, A ; 0728: 67
    ADD HL, HL ; 0729: 29
    LD C, 0x00 ; 072A: 0e00
    LD A, B ; 072C: 78
    OR A ; 072D: b7
    JR NZ, L_0732 ; 072E: 2002
    LD C, 0x80 ; 0730: 0e80
L_0732:
    ADD HL, BC ; 0732: 09
    PUSH HL ; 0733: e5
    POP IX ; 0734: dde1
    POP BC ; 0736: c1
    POP DE ; 0737: d1
    RET ; 0738: c9
L_0739:
    PUSH HL ; 0739: e5
    LD A, H ; 073A: 7c
    RLCA ; 073B: 07
    RLCA ; 073C: 07
    RLCA ; 073D: 07
    AND 0x07 ; 073E: e607
    LD E, A ; 0740: 5f
    LD D, 0x00 ; 0741: 1600
    LD HL, R(0x0857) ; 0743: 215708
    ADD HL, DE ; 0746: 19
    LD A, (HL) ; 0747: 7e
    CALL R(0x075B) ; 0748: cd5b07
    POP HL ; 074B: e1
    LD A, H ; 074C: 7c
    AND 0x1F ; 074D: e61f
    LD H, A ; 074F: 67
    ADD HL, HL ; 0750: 29
    LD BC, 0x4000 ; 0751: 010040
    ADD HL, BC ; 0754: 09
    PUSH HL ; 0755: e5
    POP IX ; 0756: dde1
    POP BC ; 0758: c1
    POP DE ; 0759: d1
    RET ; 075A: c9
L_075B:
    OUT (0xFD), A ; 075B: d3fd [Mapper page 1]
    RET ; 075D: c9
    IN A, (0xA8) ; 075E: dba8 [PPI slot select]
    LD (R(0x084F)), A ; 0760: 324f08
    LD A, (R(0x085D)) ; 0763: 3a5d08
    BIT 7, A ; 0766: cb7f
    JR Z, L_0778 ; 0768: 280e
    AND 0x03 ; 076A: e603
    LD HL, 0xFCC5 ; 076C: 21c5fc [SLTTBL]
    ADD A, L ; 076F: 85
    LD L, A ; 0770: 6f
    JR NC, L_0774 ; 0771: 3001
    INC H ; 0773: 24
L_0774:
    LD A, (HL) ; 0774: 7e
    LD (R(0x0850)), A ; 0775: 325008
L_0778:
    LD A, (R(0x0866)) ; 0778: 3a6608
    CP 0xFF ; 077B: feff
    JR Z, L_0785 ; 077D: 2806
    LD H, 0x80 ; 077F: 2680
    CALL 0x0024 ; 0781: cd2400 [BIOS ENASLT]
    DI ; 0784: f3
L_0785:
    LD A, (R(0x0865)) ; 0785: 3a6508
    CP 0xFF ; 0788: feff
    JR Z, L_0792 ; 078A: 2806
    LD H, 0x40 ; 078C: 2640
    CALL 0x0024 ; 078E: cd2400 [BIOS ENASLT]
    DI ; 0791: f3
L_0792:
    LD A, (R(0x0864)) ; 0792: 3a6408
    CP 0xFF ; 0795: feff
    JR Z, L_07BB ; 0797: 2822
    LD C, A ; 0799: 4f
    BIT 7, C ; 079A: cb79
    JR Z, L_07AD ; 079C: 280f
    RRCA ; 079E: 0f
    RRCA ; 079F: 0f
    AND 0x03 ; 07A0: e603
    LD B, A ; 07A2: 47
    LD A, (0xFFFF) ; 07A3: 3affff [SLTSL subslot reg]
    CPL ; 07A6: 2f
    AND 0xFC ; 07A7: e6fc
    OR B ; 07A9: b0
    LD (0xFFFF), A ; 07AA: 32ffff [SLTSL subslot reg]
L_07AD:
    LD A, C ; 07AD: 79
    AND 0x03 ; 07AE: e603
    LD B, A ; 07B0: 47
    IN A, (0xA8) ; 07B1: dba8 [PPI slot select]
    AND 0xFC ; 07B3: e6fc
    OR B ; 07B5: b0
    OUT (0xA8), A ; 07B6: d3a8 [PPI slot select]
    LD (R(0x0852)), A ; 07B8: 325208
L_07BB:
    RET ; 07BB: c9
    LD A, (R(0x084F)) ; 07BC: 3a4f08
    OUT (0xA8), A ; 07BF: d3a8 [PPI slot select]
    LD A, (R(0x085D)) ; 07C1: 3a5d08
    BIT 7, A ; 07C4: cb7f
    JR Z, L_07D9 ; 07C6: 2811
    AND 0x03 ; 07C8: e603
    LD HL, 0xFCC5 ; 07CA: 21c5fc [SLTTBL]
    ADD A, L ; 07CD: 85
    LD L, A ; 07CE: 6f
    JR NC, L_07D2 ; 07CF: 3001
    INC H ; 07D1: 24
L_07D2:
    LD A, (R(0x0850)) ; 07D2: 3a5008
    LD (HL), A ; 07D5: 77
    LD (0xFFFF), A ; 07D6: 32ffff [SLTSL subslot reg]
L_07D9:
    LD A, (R(0x0865)) ; 07D9: 3a6508
    CP 0xFF ; 07DC: feff
    JR Z, L_07ED ; 07DE: 280d
    BIT 7, A ; 07E0: cb7f
    JR Z, L_07ED ; 07E2: 2809
    LD A, (R(0x085F)) ; 07E4: 3a5f08
    LD H, 0x40 ; 07E7: 2640
    CALL 0x0024 ; 07E9: cd2400 [BIOS ENASLT]
    DI ; 07EC: f3
L_07ED:
    LD A, (R(0x0866)) ; 07ED: 3a6608
    CP 0xFF ; 07F0: feff
    JR Z, L_0801 ; 07F2: 280d
    BIT 7, A ; 07F4: cb7f
    JR Z, L_0801 ; 07F6: 2809
    LD A, (R(0x085D)) ; 07F8: 3a5d08
    LD H, 0x80 ; 07FB: 2680
    CALL 0x0024 ; 07FD: cd2400 [BIOS ENASLT]
    DI ; 0800: f3
L_0801:
    RET ; 0801: c9
    PUSH AF ; 0802: f5
    PUSH BC ; 0803: c5
    PUSH DE ; 0804: d5
    PUSH HL ; 0805: e5
    IN A, (0xA8) ; 0806: dba8 [PPI slot select]
    LD (R(0x0851)), A ; 0808: 325108
    AND 0xFC ; 080B: e6fc
    OUT (0xA8), A ; 080D: d3a8 [PPI slot select]
    LD A, (R(0x0864)) ; 080F: 3a6408
    BIT 7, A ; 0812: cb7f
    JR Z, L_0823 ; 0814: 280d
    AND 0x03 ; 0816: e603
    JR NZ, L_0823 ; 0818: 2009
    LD A, (0xFFFF) ; 081A: 3affff [SLTSL subslot reg]
    CPL ; 081D: 2f
    AND 0xFC ; 081E: e6fc
    LD (0xFFFF), A ; 0820: 32ffff [SLTSL subslot reg]
L_0823:
    CALL 0x0038 ; 0823: cd3800
    DI ; 0826: f3
    LD A, (R(0x0864)) ; 0827: 3a6408
    BIT 7, A ; 082A: cb7f
    JR Z, L_0844 ; 082C: 2816
    AND 0x03 ; 082E: e603
    JR NZ, L_0844 ; 0830: 2012
    LD A, (R(0x0864)) ; 0832: 3a6408
    RRCA ; 0835: 0f
    RRCA ; 0836: 0f
    AND 0x03 ; 0837: e603
    LD B, A ; 0839: 47
    LD A, (0xFFFF) ; 083A: 3affff [SLTSL subslot reg]
    CPL ; 083D: 2f
    AND 0xFC ; 083E: e6fc
    OR B ; 0840: b0
    LD (0xFFFF), A ; 0841: 32ffff [SLTSL subslot reg]
L_0844:
    LD A, (R(0x0851)) ; 0844: 3a5108
    OUT (0xA8), A ; 0847: d3a8 [PPI slot select]
    POP HL ; 0849: e1
    POP DE ; 084A: d1
    POP BC ; 084B: c1
    POP AF ; 084C: f1
    EI ; 084D: fb
    RET ; 084E: c9
; 24-byte slot/mapper descriptor table (2131..2150: F, E, T4, T6, L, O, P, Q, R)
L_084F:
    DB 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ; 084F
    DB 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ; 0857
    DB 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF ; 085F
; s2_helper (A!+2151): configures multi-slot flags for V=0, T3=2
    LD HL, R(0x0861) ; 0867: 216108
    LD A, (R(0x0866)) ; 086A: 3a6608
    INC A ; 086D: 3c
    JR Z, L_0873 ; 086E: 2803
    LD (HL), 0x80 ; 0870: 3680
    INC HL ; 0872: 23
L_0873:
    LD A, (R(0x0865)) ; 0873: 3a6508
    INC A ; 0876: 3c
    JR Z, L_087C ; 0877: 2803
    LD (HL), 0x40 ; 0879: 3640
    INC HL ; 087B: 23
L_087C:
    LD A, (R(0x0864)) ; 087C: 3a6408
    INC A ; 087F: 3c
    JR Z, L_0888 ; 0880: 2806
    LD (HL), 0x00 ; 0882: 3600
    LD A, 0x01 ; 0884: 3e01
    JR L_0889 ; 0886: 1801
L_0888:
    XOR A ; 0888: af
L_0889:
    LD (R(0x0856)), A ; 0889: 325608
    RET ; 088C: c9
```

## `s3.asm` (1245 B code + 108 B reloc = 1353 B)

```asm
ORG 0x088D
; J!_msx2 (A!+2189): calls pal_set, clears SCREEN 5/6 VRAM, jumps to J!_exit (1744)
    CALL R(0x0D2D) ; 088D: cd2d0d
    NOP ; 0890: 00
    NOP ; 0891: 00
    NOP ; 0892: 00
    NOP ; 0893: 00
    NOP ; 0894: 00
    LD D, C ; 0895: 51
    LD E, 0x01 ; 0896: 1e01
    CP 0x03 ; 0898: fe03
    JR NZ, L_089D ; 089A: 2001
    INC E ; 089C: 1c
L_089D:
    XOR A ; 089D: af
    CALL R(0x08B8) ; 089E: cdb808
    LD A, (R(0x0563)) ; 08A1: 3a6305
    CP 0x03 ; 08A4: fe03
    JP NZ, R(0x06D0) ; 08A6: c2d006
    LD D, 0xAA ; 08A9: 16aa
    LD E, 0x02 ; 08AB: 1e02
    CALL R(0x08FC) ; 08AD: cdfc08
    LD A, 0x02 ; 08B0: 3e02
    CALL R(0x08B8) ; 08B2: cdb808
    JP R(0x06D0) ; 08B5: c3d006
; vram_clear_msx2 (2232): fills V9938 bitmap pages via port 0x98/0x99
L_08B8:
    LD (R(0x056C)), A ; 08B8: 326c05
    LD L, 0xD4 ; 08BB: 2ed4
    LD H, 0x00 ; 08BD: 2600
L_08BF:
    LD A, H ; 08BF: 7c
    OR A ; 08C0: b7
    JR Z, L_08C7 ; 08C1: 2804
    CP 0x80 ; 08C3: fe80
    JR NZ, L_08DF ; 08C5: 2018
L_08C7:
    PUSH HL ; 08C7: e5
    DI ; 08C8: f3
    RLCA ; 08C9: 07
    AND 0x01 ; 08CA: e601
    LD HL, R(0x056C) ; 08CC: 216c05
    ADD A, (HL) ; 08CF: 86
    OUT (0x99), A ; 08D0: d399 [VDP reg/addr]
    LD A, 0x8E ; 08D2: 3e8e
    OUT (0x99), A ; 08D4: d399 [VDP reg/addr]
    XOR A ; 08D6: af
    OUT (0x99), A ; 08D7: d399 [VDP reg/addr]
    LD A, 0x40 ; 08D9: 3e40
    OUT (0x99), A ; 08DB: d399 [VDP reg/addr]
    EI ; 08DD: fb
    POP HL ; 08DE: e1
L_08DF:
    DI ; 08DF: f3
    LD B, 0x80 ; 08E0: 0680
L_08E2:
    LD A, D ; 08E2: 7a
    OUT (0x98), A ; 08E3: d398 [VDP VRAM data]
    NOP ; 08E5: 00
    NOP ; 08E6: 00
    DJNZ L_08E2 ; 08E7: 10f9
    EI ; 08E9: fb
    CALL R(0x08FC) ; 08EA: cdfc08
    LD A, (R(0x0563)) ; 08ED: 3a6305
    CP 0x03 ; 08F0: fe03
    JR NZ, L_08F7 ; 08F2: 2003
    CALL R(0x08FC) ; 08F4: cdfc08
L_08F7:
    INC H ; 08F7: 24
    DEC L ; 08F8: 2d
    JR NZ, L_08BF ; 08F9: 20c4
    RET ; 08FB: c9
L_08FC:
    DEC E ; 08FC: 1d
    JR NZ, L_0904 ; 08FD: 2005
    LD E, 0x05 ; 08FF: 1e05
    LD A, D ; 0901: 7a
    XOR C ; 0902: a9
    LD D, A ; 0903: 57
L_0904:
    RET ; 0904: c9
; K!_msx2 (2309): renders 4-digit group in SCREEN 5 (4bpp) or SCREEN 6 (2bpp)
    XOR A ; 0905: af
    LD (R(0x0567)), A ; 0906: 326705
    LD HL, (R(0x0565)) ; 0909: 2a6505
    DEC HL ; 090C: 2b
    LD A, (R(0x0563)) ; 090D: 3a6305
    CP 0x03 ; 0910: fe03
    JR NZ, L_0915 ; 0912: 2001
    DEC HL ; 0914: 2b
L_0915:
    XOR A ; 0915: af
    LD DE, 0x0005 ; 0916: 110500
L_0919:
    OR A ; 0919: b7
    SBC HL, DE ; 091A: ed52
    JR C, L_0922 ; 091C: 3804
    XOR 0x01 ; 091E: ee01
    JR L_0919 ; 0920: 18f7
L_0922:
    OR A ; 0922: b7
    JR Z, L_0933 ; 0923: 280e
    LD A, (R(0x0563)) ; 0925: 3a6305
    CP 0x01 ; 0928: fe01
    LD A, 0x22 ; 092A: 3e22
    JR Z, L_0930 ; 092C: 2802
    LD A, 0xAA ; 092E: 3eaa
L_0930:
    LD (R(0x0567)), A ; 0930: 326705
L_0933:
    LD DE, R(0x0574) ; 0933: 117405
    LD C, 0x00 ; 0936: 0e00
L_0938:
    PUSH BC ; 0938: c5
    PUSH DE ; 0939: d5
    CALL R(0x0528) ; 093A: cd2805
    LD HL, (R(0x0565)) ; 093D: 2a6505
    LD A, L ; 0940: 7d
    ADD A, C ; 0941: 81
    LD L, A ; 0942: 6f
    JR NC, L_0946 ; 0943: 3001
    INC H ; 0945: 24
L_0946:
    LD A, (R(0x0563)) ; 0946: 3a6305
    CP 0x01 ; 0949: fe01
    JP Z, R(0x09A0) ; 094B: caa009
    LD B, 0x00 ; 094E: 0600
    CP 0x03 ; 0950: fe03
    JR NZ, L_095C ; 0952: 2008
    SRL H ; 0954: cb3c
    RR L ; 0956: cb1d
    JR NC, L_095C ; 0958: 3002
    LD B, 0x02 ; 095A: 0602
L_095C:
    LD A, L ; 095C: 7d
    RLCA ; 095D: 07
    AND 0x01 ; 095E: e601
    OR B ; 0960: b0
    PUSH AF ; 0961: f5
    LD A, L ; 0962: 7d
    AND 0x7F ; 0963: e67f
    LD L, A ; 0965: 6f
    LD H, 0x00 ; 0966: 2600
    ADD HL, HL ; 0968: 29
    ADD HL, HL ; 0969: 29
    ADD HL, HL ; 096A: 29
    ADD HL, HL ; 096B: 29
    ADD HL, HL ; 096C: 29
    ADD HL, HL ; 096D: 29
    ADD HL, HL ; 096E: 29
    LD A, (R(0x0564)) ; 096F: 3a6405
    OR L ; 0972: b5
    LD L, A ; 0973: 6f
    POP AF ; 0974: f1
    DI ; 0975: f3
    OUT (0x99), A ; 0976: d399 [VDP reg/addr]
    LD A, 0x8E ; 0978: 3e8e
    OUT (0x99), A ; 097A: d399 [VDP reg/addr]
    CALL R(0x0434) ; 097C: cd3404
    LD A, (R(0x0567)) ; 097F: 3a6705
    LD C, A ; 0982: 4f
    LD IX, R(0x056C) ; 0983: dd216c05
    LD B, 0x04 ; 0987: 0604
L_0989:
    LD A, (IX+0) ; 0989: dd7e00
    LD HL, R(0x0A04) ; 098C: 21040a
    ADD A, L ; 098F: 85
    LD L, A ; 0990: 6f
    JR NC, L_0994 ; 0991: 3001
    INC H ; 0993: 24
L_0994:
    LD A, (HL) ; 0994: 7e
    OR C ; 0995: b1
    OUT (0x98), A ; 0996: d398 [VDP VRAM data]
    INC IX ; 0998: dd23
    DJNZ L_0989 ; 099A: 10ed
    EI ; 099C: fb
    JP R(0x09F3) ; 099D: c3f309
L_09A0:
    LD A, L ; 09A0: 7d
    RLCA ; 09A1: 07
    AND 0x01 ; 09A2: e601
    PUSH AF ; 09A4: f5
    LD A, L ; 09A5: 7d
    AND 0x7F ; 09A6: e67f
    LD L, A ; 09A8: 6f
    LD H, 0x00 ; 09A9: 2600
    ADD HL, HL ; 09AB: 29
    ADD HL, HL ; 09AC: 29
    ADD HL, HL ; 09AD: 29
    ADD HL, HL ; 09AE: 29
    ADD HL, HL ; 09AF: 29
    ADD HL, HL ; 09B0: 29
    ADD HL, HL ; 09B1: 29
    LD A, (R(0x0564)) ; 09B2: 3a6405
    ADD A, A ; 09B5: 87
    OR L ; 09B6: b5
    LD L, A ; 09B7: 6f
    POP AF ; 09B8: f1
    DI ; 09B9: f3
    OUT (0x99), A ; 09BA: d399 [VDP reg/addr]
    LD A, 0x8E ; 09BC: 3e8e
    OUT (0x99), A ; 09BE: d399 [VDP reg/addr]
    CALL R(0x0434) ; 09C0: cd3404
    LD A, (R(0x0567)) ; 09C3: 3a6705
    LD E, A ; 09C6: 5f
    LD IX, R(0x056C) ; 09C7: dd216c05
    LD B, 0x04 ; 09CB: 0604
L_09CD:
    PUSH BC ; 09CD: c5
    LD A, (IX+0) ; 09CE: dd7e00
    LD C, A ; 09D1: 4f
    AND 0x08 ; 09D2: e608
    ADD A, A ; 09D4: 87
    LD B, A ; 09D5: 47
    LD A, C ; 09D6: 79
    AND 0x04 ; 09D7: e604
    RRCA ; 09D9: 0f
    RRCA ; 09DA: 0f
    OR B ; 09DB: b0
    OR E ; 09DC: b3
    OUT (0x98), A ; 09DD: d398 [VDP VRAM data]
    LD A, C ; 09DF: 79
    AND 0x02 ; 09E0: e602
    ADD A, A ; 09E2: 87
    ADD A, A ; 09E3: 87
    ADD A, A ; 09E4: 87
    LD B, A ; 09E5: 47
    LD A, C ; 09E6: 79
    AND 0x01 ; 09E7: e601
    OR B ; 09E9: b0
    OR E ; 09EA: b3
    OUT (0x98), A ; 09EB: d398 [VDP VRAM data]
    POP BC ; 09ED: c1
    INC IX ; 09EE: dd23
    DJNZ L_09CD ; 09F0: 10db
    EI ; 09F2: fb
L_09F3:
    POP DE ; 09F3: d1
    POP BC ; 09F4: c1
    LD HL, 0x000B ; 09F5: 210b00
    ADD HL, DE ; 09F8: 19
    EX DE, HL ; 09F9: eb
    INC C ; 09FA: 0c
    LD A, C ; 09FB: 79
    CP 0x05 ; 09FC: fe05
    JP NZ, R(0x0938) ; 09FE: c23809
    JP R(0x04E5) ; 0A01: c3e504
; 16-byte 2bpp pixel expansion lookup table (SCREEN 6)
L_0A04:
    DB 0x00, 0x01, 0x04, 0x05, 0x10, 0x11, 0x14, 0x15 ; 0A04
    DB 0x40, 0x41, 0x44, 0x45, 0x50, 0x51, 0x54, 0x55 ; 0A0C
; div_iy32k (2580): 16-bit divide helper for IY >= 32768 (C > 9360)
    PUSH IX ; 0A14: dde5
    PUSH HL ; 0A16: e5
    POP IX ; 0A17: dde1
    LD HL, 0x0000 ; 0A19: 210000
    LD A, 0x20 ; 0A1C: 3e20
    LD (R(0x0430)), A ; 0A1E: 323004
    XOR A ; 0A21: af
L_0A22:
    ADD IX, IX ; 0A22: dd29
    RL E ; 0A24: cb13
    RL D ; 0A26: cb12
    ADC HL, HL ; 0A28: ed6a
    RLA ; 0A2A: 17
    OR A ; 0A2B: b7
    JR Z, L_0A4D ; 0A2C: 281f
    CP 0x01 ; 0A2E: fe01
    JR NZ, L_0A3F ; 0A30: 200d
    OR A ; 0A32: b7
    SBC HL, BC ; 0A33: ed42
    JR NC, L_0A3A ; 0A35: 3003
    ADD HL, BC ; 0A37: 09
    JR L_0A4D ; 0A38: 1813
L_0A3A:
    XOR A ; 0A3A: af
    INC IX ; 0A3B: dd23
    JR L_0A4D ; 0A3D: 180e
L_0A3F:
    OR A ; 0A3F: b7
    SBC HL, BC ; 0A40: ed42
    JR C, L_0A4A ; 0A42: 3806
    LD A, 0x01 ; 0A44: 3e01
    INC IX ; 0A46: dd23
    JR L_0A4D ; 0A48: 1803
L_0A4A:
    XOR A ; 0A4A: af
    INC IX ; 0A4B: dd23
L_0A4D:
    PUSH HL ; 0A4D: e5
    LD HL, R(0x0430) ; 0A4E: 213004
    DEC (HL) ; 0A51: 35
    POP HL ; 0A52: e1
    JR NZ, L_0A22 ; 0A53: 20cd
    LD B, H ; 0A55: 44
    LD C, L ; 0A56: 4d
    PUSH IX ; 0A57: dde5
    POP HL ; 0A59: e1
    POP IX ; 0A5A: dde1
    RET ; 0A5C: c9
; bit_addr (2653): computes byte ptr & mask in A!+2694 bitmap for IY >= 32768
    LD A, IYL ; 0A5D: fd7d
    AND 0x07 ; 0A5F: e607
    INC A ; 0A61: 3c
    LD B, A ; 0A62: 47
    XOR A ; 0A63: af
    SCF ; 0A64: 37
L_0A65:
    RLA ; 0A65: 17
    DJNZ L_0A65 ; 0A66: 10fd
    LD C, A ; 0A68: 4f
    LD A, IYL ; 0A69: fd7d
    LD L, A ; 0A6B: 6f
    LD A, IYH ; 0A6C: fd7c
    AND 0x7F ; 0A6E: e67f
    LD H, A ; 0A70: 67
    SRL H ; 0A71: cb3c
    RR L ; 0A73: cb1d
    SRL H ; 0A75: cb3c
    RR L ; 0A77: cb1d
    SRL H ; 0A79: cb3c
    RR L ; 0A7B: cb1d
    PUSH DE ; 0A7D: d5
    LD DE, (R(0x0009)) ; 0A7E: ed5b0900
    ADD HL, DE ; 0A82: 19
    POP DE ; 0A83: d1
    LD A, C ; 0A84: 79
    RET ; 0A85: c9
; s3p (A!+2694): probes R800 MULUW, V9938/58, RAM mapper segments/slot -> 2131..2150
    DI ; 0A86: f3
    PUSH AF ; 0A87: f5
    PUSH BC ; 0A88: c5
    PUSH DE ; 0A89: d5
    PUSH HL ; 0A8A: e5
    PUSH IX ; 0A8B: dde5
    PUSH IY ; 0A8D: fde5
    IN A, (0xA8) ; 0A8F: dba8 [PPI slot select]
    RLCA ; 0A91: 07
    RLCA ; 0A92: 07
    AND 0x03 ; 0A93: e603
    LD B, 0x06 ; 0A95: 0606
    CALL R(0x0CBE) ; 0A97: cdbe0c
    LD (R(0x0860)), A ; 0A9A: 326008
    POP IY ; 0A9D: fde1
    POP IX ; 0A9F: dde1
    POP HL ; 0AA1: e1
    POP DE ; 0AA2: d1
    POP BC ; 0AA3: c1
    POP AF ; 0AA4: f1
    DI ; 0AA5: f3
    PUSH AF ; 0AA6: f5
    PUSH BC ; 0AA7: c5
    PUSH DE ; 0AA8: d5
    PUSH HL ; 0AA9: e5
    PUSH IX ; 0AAA: dde5
    PUSH IY ; 0AAC: fde5
    XOR A ; 0AAE: af
    LD (R(0x0853)), A ; 0AAF: 325308
    LD (R(0x0854)), A ; 0AB2: 325408
    LD (R(0x0855)), A ; 0AB5: 325508
    LD (R(0x0010)), A ; 0AB8: 321000
    LD (R(0x0856)), A ; 0ABB: 325608
    LD A, 0x02 ; 0ABE: 3e02
    LD (R(0x085E)), A ; 0AC0: 325e08
    LD HL, 0x0064 ; 0AC3: 216400
    LD BC, 0x0064 ; 0AC6: 016400
    MULUW HL, BC ; 0AC9: edc3 [R800 16x16->32 hardware mul]
    LD A, H ; 0ACB: 7c
    CP 0x27 ; 0ACC: fe27
    JR NZ, L_0AD5 ; 0ACE: 2005
    LD A, 0x01 ; 0AD0: 3e01
    LD (R(0x0010)), A ; 0AD2: 321000
L_0AD5:
    IN A, (0xA8) ; 0AD5: dba8 [PPI slot select]
    PUSH AF ; 0AD7: f5
    RRCA ; 0AD8: 0f
    RRCA ; 0AD9: 0f
    AND 0x03 ; 0ADA: e603
    LD B, 0x00 ; 0ADC: 0600
    CALL R(0x0CBE) ; 0ADE: cdbe0c
    LD (R(0x085F)), A ; 0AE1: 325f08
    POP AF ; 0AE4: f1
    RLCA ; 0AE5: 07
    RLCA ; 0AE6: 07
    AND 0x03 ; 0AE7: e603
    LD B, 0x04 ; 0AE9: 0604
    CALL R(0x0CBE) ; 0AEB: cdbe0c
    LD (R(0x085D)), A ; 0AEE: 325d08
    LD A, (0x002D) ; 0AF1: 3a2d00 [BIOS MSXVER]
    OR A ; 0AF4: b7
    JP Z, R(0x0B82) ; 0AF5: ca820b
    LD A, (0xFB20) ; 0AF8: 3a20fb
    RRA ; 0AFB: 1f
    JP NC, R(0x0B82) ; 0AFC: d2820b
    XOR A ; 0AFF: af
    LD HL, 0x0000 ; 0B00: 210000
    LD DE, 0x0401 ; 0B03: 110104
    CALL 0xFFCA ; 0B06: cdcaff
    DI ; 0B09: f3
    OR A ; 0B0A: b7
    JP Z, R(0x0B82) ; 0B0B: ca820b
    PUSH AF ; 0B0E: f5
    LD A, H ; 0B0F: 7c
    OR L ; 0B10: b5
    JR NZ, L_0B17 ; 0B11: 2004
    POP AF ; 0B13: f1
    JP R(0x0B82) ; 0B14: c3820b
L_0B17:
    POP AF ; 0B17: f1
    CP (HL) ; 0B18: be
    JP NZ, R(0x0B82) ; 0B19: c2820b
    LD (R(0x085D)), A ; 0B1C: 325d08
    INC HL ; 0B1F: 23
    LD A, (HL) ; 0B20: 7e
    LD (R(0x0855)), A ; 0B21: 325508
    XOR A ; 0B24: af
    LD DE, 0x0402 ; 0B25: 110204
    CALL 0xFFCA ; 0B28: cdcaff
    DI ; 0B2B: f3
    PUSH HL ; 0B2C: e5
    POP IX ; 0B2D: dde1
    LD DE, 0x001E ; 0B2F: 111e00
    ADD HL, DE ; 0B32: 19
    EX DE, HL ; 0B33: eb
    LD A, 0xC3 ; 0B34: 3ec3
    LD (R(0x075B)), A ; 0B36: 325b07
    LD HL, R(0x075B) ; 0B39: 215b07
    INC HL ; 0B3C: 23
    LD (HL), E ; 0B3D: 73
    INC HL ; 0B3E: 23
    LD (HL), D ; 0B3F: 72
    PUSH IX ; 0B40: dde5
    POP HL ; 0B42: e1
    LD DE, 0x0021 ; 0B43: 112100
    ADD HL, DE ; 0B46: 19
    CALL R(0x0D0F) ; 0B47: cd0f0d
    DI ; 0B4A: f3
    LD (R(0x085E)), A ; 0B4B: 325e08
    LD HL, R(0x0857) ; 0B4E: 215708
    LD C, 0x06 ; 0B51: 0e06
L_0B53:
    PUSH HL ; 0B53: e5
    PUSH BC ; 0B54: c5
    PUSH IX ; 0B55: dde5
    PUSH IX ; 0B57: dde5
    POP HL ; 0B59: e1
    XOR A ; 0B5A: af
    LD B, 0x00 ; 0B5B: 0600
    CALL R(0x0D0F) ; 0B5D: cd0f0d
    DI ; 0B60: f3
    POP IX ; 0B61: dde1
    POP BC ; 0B63: c1
    POP HL ; 0B64: e1
    JR C, L_0B73 ; 0B65: 380c
    LD (HL), A ; 0B67: 77
    INC HL ; 0B68: 23
    LD A, (R(0x0853)) ; 0B69: 3a5308
    INC A ; 0B6C: 3c
    LD (R(0x0853)), A ; 0B6D: 325308
    DEC C ; 0B70: 0d
    JR NZ, L_0B53 ; 0B71: 20e0
L_0B73:
    LD A, (R(0x0853)) ; 0B73: 3a5308
    OR A ; 0B76: b7
    JP Z, R(0x0C8F) ; 0B77: ca8f0c
    LD A, 0x01 ; 0B7A: 3e01
    LD (R(0x0854)), A ; 0B7C: 325408
    JP R(0x0C8F) ; 0B7F: c38f0c
L_0B82:
    LD A, (R(0x085D)) ; 0B82: 3a5d08
    LD H, 0x40 ; 0B85: 2640
    CALL 0x0024 ; 0B87: cd2400 [BIOS ENASLT]
    DI ; 0B8A: f3
    LD HL, R(0x0D6A) ; 0B8B: 216a0d
    LD (HL), 0x00 ; 0B8E: 3600
    LD D, H ; 0B90: 54
    LD E, L ; 0B91: 5d
    INC DE ; 0B92: 13
    LD BC, 0x001F ; 0B93: 011f00
    LDIR ; 0B96: edb0
    LD IX, 0x8000 ; 0B98: dd210080
    LD IY, 0x4000 ; 0B9C: fd210040
    CALL R(0x0CE2) ; 0BA0: cde20c
    LD IX, 0xF55E ; 0BA3: dd215ef5
    LD IY, 0x755E ; 0BA7: fd215e75
    CALL R(0x0CE2) ; 0BAB: cde20c
    LD C, 0x00 ; 0BAE: 0e00
L_0BB0:
    LD HL, R(0x0D6A) ; 0BB0: 216a0d
    LD B, 0x00 ; 0BB3: 0600
    ADD HL, BC ; 0BB5: 09
    LD A, (HL) ; 0BB6: 7e
    OR A ; 0BB7: b7
    JR NZ, L_0C1C ; 0BB8: 2062
    LD A, C ; 0BBA: 79
    OUT (0xFD), A ; 0BBB: d3fd [Mapper page 1]
    LD A, (0x4000) ; 0BBD: 3a0040
    LD D, A ; 0BC0: 57
    LD A, 0x55 ; 0BC1: 3e55
    LD (0x4000), A ; 0BC3: 320040
    LD A, (0x4000) ; 0BC6: 3a0040
    CP 0x55 ; 0BC9: fe55
    JR NZ, L_0BD9 ; 0BCB: 200c
    LD A, 0xAA ; 0BCD: 3eaa
    LD (0x4000), A ; 0BCF: 320040
    LD A, (0x4000) ; 0BD2: 3a0040
    CP 0xAA ; 0BD5: feaa
    JR Z, L_0BDF ; 0BD7: 2806
L_0BD9:
    LD A, D ; 0BD9: 7a
    LD (0x4000), A ; 0BDA: 320040
    JR L_0C1C ; 0BDD: 183d
L_0BDF:
    LD A, (R(0x0853)) ; 0BDF: 3a5308
    OR A ; 0BE2: b7
    JR Z, L_0C00 ; 0BE3: 281b
    LD B, A ; 0BE5: 47
    LD E, 0xA0 ; 0BE6: 1ea0
    LD HL, R(0x0857) ; 0BE8: 215708
L_0BEB:
    LD A, (HL) ; 0BEB: 7e
    OUT (0xFD), A ; 0BEC: d3fd [Mapper page 1]
    LD A, (0x4000) ; 0BEE: 3a0040
    CP E ; 0BF1: bb
    JR NZ, L_0BFA ; 0BF2: 2006
    INC HL ; 0BF4: 23
    INC E ; 0BF5: 1c
    DJNZ L_0BEB ; 0BF6: 10f3
    JR L_0C00 ; 0BF8: 1806
L_0BFA:
    LD A, E ; 0BFA: 7b
    LD (0x4000), A ; 0BFB: 320040
    JR L_0C1C ; 0BFE: 181c
L_0C00:
    LD A, C ; 0C00: 79
    OUT (0xFD), A ; 0C01: d3fd [Mapper page 1]
    LD A, (R(0x0853)) ; 0C03: 3a5308
    LD E, A ; 0C06: 5f
    LD D, 0x00 ; 0C07: 1600
    ADD A, 0xA0 ; 0C09: c6a0
    LD (0x4000), A ; 0C0B: 320040
    LD HL, R(0x0857) ; 0C0E: 215708
    ADD HL, DE ; 0C11: 19
    LD (HL), C ; 0C12: 71
    INC E ; 0C13: 1c
    LD A, E ; 0C14: 7b
    LD (R(0x0853)), A ; 0C15: 325308
    CP 0x06 ; 0C18: fe06
    JR Z, L_0C22 ; 0C1A: 2806
L_0C1C:
    INC C ; 0C1C: 0c
    LD A, C ; 0C1D: 79
    CP 0x20 ; 0C1E: fe20
    JR NZ, L_0BB0 ; 0C20: 208e
L_0C22:
    LD A, (R(0x0853)) ; 0C22: 3a5308
    OR A ; 0C25: b7
    JR Z, L_0C8F ; 0C26: 2867
    LD A, 0x01 ; 0C28: 3e01
    LD (R(0x0854)), A ; 0C2A: 325408
    LD A, (R(0x0853)) ; 0C2D: 3a5308
    ADD A, 0x02 ; 0C30: c602
    LD (R(0x0855)), A ; 0C32: 325508
    LD A, (R(0x0853)) ; 0C35: 3a5308
    CP 0x01 ; 0C38: fe01
    JR NZ, L_0C8F ; 0C3A: 2053
    LD A, (R(0x085E)) ; 0C3C: 3a5e08
    CALL R(0x075B) ; 0C3F: cd5b07
    LD A, (R(0x085F)) ; 0C42: 3a5f08
    LD H, 0x40 ; 0C45: 2640
    CALL 0x0024 ; 0C47: cd2400 [BIOS ENASLT]
    DI ; 0C4A: f3
    CALL R(0x0D10) ; 0C4B: cd100d
    LD A, (0x0000) ; 0C4E: 3a0000
    LD D, A ; 0C51: 57
    LD A, 0x55 ; 0C52: 3e55
    LD (0x0000), A ; 0C54: 320000
    LD A, (0x0000) ; 0C57: 3a0000
    CP 0x55 ; 0C5A: fe55
    JR NZ, L_0C86 ; 0C5C: 2028
    LD A, 0xAA ; 0C5E: 3eaa
    LD (0x0000), A ; 0C60: 320000
    LD A, (0x0000) ; 0C63: 3a0000
    CP 0xAA ; 0C66: feaa
    JR NZ, L_0C86 ; 0C68: 201c
    LD A, (0x4000) ; 0C6A: 3a0040
    CP 0xA0 ; 0C6D: fea0
    JR NZ, L_0C86 ; 0C6F: 2015
    LD HL, 0x8000 ; 0C71: 210080
    CALL R(0x0CB3) ; 0C74: cdb30c
    JR NZ, L_0C86 ; 0C77: 200d
    LD HL, 0xF55E ; 0C79: 215ef5
    CALL R(0x0CB3) ; 0C7C: cdb30c
    JR NZ, L_0C86 ; 0C7F: 2005
    LD A, 0x01 ; 0C81: 3e01
    LD (R(0x0856)), A ; 0C83: 325608
L_0C86:
    LD A, D ; 0C86: 7a
    LD (0x0000), A ; 0C87: 320000
    CALL R(0x0D21) ; 0C8A: cd210d
    JR L_0C9E ; 0C8D: 180f
L_0C8F:
    LD A, (R(0x085E)) ; 0C8F: 3a5e08
    CALL R(0x075B) ; 0C92: cd5b07
    LD A, (R(0x085F)) ; 0C95: 3a5f08
    LD H, 0x40 ; 0C98: 2640
    CALL 0x0024 ; 0C9A: cd2400 [BIOS ENASLT]
    DI ; 0C9D: f3
L_0C9E:
    LD HL, 0x0000 ; 0C9E: 210000
    LD (0xF7F8), HL ; 0CA1: 22f8f7 [BASIC USR arg/ret]
    LD A, 0x02 ; 0CA4: 3e02
    LD (0xF663), A ; 0CA6: 3263f6
    POP IY ; 0CA9: fde1
    POP IX ; 0CAB: dde1
    POP HL ; 0CAD: e1
    POP DE ; 0CAE: d1
    POP BC ; 0CAF: c1
    POP AF ; 0CB0: f1
    EI ; 0CB1: fb
    RET ; 0CB2: c9
L_0CB3:
    LD C, (HL) ; 0CB3: 4e
    LD A, C ; 0CB4: 79
    CPL ; 0CB5: 2f
    LD (HL), A ; 0CB6: 77
    LD A, (0x0000) ; 0CB7: 3a0000
    CP 0xAA ; 0CBA: feaa
    LD (HL), C ; 0CBC: 71
    RET ; 0CBD: c9
L_0CBE:
    LD C, A ; 0CBE: 4f
    LD HL, 0xFCC1 ; 0CBF: 21c1fc [EXPTBL]
    LD A, C ; 0CC2: 79
    ADD A, L ; 0CC3: 85
    LD L, A ; 0CC4: 6f
    JR NC, L_0CC8 ; 0CC5: 3001
    INC H ; 0CC7: 24
L_0CC8:
    LD A, (HL) ; 0CC8: 7e
    AND 0x80 ; 0CC9: e680
    OR A ; 0CCB: b7
    JR NZ, L_0CD0 ; 0CCC: 2002
    LD A, C ; 0CCE: 79
    RET ; 0CCF: c9
L_0CD0:
    LD DE, 0x0004 ; 0CD0: 110400
    ADD HL, DE ; 0CD3: 19
    LD A, (HL) ; 0CD4: 7e
    INC B ; 0CD5: 04
    DEC B ; 0CD6: 05
    JR Z, L_0CDC ; 0CD7: 2803
L_0CD9:
    RRCA ; 0CD9: 0f
    DJNZ L_0CD9 ; 0CDA: 10fd
L_0CDC:
    AND 0x0C ; 0CDC: e60c
    OR C ; 0CDE: b1
    OR 0x80 ; 0CDF: f680
    RET ; 0CE1: c9
L_0CE2:
    LD A, (IX+0) ; 0CE2: dd7e00
    LD C, A ; 0CE5: 4f
    CPL ; 0CE6: 2f
    LD D, A ; 0CE7: 57
    LD HL, R(0x0D6A) ; 0CE8: 216a0d
    LD B, 0x00 ; 0CEB: 0600
L_0CED:
    LD A, B ; 0CED: 78
    OUT (0xFD), A ; 0CEE: d3fd [Mapper page 1]
    LD (IX+0), D ; 0CF0: dd7200
    LD A, (IY+0) ; 0CF3: fd7e00
    CP D ; 0CF6: ba
    JR NZ, L_0D04 ; 0CF7: 200b
    LD (IX+0), C ; 0CF9: dd7100
    LD A, (IY+0) ; 0CFC: fd7e00
    CP C ; 0CFF: b9
    JR NZ, L_0D04 ; 0D00: 2002
    LD (HL), 0x01 ; 0D02: 3601
L_0D04:
    LD (IX+0), C ; 0D04: dd7100
    INC HL ; 0D07: 23
    INC B ; 0D08: 04
    LD A, B ; 0D09: 78
    CP 0x20 ; 0D0A: fe20
    JR NZ, L_0CED ; 0D0C: 20df
    RET ; 0D0E: c9
L_0D0F:
    JP (HL) ; 0D0F: e9
L_0D10:
    LD A, (R(0x085D)) ; 0D10: 3a5d08
    LD (R(0x0864)), A ; 0D13: 326408
    LD (R(0x0865)), A ; 0D16: 326508
    LD A, 0xFF ; 0D19: 3eff
    LD (R(0x0866)), A ; 0D1B: 326608
    JP R(0x075E) ; 0D1E: c35e07
L_0D21:
    CALL R(0x07BC) ; 0D21: cdbc07
    LD A, 0xFF ; 0D24: 3eff
    LD (R(0x0864)), A ; 0D26: 326408
    LD (R(0x0865)), A ; 0D29: 326508
    RET ; 0D2C: c9
; pal_set (3373): programs 4 V9938 palette registers via port 0x99/0x9A
L_0D2D:
    PUSH AF ; 0D2D: f5
    DI ; 0D2E: f3
    XOR A ; 0D2F: af
    OUT (0x99), A ; 0D30: d399 [VDP reg/addr]
    LD A, 0x90 ; 0D32: 3e90
    OUT (0x99), A ; 0D34: d399 [VDP reg/addr]
    LD HL, R(0x0D4C) ; 0D36: 214c0d
    LD B, 0x08 ; 0D39: 0608
L_0D3B:
    LD A, (HL) ; 0D3B: 7e
    OUT (0x9A), A ; 0D3C: d39a [V9938 palette]
    INC HL ; 0D3E: 23
    DJNZ L_0D3B ; 0D3F: 10fa
    EI ; 0D41: fb
    POP AF ; 0D42: f1
    LD C, 0x22 ; 0D43: 0e22
    CP 0x01 ; 0D45: fe01
    JR Z, L_0D4B ; 0D47: 2802
    LD C, 0xAA ; 0D49: 0eaa
L_0D4B:
    RET ; 0D4B: c9
; pal_data (3404): 4 V9938 GRB palette pairs (0x0777, 0x0151, 0x0733, 0x0000)
L_0D4C:
    DB 0x77, 0x07, 0x51, 0x01, 0x33, 0x07, 0x00, 0x00 ; 0D4C
; r800_aligner (3412): copies 27B spd_loop to 12B-aligned A!+3689 for R800 timing
    LD HL, R(0x06DB) ; 0D54: 21db06
    LD DE, R(0x0E69) ; 0D57: 11690e
    LD E, 0x00 ; 0D5A: 1e00
    PUSH DE ; 0D5C: d5
    LD BC, 0x001B ; 0D5D: 011b00
    LDIR ; 0D60: edb0
    POP HL ; 0D62: e1
    PUSH HL ; 0D63: e5
    LD C, 0x0C ; 0D64: 0e0c
    ADD HL, BC ; 0D66: 09
    LD (HL), 0x64 ; 0D67: 3664
    RET ; 0D69: c9
```

