# Measuring electronics for the SCP contact-matrix cell — verified component selection

**Date:** 2026-09-17  
**Scope:** single lab cell, 4–8 gold-plated pogo pins against one common reference pin, 0.1–10 µV DC signals, prototype only (no cost/size/scaling optimisation).  
**Method:** deep-research workflow (5 search angles → 22 sources fetched → 109 claims extracted → 25 top claims put through 3-vote adversarial verification: 23 confirmed, 2 refuted), followed by a manual read of the ADS1262/ADS1263 datasheet (SBAS661B mirror) for the input-current rows the workflow had left unverified. Numbers below are datasheet/handbook values unless marked *inferred*.

**Repo context used:** summaries 04/05/06/09 in `summaries/` — the original Spectroelph-FRR chain was transducers → multiplexer → differential preamp (gain ≈30) → TI ADS1262 32-bit ΔΣ at 2.5 SPS (23.5 noise-free bits, ≈7 nV limiting resolution, Vref 2.5 V, SPI) → PC, 1 Hz acquisition; signals 1–60 µV over a ≈±1 µV raw noise band; U10-steel needle transducers, reference = machine ground; EDSS-1 also used with a nanovolt-reading benchtop DMM.


## 1. Recommendation


**Path B — TI ADS1263 placed next to the contact matrix, read over SPI by a Raspberry Pi.** Same ADC family the original instrument used; its internal 10-input multiplexer plus AINCOM maps directly onto "each pin against one common reference", so no external switch is needed. Path A (mux + external DMM) is kept only as a one-channel metrology cross-check: no in-stock switch except the Keithley 7168 scanner card has a thermal EMF specified below the signal.

In every architecture the ADC/DMM is **not** the limiting element. The pogo-pin fixture (BeCu ≈5 µV/°C vs Cu; Au–Cu 0.3 µV/°C; Cu–CuO ≈1 mV/°C) and nA-class input currents into kΩ–MΩ oxidised contacts dominate the error budget.


## 2. Recommended components (Path B)


| # | Component | Key numbers (verified) | Why it fits / notes |
|---|---|---|---|
| 1 | **TI ADS1263** 32-bit ΔΣ ADC, PGA 1–32, global chop, 10 inputs + AINCOM | Gain 32: noise 6 nV rms / 23 nV p-p at 2.5 SPS Sinc3 (11 nV rms FIR), 13 nV rms / 65 nV p-p at 10 SPS Sinc4, 17–30 nV rms at 20 SPS. Chop on: offset ±0.1/G µV typ, ±0.5/G max (≈±3 nV typ / ±16 nV max at G=32); drift 1 nV/°C typ, 5 max. Chop off: 350/G µV offset, 30/G+10 nV/°C. Absolute input current 2 nA typ, differential 0.1 nA typ, 1 GΩ diff. impedance (PGA on); 150 nA / 40 MΩ PGA bypassed. Chop halves the effective data rate and cuts noise ×1.4. Bipolar ±2.5 V or single 5 V analog supply. | Noise and drift are 1–2 orders below the 0.1–10 µV signal. Internal mux does the pin scanning. Chop switch sits **after** the mux (mux is on-die, near-isothermal, but outside the chop loop and unspecified for thermal EMF). |
| 2 | **TI ADS1263V2EVM-PDK** (primary board) | Digi-Key 296-ADS1263V2EVM-PDK-ND, status Active, $393.74, 19 in stock, 12-week lead time, max 10 per 30 days (2026-09-17). Original ADS1262EVM-PDK / ADS1263EVM-PDK are Obsolete. Distributor listing: board + cable, user guide SBAU206B. | TI-designed supply/reference layout. TI's own tool page returned HTTP 403, so the host-board contents could not be read; plan to tap the SPI header for the Pi. |
| 3 | **Waveshare High-Precision AD HAT** (low-cost fallback) | ≈$33; genuine ADS1263 (24-bit ADC2 present); SPI on BCM GPIO 10/9/11, DRDY 17, RESET 18, CS 22; screw-terminal + header inputs; AVDD = Pi 5 V via 0 Ω link R23, 47 Ω / 47 pF / 100 nF input RC, no preamp; Waveshare spec claims only "accuracy ≥1.65 mV". Schematic + demo code on the wiki. | Usable only after replacing the Pi-5 V AVDD feed with a clean linear/battery supply and adding an isothermal copper input block. With unipolar 5 V the common reference pin must be biased to ≈2.5 V; with bipolar ±2.5 V it can sit at 0 V. |
| 4 | **Raspberry Pi 4/5** host over SPI | 5–10 SPS with chop → ≈1–2.5 Hz effective, averaged to the 1 Hz record of the original method. | Any SPI-capable MCU works equally. |
| 5 | **Isothermal copper input block + Cu-to-Cu wiring** | Seebeck vs Cu: Cu–Cu ≤0.2, Au 0.3, Ag 0.3, brass 3, BeCu 5, Pb/Sn solder 1–3, Kovar 40–75, CuO ≈1000 µV/°C. | All pins and the reference pin clamp into one copper block; crimped copper twisted pair; no solder, nickel or Kovar in the signal path; 2–2.5 h warm-up. Keithley names BeCu / phosphor-bronze spring contacts explicitly as a hazard. |
| 6 | **Keithley 2182A nanovoltmeter** (validation reference, 10 mV range, ch. 1) | 1 nV resolution; 6 nV p-p at 25 s response, 25 nV p-p at 1 s, 70 nV p-p at 60 ms; noise vs source R: 8 nV @100 Ω, 15 nV @1 kΩ, 35 nV @10 kΩ, 100 nV @100 kΩ, 350 nV @1 MΩ; <60 pA bias; 1-yr ±(50 ppm rdg + 4 ppm range) with REL; 2.5 h warm-up. Channel 2 has no 10 mV range. Current product. | Wire in parallel with one pin pair to confirm the ADS1263 channel agrees within ≈50 nV and to measure the true noise floor vs contact resistance. |


## 3. Path A alternatives (verified, not recommended as the primary scanner)


| Component | Key numbers | Verdict |
|---|---|---|
| **Keithley 7168** nanovolt scanner card (+ 7001/7002 mainframe) | 8 ch, 2-pole, JFET switches; <30 nV HI–LO contact potential zeroed (<60 nV unzeroed), <6 nV/°C, <50 pA leakage, <12 Ω; 2 h warm-up. Keithley: "noise and drift performance of the 2182A is not degraded" (unquantified, 2-1 vote). | The only switch with a spec that fits. 7001/7002 no longer listed by Tek; 7168 "price on request" — availability unconfirmed. |
| **Pickering Series 100** reed relay, 100-1-A-5/2D (Switch No. 2, ruthenium) | 0.12 Ω max initial CR; ~1e9 ops cold-switched; Farnell 3975776, ~198 in UK stock. Thermal EMF only "about 1 µV or less", no conditions; "controlled thermal EMF" is a custom build option. Pickering dwell test (Series 120): −0.38 µV at 0 s → −46 µV after 600 s coil-on. | Thermal EMF is the same order as the signal. Only with latching/short-dwell drive plus channel-reversal / zero subtraction. |
| **ADG1408 / ADG1409** iCMOS mux (±15 V) | On-leakage ±0.1 nA typ, ±1.5 nA max (25 °C), ±3 nA (85 °C); off-source ±0.2 nA max; measured at ±10 V bias (conservative). No thermal-EMF / offset spec at all. | 1.5 nA × 1 kΩ = 1.5 µV; 3 nA × 1 MΩ = 3 mV. Only for metallic contacts, and its thermal offset must be measured by the user. |
| **AD7124-8** (EVAL-AD7124-8), 24-bit, PGA 128, 16-ch mux | 17–24 nV rms / 0.09–0.14 µV p-p at 1.17–9.4 SPS, G=128; no chopper: 200/G µV uncalibrated offset (≈1.6 µV), 10 nV/°C typ drift; input current ±1/±1.2/±3.3 nA (low/mid/full power); per-channel rate drops to 2.34 SPS in zero-latency multi-channel mode. | Viable second choice for Path B; ≈3× noisier, 10× more drift, needs periodic recalibration instead of chop. |
| **ADS1235 / ADS1261** | G=128, chop off: 5 nV rms / 14 nV p-p at 2.5 SPS Sinc3, 10 nV rms at 10 SPS; chop on: drift 1 nV/°C typ, 5 max; absolute input current 4 nA typ / 6 nA max (200 nA PGA bypass), 1 GΩ; gains 1/64/128 only. | Noise-equivalent to ADS1263 but 2–3× the input current; 4 nA × 1 MΩ = 4 mV. |


