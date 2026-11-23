## MSX-family single-screen pi spigot

there are two versions: the full version which is a single monolithing BASIC listing with embedded compressed relocatable machine code, and which requires at least 16k of Z80 RAM and supports enhanced graphics modes on MSX2/2+/turboR; and the reduced-feature version runnable on any MSX with 8k or more of Z80 RAM, which BLOAD's the machine code separately and then relocates it. the reduced version is actually constructed from the full version by a MERGE'd-in transformer program.

initial development relied heavily on LLM assistance

digit capacities:

**full version** MSX2+DiskROM, 64K (no mapper): 10752 digits; tR+DiskROM, 1024k mapper: 10752 digits; MSX 24k: 2432 digits; MSX 48k: 2432 digits; MSX2+DiskROM, 64K mapper: 10752 digits; MSX2+ +DiskROM, 128k mapper: 10752 digits; MSX 16k: 1408 digits; MSX+DiskROM, 64k (no mapper): 2432 digits.

**8k+ version** MSX 8k: 1392 digits; MSX/2/2+/tR 16k+: 2432 digits

when a lower-RAM MSX1 is using on-screen VRAM pattern storage as work RAM earlier in the computation that is intentionally visible. you can watch the work area move "out of the way" of the advancing digit display:
<img width="537" alt="image" src="https://github.com/user-attachments/assets/9cb0e561-d8de-4e4b-bedc-e9492d9d5880" />
<img width="537" alt="image" src="https://github.com/user-attachments/assets/15924f9f-074a-41d4-a8b9-9d97a4cc0a61" />

### screenshots
2432 digits computed on an (emulated) MSX with 16K of RAM and 16K of VRAM using the 8k+ version
<img width="537" alt="image" src="https://github.com/user-attachments/assets/ac8b3d8f-9db2-470f-94fc-0e52f51eb51c" />

1392 digits computed on an (emulated) MSX with 8K of RAM and 16K of VRAM using the 8k+ version
<img width="537" alt="image" src="https://github.com/user-attachments/assets/2e21db5f-56fd-4edd-aa1d-392b79edf6e1" />

2432 digits computed on an (emulated) MSX2+ using the 8k+ version

*(emulated on unaccelerated hardware and the computation+display took around 1 hour 33 minutes)*
<img width="537" alt="image" src="https://github.com/user-attachments/assets/fa4e68d2-df6c-4ffd-9d1c-da85fbe61cff" />
