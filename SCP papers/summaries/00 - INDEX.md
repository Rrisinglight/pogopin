# SCP papers — summary index

Maximum-fidelity English summaries of the 10 PDFs in `../` (**9 unique articles**; two
files are byte-identical — see [`_duplicate-note.md`](_duplicate-note.md)).

Each summary mirrors its source's own section structure and keeps every formula (LaTeX,
numbered as in the original), every figure described rather than merely listed, every
table reproduced in full, and every numeric value with its units and measurement
conditions. Journal front-matter, affiliations and bibliographies are omitted; in-text
citation markers are kept where they carry meaning.

| # | Summary | Source language | Source pages | Size |
|---|---|---|---|---|
| 01 | [A Review of NDT Techniques for Defect Detection](01%20-%20A%20Review%20of%20NDT%20Techniques%20for%20Defect%20Detection.md) | EN | 26 | 93 KB |
| 02 | [Determination of CPD by the Kelvin Probe (Part I)](02%20-%20Determination%20of%20Contact%20Potential%20Difference%20by%20the%20Kelvin%20Probe%20%28Part%20I%29.md) | EN | 10 | 37 KB |
| 03 | [Theoretical Description of Scanning Tunneling Potentiometry](03%20-%20Theoretical%20Description%20of%20Scanning%20Tunneling%20Potentiometry.md) | EN | 14 | 83 KB |
| 04 | [SCP and Thermal Neutron Diffraction in Physico-Mechanical Tests](04%20-%20Scanning%20Contact%20Potentiometry%20and%20Thermal%20Neutron%20Diffraction%20in%20Physico-Mechanical%20Tests.md) | EN | 18 | 69 KB |
| 05 | [Methods of Electrophysical Diagnostics and Monitoring of Reactor Equipment](05%20-%20Methods%20of%20Electrophysical%20Diagnostics%20and%20Monitoring%20of%20Reactor%20Equipment.md) | RU | 11 | 50 KB |
| 06 | [Automation of Electrophysical Diagnostics in Physico-Mechanical Testing](06%20-%20Automation%20of%20Electrophysical%20Diagnostics%20in%20Physico-Mechanical%20Testing%20of%20Materials.md) | RU | 4 | 37 KB |
| 07 | [Influence of Environmental Parameters on NDT by the CPD Method](07%20-%20Influence%20of%20Environmental%20Parameters%20on%20NDT%20of%20Metal%20Machine%20Parts%20by%20the%20CPD%20Method.md) | RU | 6 | 33 KB |
| 08 | [Review of Welded Joint Quality Control Methods](08%20-%20Review%20of%20Welded%20Joint%20Quality%20Control%20Methods.md) | RU | 3 | 22 KB |
| 09 | [Method for Local Detection of Flaws and Device for Realizing It (WO 2017/180007 A1)](09%20-%20Method%20for%20Local%20Detection%20of%20Flaws%20and%20Device%20for%20Realizing%20It%20%28WO%202017-180007%20A1%29.md) | RU | 27 | 86 KB |

---

## 01 — A Review of NDT Techniques for Defect Detection

Shaloo, Schnall, Klein, Huber, Reitinger — *Materials* (MDPI), review. Surveys
non-destructive testing for fusion welding and, prospectively, wire arc additive
manufacturing. Organised by technique: laser-ultrasonics, acoustic emission, optical
emission spectroscopy, laser-induced breakdown spectroscopy, laser opto-ultrasonic dual
detection, thermography (lock-in, pulsed, step-pulsed, vibro-, eddy-current variants), and
defect detection by monitoring process parameters. Its Table 1 — 22 NDT methods against
detectable defect type, minimum detectable size, and applicability — is the single most
reusable artifact in the whole corpus; it is reproduced cell-for-cell. Detection limits
span >10 µm (micro-CT) to >1000 µm (magnetic particle); laser-ultrasonics finds >100 µm
defects up to 700 µm deep at >1 m standoff, bandwidth 1–100 MHz. 19 figures, 2 tables, no
equations. *Source caveat: the PDF carries a second overlapping "FOR PEER REVIEW" text
layer that corrupts text extraction on pp. 3–6; table cells were read from the rendered
pages instead.*

## 02 — Determination of Contact Potential Difference by the Kelvin Probe (Part I)

Vilitis, Rutkis, Busenberg, Merkulov — *Latvian J. Physics and Technical Sciences*, 2016,
N 2. The physics foundation for everything else in this corpus: what contact potential
difference is, how the vibrating-capacitor (Kelvin–Zisman) method nulls it, and where the
errors come from. All 11 numbered equations, from the work-function/Fermi-level relations
through the vibrating-capacitor current to the null condition. Resolution ±(1–2 mV) over a
±10 kV range; dipole layer "a few Å". Principles only — the instrument itself is deferred
to Part 2, so no apparatus parameters appear. *Source caveats recorded, not corrected: the
sign convention is inconsistent between Eq. (1) and Fig. 1c; Eq. (11) is printed with a
missing divisor and a misplaced square; Fig. 2's caption prints* V_CPB *for* V_CPD.