## 4. Design constraints (any path)


1. **Thermal-EMF budget.** With BeCu pin bodies at ≈5 µV/°C, a 0.02 °C gradient along a pin equals the 0.1 µV floor and 1 °C equals half the full signal range. One isothermal copper block, copper-only signal path, 2–2.5 h warm-up, periodic zeroing at working temperature.
2. **Contact-resistance gate.** The ADS1263's 2 nA absolute input current flows through each pin's contact resistance; error ≈ I × (R_pin − R_ref). 50 Ω mismatch ≈ 0.1 µV; 1 kΩ ≈ 2 µV; 1 MΩ ≈ 2 mV. Four-wire check every pin before each scan; re-seat anything above a few tens of ohms.
3. **Chop on, PGA 32, ≤10 SPS.** Without chop the ADS1263 offset is ≈11 µV at G=32 with ≈11 nV/°C drift; offset-calibration register is disabled in chop mode. 20 SPS FIR p-p noise (167 nV) already exceeds the 0.1 µV floor.
4. **Drift handling.** All quoted noise figures are 10 s to 2 min windows at 25 °C; hours-long SCP drift must be separated by slow reference-channel subtraction or pin-reversal, not longer averaging. The original ±1 µV raw band is 2 orders above the ADC noise and must originate in the contacts/thermal path.
5. **Switching discipline.** Cold-switch only; prefer the ADC's internal mux or a JFET scanner; if relays are used, latching types or short coil-on dwell, then wait for thermal equilibrium.


## 5. Physics flag (*inferred*, no source survived verification)

With ohmic pogo-pin contact at uniform temperature, a DC voltmeter cannot read a true Volta contact potential difference (law of intermediate metals). What the cell records is thermoelectric EMF plus oxide/adsorbate-film potentials at the contact spots. This is consistent with the SCP literature's own contact-spot / electrical-double-layer explanation and with the µV magnitudes, but it makes the isothermal block part of the experiment rather than good practice. The Volta's-law discussion and thermoelectric-power weld NDT prior art produced no verified claims and remain open.


## 6. Verified findings (full evidence)

### F1. PATH B core (recommended): TI ADS1262/ADS1263 32-bit ΔΣ ADC in global-chop mode, PGA gain 32, 2.5–10 SPS. Datasheet input-referred noise at…

**Confidence:** high · **Vote:** 3-0 and 3-0 (claims 9 and 10 merged)

**Claim.** PATH B core (recommended): TI ADS1262/ADS1263 32-bit ΔΣ ADC in global-chop mode, PGA gain 32, 2.5–10 SPS. Datasheet input-referred noise at gain 32 (ADC1, 25 °C, shorted inputs): 6–11 nV rms (23–51 nV p-p) at 2.5 SPS depending on filter (Sinc3/Sinc4 lowest, FIR highest), 13 nV rms (65 nV p-p) at 10 SPS Sinc4, 17–30 nV rms (98–167 nV p-p) at 20 SPS; headline 7 nV rms at 2.5 SPS. With chop on: offset ±0.1/Gain µV typ, ±0.5/Gain max (≈±3 nV typ / ±16 nV max at G=32) and drift 1 nV/°C typ, 5 nV/°C max over −40..+125 °C; with chop off: offset 350/Gain µV typ (≈11 µV at G=32) and drift 30/Gain+10 nV/°C. Chop cuts noise a further 1.4×, disables the offset-calibration register and lowers the effective data rate (negligible for FIR at 2.5 SPS; Sinc4 at the 2.5 SPS setting falls to ~0.6 SPS). The ADC's own noise and drift are therefore 1–2 orders below the 0.1–10 µV SCP signal and the ±1 µV raw band, and chop mode is effectively mandatory for hours-long drift.

**Evidence.** Verified in two revisions (SBAS661B 2015 and current SBAS661C May 2021), identical numbers: Table 8-1 gain-32 column 2.5 SPS FIR 0.011 (0.051), Sinc3 0.006 (0.023); 10 SPS Sinc4 0.013 (0.065); 20 SPS Sinc4 0.017 (0.098), FIR 0.030 (0.167) µVrms (µVpp); Sec. 7.5: VOS chop on ±0.1/Gain typ, ±0.5/Gain max µV; drift chop on 1 typ / 5 max nV/°C, chop off 30/Gain+10 typ / 100/Gain+50 max; Sec. 8.8/9.4.12 'noise reduced by a factor of 1.4 with chop mode', 'offset calibration register is disabled in chop mode'. Qualifications: noise values are typical, taken over 10 s or 8192 points (so mHz 1/f and hour-scale drift are excluded); datasheet does not state whether Table 8-1 is chop-on or off; at 20 SPS FIR the 167 nV p-p exceeds the 0.1 µV low end of the signal, so use ≤10 SPS.

**Sources.** <https://www.ti.com/lit/ds/symlink/ads1262.pdf>

### F2. ADS1263 hardware is in stock in 2026. (a) TI ADS1263V2EVM-PDK: Product Status Active, Digi-Key 296-ADS1263V2EVM-PDK-ND, $393.74 per kit, 19…

**Confidence:** high · **Vote:** 3-0 ×4 (claims 11, 12, 13, 14 merged)

**Claim.** ADS1263 hardware is in stock in 2026. (a) TI ADS1263V2EVM-PDK: Product Status Active, Digi-Key 296-ADS1263V2EVM-PDK-ND, $393.74 per kit, 19 in stock, 12-week manufacturer lead time, 10-per-30-days purchase cap (TI store lists $314.99 but shows out of stock; the original ADS1262EVM-PDK and ADS1263EVM-PDK are Obsolete). (b) Waveshare 'High-Precision AD HAT' (SKU 18983, $32.95–34.99 on the Waveshare store): a genuine ADS1263 Raspberry Pi HAT with 10 single-ended / 5 differential inputs, 38.4 kSPS max, PGA to 32, 2.5 V internal reference, 24-bit ADC2, IDAC, test DAC, SPI on the 40-pin header (CS/DRDY/RESET on GPIO22/17/18). The HAT feeds AVDD straight from the Pi 5 V rail through a 0 Ω link, has only 47 Ω/47 pF/100 nF input RC and no preamp, and Waveshare's own spec table claims only 'Accuracy ≥1.65 mV (under 3.3 V range)' — no µV/nV figure anywhere in the wiki, store page or schematic — so all sub-µV performance must be taken from the TI datasheet and the board needs an external clean supply/reference and an isothermal copper input block before it can be trusted at nV level.

**Evidence.** Digi-Key page re-fetched 2026-09-16/17: 'Product Status: Active', 'In-Stock: 19', '$393.74000 per box', standard package 1, 'Maximum 10 boxes per 30-day period', lead time 12 weeks. Waveshare wiki spec block verbatim: Resolution 32 bits, 10 channels, 38.4 kSPS, PGA 32, 'Accuracy ≥1.65mV (under 3.3V range)'; full-text scan gave zero hits for µV/nV/ENOB. Waveshare schematic (14 Dec 2020) shows U1 'ADS1263/2' 28-pin, AVDD=RPI_5V via R23 0R, IN0–IN9+INCOM through 47 R/47 pF, RT9193-33 LDO for DVDD; 24-bit ADC2 exists only on the ADS1263, confirming the fitted part. Caveat: Digi-Key keyword search did not list the Waveshare HAT and Mouser timed out, so its availability rests on Waveshare's own store; Digi-Key stock is thin and should be rechecked at order time.

