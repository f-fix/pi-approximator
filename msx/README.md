MSX-family single-screen pi spigot

there are two versions: the full version which is a single monolithing BASIC listing with embedded compressed relocatable machine code, and which requires at least 16k of Z80 RAM and supports enhanced graphics modes on MSX2/2+/turboR; and the reduced-feature version runnable on any MSX with 8k or more of Z80 RAM, which BLOAD's the machine code separately and then relocates it. the reduced version is actually constructed from the full version by a MERGE'd-in transformer program.

initial development relied heavily on LLM assistance

digit capacities:

**full version** MSX2+DiskROM, 64K (no mapper): 10752 digits; tR+DiskROM, 1024k mapper: 10752 digits; MSX 24k: 2432 digits; MSX 48k: 2432 digits; MSX2+DiskROM, 64K mapper: 10752 digits; MSX2+ +DiskROM, 128k mapper: 10752 digits; MSX 16k: 1408 digits; MSX+DiskROM, 64k (no mapper): 2432 digits.

**8k+ version** MSX 8k: 1392 digits; MSX/2/2+/tR 16k+: 2432 digits