## 03 — Theoretical Description of Scanning Tunneling Potentiometry

Wang & Beasley (Stanford) — arXiv:1007.1512v2. The theory counterpart: a quantum-transport
derivation of what scanning tunneling potentiometry actually measures. All 35 numbered
equations transcribed contiguously with the derivation chain intact — tunneling current in
terms of the sample **density matrix**, Chen's derivative rule eliminating the tip wave
function, and the potentiometric voltage defined *implicitly* as the voltage that nulls
the tunneling current. Five limiting cases connect it to prior literature, including the
Landauer resistive dipole and an explicit reproduction of Chu & Sorbello's Eq. (14).
Concludes that the global formulation is intractable and must be reformulated on a **local
density matrix**. Includes a ~100-entry symbol glossary. Key negative result: STP shows no
atomic corrugation at equilibrium, and corrugation is only a second-order effect with
defects — unlike STM mode, where it is first-order.

## 04 — SCP and Thermal Neutron Diffraction in Physico-Mechanical Tests

Abu Ghazal, Bokuchava, Papushkin, Surin, Shef (MEPhI; FLNP JINR) — AtomFuture-2017,
DOI 10.18502/keg.v3i3.1611. **The corpus's central experimental result.** Tensile tests on
12Kh18N10T austenitic steel, 100–700 MPa, measured simultaneously by SCP and by neutron
diffraction at the FSD Fourier stress diffractometer (IBR-2, JINR Dubna). The payoff:
diffraction detects α′-martensite only *above* 650 MPa, while the SCP signal reveals the
nucleation precursor already at **400–600 MPa** — an independent, structurally-validated
demonstration that SCP sees damage earlier than the reference method. Microstrain from peak
broadening stays flat at ≈1.4–1.55×10⁻³ up to 500 MPa, then roughly doubles. Two samples:
one intact, one fibre-laser-welded and taken to rupture. 17 figures, 4 equations.

## 05 — Methods of Electrophysical Diagnostics and Monitoring of Reactor Equipment

Surin, Volkova, Denisov, Motovilin, Rein (MEPhI) — *Global Nuclear Safety*, 2016, No. 4(21).
The application case. Argues that dangerous cracks in long-serving reactor equipment form
in stages, and that conventional NDT catches them too late: a crack opening of only
**5–10 µm defeats ultrasonic inspection**, which is the gap electrophysical methods fill.
Covers the physical basis (contact-spot statistics, electrical double layer,
electron-density change in the gap), the EDSS-1 instrumentation, conical transducers with
0.3 mm tips, and three real targets — a VVER-1000 collector-to-steam-generator weld
(zone No. 111), the fuel kernel/cladding gap at the IRT MEPhI reactor, and Ø219×6 mm
steel-20 pipeline welds. 7 equations, 5 figures, 2 tables.

## 06 — Automation of Electrophysical Diagnostics in Physico-Mechanical Testing

Abu Ghazal, Surin, Shef (MEPhI); Bokuchava, Papushkin (FLNP JINR) — *Автоматизация в
промышленности*, Feb 2019. The instrument paper for 04: the benchtop **Spectroelph-FRR**.
Needle transducer ⌀2–3 mm in U7–U10 steel, 30 mm measuring rod, sliding at 0.5–2.2 mm/s,
sensitivity 0.01 µV, TI ADS1262 32-bit ADC giving ~7 nV limiting resolution, 40 dB
programmable amplitude discriminator, 1 Hz acquisition, ElphysLAB-IDS processing. The
measurement principle is that the mechanical contact surface *is* the sensing element —
the informative signal forms at contact spots whose number depends on contact-interaction
intensity and on surface waviness and roughness. *Note: the filename and the printed title
differ; both are recorded in the summary header.*

## 07 — Influence of Environmental Parameters on NDT by the CPD Method

Oleshko (Moscow Aviation Institute) — *Проблемы машиностроения и надёжности машин*, 2020,
No. 6. The practical-error paper: how much ambient conditions move a CPD reading. 314
measurement sessions on 99%-pure Al, Ti and Ni with a "Поверхность-11" Kelvin probe
(Ni electrode, 410 Hz) across t = 14–29 °C, RH = 19–59 %, p = 963–1022 hPa. **Temperature
dominates**: −6 mV/°C (Al), −14 mV/°C (Ti), −9 mV/°C (Ni), against mean CPD values of 874,
284 and 208 mV. Humidity and pressure effects are weak, and humidity even changes sign by
metal (acceptor for Al and Ti, donor for Ni). Recommends measuring under stable normal
conditions or applying the tabulated correction coefficients — and notes that Ni is the
least environment-sensitive metal, which is why measuring electrodes are made of it. The
article contains no figures at all; this was confirmed page by page.