**Sources.** <https://www.digikey.com/en/products/detail/texas-instruments/ADS1263V2EVM-PDK/20414007> · <https://www.waveshare.com/wiki/High-Precision_AD_HAT> · <https://files.waveshare.com/upload/f/f7/High-Precision_AD_HAT.pdf> · <https://www.ti.com/lit/ds/symlink/ads1262.pdf>

### F3. PATH B alternative: Analog Devices AD7124-8 (24-bit, PGA to 128, 16-channel internal mux, EVAL-AD7124-8). At gain 128 the lowest-rate noise…

**Confidence:** high · **Vote:** 3-0 ×3 (claims 15, 16, 17 merged)

**Claim.** PATH B alternative: Analog Devices AD7124-8 (24-bit, PGA to 128, 16-channel internal mux, EVAL-AD7124-8). At gain 128 the lowest-rate noise is 17–24 nV rms / 0.09–0.14 µV p-p: 23 nV rms (0.14 µV p-p, 18.1 bits p-p on ±19.53 mV) at 9.4 SPS full power sinc4, 17 nV rms (0.09 µV p-p) sinc3, 20 nV rms (0.10 µV p-p) at 2.34 SPS mid power, 24 nV rms (0.12 µV p-p) at 1.17 SPS low power; when several channels are enabled the ADC runs in zero-latency mode and the per-channel rate at the 9.4 SPS setting drops to 2.34 SPS (sinc4). It has no chopper: uncalibrated offset is 200/gain µV (≈1.6 µV at G=128), reduced to the noise level by internal/system zero-scale calibration; offset drift 10 nV/°C typ (full power, all gains; 20–80 nV/°C at gains 2–16 in low/mid power), gain drift 1 ppm/°C typ / 2 max, recalibration at temperature removes the drift. With PGA on (buffers forced on) absolute input current is ±1 / ±1.2 / ±3.3 nA (low/mid/full power), differential ±0.2 / ±0.4 / ±1.5 nA, 25 pA/°C drift — so a 1 MΩ oxidised contact gives ~1 mV error, a metallic contact negligible error. Worse than the ADS1263 on noise (≈3×), drift (10× typ) and input current, and its 200/gain µV offset must be periodically recalibrated rather than chopped.

**Evidence.** AD7124-8 datasheet Rev. F (4/2023, current). Front-page features and Tables 8/9/10/18/28 give exactly the quoted noise/ODR/zero-latency numbers ('These numbers are typical and are generated with a differential input voltage of 0 V when the ADC is continuously converting on a single channel'). Table 3: Analog Input Current, Gain > 1 or Gain = 1 (Buffered): ±1 nA/±0.2 nA (low), ±1.2/±0.4 (mid), ±3.3/±1.5 (full), 25 pA/°C; footnote 11 'When the gain is greater than 1, the analog input buffers are enabled automatically'. Offset Error Before Calibration ±15 µV (G=1–8), 200/gain µV (G=16–128), 'After Internal/System Calibration: In order of noise'; drift rows 10/80/40 nV/°C (low), 10/40/20 (mid), 10 (full); Gain Error Drift 1 typ, 2 max ppm/°C; footnote 6 'Recalibration at any temperature removes these errors'. The string 'chop' occurs zero times in the datasheet. All drift/current figures are typical-only (no max).

**Sources.** <https://www.analog.com/media/en/technical-documentation/data-sheets/ad7124-8.pdf>

### F4. PATH B alternative: TI ADS1235 (and the closely related ADS1261). Chop-mode offset drift 1 nV/°C typ / 5 nV/°C max (−40..+125 °C), 10 / 50 n…

**Confidence:** high · **Vote:** 3-0 ×3 (claims 18, 19, 20 merged)

**Claim.** PATH B alternative: TI ADS1235 (and the closely related ADS1261). Chop-mode offset drift 1 nV/°C typ / 5 nV/°C max (−40..+125 °C), 10 / 50 nV/°C without chop at gain 64/128, gain drift 0.5 ppm/°C typ / 4 max, chop-mode offset ±0.2/Gain µV (ADS1261 adds long-term drift ±0.1 µV/1000 h at G=1). Table 1 noise at gain 128 (VREF 5 V, chop off): 5 nV rms (14 nV p-p) at 2.5 SPS Sinc3, 10 nV rms (42 nV p-p) at 10 SPS Sinc4, 18 nV rms (100 nV p-p) at 20 SPS Sinc4; 8 nV/√Hz input noise density at gain 64/128; chop divides these by √2 at the cost of halving the effective rate. Input current in PGA mode: absolute 4 nA typ / 6 nA max (200 nA in PGA bypass), 0.01 nA/°C; differential ±0.1 nA at VIN=39 mV, rising to ±5 nA in PGA+chop at VIN=2.5 V (scales with data rate); 1 GΩ differential input impedance. With the SCP topology (each pin vs one shared reference, unbalanced source resistances) the 4 nA absolute current gives 4 mV at 1 MΩ and ~4 µV at 1 kΩ, so a contact-resistance check is mandatory; drift alone (≤25 nV over ±5 °C at the max spec) stays under the 0.1 µV floor. Noise-wise comparable to the ADS1263 but with higher input current and only gains 1/64/128.

**Evidence.** ADS1235 datasheet SBAS824 (Oct 2018, only revision as of the Aug-2025 archive copy) Sec. 6.5: Offset voltage drift G=64/128 10 typ/50 max nV/°C; Chop mode 1 typ/5 max; Gain drift 0.5/4 ppm/°C; VOS chop mode ±0.2/Gain µV typ; Absolute input current PGA mode 4 typ/6 max nA, PGA bypass 200 nA; Differential input current PGA mode VIN=39 mV ±0.1 nA, PGA+Chop VIN=2.5 V ±5 nA (footnote: 'Chop-mode input current scales with data rate'); Differential input impedance PGA mode 1 GΩ. Table 1: 2.5 SPS Sinc3 G128 0.005 (0.014); 10 SPS Sinc4 0.01 (0.042); 20 SPS Sinc4 0.018 (0.1) µVrms (µVpp); Sec. 7.1 'noise decreases by √2' in chop mode; 'Divide the noise data values shown in Table 1 by √2 to derive the chop mode noise' confirms Table 1 is chop-off. ADS1260/1261 SBAS760C (Jan 2019) Sec. 7.5 carries identical drift/gain-drift rows plus long-term drift ±0.1 µV/1000 hr. Noise values are typical, 10 s / 8192-point windows.

**Sources.** <https://www.ti.com/product/ADS1235> · <https://www.ti.com/lit/ds/symlink/ads1235.pdf> · <https://www.ti.com/lit/ds/symlink/ads1261.pdf>

### F5. PATH A reference instrument: Keithley 2182A nanovoltmeter, channel 1, 10 mV range — 1 nV resolution, >10 GΩ input resistance, DC input bias…

**Confidence:** high · **Vote:** 3-0 ×3 (claims 2, 3, 4 merged)

