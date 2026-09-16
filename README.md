# DSBoard2026

Minimal digital-logic **test board** for home study. It generates stimulus, drives a student’s external logic circuit (DUT), captures outputs, and returns results to a PC Python app.

**Status:** draft — pre-schematic freeze (spec revision 2.7). This repository currently holds documentation only. KiCad or Altium CAD, Arduino firmware, and the Python app will land in the folders below.

A student shall be able to order the PCB, receive it fully assembled, plug in power and USB, and use it immediately without soldering.

## Use

| When | Tool | Connection |
| --- | --- | --- |
| One-time firmware upload | Arduino IDE | Arduino Nano USB, **off the board** |
| Every study session | PC Python App (Qt, Windows first) | Arduino Nano USB, **on the board** |

Main-board USB-C is **power only** (external charger). The logic **+5 V** rail is a 2:1 mux (Arduino **VIN** vs external VBUS) into **TPS2553-1**. When both sources are present, external VBUS is selected so the laptop is not loaded by the DUT.

## Repository layout

```text
docs/            Product spec and diagrams (source of truth)
hardware/        KiCad or Altium project (not started)
firmware/        Arduino Nano controller sketch (not started)
software/        PC Python App (not started; specified separately)
manufacturing/   Released Gerbers, BOM, assembly notes (not started)
tools/           Doc helpers (e.g. spec → PDF)
```

Start with [`docs/DSBoard2026_specs.md`](docs/DSBoard2026_specs.md). Regenerated PDFs live in `docs/generated/`.

```bash
python tools/export_pdf.py
```

This project is AI-assisted. Design decisions and documents are reviewed by the project owner.