## 08 — Review of Welded Joint Quality Control Methods

Труды Международного симпозиума «Надёжность и качество», 2017, vol. 2. A compact,
numbers-dense survey of eight classical weld-inspection methods: visual, radiographic
transillumination (X-ray and gamma), ultrasonic, kerosene test, magnetographic,
fluorescent and dye-penetrant, chemical-reaction, and hydraulic testing — each with its
sensitivity limits and blind spots. X-ray: ≤60 mm thickness at 0.5–3 % of thickness;
gamma: ≤100 mm at 2–5 %; ultrasonic: 0.8–2.5 MHz, limiting sensitivity 0.2–2.5 / 2–7 /
3.5–15 mm² across three thickness bands. Useful as the baseline that 05 and 09 argue
against. *Source caveat: the PDF is a 3-page proceedings extract whose pages 1 and 3 carry
fragments of two unrelated articles (PCB manufacturing; audio dynamics processing); only
the span between the two УДК markers is summarized, and the two figures in the extract
belong to the following article.*

## 09 — Method for Local Detection of Flaws and Device for Realizing It

**WO 2017/180007 A1**, PCT/RU2016/000213, IPC G01N 27/61 — inventor V. I. Surin. The
patent that claims the method the rest of the corpus develops. Passive electromagnetic
flaw detection by SCP: the CPD between two points of the object is measured with **no
current passed and no voltage applied**, decomposed by DFT and continuous wavelet
transform, denoised, and its amplitude-frequency characteristic compared against that of a
flaw-free reference. All 15 claims translated in full (method, two device variants, and a
complete system), 9 drawings described, and a 28-entry reference-numeral index. Contact
physics: real contact spots 0.1–40 µm, real bimetallic contact area 10⁻⁴–10⁻¹ of nominal
and never above 40 %. D16T fatigue signal rises from 1–2 µV at 1.5·10³ cycles to 60 µV at
3·10³. Includes the international search report (X-category WO 2004/070355 A2, Qcept
Technologies, against claims 1–2). *Three internal inconsistencies in the source are
recorded rather than fixed, including a divergence between claim 1 and the
statement-of-invention over "processed" vs "registered" signal.*

---

## The thread running through the corpus

Read in this order, the papers form one argument:

1. **The gap.** Conventional NDT has a floor. Ultrasound holds 31.57 % of the flaw-detection
   market (09) but cannot report real defect size, fails on coarse-grained metal and
   austenitic seams over 60 mm, and misses cracks whose opening is only 5–10 µm (05).
   The classical methods and their limits are tabulated in 08 and, far more thoroughly,
   in 01.
2. **The physics.** Contact potential difference is set by the work-function difference
   between two surfaces, and the Kelvin vibrating-capacitor method measures it by nulling
   (02). The quantum-transport treatment of the tunneling analogue (03) shows what such a
   nulled potentiometric measurement does and does not correspond to — and warns that it
   is not a well-defined thermodynamic potential.
3. **The method.** Scanning contact potentiometry applies this to a loaded metal surface,
   where the contact spots between a sliding transducer and the object act as the sensing
   element (06, 09).
4. **The instrument.** Spectroelph-FRR / EDSS-1 with ElphysLAB-IDS, µV-to-nV sensitivity,
   spectral and wavelet decomposition of the signal (06, 05, 09).
5. **The validation.** Simultaneous SCP and neutron diffraction on 12Kh18N10T: SCP flags
   the martensite precursor at 400–600 MPa, 50–250 MPa before diffraction confirms the
   phase (04).
6. **The caveat.** Ambient temperature alone shifts a CPD reading by 6–14 mV/°C against
   signals of 200–900 mV, so field measurement demands controlled conditions or explicit
   correction (07).
7. **The claim.** All of it is claimed in WO 2017/180007 A1 (09).

**Recurring authorship.** V. I. Surin (NRNU MEPhI) is an author of 04, 05 and 06 and the
sole inventor of 09; Abu Ghazal, Shef, Bokuchava and Papushkin recur across 04 and 06. The
Russian-language group of papers is therefore a single research programme, not independent
sources — 04 and 06 describe the same experimental campaign from the results side and the
instrument side respectively.

**Terminology.** Russian sources were translated with a consistent glossary
(контактная разность потенциалов → contact potential difference; работа выхода → work
function; сканирующая контактная потенциометрия → scanning contact potentiometry;
неразрушающий контроль → non-destructive testing). Each Russian summary carries its own
Terminology notes section. Alloy grades are transliterated (12Х18Н10Т → 12Kh18N10T,
Д16Т → D16T) with the Cyrillic form given on first use.