**Claim.** PATH A reference instrument: Keithley 2182A nanovoltmeter, channel 1, 10 mV range — 1 nV resolution, >10 GΩ input resistance, DC input bias current <60 pA at 23 °C, 1-year accuracy ±(50 ppm of reading + 4 ppm of range) i.e. a 40 nV range term when zeroed with REL (add 100 nV if REL is not used), tempco (1 ppm rdg + 0.5 ppm range)/°C ≈ 5 nV/°C near zero, 2.5 h warm-up to rated accuracy, autozero and 1 PLC/10-reading or 5 PLC/2-reading filter required. Specified DC noise (p-p, 60 Hz, 2188 low-thermal short, ±1 °C): 6 nV at 25 s response (5 PLC, 75-reading filter; 'guaranteed by design'), 25 nV at 1.0 s (1 PLC, 18 filter), 70 nV at 60 ms (filter off); 100 mV range 25 nV / 175 nV / 300 nV. Noise vs source resistance (10 mV, 5 PLC, 100-reading filter, 2-min window): 6 nV p-p at 0 Ω, 8 nV at 100 Ω, 15 nV at 1 kΩ, 35 nV at 10 kΩ, 100 nV at 100 kΩ, 350 nV at 1 MΩ (analog filter on above 10 kΩ). The noise floor therefore stays under 0.4 µV p-p even at 1 MΩ, but the 60 pA bias current alone produces up to 60 µV of DC offset at 1 MΩ (6 µV at 100 kΩ), so oxidised MΩ contacts are unacceptable even with this instrument. Channel 2 has no 10 mV range, so the 2182A natively covers only one nanovolt-class pin; the 2182A remains a current, orderable product (tek.com 2026).

**Evidence.** SPEC-2182A Rev. F (Dec 2016, still the linked spec on tek.com) p.1 row '10.000000 mV | 1 nV | >10 GΩ | 20+4 | 40+4 | 50+4 | 60+4 | (1+0.5)/°C', footnote 3 'When properly zeroed using the relative offset (REL) function. If REL is not used, add 100 nV to the range accuracy', 'Warm-up 2.5 hours to rated accuracy', 'DC Input Bias Current: <60pA DC at 23°C'. DC NOISE PERFORMANCE table p.2: '25.0 s | 5, 75 | 6 nV(12) | 25 nV', '1.0 s | 1, 18 | 25 nV | 175 nV', '60 ms | 1, off | 70 nV | 300 nV'; footnote 9 '2188 low thermal short after 2.5 hour warm-up, ±1 °C', observation time ≤2 min; footnote 12 'Guaranteed by design'. VOLTAGE NOISE VS. SOURCE RESISTANCE: 0 Ω 6 nV Off; 100 Ω 8 nV; 1 kΩ 15 nV; 10 kΩ 35 nV; 100 kΩ 100 nV On; 1 MΩ 350 nV On. Cross-checked against the older TestEquity-hosted datasheet (identical). Johnson-noise sanity check: 1 MΩ in ~0.06 Hz ENBW ≈ 200 nV p-p, consistent with 350 nV spec. The 2-min window means hours-long drift in the SCP use case will exceed these p-p figures.

**Sources.** <https://download.tek.com/document/SPEC-2182A_DEC2016.pdf> · <https://download.tek.com/datasheet/2182A-15912.pdf>

### F6. PATH A scanner reference design: Keithley 7168 nanovolt scanner card — 8 channels, 2-pole (HI and LO), solid-state JFET switches, contact po…

**Confidence:** high · **Vote:** 3-0 (claim 0)

**Claim.** PATH A scanner reference design: Keithley 7168 nanovolt scanner card — 8 channels, 2-pole (HI and LO), solid-state JFET switches, contact potential HI-to-LO between channels <30 nV when zeroed with the supplied copper leads, typically <60 nV without zeroing, temperature coefficient <6 nV/°C between channels, input leakage <50 pA/channel at 23 °C, contact resistance <12 Ω, 2 h warm-up in the mainframe (4 h for the nanovoltmeter); requires a 7001/7002 switch mainframe. This is the thermal-EMF budget a low-level switching front end should be judged against (~30 nV, i.e. ≥30× below the 1 µV SCP signal). Availability is doubtful in 2026: 7001/7002 no longer appear on Tek's 700-series page (7002-HD maps to the 3706A in Tek's replacement list) and the 7168 is 'price on request' at resellers.

**Evidence.** Keithley 7168 datasheet (Dec 2011, identical reseller and Tek-hosted copies): 'CHANNELS PER CARD: 8. CONFIGURATION: Two poles per channel, input HI and LO ... CONTACT POTENTIAL (HI to LO) BETWEEN CHANNELS: <30nV when properly zeroed with supplied leads ... Typically <60nV without zeroing. CONTACT TYPE: Solid state JFET switch', leakage <50 pA/channel, 'WARM-UP: 2 hours in mainframe', 'Use with 7001 and 7002'. Instruction Manual Rev. C adds 'Temperature Coefficient: <6nV/°C between channels', sec. 2.6.7 (zero correction valid only at the temperature at which it was performed; nanovoltmeter drift not corrected; uncorrected accuracy ~10 % at 1 µV) and sec. 2.6.6 (1 h wait after switching >1 mA due to JFET self-heating — irrelevant at zero current). Keithley's ReplacementProducts.pdf (2013) names the 7168 as the replacement for the 7059/7064, and Newark still lists it (59T8907), but Newark/Mouser/RS returned 403 so 2026 new-stock status is unconfirmed. Note: a related claim that the JFET/50 pA design 'shows a semiconductor switch can be used in a nanovolt scanner if leakage is tens-of-pA class' was refuted (1-2) as an over-generalisation, so the 7168's performance should not be extrapolated to CMOS muxes.

**Sources.** <https://www.finaltest.com.mx/v/vspfiles/assets/datasheet/7168.pdf> · <https://download.tek.com/datasheet/7168.pdf> · <https://download.tek.com/manual/7168%5F901%5F01C.pdf>

### F7. Keithley states that when the 7168 is used with the 2182A 'the noise and drift performance of the 2182A is not degraded', i.e. a scanner-plu…

**Confidence:** medium · **Vote:** 2-1 (claim 1)

**Claim.** Keithley states that when the 7168 is used with the 2182A 'the noise and drift performance of the 2182A is not degraded', i.e. a scanner-plus-nanovoltmeter chain can in principle retain the DMM's native nV-level performance — but the statement is unquantified and the 7168's own 30–60 nV offset, <6 nV/°C tempco and 50 pA leakage are the same order as the meter's 40 nV range term, ~5 nV/°C tempco and 60 pA bias, so in practice the chain roughly doubles the meter's offset/drift/leakage budget (still far below the 0.1–10 µV signal for metallic contacts, but 50 pA × 100 kΩ = 5 µV for an oxidised contact).

**Evidence.** Quote verified verbatim in the 7168 datasheet. Verifier noted it carries no test condition, does not appear in the 1991 manual (written for the 705/706 mainframes and Model 181), and no independent measurement was found (EEVblog teardown reports no numbers; xDevs kei7168 'Results' section is empty). Numeric comparison with SPEC-2182A: 10 mV 1-yr range term 40 nV (REL), tempco ≈5 nV/°C, bias <60 pA vs 7168 <30/60 nV, <6 nV/°C, <50 pA. Split 2-1 vote reflects the unquantified nature of the manufacturer sentence, not a contradiction.

**Sources.** <https://www.finaltest.com.mx/v/vspfiles/assets/datasheet/7168.pdf> · <https://download.tek.com/document/SPEC-2182A_DEC2016.pdf>

### F8. Low-thermal reed relay option (Pickering Series 100 SIL, CMOS-drive): the low-level variant 100-1-A-5/2D (1 Form A, dry reed, Switch No. 2,…

**Confidence:** high · **Vote:** 3-0 ×2 (claims 5, 6 merged)

**Claim.** Low-thermal reed relay option (Pickering Series 100 SIL, CMOS-drive): the low-level variant 100-1-A-5/2D (1 Form A, dry reed, Switch No. 2, vacuum-sputtered ruthenium contacts) has 0.12 Ω max initial contact resistance, 10 W / 0.5 A / 200 V ratings, ~1e9 operations to a 1 Ω end-of-life criterion when cold-switched, and is explicitly recommended by Pickering for low-current/low-voltage and cold-switching ATE use — matching zero-current potential scanning; Farnell lists it (order code 3975776, ~198 units UK stock). However its thermal EMF is stated only as a headline 'about 1 µV or less' with no tabulated min/max, no coil-on dwell, ambient or coil-voltage condition; a characterised value exists only as the custom 'Controlled thermal EMF' build option with a unique part-number suffix. A stock Series 100 therefore has a thermal offset of the same order as the 0.1–10 µV SCP signal and ~30× worse than the 7168's 30 nV class, unless the controlled-EMF option, latching/short coil-on dwell, or channel-reversal / zero-subtraction measurement is used. Pickering's own Sept-2026 test on a sibling series (120) showed thermal EMF growing from −0.38 µV at 0 s to −46 µV after 600 s of coil-on dwell, so coil self-heating and dwell time dominate.

