# pogopin

Lab work on a contact-matrix (scanning contact potentiometry) cell for welded joints.

- **`pogoscan/`** — Raspberry Pi 5 tool that reads an AD7705/TM7705 ADC module over SPI, records one averaged point per
  click on a 21×21 grid through a small web page, and renders the heatmap. Design notes and the implementation plan are in
  `pogoscan/docs/`. See `pogoscan/README.md` for wiring, settings, API and the systemd service.
- **`SCP papers/`** — English summaries (`summaries/`, one per paper, with `00 - INDEX.md` as the entry point) of the source
  papers on scanning contact potentiometry and related NDT methods, and the verified electronics-selection report
  (`10 - Measuring electronics selection for the SCP contact cell (verified research, 2026-09-17).md`). The papers
  themselves are copyrighted journal and patent PDFs and are not included; the index lists their titles and authors.