**Evidence.** Series 100 datasheet Issue 2.1 (May 2025): only thermal statement is the bullet 'Thermal EMF about 1 μV or Less'; no spec-table row; 'Controlled thermal EMF' listed under Electrical Build Options with 'you will be allocated a unique part number suffix'. Coil table: 100-1-A-3/5/12/24/2D, 1 Form A Switch No.2 max initial contact resistance 0.12 Ω; switch-ratings row 2: 10 W, 0.5 A, 1.2 A carry, 200 V, 'Low level'; Note 1: 'For an end of life contact resistance specification of 1 Ω, switching low loads (10 V at 10 mA resistive) or when cold switching, typical life is approx 1 x 10^9 ops'; 'Switch no.2 is particularly good for switching low currents and/or voltages. It is the ideal switch for A.T.E. systems where cold switching techniques are often used.' Series 103 datasheet confirms switch no.2 = vacuum-sputtered ruthenium 'ideal for very low level or cold switching'. Pickering product/low-thermal pages repeat 'about 1 microvolt or less' with no conditions. Pickering Series 120-vs-competitor test (Keysight 34465A, 10 NPLC, 600 s) shows the dwell dependence; Series 100 was not in that test.

**Sources.** <https://www.pickeringrelay.com/pdfs/100-low-thermal-cmos-drive-sil-reed-relays.pdf> · <https://www.pickeringrelay.com/pdfs/103-low-capacitance-coaxial-sil-reed-relays.pdf> · <https://download.tek.com/datasheet/7168.pdf>

### F9. CMOS analog mux option (Analog Devices ADG1408 8:1 / ADG1409 dual 4:1, iCMOS, ±15 V): at VDD/VSS = ±16.5 V the ON-channel leakage is ±0.1 nA…

**Confidence:** high · **Vote:** 3-0 ×2 (claims 7, 8 merged)

**Claim.** CMOS analog mux option (Analog Devices ADG1408 8:1 / ADG1409 dual 4:1, iCMOS, ±15 V): at VDD/VSS = ±16.5 V the ON-channel leakage is ±0.1 nA typ, ±1.5 nA max (25 °C), ±3 nA max (−40..+85 °C); OFF source leakage ±0.04 nA typ, ±0.2 nA max (25 °C), ±0.6 nA (85 °C); OFF drain leakage ±0.45 nA max (25 °C), ±2 nA (85 °C) — measured at ±10 V signal bias, so conservative for a ~0 V SCP signal. The datasheet (Rev. D, current) contains no thermal-EMF, thermoelectric-offset or switch-offset-voltage specification whatsoever; its only thermal data are θJA 150.4 °C/W (TSSOP) / 30.4 °C/W (LFCSP) and a qualitative 'ultralow power dissipation' statement. Consequently the ADG1408/1409 (and by extension the untested ADG1208/5408/1608/708, DG408, MAX4708 family) is adequate for sub-µV SCP work only when contact resistance stays metallic (3 nA × 1 Ω = 3 nV; 1.5 nA × 1 kΩ = 1.5 µV; 3 nA × 1 MΩ = 3 mV), its leakage is ~25× the 2182A's 60 pA, and its thermal offset must be measured by the user rather than taken from a spec.

**Evidence.** ADG1408/1409 datasheet Rev. D (6/2016; ADI product page Feb 2026 lists Rev. D, PRODUCTION) LEAKAGE CURRENTS table at VDD=+16.5 V, VSS=−16.5 V: IS(Off) ±0.04 typ / ±0.2 / ±0.6 / ±5 nA; ID(Off) ±0.04 / ±0.45 / ±2 / ±30 nA; ID,IS(On) ±0.1 typ / ±1.5 / ±3 / ±30 nA (25 °C | −40..+85 | −40..+125); unchanged since Rev. 0 (2006). Case-insensitive grep of the 1402-line extracted text for emf|thermoelectric|seebeck|self-heat|offset|nV|µV returns zero hits; 'thermal' occurs only in Table 7 Thermal Resistance. The IR arithmetic follows the Keithley handbook formula VM = VS ± IOFFSET·RS. Verifier noted the ±10 V bias test condition makes the leakage figures conservative for the SCP case.

**Sources.** <https://www.analog.com/media/en/technical-documentation/data-sheets/adg1408_1409.pdf> · <https://wiki.epfl.ch/carplat/documents/LowLevMsHandbk.pdf>

### F10. Thermal-EMF budget of the contact matrix (Keithley Low Level Measurements Handbook, 6th and 7th ed., Table 3-1, Seebeck coefficients vs copp…

**Confidence:** high · **Vote:** 3-0 ×2 (claims 21, 22 merged)

**Claim.** Thermal-EMF budget of the contact matrix (Keithley Low Level Measurements Handbook, 6th and 7th ed., Table 3-1, Seebeck coefficients vs copper): Cu–Cu ≤0.2 µV/°C, Cu–Ag 0.3, Cu–Au 0.3, Cu–Pb/Sn solder 1–3, Cu–Kovar ~40–75, Cu–Si 400, Cu–CuO (copper oxide) ~1000 µV/°C. Keithley explicitly flags spring-contact test fixtures of beryllium-copper or phosphor-bronze — the base alloys of pogo pins — as high-Seebeck elements where a small temperature difference corrupts low-voltage measurements, prescribing all-copper connections first and, where dissimilar metals are unavoidable, reduction of gradients by heat sinking/heat shielding, warm-up and zeroing. Keysight's 34970A guide (independent corroboration) gives Cu-to-Gold 0.5, Silver 0.5, Brass 3, Beryllium Copper 5, Aluminum 5, Kovar 40 µV/°C. Implication: a gold-plated contact junction contributes ~0.3–0.5 µV per °C only if the pin body is isothermal; the BeCu pin body at ~5 µV/°C means a 1 °C gradient along a pin equals half the full SCP signal range and 0.02 °C already equals the 0.1 µV floor; a solder joint is up to 10× and an oxidised copper junction up to ~3000× worse than gold-on-copper.

**Evidence.** 6th-edition (© 2004, No. 1559) Section 3 Table 3-1 rows verbatim: 'Cu - Cu ≤0.2 µV/°C / Cu - Ag 0.3 / Cu - Au 0.3 / Cu - Pb/Sn 1–3 / Cu - Si 400 / Cu - Kovar ~40–75 / Cu - CuO ~1000', with E_AB = Q_AB(T1 − T2); identical table and passage in the current 7th edition (Tektronix). Passage p. 3-4/3-5 verbatim: 'Test fixtures often use spring contacts, which may be made of phosphor-bronze, beryllium-copper, or other materials with high Seebeck coefficients. In these cases, a small temperature difference may generate a large enough thermoelectric voltage to affect the accuracy of the measurement. If dissimilar metals cannot be avoided, an effort should be made to reduce the temperature gradients throughout the test circuit by use of a heat sink or by shielding the circuit from the source of heat.' Qualifications: Table 3-1 lists bulk Au, not gold plating over Ni over BeCu — the bulk metals spanning the gradient set the EMF, so 0.3 µV/°C is a best-case isothermal-junction figure; Keithley gives no number for BeCu/phosphor bronze — the 5 µV/°C is from Keysight's 34970A manual (verifier-supplied), and no value for phosphor bronze was found.

**Sources.** <https://wiki.epfl.ch/carplat/documents/LowLevMsHandbk.pdf> · <https://download.tek.com/document/LowLevelHandbook_7Ed.pdf>

### F11. Recommendation (synthesis): build the multi-channel scanner as PATH B on the ADS1263 — ADS1263V2EVM-PDK as the primary board (in stock, TI-d…

**Confidence:** medium · **Vote:** synthesis (no single vote)

**Claim.** Recommendation (synthesis): build the multi-channel scanner as PATH B on the ADS1263 — ADS1263V2EVM-PDK as the primary board (in stock, TI-designed analog supply/reference, direct SPI to a Raspberry Pi or MCU) with the Waveshare High-Precision AD HAT as a low-cost fallback only after replacing its Pi-5 V AVDD feed with a clean linear supply and adding an isothermal copper input block. Wire each pogo pin to AINx and the common reference pin to AINCOM so the ADC's internal mux does the scanning, run global chop, PGA gain 32, 5–10 SPS Sinc4 (≈1–2.5 Hz effective after chop), and average to the ~1 Hz record. Keep PATH A as the validation reference: a Keithley 2182A on the 10 mV range (channel 1) connected in parallel to one pin pair through all-copper leads, used to (i) confirm the ADS1263 channel reads the same DC value to within ~50 nV and (ii) measure the true noise floor vs source resistance. Do not rely on a Pickering/reed relay or ADG1408 matrix as the primary nanovolt switch: relays carry an unconditioned ~1 µV thermal EMF and CMOS muxes carry nA leakage with no thermal-EMF spec; a Keithley 7168 + 7001/7002 is the only specified ≤30 nV switch and its availability is unconfirmed. AD7124-8 (EVAL-AD7124-8) and ADS1235/ADS1261 are viable second choices for PATH B but are worse than the ADS1263 on offset/chop (AD7124-8, no chopper, 1.6 µV pre-cal offset) or on input current (ADS1235, 4–6 nA absolute).

**Evidence.** Inference from the verified findings above: ADS1263 chop-on offset ±16 nV max / drift 1 nV/°C typ vs AD7124-8 200/gain µV uncalibrated and 10 nV/°C; ADS1235 absolute input current 4–6 nA vs AD7124-8 1–3.3 nA; 7168 <30 nV vs Pickering 'about 1 µV or less' vs ADG1408 unspecified; 2182A 6 nV p-p at 25 s is the best available noise floor for validation. The ADS1263 mux/AINCOM mapping is from the datasheet's 11 multifunction inputs (AIN0–AIN9 + AINCOM) and the Waveshare schematic (INCOM as negative reference in single-ended mode). Confidence is medium because the recommendation is a judgment across findings, the ADS1263's own input current at gain 32 was NOT verified (that claim was refuted 0-3), and the thermal EMF of the ADS1263's internal mux is unspecified just as for external CMOS muxes — it must be measured with a shorted, temperature-stepped input.

**Sources.** <https://www.ti.com/lit/ds/symlink/ads1262.pdf> · <https://www.digikey.com/en/products/detail/texas-instruments/ADS1263V2EVM-PDK/20414007> · <https://www.waveshare.com/wiki/High-Precision_AD_HAT> · <https://download.tek.com/document/SPEC-2182A_DEC2016.pdf> · <https://download.tek.com/datasheet/7168.pdf> · <https://www.pickeringrelay.com/pdfs/100-low-thermal-cmos-drive-sil-reed-relays.pdf> · <https://www.analog.com/media/en/technical-documentation/data-sheets/adg1408_1409.pdf> · <https://www.analog.com/media/en/technical-documentation/data-sheets/ad7124-8.pdf> · <https://www.ti.com/lit/ds/symlink/ads1235.pdf>

### F12. Key design constraints for the prototype (any path): (1) Thermal-EMF budget — the fixture, not the ADC, sets the floor: with BeCu pin bodies…

**Confidence:** high · **Vote:** synthesis of 3-0 claims

**Claim.** Key design constraints for the prototype (any path): (1) Thermal-EMF budget — the fixture, not the ADC, sets the floor: with BeCu pin bodies at ~5 µV/°C a 0.02 °C gradient equals the 0.1 µV signal floor, so all pins and the reference must sit in one isothermal copper block, wiring must be Cu-to-Cu crimped/twisted pair with no solder, nickel or Kovar in the signal path, and readings taken only after 2–2.5 h warm-up (2182A 2.5 h; 7168 2 h) with periodic zeroing at the working temperature. (2) Averaging time vs noise — the instrument p-p noise falls ~10× from 60 ms to 25 s response (2182A 70→6 nV p-p; ADS1263 17–30 nV rms at 20 SPS → 6–11 nV rms at 2.5 SPS) but all quoted figures are 10 s to 2 min windows, so the hours-long SCP drift must be separated by a slow reference-channel subtraction or channel-reversal scheme rather than by longer averaging; the original instrument's ±1 µV raw band is 2 orders above the ADC noise and must originate in the contacts/thermal path. (3) Chop and PGA settings — global chop ON is mandatory (ADS1263: 350/Gain µV offset and 30/Gain+10 nV/°C drift without it vs ±0.5/Gain µV max and 1–5 nV/°C with it; ADS1235 likewise 1/5 nV/°C), PGA at the maximum gain (32 for ADS1263, 128 for AD7124-8/ADS1235), data rate ≤10 SPS so the effective chopped rate still exceeds the 1 Hz record rate. (4) Contact-resistance gate — every candidate front end except the 2182A/7168 draws nA-class input current (ADS1235 4–6 nA, AD7124-8 1–3.3 nA, ADG1408 ≤1.5–3 nA, 7168 <50 pA, 2182A <60 pA), so 1 MΩ of oxide gives 1–6 mV and 1 kΩ gives 1–6 µV of offset: measure each pin's contact resistance before every scan (2182A noise table shows the meter itself tolerates ≤10 kΩ at 35 nV p-p) and reject or re-seat pins above a few tens of Ω if 0.1 µV accuracy is required. (5) Switching discipline — cold-switch only (Pickering 1e9 ops), prefer the ADC's internal mux or a JFET scanner over reed relays; if relays are used, minimise coil-on dwell (Pickering's dwell test: −0.38 µV → −46 µV over 600 s) by using latching types or short-dwell drive and wait for thermal equilibrium after each actuation.

**Evidence.** All numbers are direct datasheet/handbook values from the findings above combined with Ohm's-law and Seebeck arithmetic (E = Q·ΔT; V = I·R): Keithley Table 3-1 and spring-contact passage; Keysight 34970A 5 µV/°C for BeCu; SPEC-2182A noise-vs-response and noise-vs-source-resistance tables and 2.5 h warm-up; ADS1262/3 Sec. 7.5 and Table 8-1; ADS1235 Sec. 6.5; AD7124-8 Table 3; ADG1408 leakage table; 7168 datasheet leakage/warm-up; Pickering Series 100 Note 1 and Pickering's dwell-time test. The specific numeric thresholds (0.02 °C, 'a few tens of Ω') are derived, not quoted, and assume the 0.1 µV floor with nA-class bias current.

**Sources.** <https://wiki.epfl.ch/carplat/documents/LowLevMsHandbk.pdf> · <https://download.tek.com/document/SPEC-2182A_DEC2016.pdf> · <https://www.ti.com/lit/ds/symlink/ads1262.pdf> · <https://www.ti.com/lit/ds/symlink/ads1235.pdf> · <https://www.analog.com/media/en/technical-documentation/data-sheets/ad7124-8.pdf> · <https://www.analog.com/media/en/technical-documentation/data-sheets/adg1408_1409.pdf> · <https://www.pickeringrelay.com/pdfs/100-low-thermal-cmos-drive-sil-reed-relays.pdf> · <https://download.tek.com/datasheet/7168.pdf>


## 7. Manual datasheet check (added after the workflow)


ADS1262/ADS1263 datasheet SBAS661B (Feb 2015, rev. July 2015; mirror at <https://files.waveshare.com/upload/2/2a/Ads1262.pdf>), Sec. 7.5 Electrical Characteristics, ADC1 ANALOG INPUTS: *Absolute input current — Gain = 32: 2 nA typ; PGA bypassed: 150 nA typ. Differential input current — Gain = 32: 0.1 nA typ; PGA bypassed, VIN = 5 V: 150 nA. Differential input impedance — PGA enabled 1 GΩ; PGA bypassed 40 MΩ. Channel-to-channel crosstalk 0.5 µV/V.* Sec. 9.4.12 Chop Mode: the chop switch reverses the internal input polarity **between the input MUX and the PGA**, so the on-die mux is outside the chop loop. PGA input range: V_AVSS + 0.3 + |V_IN|·(G−1)/2 < V_INP, V_INN < V_AVDD − 0.3 − |V_IN|·(G−1)/2; the ADC operates with bipolar ±2.5 V or single 5 V supplies. The workflow had refuted a claim built on these numbers (0-3) over its consequence arithmetic, not the rows themselves; the noise/offset rows were confirmed identical between SBAS661B and the current SBAS661C (2021), the input-current rows were not re-checked in rev. C.


## 8. Refuted claims

- **(1-2)** The 7168 achieves its sub-30 nV offset with solid-state JFET switches rather than electromechanical relays, with actuation under 3 ms and input leakage below 50 pA per channel at 23 °C, showing that a semiconductor switch can be used in a nanovolt scanner if leakage is in the tens-of-pA class.  
  Source: <https://www.finaltest.com.mx/v/vspfiles/assets/datasheet/7168.pdf>

- **(0-3)** With the PGA enabled at gain 32 the ADS1262 draws 2 nA typical absolute (common-mode) input current and 0.1 nA typical differential input current, with 1 GΩ differential input impedance; with the PGA bypassed these rise to 150 nA and 40 MΩ. Consequently a contaminated/oxidized weld contact of 1 MΩ would produce roughly 0.1 µV differential error (0.1 nA × 1 MΩ) and a 2 mV common-mode shift, whereas a metallic mΩ-to-Ω contact produces negligible error — so the PGA must be enabled and contact resistance must be checked when signals of 0.1 to 10 µV are expected.  
  Source: <https://www.ti.com/lit/ds/symlink/ads1262.pdf>


## 9. Caveats and coverage gaps

Coverage gaps: no claim survived verification for large parts of the brief — chopper/zero-drift preamps (ADA4528-1, ADA4522-2, LTC2057, OPA189, OPA2188, AD8628, LMP2021, LTC2053, MAX44250) and the classic LT1028/AN124-style nanovolt preamps; other DMMs (Keysight 34470A/34465A/34461A, Keithley DMM7510/DMM6500/2002/2010, Rigol DM3068, Siglent SDM3065X, 3706A-NFP); AD4130-8, AD7177-2/AD7175-2, ADS124S08, ADS1220, ADS1256 and the Waveshare ADS1256 HAT, LTC2508-32/LTC2500-32; other muxes (ADG1208/1209, ADG5408/5409, ADG1608/1609, ADG708/709, DG408/409, ADG1404/1414, MAX4708/4709) and relays (Coto 9007/9011/9012, Panasonic TQ2/TX2, Omron G6K/G6S, Standex-Meder); the SCP physics/Volta's-law discussion, thermoelectric-power NDT of welds and HAZ, and contact-resistance data for gold pogo pins on steel or oxidised welds. Statements about those items in this report are absent or inferred, not verified. A claim giving the ADS1262 input current at gain 32 (2 nA absolute / 0.1 nA differential, 1 GΩ) was refuted 0-3, so the ADS1263's bias-current error at kΩ–MΩ contact resistance is unverified; one verifier's note quoting 2 nA typ from the datasheet should be re-read from the primary source before use. The Keithley 7168 'not degraded' statement passed only 2-1 and is unquantified; 7168/7001/7002 new-stock status could not be confirmed because Newark, Mouser, RS, TI.com, Farnell and Octopart returned HTTP 403 to automated fetches. Availability data are time-sensitive snapshots (Digi-Key 2026-09-16/17: 19 units, 12-week lead time, 10-per-30-days cap; Waveshare HAT confirmed only on Waveshare's own store, not at Digi-Key/Mouser). All ADC and DMM noise figures are typical, shorted-input, short-window (10 s to 2 min) values at 25 °C and do not capture mHz 1/f or hours-long drift; the 2182A 6 nV figure is 'guaranteed by design'. The 5 µV/°C BeCu Seebeck value comes from a Keysight 34970A manual quoted by a verifier, not from the Keithley table; Pickering's dwell-time thermal-EMF test was on the Series 120, not Series 100. Several verifiers reported exhausted web-search budgets, so contradiction searches were limited to the primary documents themselves.


## 10. Open questions

- Does the ADS1263's internal input mux (and the 47 Ω input resistors/headers on the Waveshare HAT) add a measurable thermal EMF, and does global chop cancel offsets generated ahead of the PGA input-swap point? This needs a shorted-input, temperature-stepped test; no datasheet specifies it, exactly as for the ADG1408.

- What is the actual ADS1263 absolute and differential input current at gain 32 with chop on, and therefore the maximum tolerable contact resistance for 0.1 µV accuracy? The only claim addressing it was refuted, and no verified contact-resistance data for gold-plated pogo pins on as-welded or oxidised steel were found to size the error.

- Is a Keithley 7168 with a 7001/7002 mainframe (or the 3706A-NFP / 2182A-scan alternative) still obtainable new in 2026 and at what price, so that Path A could scan 4–8 pins at the ≤30 nV level rather than only cross-check one pair?

- How much of the 0.1–10 µV SCP signal survives when the whole cell is held isothermal to better than ~0.02 °C and contact resistance is verified metallic — i.e. what fraction of the prior-art signal is thermoelectric/oxide-film EMF versus the 'contact potential' the SCP literature claims (Volta's law caveat and TEP-NDT prior art remain unaddressed by verified evidence)?


## 11. Sources fetched

| Source | Quality | Angle | Claims |
|---|---|---|---|

| <https://www.finaltest.com.mx/v/vspfiles/assets/datasheet/7168.pdf> | primary | Path A: low-thermal-EMF switching and nanovoltmeter datasheet specs | 5 |

| <https://download.tek.com/document/SPEC-2182A_DEC2016.pdf> | primary | Path A: low-thermal-EMF switching and nanovoltmeter datasheet specs | 5 |

| <https://www.pickeringrelay.com/pdfs/100-low-thermal-cmos-drive-sil-reed-relays.pdf> | primary | Path A: low-thermal-EMF switching and nanovoltmeter datasheet specs | 5 |

| <https://www.analog.com/media/en/technical-documentation/data-sheets/adg1408_1409.pdf> | primary | Path A: low-thermal-EMF switching and nanovoltmeter datasheet specs | 5 |

| <https://www.ti.com/lit/ds/symlink/ads1262.pdf> | primary | Path B: 32-bit ΔΣ ADC boards, PGA/chopper noise, Raspberry Pi HAT availability | 5 |

| <https://www.digikey.com/en/products/detail/texas-instruments/ADS1263V2EVM-PDK/20414007> | primary | Path B: 32-bit ΔΣ ADC boards, PGA/chopper noise, Raspberry Pi HAT availability | 5 |

| <https://www.waveshare.com/wiki/High-Precision_AD_HAT> | primary | Path B: 32-bit ΔΣ ADC boards, PGA/chopper noise, Raspberry Pi HAT availability | 5 |

| <https://www.analog.com/media/en/technical-documentation/data-sheets/ad7124-8.pdf> | primary | Path B: 32-bit ΔΣ ADC boards, PGA/chopper noise, Raspberry Pi HAT availability | 5 |

| <https://www.ti.com/product/ADS1235> | primary | Path B: 32-bit ΔΣ ADC boards, PGA/chopper noise, Raspberry Pi HAT availability | 5 |

| <https://xdevs.com/review/ti_ads1262_p1/> | blog | Path B: 32-bit ΔΣ ADC boards, PGA/chopper noise, Raspberry Pi HAT availability | 5 |

| <https://wiki.epfl.ch/carplat/documents/LowLevMsHandbk.pdf> | primary | Nanovolt preamplifier design: zero-drift op amps, classic app notes, low-thermal wiring | 5 |

| <https://www.analog.com/media/en/technical-documentation/data-sheets/ada4523-1.pdf> | primary | Nanovolt preamplifier design: zero-drift op amps, classic app notes, low-thermal wiring | 5 |

| <https://www.ti.com/lit/ds/symlink/opa189.pdf> | primary | Nanovolt preamplifier design: zero-drift op amps, classic app notes, low-thermal wiring | 5 |

| <https://www.analog.com/en/products/ltc2057.html> | primary | Nanovolt preamplifier design: zero-drift op amps, classic app notes, low-thermal wiring | 5 |

| <https://www.analog.com/media/en/technical-documentation/application-notes/an124f.pdf> | primary | Nanovolt preamplifier design: zero-drift op amps, classic app notes, low-thermal wiring | 5 |

| <https://www.ti.com/product/LMP2021> | primary | Nanovolt preamplifier design: zero-drift op amps, classic app notes, low-thermal wiring | 5 |

| <https://en.wikipedia.org/wiki/Volta_potential> | secondary | Physics caveat and SCP literature: Volta potential, intermediate metals, thermoelectric weld NDT | 4 |

| <https://cyberleninka.ru/article/n/metody-elektrofizicheskoy-diagnostiki-i-kontrolya-reaktornogo-oborudovaniya> | primary | Physics caveat and SCP literature: Volta potential, intermediate metals, thermoelectric weld NDT | 5 |

| <https://docs.ampnuts.ru/eevblog.docs/Keithley/Ch3_LowLevMsHandbk.pdf> | primary | Physics caveat and SCP literature: Volta potential, intermediate metals, thermoelectric weld NDT | 5 |

| <https://assets.testequity.com/te1/Documents/pdf/keithley/KeithleyLowLevelHandbook_7Ed.pdf> | primary | Materials data: pogo-pin and connector Seebeck EMF, gold-plated contact resistance on oxidized steel | 5 |

| <https://media.fluke.com/3c354b25-2528-408e-b22f-b2ea003f0489_original%20file.pdd> | primary | Materials data: pogo-pin and connector Seebeck EMF, gold-plated contact resistance on oxidized steel | 5 |

| <https://promaxpogopin.com/blog/pogo-pin/specifications/> | blog | Materials data: pogo-pin and connector Seebeck EMF, gold-plated contact resistance on oxidized steel | 5 |


**Workflow stats:** angles 5, sources 22, claims extracted 109, verified 25 (confirmed 23, refuted 2), findings after synthesis 12, agent calls 104. Web-search budget was exhausted during the run; several distributor/manufacturer sites (TI, Mouser, Newark, RS, Farnell, Octopart) returned HTTP 403 to automated fetches.

## 12. Addendum (2026-09-17): HW-146 module / AD7705 assessment

**Question raised after the main report:** is the cheap HW-146 breakout (Analog Devices AD7705, 16-bit ΔΣ, 2 differential channels, PGA 1–128) usable for the cell?

**Verdict.** Fine as a bring-up board for SPI, firmware and the mechanical fixture, and adequate for a first look at 1–10 µV differences; **not** adequate for the 0.1 µV floor, and it cannot scan more than two pins without an external switch (which re-introduces the Path A thermal-EMF problem). The Waveshare ADS1263 HAT (~$33) buys ≈100× lower noise and 20–100× lower drift for ≈10× the price of an HW-146.

**Datasheet numbers** (AD7705/AD7706 datasheet Rev. C, Table 1, Table 5, Table 6, Table 22/23 and "Drift Considerations"; bipolar mode, VDD = 5 V, VREF = 2.5 V; obtained via the Wayback Machine copy of <https://www.analog.com/media/en/technical-documentation/data-sheets/AD7705_7706.pdf> because analog.com was unreachable from the research environment):

| Parameter | AD7705, gain 128 | ADS1263, gain 32, chop on (Sec. 2) |
|---|---|---|
| Lowest output update rate | 20 Hz (MCLK 1 MHz) or 50 Hz (MCLK 2.4576 MHz) | 2.5 SPS |
| Output noise at lowest rate | 0.6 µV rms typ; 14 bits p-p on ±19.5 mV ≈ 2.4 µV p-p | 6 nV rms, 23 nV p-p |
| Noise at ≈20 SPS | 0.6 µV rms (20 Hz / 50 Hz rows are identical) | 17–30 nV rms |
| Offset drift | Bipolar zero drift 0.1 µV/°C typ for gains 8–128 (0.5 µV/°C for gains 1–4); unipolar offset drift 0.5 µV/°C typ; typical only, no max | 1 nV/°C typ, 5 nV/°C max |
| Offset handling | Internal chopper-stabilised modulator plus self-calibration / system calibration ("Measurement errors due to offset drift or gain drift can be eliminated at any time by recalibrating the converter") | Global chop on every conversion |
| Input current | AIN DC input current 1 nA max; AIN sampling capacitance 10 pF max; buffered-mode buffer offset leakage 1 nA | 2 nA absolute, 0.1 nA differential typ |
| Channels | 2 fully differential | 10 inputs + AINCOM |
| Supply / input range | Single 3 V or 5 V. Unbuffered (BUF = 0): AIN allowed GND − 100 mV to VDD + 30 mV. Buffered (BUF = 1): GND + 50 mV to VDD − 1.5 V | ±2.5 V bipolar or 5 V single |
| Source-resistance limit, unbuffered, gains 8–128 (no 16-bit gain error) | 16.7 kΩ @ 10 pF ext. C; 5.95 kΩ @ 50 pF; 3.46 kΩ @ 100 pF; 924 Ω @ 500 pF; 150 Ω @ 5 nF (Table 22); input sampling frequency 8 × fCLKIN/64 = 307.2 kHz at gains 8–128 (Table 23) | 1 GΩ differential impedance |

**Implications for the cell.**

1. *Noise:* 20–100× worse than the ADS1263. The datasheet states the chopped noise is "primarily flat", so averaging works: 100 samples at 20 Hz (5 s) brings 0.6 µV rms to ≈60 nV rms — enough to resolve the 1–10 µV differences reported in the SCP papers, but it leaves a floor near 0.1 µV before any fixture effects.
2. *Drift:* 0.1 µV/°C typical with no maximum; a 1 °C lab swing equals the 0.1 µV floor. Drift is removed only by recalibration (inputs shorted, record interrupted), not by continuous chopping, so hours-long SCP drift cannot be separated from ADC drift.
3. *Channels:* 4–8 pins need an external mux/relays (Path A thermal-EMF trap) or several modules (per-chip offsets).
4. *Input mode:* unbuffered mode is the right choice (accepts the common reference pin at 0 V) but its switched-capacitor input demands low source resistance per Table 22; any RC filter on the module tightens the contact-resistance gate. Buffered mode relaxes source resistance but needs the inputs ≥ 50 mV above ground, i.e. a biased sample.

**Module-level caveats — NOT verified online** (search budget exhausted; distributor/marketplace pages unreachable): the typical HW-146 carries a TL431-type 2.5 V shunt reference and a 2.4576 MHz crystal (so 50 Hz is the lowest rate unless the crystal is changed to 1 MHz), header pins and solder joints add 1–3 µV/°C junctions (same issue as the Waveshare HAT), and many of these modules ship with a TM7705 (Titan Micro) clone instead of an Analog Devices part — check the chip marking. Reference tempco matters little here because the signal is near zero.
