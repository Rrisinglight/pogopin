# A Review of Non-Destructive Testing (NDT) Techniques for Defect Detection: Application to Fusion Welding and Future Wire Arc Additive Manufacturing Processes

> **Source:** `A Review of Non-Destructive Testing (NDT) Techniques for Defect Detection.pdf` · 26 pp. · *Materials* (MDPI), vol. 15, issue 10, article 3697, 2022 · Masoud Shaloo, Martin Schnall, Thomas Klein, Norbert Huber, Bernhard Reitinger
> **Original language:** EN · **ID:** 10.3390/ma15103697

## Bibliographic data

- **Title:** A Review of Non-Destructive Testing (NDT) Techniques for Defect Detection: Application to Fusion Welding and Future Wire Arc Additive Manufacturing Processes
- **Article type:** Review
- **Journal:** *Materials* **2022**, *15*, 3697
- **DOI:** https://doi.org/10.3390/ma15103697
- **Authors and affiliations:**
  - Masoud Shaloo ¹ (corresponding, masoud.shaloo@ait.ac.at)
  - Martin Schnall ¹ (martin.schnall@ait.ac.at)
  - Thomas Klein ¹ (corresponding, thomas.klein@ait.ac.at)
  - Norbert Huber ² (norbert.huber@recendt.at)
  - Bernhard Reitinger ² (bernhard.reitinger@recendt.at)
  - ¹ LKR Light Metals Technologies Ranshofen, Austrian Institute of Technology, Lamprechtshausenerstraße 61, 5282 Ranshofen, Austria
  - ² RECENDT Research Center for Non Destructive Testing GmbH, Science Park 2/2. OG, Altenberger Straße 69, 4040 Linz, Austria
- **Academic Editor:** Giulio Marchese
- **Dates:** Received 28 March 2022; Accepted 18 May 2022; Published 21 May 2022
- **Copyright:** © 2022 by the authors. Licensee MDPI, Basel, Switzerland. Open access under CC BY 4.0.
- **Number of references:** 131
- **Figures:** 19 · **Tables:** 2 · **Numbered equations:** none (the paper contains no displayed or numbered formulas)

## Abstract

In Wire and Arc Additive Manufacturing (WAAM) and fusion welding, various defects such as porosity, cracks, deformation and lack of fusion can occur during the fabrication process. These have a strong impact on the mechanical properties and can also lead to failure of the manufactured parts during service. These defects can be recognized using non-destructive testing (NDT) methods so that the examined workpiece is not harmed. This paper provides a comprehensive overview of various NDT techniques for WAAM and fusion welding, including laser-ultrasonic, acoustic emission with an airborne optical microphone, optical emission spectroscopy, laser-induced breakdown spectroscopy, laser opto-ultrasonic dual detection, thermography and also in-process defect detection via weld current monitoring with an oscilloscope. In addition, the novel research conducted, its operating principle and the equipment required to perform these techniques are presented. The minimum defect size that can be identified via NDT methods has been obtained from previous academic research or from tests carried out by companies. The use of these techniques in WAAM and fusion welding applications makes it possible to detect defects and to take a step towards the production of high-quality final components.

## Keywords

Wire and Arc Additive Manufacturing (WAAM); fusion welding; NDT; laser-ultrasonic; laser-induced breakdown spectroscopy; laser opto-ultrasonic dual detection; thermography; acoustic emission; airborne optical microphone

---

## 1. Introduction

### 1.1 WAAM: origin, classification and process chain

In 1925, Backer introduced a novel technology named Wire and Arc Additive Manufacturing (WAAM) [1,2]. WAAM — also known as Shape Metal Deposition (SMD), Shape Welding (SW) and Shape Melting (SM) — belongs to Directed Energy Deposition (DED) based on ASTM F2792-12a [3]. It combines arc welding technologies such as Gas Metal Arc Welding (GMAW), Gas Tungsten Arc Welding (GTAW) and Plasma Arc Welding (PAW) with wire materials to manufacture near-net-shape metallic components via a layer-by-layer deposition approach [4–6].

The difference between WAAM and welding is the geometry of the component and the resultant effects on the temperature distribution. WAAM is assumed to be one of the most promising AM techniques in various industries, such as the aerospace, space and marine industries, owing to its capability of manufacturing complex and large components, high deposition rate and reduced wasted material and lead time, resulting in cost reduction [2,7–9].

The WAAM process is made up of the following six steps [7]:

1. creating a CAD model;
2. slicing the 3D model into layers;
3. generating an adequate deposition path;
4. selecting proper welding parameters, such as travel speed, current and voltage;
5. material deposition;
6. post-processing.

Various materials — steel-, aluminium-, titanium- and Ni-based alloys — are employed in WAAM [2].

### 1.2 Defects and the need for NDT

In WAAM, defects such as porosity, cracking and oxidization may appear on the surface and subsurface of the final parts during fabrication, as a result of higher heat accumulation in the part, improper parameter configuration, contamination and inconstant weld pool dynamics [2,8]. These defects may cause failure of the manufactured component; thus it is extremely crucial to detect the defects in order to prevent failure during service [2].

The final welding properties are directly impacted by the welding parameters: voltage (polarity), current, travel speed, interpass temperature and preheat temperature. Control of the welding parameters makes it possible to enhance the properties of manufactured components [10].

NDT techniques have gained the interest of researchers due to their ability to detect welding defects [11]. Unlike traditional inspection techniques, the quality of additively manufactured or welded components can be evaluated cost-efficiently and in real time using NDT methods, so that the examined workpiece is not harmed [11–14]. Several NDT techniques are currently available; however, most of them are not applicable for real-time and automatic process monitoring for weld defect inspection in WAAM and fusion welding [9].

### 1.3 Prior reviews and comparative surveys

- **Kah et al. [11]** investigated three different NDT techniques — eddy current, ultrasonic and real-time radiography — and their sub-types. Eddy current testing (ET) can detect small welding defects and discontinuities in real time, but only for conductive materials; furthermore, deep welding imperfections cannot be inspected. In contrast, Ultrasonic Testing (UT) covers these limitations and detects deeper welding defects in metals and plastics. Conventional UT transducers are not suitable for real-time and in-process monitoring of welded parts, because they require contact with the specimen and cannot withstand the very high temperatures of the WAAM and fusion welding processes. This limitation is overcome using laser ultrasonics [15].
- **Honarvar et al. [16]** presented a review on distinct ultrasonic NDT methods, discussing their principle and their capability for in-situ and offline inspection in additive manufacturing applications.
- **Lopez et al. [9]** reviewed various NDT techniques for WAAM applications in detail; however, real-time acoustic emission inspection using an optical microphone, as well as laser-induced breakdown spectroscopy, were not discussed in their work.

Table 1 of the present paper provides additional information on the NDT techniques reviewed by Lopez et al. [9] and Ricardo et al. [17]. The minimum detected defect size for each NDT method was extracted from previously conducted academic research or from tests performed by companies. The authors point out that detecting the minimum size of the defects depends on various parameters, such as **material (grain size, anisotropy, thermal conductivity), welding process, thickness of the sample and resolution of the equipment**. These methods must be tested individually in order to acquire the best method for a specific application.

### 1.4 Automated and combined inspection approaches reported in the literature

**Radiography + image processing.** The demand for reducing manufacturing lead times and increasing welding quality persuaded many researchers to develop available NDT techniques to inspect welding defects in real time and automatically [11]. Faramarzi et al. [18] merged image processing and radiographic NDT to detect welding imperfections such as burn-through, lack of fusion, lack of penetration and slag automatically (Figure 1). Firstly, a program in MATLAB [19] was implemented in order to detect burn-through defects using data fusion and image processing. Then, the developed program was successfully applied to the other above-mentioned welding defects. The developed image-processing algorithm can be summarized in the following steps:

1. smoothing and thresholding;
2. morphology operations;
3. smoothing;
4. boundary functions.

Although radiography can be employed to automatically inspect all types of welding defects in complex welding geometries, very fine defects cannot be detected [11], and it also endangers human health [9]. Other image-based NDT methods, such as X-ray computed tomography and X-ray backscatter, are not suitable for real-time and on-line quality assessment, as these require too much time to detect defects [9].

**Dye penetrant + conventional UT + digital radiography.** Seow et al. [20] employed dye penetrant testing, conventional ultrasonic testing and digital X-ray radiography to recognize crack-like imperfections in a WAAM Alloy 718 component. As depicted in Figure 2, these technologies are able to find crack-like defects in WAAM.

**3D computed tomography.** Wang et al. [21] employed 3D computed tomography technology and could find various defect types, including small spherical pores, inverted pear-shaped pores and cavities in a molybdenum WAAM component.

**Eddy current probe.** Bento et al. [22] designed and examined an eddy current probe to detect flaws in an aluminium alloy (AA 6082-T6) WAAM part during the manufacturing process. They revealed that intentionally made defects **at a depth of up to 5 mm and with a minimum thickness of 0.350 mm** can be identified. In addition, the ability to detect defects increases as the number of coil turns rises.

**Phased Array Ultrasonic Testing (PAUT).** Lopez et al. [23] studied the ability of PAUT to identify defects inside WAAM parts made of aluminium alloy (AA2319) with rough surfaces. They carried out numerical simulations to determine the proper testing parameters and select an adequate transducer, and then conducted defect detection experiments. They reported that it was possible to detect **defects sized between 2 and 5 mm**. Chabot et al. [24] demonstrated that PAUT is capable of detecting **defects of 0.6 to 1 mm** in aluminium WAAM components. Javadi et al. [12] applied PAUT and a Total Focusing Method (TFM) to detect artificially introduced tungsten carbide spheres with various diameters in a **20-layer wall** made using WAAM; they were able to successfully detect most of the defects using a TFM technique.

**Laser-Induced Phased Array (LIPA).** Lukacs et al. [25] adopted LIPA, full matrix capture data acquisition and TFM to inspect a titanium alloy (Ti-6Al-4V) fabricated using plasma arc WAAM. As illustrated in Figures 3 and 4, they clearly indicate that **defects located at a depth of up to 10 mm** inside the sample can be found offline by means of high-quality images. In addition, it was found that the full matrix capture in LIPA is **time consuming (nearly 14 min)** due to the synthetic measurement approach, including a large number of acquired A-scan signals, the physical scan of the laser and signal averaging. Therefore, it is currently not possible to implement this technique in real time and inline inspection.

### 1.5 Scope of this review

Each NDT technique has its own benefits and limitations and is able to detect specific defects and is used for specific materials. Thus, various NDT methods must be combined to monitor the WAAM and fusion welding process. A lot of research has been conducted to investigate various NDT techniques in WAAM and fusion welding applications; only little has been done on combining distinct contactless NDT techniques and sensor technologies in order to automatically detect welding defects in real time, monitor the weld pool and part characteristics, measure the temperature distribution and also process parameters.

The main focus of this work is on WAAM. However, since most of the defects that can form during WAAM and fusion welding processing are similar (differences can result from different thermal fields and cooling conditions), non-destructive testing methods can also be applied to fusion welding. Therefore, in addition to WAAM, fusion welding is also covered. This review paper presents a concept of a combination of a set of contactless NDT and novel sensor technologies which possess the capability to be implemented and integrated in WAAM and fusion welding setups to automatically detect defects in real time and monitor the processes.

---

## 2. Laser-Ultrasonics Testing

### 2.1 Physical basis of ultrasonic waves

The oscillation/space displacement of particles, their position-restoring forces and their linkage to the surrounding particles — which in turn leads to an energy transport — is known as elastic or sound waves. The elastic waves typically used in non-destructive testing are so-called ultrasonic waves characterized by **frequencies higher than the range audible to humans (>20 kHz)** and therefore cannot be heard. However, they can be detected using different types of transducers. Transducers transform these elastic waves into electrical signals that can be monitored as visual signals on a monitor [43] and further analysed.

The most commonly used ultrasound transducer technology is based on the piezo effect, where stress leads to electric charge. A number of further technologies are available:

- Electromagnetic Acoustic Transducers (EMAT)
- Capacitive Micromachined Ultrasonic Transducers (CMUT)
- magnetostrictive transducers
- Laser Ultrasound (LU), to both generate and receive ultrasonic waves [16]

### 2.2 The laser-ultrasonic (LU) system

LU is a non-contact NDT technique that is typically composed of two systems:

1. a **pulsed laser (q-switched ns-laser)** to excite elastic waves;
2. a **long-pulsed or Continuous Wave (CW) laser in combination with an interferometer** to detect the surface movement caused by these elastic waves [44,45].

It can be used in automation processes and harsh environments [46]. As shown in Figure 5, the LU test system consists of the mentioned units including electronic data acquisition and processing hardware [47].

### 2.3 Propagation modes

A number of different propagation types (modes) of elastic waves can be used in UT inspection (Table 2). Generally, elastic waves can be categorized into **bulk waves** and **guided waves**. Bulk waves are divided into longitudinal (compression) or transverse (shear) waves. Guided waves own various modes, such as surface (Rayleigh) waves and plate (Lamb, including Zero Group Velocity (ZGV) modes) waves [16,49–51]. Typically for LU, these waves can be excited and propagate simultaneously in the material and can further be distinguished via data processing and prior knowledge of the physical nature of the elastic wave.

### 2.4 Generation mechanisms: thermoelastic vs. ablative

These waves can be generated either via a thermoelastic mechanism at lower laser energy [52] or via ablation of the component by vaporization of a small amount of the upper layers at higher laser energy. Figure 6 shows a symbolic sketch of the two excitation phenomena.

- **Thermoelastic generation** is a non-destructive method in which a short-pulsed laser, with an **energy density lower than the damage threshold of the material**, excites a short pulse on the surface of the material. This causes heating, including thermal expansion of the surface of the material, in a very short time, which leads to particle motion and therefore elastic waves.
- **Ablative generation** is enabled by enhancing the laser energy density **higher than the damage threshold** of the material surface. A small amount of material is vaporized, which causes a backdraft to the surface, and this generates elastic waves revealing much higher amplitudes.

The most prominent differences between the two ultrasonic excitation phenomena are: different elastic wave amplitudes, different wave dispersion behaviours, and being destructive vs. non-destructive [53,54].

### 2.5 Detection

In the next step, the excited elastic waves are detected by the second laser optical system [16,47,48,55,56], which in the majority of cases illuminates a certain spot on the material surface. The elastic waves generate small vibrations of the surface which lead to a **phase modulation (Doppler shift)** of the reflected laser light of the detection system. This is further demodulated to an amplitude modulation via the use of different interferometer systems: **homodyne, heterodyne, self-interference, two-beam, photorefractive, time delay**.

### 2.6 Advantages and capabilities of LU

LU enables competitive advantages compared to conventional ultrasonic NDT techniques:

- ability to operate contactless, in real time, at various distances, **even more than 1 m**, and at any temperature;
- ability to measure the thickness, to inspect flaws and to characterize the material, **even on non-stationary components** [45,47,58];
- requires **no couplant** between the transducer and the component;
- can operate at a **very high bandwidth (from 1 MHz to 100 MHz or even more)** [58];
- cracks, lack of fusion, porosity and residual stresses can be detected via UT in powder- and wire-based DED processes [16];
- capability to detect **defects larger than 100 µm and up to 700 µm deep** [9].

### 2.7 Research results with LU in AM and welding

- **Levesque et al. [59]** investigated the use of laser ultrasound for offline defect analysis of INCONEL718 and Ti-6Al-4V coupons and compared the results with X-ray tomography. The coupons were processed using a laser powder, a laser wire and an electron beam wire deposition process. Laser ultrasound results were reconstructed using the **Synthetic Aperture Focusing Technique (SAFT)** method, improving resolution and the Signal-to-Noise Ratio (SNR). Defects such as **porosity with typical sizes of about 0.4 mm** and lack of fusion in the laser wire deposition process could be clearly identified. The measurements were made from the bottom side of the coupon; use on a rough surface for a later inline application still has to be tested.
- **Levesque et al. [60]** later showed the possibility of using LU for defect analysis of **thick welded structures (butt welds)**. Since similar surface roughness and geometry problems are expected here as in the previous investigations, a comparison can be made to the applicability of LU to WAAM structures. LU was applied directly to the machined surface, and the reconstruction of the data using SAFT was corrected for the geometry information obtained via a **profile camera**. In this way, artificial defects (EDM slits in one) with a **size of 2–3 mm could be resolved at a depth of 50 mm**.
- **Klein et al. [61]** researched the possibility of using surface acoustic waves (Rayleigh waves) to detect defects positioned near the surface. SAW in contrast to the bulk-wave approach should offer advantages especially for near-surface defects. The analysis of the Surface Acoustic Wave (SAW) waves and their temporal displacement, induced by defects, was carried out by means of **wavelet analysis and numerical simulations**. Artificial defects (**flat-bottom drilled holes, 1 mm diameter and 0.4 mm deep**) were clearly detected on titanium and steel samples with machined surfaces. Following studies have to show the applicability on typical WAAM components with their relatively high surface roughness.
- **Dixon et al. [62]** took a similar approach, based on a pulsed laser to excite SAW waves and an **EMAT (Electromagnetic Acoustic Transducer)** detector. The combination of laser and EMAT allowed, on the one hand, a low-cost detector (in contrast to the typical laser-based LU detectors) and, on the other hand, the use of EMAT on materials with low electrical conductivity or magnetic properties. With this setup, samples with artificial defects and real components with porosities were investigated. The defects could be found, but a characterization of the defects in size and location was not possible at the time of publication; therefore this hybrid system could be used as a **pre-screening technology**.
- **Zeng et al. [63]** numerically and experimentally investigated three intentionally embedded defects in WAAM **without any surface treatment**:
  - a crack with a **width of 0.2 mm and a depth of 2 mm**;
  - a flat-bottom hole with a **diameter of 2 mm and a depth of 1 mm**;
  - a through hole with a **diameter of 2 mm and a depth of 2.5 mm**.

  They successfully identified all of the above using laser ultrasound technology.
- **Fang et al. [64]** determined that LU in **transmission mode** allows subsurface defects **as small as 1 mm in diameter** inside an additively manufactured **A 316 L stainless steel** part to be detected. The component was scanned simultaneously with a laser generator on one side and an ultrasonic detector on the other side of the probe. The time delay was measured using a **cross-correlation algorithm**. The position of the internal defects was evaluated based on the sample thickness and two maximum signal delay points at the left and right scanning.
- **Guo et al. [65]** merged a **convolutional neural network (CNN)** and **wavelet transform** techniques to evaluate the laser ultrasound signals and automatically detect the width of subsurface defects artificially introduced into an aluminium alloy (**AW 2024**) plate. The laser ultrasound signals were transformed into images using the wavelet transform method; the transformed images were then adopted as training data for the CNN approach. They proved that the applied technique is an effective methodology with a very high detection accuracy.
- **Nomura et al. [15]** assessed the feasibility of laser ultrasonic technology for **real-time defect detection in GMAW of a mild steel**. Two defects were investigated: a lack of penetration and a solidification crack. A pulsed laser with a **pulse width of 9 ns** and a **frequency of 100 Hz**, placed at a **distance of 50 mm behind the welding torch and 4.5 mm behind the melt pool**, generated the sound waves in **ablation mode**, and a laser detector received the excited sound waves. The SAFT [55,60,66,67] was adopted to acquire images by means of longitudinal sound wave velocities. Although the depth position of the defects was estimated inaccurately (**around 5% deviation**) due to the difference between the applied room temperature and the true value for the ultrasonic waves, it was successfully shown that LU is capable of detecting defects in real time as well as during the welding process. It was proposed that the heat diffusion caused by the welding process should be taken into account to overcome this deviation.
- **Wei Zeng et al. [68]** performed a **Finite Element Method (FEM)** simulation to study the interaction of generated soundwaves using laser ultrasonics with subsurface defects in an aluminium sample. It was claimed that subsurface defect depth alternation impacts the **maximum displacement of the echo and oscillating waves**.
- **Karabutov et al. [69]** reported the detection of **subsurface stress distribution** for titanium and nickel alloys using LU.

---

## 3. Acoustic Emission

### 3.1 Principle

Acoustic Emission (AE) belongs to the NDT techniques which enable detection of welding imperfections and metallurgical transformations in a component under use or stress, cost effectively. As these phenomena happen inside a material, a specific amount of energy discharges rapidly, resulting in the generation of **transient elastic waves**. The elastic waves travel within the material to the surface and can be detected in real time using sensors — e.g. a piezoelectric transducer in conventional AE mounted on the surface of the tested material, or via vibrometers [42,70].

Signal chain: transducers convert the generated mechanical motion on the surface into an electrical signal. Then, a **Low Noise Preamplifier (LNA)** is applied to increase signal amplitude and possibly reduce electrical noise (**bandpass filtering**). The signals are collected, post-processed and further analysed. **The AE frequency ranges typically from 150 up to 300 kHz** [43,71–75].

AE detects the generated soundwaves during the process and therefore is a **passive** technology. In contrast, the ultrasonic testing method generates the soundwaves using an external soundwaves generator, such as a piezoelectric transducer (or a laser in LU), and consequently is an **active** technology. Conventional AE is **not adequate for real-time inspection of WAAM and fusion welding processes** [9]. Figure 7 indicates a graphical illustration of a conventional AE measurement system.

### 3.2 Sensors: from piezoelectric to airborne optical microphones

Besides piezoelectric transducers, wide-band transducers and optical microphones are employed in AE [74,77]. A microphone is a sensor that has been applied since the last century to detect pressure waves (sound waves) in gas or fluids. It is made up of a solid diaphragm and a displacement transducer, and may be equipped with extra components, e.g. mufflers and a focusing reflector. It converts sound waves into an electrical signal via its diaphragm vibrations caused by soundwave collision. However, this feature intrinsically constrains standard microphones from detecting high-frequency airborne sound waves via the mechanical construction (leading to oscillations and high-frequency damping) [78,79].

To overcome this limitation, commercial systems based on **laser interferometry** provide real-time, non-contact detection of sound waves in air with a **variable frequency from 10 kHz up to 2 MHz**, using a laser interferometer in place of the vibrating diaphragm of conventional microphones [30]. Figure 8 shows a sketch of the **membrane-free optical microphone**. The interaction of the ultrasonic waves and air results in a change of density and consequently of the optical refractive index of the air. As a result, the wavelength of the laser beam, which is trapped inside the tiny laser interferometer, is affected. The intensity of the returned laser beam is obtained using a **photodiode** [77,80,81].

### 3.3 Research results with AE

- **Ramalho et al. [82]** explored the impact of different impurities on the sound waves recorded by a microphone during the WAAM process by means of **power spectral density** and **Short Time Fourier Transform (STFT)** analysis techniques. They were able to successfully detect defects.
- **Aboali et al. [83]** employed **energy, number of counts and amplitude** of the AE signals to detect pre-introduced lack of fusion, porosity and slag in a **carbon steel** welded part. The results were compared with those of a defect-free part. It was demonstrated that the **lowest values of energy and amplitude and the highest value of number of counts were registered for the defect-free part**. The registered AE parameters were mostly impacted by **slag defects, followed by porosity and lack of fusion**.
- **Droubi et al. [84]** studied the ability of AE to detect welding defects including slag, porosity and cracks. It was clearly evidenced that defect detection is much more straightforward using **AE energy, Root Mean Square (RMS) and peak amplitude** parameters. The recognition and detection of welding defects was precisely conducted via **wavelet transform** results. In addition, it was claimed that the **distance between the sensor and the model clearly impacts the results**.
- **Luo et al. [85]** applied the AE **count statistic**, **RMS waveform calculation** and **power spectrum distribution** methods to analyse the AE signals during **pulsed YAG laser welding**. They claimed that the **plasma plume produces the recoil force and the thermal vibration**, and these are the source of the generated AE waves during pulsed YAG laser welding.
- **Grad et al. [86]** registered the produced AE waves using a microphone and a piezoelectric sensor during a **GMAW** process. It was stated that **short circuiting and arc reignition** are the main sources of generated acoustic waves during the GMAW process. Furthermore, the acoustic parameters are affected by the type of applied shielding gas and a **wire extension length of greater than 12 mm**.
- **Zhang et al. [87]** used acoustic emission and **air-coupled ultrasonic testing** to study in real time the presence of **burn-through in GTAW**. As shown in Figure 9, it was proved that when welding defects appear, a **sudden surge in the AE absolute energy** occurs.
- **Lee et al. [88]** investigated the generated plasma in **CO₂ laser lap welding** using a **photodiode and microphone**. It was shown that as the pore and spatter formation amount increases, the signal intensity decreases.

### 3.4 Data analysis of AE signals

The data analysis of the AE results, on which the subsequent interpretation is based, refers in most cases to the so-called detection of **"signal events"**. This means the characterization of acoustic signals which exceed a certain amplitude limit, on number of counts (statistics), amplitude energy, spectrum distribution, and similar descriptors. An exciting new area for the analysis and interpretation of AE signals is the use of **machine (deep) learning** methods. Some very interesting approaches similar to the process of LPBF (Laser Powder Bed Fusion) have already been made and could also be transferred/applied to WAAM; the authors refer the reader to the non-exhaustive bibliography [89–93].

---

## 4. Optical Emission Spectroscopy

### 4.1 Principle

In Optical Emission Spectroscopy (OES) the **electronic temperature profile** is determined during the process by means of assessing the generated light during the welding process. This temperature profile is then correlated with existing flaws in the component [17,94]. Figure 10 illustrates a schematic of OES analysis.

### 4.2 Research results with OES

- **Mills et al. [96]** discussed the applicability of different emission spectroscopy techniques in **GTAW**.
- **Mirapeix et al. [97]** proposed a **real-time technique** according to the electronic temperature determination of the plasma to identify **small defects in GTAW**.
- **Zhang et al. [98]** applied optical emission spectroscopy **for the first time** to study the structural characteristics of WAAM of an **Al alloy**. It was proved that the **spectral intensity, electron density and the width of the deposited layer are linearly related**. The spectral intensity and the electron density rose with the increase in the number of deposited layers; these showed a **steady-state tendency after the number of deposited layers reached 5 to 7**. In addition, it was evidenced that **porosity could be roughly identified via spectral analysis of the arc properties**, due to the relation between hydrogen content and porosity.
- **Kisielewicz et al. [99]** used **inline optical spectroscopy** to monitor **laser blown powder directed energy deposition (LBP DED) of Alloy 718**. Spectroscopy can be a solution for inspecting the LBP-DED process for the deposition of Alloy 718, and **laser power variables and continuum radiation intensity clearly correlate**.
- **Nassar et al. [100]** combined OES, data acquisition and a control system to recognize predefined defects in real time during **DED of a Ti-6Al-4V** part. It was demonstrated that a correlation exists between **atomic titanium (Ti I) and vanadium (V I) emissions** and predefined defects in the part.

---

## 5. Laser-Induced Breakdown Spectroscopy

### 5.1 Principle and equipment

Laser-Induced Breakdown Spectroscopy (LIBS) is a **real-time chemical analysis technology** that can determine the qualitative and quantitative chemical composition of a material based on the **wavelength and spectral intensity emitted by a laser-induced plasma**.

As shown in Figure 11, the following equipment is typically required: a pulsed laser, focusing optics, light collection optics, a spectrometer and a computer system.

Procedure:

1. Usually, LIBS uses a **Q-switched Nd:YAG laser** that emits a short laser pulse (commonly with a **pulse duration of 5–100 ns**) which is focused onto the surface of the specimen.
2. Owing to the high energy of the laser beam, a tiny amount of the sample is vaporized and forms a **plasma vapor cloud** above the surface.
3. The light emitted by the plasma is captured and transmitted into a **spectrometer via an optical fibre**, where the measurement of spectral intensities takes place.
4. The LIBS process is controlled, and the collected data are analysed, via a computer system [56,101].

### 5.2 Advantages and limitations

LIBS is widely applied in various industrial applications, e.g. for the inspection of solar cells to detect impurities. It provides several advantages over other analytical techniques such as **Inductively Coupled Plasma Atomic Emission Spectroscopy (ICP-AES)**, **Atomic Absorption Spectroscopy (AAS)**, **X-ray Fluorescence (XRF)** and **Energy Dispersive X-ray (EDX) spectroscopy**:

- requires no sample pre-treatment and little or no sample preparation;
- is performed in real time, in situ, in the field and contactlessly.

Limitations:

- lower accuracy;
- matrix effects;
- lower spectral intensities, due to the emission absorption of adjacent atoms around the generated plasma [56,101].

**Variants.** Double-Pulse LIBS (DP-LIBS), multi-pulse LIBS and Hand-Held LIBS (HH-LIBS) were later developed. In comparison to conventional LIBS, DP-LIBS applies **two laser pulses in sequence with different parameters**, and multi-pulse LIBS performs the analysis using **several laser pulses** to enhance the acquired intensities [56].

### 5.3 Research results with LIBS

- **Lednev et al. [102]** investigated the LIBS method to detect laser welding process failures **in situ**. They tested three methods:
  1. passive detection of the weld pool and weld plasma emission;
  2. online LIBS sampling of the solidified hot weld;
  3. in-situ LIBS measurements of the weld pool surface.

  Among them, **in-situ LIBS measurements successfully identified the defective zone from the non-defective area**.
- **Taparli et al. [103]** examined in-situ LIBS during the **GTAW** welding process. It was shown that the **Ar shielding gas flow and the welding arc plasma considerably influence the emission lines of chromium, nickel and manganese**.

There is a **lack of knowledge related to the implementation of LIBS in WAAM and fusion welding applications**.

---

## 6. Laser Opto-Ultrasonic Dual Detection

### 6.1 Principle

The Laser Opto-Ultrasonic Dual (LOUD) detection approach is based on the combination of **Laser-Induced Breakdown Spectroscopy (LIBS)** and **Laser Ultrasonics (LU)** technologies. Figure 12 displays the LOUD technology. The process can be briefly explained as follows:

1. A laser generates acoustic waves in **ablation mode**.
2. The produced **plasma spectra** are collected via an optical collector and transmitted through a fibre into a spectrometer.
3. The excited acoustic waves are received by an **ultrasound detector** and transmitted into a **data acquisition card**.
4. A **Digital Delay Generator (DDG)** is provided to activate the laser, the **Data Acquisition (DAQ) card** and the **Charge-Coupled Device (CCD) detector**.
5. Plasma spectra are used to detect **elemental information**, and the excited acoustic waves are recorded to investigate **defects or residual stresses** [28,29].

Figure 13 illustrates a possible concept of an **online LOUD monitoring system** proposed by Ma et al. [28], in which the ultrasonic detector and optical collector are attached to the robot arm.

### 6.2 Research results with LOUD

- **Ma et al. [28]** successfully utilized the LOUD approach **for the first time** to determine residual stresses and elemental information, as well as defects, of an aluminium alloy (**A6061**) produced with WAAM **in-process and simultaneously**. The use of LOUD as an NDT online monitoring tool in WAAM was recommended due to its **time and cost efficiency**.
- **Ma et al. [29]** in another work investigated at the same time the **grain size and elemental distribution** in an aluminium alloy produced in WAAM using LOUD. The results were in accordance with those obtained using **Electron Backscatter Diffraction (EBSD)**. It was also reported that LOUD is an excellent tool for evaluating the mechanical and chemical characteristics of AM parts.

There is a **lack of information regarding applying LOUD for other metals**, such as titanium alloy and other aluminium alloy-based parts.

---

## 7. Thermography

### 7.1 Classification

Thermography is commonly employed in many fields as it is able to detect **subsurface faults**, determine **thermophysical properties** and measure the **coating thickness** of components [104]. There are various criteria for the classification of thermography, e.g. **testing approach** and **applied stimulation source**. As shown in Figure 14, thermography is divided into two main techniques according to the testing approach:

1. **active thermography**
2. **passive thermography**

Based on the applied stimulation source, active thermography is subdivided into **five categories**:

- Lock-In Thermography (LIT)
- Pulsed Thermography (PT)
- Vibro-Thermography (VT)
- Step Heating Thermography (SHT)
- Eddy current thermography [105–107]

### 7.2 Active vs. passive thermography

Figure 15 indicates an illustration of defect detection by means of the thermography method; Figure 16 shows a schematic of the active thermography technology.

- In **active thermography**, the under-inspection component is exposed to **thermal stimulation (cold or warm) from an external source**, such as halogen lamps, pulsed lamps and laser.
- In **passive thermography**, the heat distribution inside the material is **inherent**, e.g. as a result of the manufacturing process.

The homogenous heat distribution inside the material interacts with the imperfections within the material. This **inhomogeneous heat diffusion** on the surface of the part caused by existing defects inside the material is recorded via an **infrared (IR) camera**. The IR camera receives the emitted infrared waves from the surface of the material and converts them into electrical signals and subsequently into IR images. The defects can then be visualized by analysing the images [105–107].

### 7.3 Lock-in thermography

Lock-in thermography belongs to the NDT techniques according to **photothermal radiometry**, in which one or more heat sources are used to **continuously heat** the surface of the part under inspection. The heat waves are transmitted to the components through **radiation**; they interact with the imperfections within the part and return. An infrared camera is used to capture the returned heat waves and a **lock-in amplifier** measures the **amplitude and phase of the modulation**. The phase and amplitude of the returned thermal waves change owing to the difference in the thermal properties of the defected and non-defected regions inside the component [106,109]. **Data acquisition takes more time in lock-in thermography** [110].

### 7.4 Pulsed Thermography (PT)

PT has been employed in the aerospace industry for various applications, such as the evaluation of airplane components [104]. This technology is able to detect **online and very quickly** various defects such as **cracks, fatigue damage, rust and delamination** in different materials [111].

Infrared lamps, halogen lamps and hot air guns are used to generate **one or more thermal pulse(s)** on the surface of the components **within 2–10 ms**. Heat transfers inside the material and interacts with the existing defects. The inhomogeneous heat distribution on the surface of the part caused by the internal defects is measured using an IR camera. Figure 17 illustrates a common PT setup. The required equipment is usually:

- an external heat generator (infrared lamps, halogen lamps, hot air guns);
- an infrared camera;
- a control unit;
- a computer with data processing software [111,112].

### 7.5 Step pulsed thermography

Compared to pulsed thermography, step pulsed thermography applies **longer, homogenous and uninterrupted pulses with a low energy density** to detect defects located at a **deeper distance** from the surface of the material. Defects have a different temperature and heat transfer rate in comparison to non-damaged parts of the under-inspection component. An IR camera is used to record the **whole heating and cooling process**. The surface temperature alternations are captured and analysed to detect defects [113,114].

### 7.6 Vibrothermography

Vibrothermography combines an ultrasonic testing method and thermography to detect **subsurface and near-surface defects**, such as **cracks, disbands and delamination**, quickly and precisely. As depicted in Figure 18, the soundwaves created by a **vibration source**, e.g. a piezoelectric transducer, travel through the component. As they meet the defects, the **vibration energy is converted into heat due to friction**. The generated heat is transferred to the surface and captured via an IR camera. A common setup is composed of an ultrasonic vibration source, an infrared camera, a control unit and a PC with data processing software [112,115].

### 7.7 Eddy current thermography

This technology is categorized under **non-optical thermography methods** [106] and takes advantage of eddy current and thermography NDT approaches. Figure 19 displays an illustration of eddy current thermography. **Eddy current flow is created inductively inside electroconductive materials**, which results in an increasing temperature of the component. When defects exist inside the material being tested, the current flow — and subsequently the heat distribution — is disturbed. The non-uniform heat distribution is captured through an IR camera [117]. Eddy current thermography makes it possible to **quickly and contactlessly inspect the components with a high resolution** [110].

### 7.8 Research results with thermography

- **Bacelar et al. [17]** utilised **passive thermography** to detect **four intentionally introduced holes** during the WAAM process. It was found that the defective area has a **higher temperature** compared to the flawless region, as it dissipated less heat to the surroundings.
- **Yang et al. [119]** monitored the surface temperature of the deposited layers in the WAAM process by means of passive thermography and reported that thermography is able to precisely measure the surface temperature during the process.
- **Mireles et al. [39]** explored the ability of IR thermography to monitor in situ the parts produced by **powder bed fusion** technology. They purposely placed different defects with diverse sizes and shapes into an assembly part. An IR camera with a **resolution of 640 × 480 and a pixel length of 260 µm** was adopted. It was reported that **defects smaller than 600 µm were not detected** with the setup used.
- **Runnemalm et al. [120]** evaluated three types of excitation sources — a **flash lamp, eddy current induction and a continuous laser** — for thermography, to study surface defects such as cracks, pores and lack of penetration.
  - A combination of a **flash lamp positioned at a distance of 120 mm with 6 kJ energy within 0.05 s**, a **FLIR SC5650 IR camera with a spectral range of 2.5–5.1 µm** and an **optical lens of 27 mm** allowed a notch to be detected with a **length of 760 µm and a width of 400 µm**.
  - **Five holes with a diameter of 1.0 to 2.5 mm** were created on the workpiece and examined via eddy current thermography. An **induction coil located at a distance of greater than 10 mm** from the component heated up the component. **All holes were recognized** via eddy current thermography.
  - It was possible to **detect all eight artificially produced defects** on the component under evaluation by means of the laser.
- **Roemer et al. [112]** compared **laser thermography** and **vibrothermography** for fatigue crack detection in an **aluminium bar**. They coated the sample surface with black paint, because aluminium has a lower heat emissivity.
  - Laser thermography: a **laser power of 100 W** with a **pulse length of 100 ms** generated a **5 K temperature increase**; heat diffusion was monitored with an IR camera with a **resolution of 256 × 320** and a **frequency of 60 Hz**.
  - Vibrothermography: an ultrasonic transducer with a **frequency of 35 kHz** and a **power of 500 W** generated sound waves with a **pulse duration of 500 ms**; the process was recorded with an IR camera with the same resolution and a **frequency of 150 Hz**.
  - In both experiments, fatigue cracks were identified easily. They also claimed that an IR camera equipped with a **zoom and focus lens** enables the detection of **micro-size defects** in laser thermography.
- **Sreedhar et al. [121]** utilized the **passive thermography** method for real-time inspection of a **TIG-welded aluminium alloy-based tank (aluminium alloy 2219)**. An IR camera was attached on the welding arm at an **angle of 60°** to the welding plate and **150 mm behind the welding arc** to capture a newly welded area of **100 mm**. They could detect a **cluster pore of size 0.6 mm × 0.4 mm**.
- **Elkihel et al. [122]** studied the thermal propagation of a weld joint using an **active thermography** method. They heated the weld joint **inductively up to 80 °C** and captured the heat propagation using a **FLIR T440 infrared camera with a resolution of 320 × 240 and a bandwidth of 7.5 to 13 µm** pixels. It was claimed that the **heat loss on the weld zone is much more significant than that of the defective region**.
- **Massaro et al. [123]** proposed a novel technique for identifying weld defects on a welded **steel tank (AISI 304/316)** using infrared thermography and image processing. They cut out a specimen and excited it with a **heat gun**. The heat distribution on the surface was registered using a **FLIR T 1020 with a resolution of 1024 × 768 pixels**. It was reported that a combination of IR thermography and various image-processing techniques — the **line calculus method, 2D K-Means algorithm, 2D morphology functions and a Long Short Term Memory (LSTM) artificial neural network** — can be a powerful tool for real-time identification and classification of weld defects.
- **Ziegler et al. [124]** evaluated the use of **high-power laser excitation sources** in the lock-in thermography technique. They claimed that the use of high-power lasers instead of LEDs and halogen lamps has practically no influence on the thermal emission generated by the excited sample, as their emission is based on **electroluminescence**. Thus, it can be performed in **single-sided transient thermography**. Furthermore, it is possible to use **high-power laser arrays** for the analysis of highly reflective materials such as aluminium, if additional power scaling or focusing is provided.
- **Cerniglia et al. [125]** evaluated **two additively manufactured Inconel 600 specimens** with various intentionally inserted **micro-sized defects located at different depths** to establish an analogy between **laser ultrasonic** and **laser thermography** techniques. Both methods demonstrated their ability to inspect the samples **in-line**. They emphasized that for the deployment of laser thermography for automatic inline inspection, **liquid-cooled IR cameras should be replaced by microbolometric IR cameras**, since they [liquid-cooled cameras] are more expensive and larger. In addition, using laser thermography for component surfaces with **low emissivity values requires a high-power laser**.

---

## 8. Defect Detection by Monitoring WAAM and Fusion Welding Process Parameters

### 8.1 Principle

Various physical phenomena — **metal transfer, short circuiting, spatter, ionization, gas-metal reactions** — occur very fast during the welding process, which causes **variations in current and voltage**. Distinct welding parameters can be assessed if the current and voltage signals are recorded simultaneously as these phenomena take place [126]. **High-speed data acquisition systems, such as digital storage oscilloscopes (DSOs)**, are able to register these signals [127].

### 8.2 Research results with DSOs and process-parameter monitoring

- **Mičian et al. [128]** utilised a digital oscilloscope in combination with other equipment, such as a **galvanic separator** and a notebook with software, to capture the **instantaneous current and voltage of the CMT process during MIG brazing** of automotive components.
- **Kumar et al. [129]** employed a DSO with a **sample rate of 40 kHz** to collect the welding parameters for **two inverter and two generator power sources** during welding using **two different electrodes**. It was claimed that a commercial DSO is able to obtain the welding data and can be further used to assess the welding process **in situ and online**, and can be a powerful competitor to other data acquisition systems designed for the same purpose due to the comparable **data acquisition speed, volume and accuracy**.
- **Savyasachi et al. [130]** took advantage of a DSO and a **high-speed camera simultaneously** to monitor **Shielded Metal Arc Welding (SMAW)**. They proved that combining both technologies allows the investigation of different physical phenomena during the process at once. In addition, the collected data from a DSO require **proper filtering** to analyse the data.
- **Kumar et al. [126]** found that a **Fast Fourier Transform Low Pass Filter (FFT LPF)** is a suitable method to filter the acquired signals during SMAW, due to its higher **signal-to-noise ratio** value compared to other techniques. In addition, a **100 kHz sample rate is a sufficient value** for data acquisition using a DSO during SMAW.
- **Mazlan et al. [131]** successfully combined a DSO and a **Short Time Energy (STE)** method to detect welding defects in **GMAW**. The acquired welding current using a DSO was applied as input data for the STE analysis method conducted in **MATLAB/Simulink**. Using this method enabled the **smooth current and disturbance current to be distinguished**, which results in differentiating the defective weld from the non-defective weld.
- **Šoštarić et al. [10]** introduced an **online monitoring system** to acquire the main welding parameters and to process the data in **resistance welding and arc welding**. They made an analogy between the acquired results using a self-developed online monitoring system and those obtained using an oscilloscope. The results demonstrated that the self-developed online monitoring has the ability to be implemented in practical applications.

---

## 9. Summary and Conclusions

This paper provides a comprehensive review of various NDT techniques, including laser-ultrasonic, acoustic emission with an airborne optical microphone, optical emission spectroscopy, laser-induced breakdown spectroscopy, laser opto-ultrasonic dual detection, thermography and also in-process defect detection via monitoring the process parameters in WAAM and fusion welding. In addition, novel research results, operating principles and the equipment required to perform these techniques have been presented. The minimum detectable welding defect size of most current NDT techniques was collected via previous research or experience of companies.

(The full conclusion bullet list is reproduced verbatim in the section **"Conclusions (as stated by the authors)"** below.)

### Back matter

- **Author Contributions:** Conceptualization, M.S. (Masoud Shaloo), M.S. (Martin Schnall), T.K., N.H. and B.R.; methodology, M.S. (Masoud Shaloo), N.H. and B.R.; investigation, M.S. (Masoud Shaloo); resources, T.K.; data curation, M.S. (Masoud Shaloo); writing—original draft preparation, M.S. (Masoud Shaloo); writing—review and editing, M.S. (Masoud Shaloo), M.S. (Martin Schnall), T.K., N.H. and B.R.; visualization, M.S. (Masoud Shaloo); supervision, T.K., N.H. and B.R.; project administration, M.S. (Masoud Shaloo), M.S. (Martin Schnall); funding acquisition, T.K. All authors have read and agreed to the published version of the manuscript.
- **Funding:** The consortium thanks the ministry of "Climate Action, Environment, Energy, Mobility, Innovation and Technology" (BMK), the ministry of "Digital and Economic Affairs" (BMDW), the Austrian Funding Agency (FFG), as well as the four federal funding agencies Amt der Oberösterreichischen Landesregierung, Steirische Wirtschaftsförderungsgesellschaft m.b.H., Amt der Niederösterreichischen Landesregierung and Wirtschaftsagentur Wien and Ein Fonds der Stadt Wien for funding project **"We3D" (FFG Nr. 886184)** in the framework of the **8th COMET call**. Further thanks go to the industry partners for their financial contributions as well as their research contributions in the five multi-firm projects.
- **Data Availability Statement:** The data can be found in the original works cited throughout this article.
- **Acknowledgments:** The authors thank the academic partners involved in the project for fruitful discussions.
- **Conflicts of Interest:** The authors declare no conflict of interest.

---

## Figures

### Figure 1 — A combination of radiographic and image processing techniques for welding defect detection conducted by Faramarzi et al. [18] (p. 3)

Four side-by-side image pairs, one pair per defect type. Each pair shows, on top, the raw radiographic/inspection image of a horizontal weld seam (a bright, slightly grainy band running left to right on a black background), and, below it, the same image after the MATLAB image-processing chain, with the detected defect marked in **red**.

- **"Brun Through" (burn-through):** greyscale radiograph of a bright weld bead crossing the frame; two small dark round spots interrupt the bead. In the processed image, the two spots are overlaid with red blobs.
- **"Lack of Fusion":** the image is rendered in blue/cyan false colour; the weld bead appears as a chain of bright cyan ellipses; several short dark linear features lie along the bead. Processed image marks three of them in red, plus a small red mark at the left edge.
- **"Lack of Penetration":** greyscale radiograph of a bright bead with a thin, continuous dark line running along the middle of the seam. In the processed image, a long, continuous red line traces this linear indication over roughly the central half of the seam.
- **"Slag":** greyscale radiograph of a ribbed/segmented bright bead; three dark inclusions sit on the bead. The processed image marks each of the three with a short red vertical tick/blob.

### Figure 2 — A comparison between dye penetrant testing (the dashed section in (A) depicts the area examined with ultrasound techniques shown in (B)) (A), conventional ultrasonic (B) and X-ray radiographic technologies (C) carried out by Seow et al. [20] (p. 3)

Three stacked panels sharing a common horizontal length scale for a long WAAM wall (Alloy 718).

- **(A) Fluorescent dye penetrant:** a photograph under UV light of a long, narrow WAAM wall, imaged in deep blue. A ruler across the top is graduated in mm with labelled ticks at **100, 200 and 300 mm**. About 20–25 bright white, branched, near-vertical **crack-like indications** rise from the lower part of the wall into the deposit; they are concentrated between roughly 60 mm and 300 mm. A **red dashed rectangle** encloses the upper band of the wall and is labelled **"Ultrasound region"** at the right; the label "Fluorescent dye penetrant" appears in white at the lower left. A bright wavy white line runs along the bottom edge of the wall.
- **(B) Ultrasound measurements:** a line plot. **y-axis: Amp (dB), from −50 to 0 dB** with ticks every 10 dB. **x-axis: Location at WA direction (mm), from about 25 to 310 mm**, ticks at 50, 100, 150, 200, 250, 300. The dark blue trace oscillates rapidly, with the envelope mostly between about 0 and −15 dB and numerous deep, narrow downward spikes reaching **−30 to −40 dB** (deepest excursions near ~110 mm, ~118 mm, ~150 mm and ~188 mm, touching about −40 dB). The density of deep minima increases along the scan, matching the positions of the crack indications visible in (A).
- **(C) Filtered digital X-ray radiograph:** a greyscale radiograph of the same wall, shown as a light-grey elongated rectangle with a scalloped (wavy) upper and lower edge from the individual weld beads. Faint dark vertical lines (the cracks) are visible mainly in the right half. Axis arrows at the lower left are labelled **TT** (vertical, travel/through-thickness direction) and **WA** (horizontal, wall direction); "Ultrasound region" is labelled at the upper right.

### Figure 3 — Inspected WAAM component. D1, D2 and D3 represent the welding defects [25] (p. 4)

A close-up photograph of the side face of a plasma-arc WAAM Ti-6Al-4V wall. The surface shows horizontal, strongly iridescent layer bands (oxide tint colours: green, brown, purple, cream, blue-grey), one band per deposited layer. Three small dark, roughly circular defects are marked with cyan labels **D1** (upper left area), **D2** (centre) and **D3** (centre right, slightly lower). A **white dashed rectangle** outlines the **"Imaging area"**, and a horizontal double-headed blue arrow above it marks the **"Array Aperture"**. Two further dark spots are visible to the right, outside the imaging area.

### Figure 4 — Intentionally introduced defects (D1, D2 and D3 in Figure 3) are detected by means of TFM image of the component using ultrasonic longitudinal waves [25] (p. 4)

A rectangular Total Focusing Method (TFM) B-scan-style colour image on a dark blue (low-amplitude) background.

- **y-axis: "Depth from surface (mm)", running 0 (top) to 15 (bottom)**, labelled ticks at 5, 10, 15.
- **x-axis: lateral position, running from +15 on the left through 0 to −15 on the right** (ticks at 15, 10, 5, 0, −5, −10, −15; units mm).
- **Colour bar on the right: 0 (red) down to −8 (dark blue)**, in dB, with labelled ticks at 0, −2, −4, −6, −8.

Content: a bright, speckled red/green/cyan horizontal band along the very top of the image (the surface/entry echo), strongest between about x = +5 and x = −7. A faint diagonal streak of cyan speckle runs from the top down to roughly (x ≈ +5, depth ≈ 3–4 mm). Three isolated, well-focused hot spots (red cores with green/cyan haloes) are visible, corresponding to the three defects:

- one at about **x ≈ +8, depth ≈ 5.5 mm** (D1),
- one at about **x ≈ −2, depth ≈ 8 mm** (D2),
- one at about **x ≈ −13, depth ≈ 10 mm** (D3).

Everything below ~11 mm is uniform dark blue (no indication).

### Figure 5 — Laser ultrasonic inspection system [48] (p. 7)

A block schematic of a LU inspection setup, drawn in grey line art.

- On the far left: a tall grey rectangle labelled **"Sample"**.
- Just right of it: a **"Measurement Head"** (a small block with a lens/nozzle pointing at the sample); zig-zag arrows between head and sample indicate the outgoing/returning laser beams.
- The head connects through a dashed box labelled **"Fiber Umbilical"** (a fibre bundle) to a large dashed box on the right labelled **"Base Station"**.
- Inside the Base Station: three stacked units — **"Generation Pulsed Laser"** (top), **"CW Probe Laser"** (middle, with a small beam-steering mirror block in front of it), and **"Receiver"** (bottom, a rack unit with knobs and connectors).
- At the bottom left, a **"Computer"** (CRT monitor plus keyboard) is cabled to the Receiver.

Signal/energy path: pulsed generation laser and CW probe laser → fibre umbilical → measurement head → sample; the reflected/phase-modulated probe light returns via the same head and fibre to the receiver, whose demodulated output is digitized and displayed on the computer.

### Figure 6 — Thermoelastic (a) and ablative (b) phenomena in UL [57] (p. 8)

Two side-by-side cross-sectional sketches of a grey solid half-space with a white background above the surface.

- **(a) Thermoelastic source:** three vertical downward arrows labelled **"Laser pulse"** strike a small cross-hatched patch at the surface. Two horizontal arrows point outward (left and right) from the patch within the solid, labelled **"Temperature rise"** (left) and **"Principal stresses"** (right). A short upward arrow at the right edge of the patch is labelled **"Thermoelastic expansion"**. No material is removed — the source is a buried in-plane stress dipole.
- **(b) Ablative source:** downward arrows labelled **"Laser pulse"** pass through a **"Converging lens"** (drawn as a lens outline) and focus to a spot on the surface; above the spot a plume labelled **"Ablation of metal and plasma"** expands upward. Below the surface a cross-hatched patch is labelled **"Region of melting and vaporization"**; a downward arrow labelled **"Net reactive force"** points into the solid, and horizontal arrows point outward on both sides. The recoil of the ejected vapour acts as a normal force source, which is why the ablative regime produces much larger wave amplitudes but is destructive.

### Figure 7 — Graphical illustration of a conventional AE measurement system [76] (p. 10)

A schematic of the AE signal chain.

- **Left:** a specimen drawn as a curved, wedge-shaped body. Three arrows at the upper-left edge and three arrows at the bottom indicate applied load. Inside it, a **"Crack"** is marked, radiating concentric arc-shaped wavefronts up toward the surface.
- An **"AE transducer"** is mounted on the top surface of the specimen.
- **Signal path (left to right):** AE transducer → **"Pre-amplifier"** (triangle symbol) → **"Filter"** (box containing a bandpass response curve) → **"Amplifier"** (triangle symbol) → **"Signal conditioner and event detector"** (large box). An additional input arrow labelled **"Parametric inputs"** enters the signal conditioner from the left.
- **Output:** from the signal conditioner down to a monitor/terminal labelled **"Computer data storage post-processor"**.

### Figure 8 — Schematic of the membrane-free optical microphone by Xarion [77] (p. 11)

A 3-D perspective schematic of a rigid optical (membrane-free) microphone.

- On the left, a grey block labelled **"Laser"** emits a red beam horizontally to the right.
- The beam first hits a tilted blue-glass **beam splitter**; a red arrow goes downward from it into a small grey cylinder labelled **"Optical fibre"** (the return path toward the photodiode).
- The transmitted red beam continues horizontally and passes through the gap between **two parallel transparent plates, each labelled "Mirror"** — a Fabry–Pérot etalon with air as the sensing medium.
- Above and between the two mirrors, a loudspeaker icon at the top emits a fan of concentric blue arcs labelled **"Sound"** which propagate down into the gap between the mirrors.

The sound wave modulates the air density (hence the refractive index) in the etalon, changing the optical path length; this intensity/phase change is read out through the fibre.

### Figure 9 — A correlation between acoustic emission absolute energy and welding defect [87]. (a) depicts the inspected sample. (b) shows the acquired AE absolute energy of the inspected weld seam (p. 12)

- **(a)** A colour photograph of a GTAW weld seam on a copper-coloured plate, seen from above, with the weld bead running horizontally through the middle. The right-hand third of the plate is visibly discoloured (dark/grey-blue oxide banding) and shows a lighter, disturbed bead. A white vertical rectangular box marks the region of interest at roughly **80–90 mm**. Below the photo, a ruler graduated in **MM/CM** with labels **0 to 14 cm** provides the length scale.
- **(b)** A plot of the AE data. **y-axis: "AE absolute energy", from 0 to 2.5 × 10⁶** (ticks 0, 0.5, 1, 1.5, 2, 2.5; the ×10⁶ multiplier is printed at the top left). **x-axis: "Location(mm)", 0 to 140 mm** (ticks every 20 mm). The trace is essentially flat at ~0 along the whole seam, except for a **rectangular/trapezoidal plateau of about 0.45 × 10⁶ between roughly 78 and 88 mm**. Superimposed at the same location is a near-vertical cluster of scattered black dots spanning from about **0.7 × 10⁶ up to a maximum of ≈2.1 × 10⁶**, plus a single isolated dot at about 0.42 × 10⁶ near x ≈ 5 mm. The energy surge coincides exactly with the boxed burn-through region in (a).

### Figure 10 — A schematic of the OES technique [95]. In this illustration, the recorded electronic temperature is correlated with the existing welding defects (A, B and C) (p. 12)

Two vertically aligned panels sharing the x-axis.

- **Upper panel:** a line plot with **y-axis Tₑ (eV) from 0.4 to 0.8** (ticks 0.4, 0.5, 0.6, 0.7, 0.8) and **x-axis 0 to ~270** (ticks 0, 50, 100, 150, 200, 250; units mm as given by the lower label). The trace has a quiet baseline at about **0.48–0.50 eV** for x ≈ 0–150 mm, interrupted by a few isolated narrow spikes (to ~0.55–0.62 eV near x ≈ 5, 45, 57, 70–80 and a prominent one to ~0.62 eV at x ≈ 108). From about **x ≈ 160 mm onward the signal becomes strongly and densely spiked**, with many excursions to **0.65–0.79 eV** (the tallest near x ≈ 163, 214, 232 and 265) and one downward excursion to ~0.43 eV near x ≈ 233.
- **Lower panel:** a greyscale photograph of the corresponding weld seam (a bright, narrow bead on a dark, rough plate), aligned to the same length axis and labelled **"Length (mm)"**. Three defect positions are marked with letters between the plot and the photo: **A** at about x ≈ 110 mm, **B** at about x ≈ 215 mm, **C** at about x ≈ 240 mm. The seam appears smooth and regular up to about 160 mm and visibly disturbed/irregular to the right, where the electronic-temperature spikes cluster.

### Figure 11 — Picture of the LIBS setup [56] (p. 13)

A block schematic of a laboratory LIBS system.

- **Top left:** a desktop **computer** (monitor showing a spectrum with sharp emission peaks, plus keyboard). A line labelled **"Laser control"** runs from the computer to the right, to a vertical black cylinder labelled **"Q-switched Nd:YAG laser"**.
- **Middle left:** a blue box labelled **"ICCD"**, connected upward to the computer by a double-headed arrow and to the right by a line labelled **"Synchronization"** running to the laser.
- **Lower left:** a large green box labelled **"Echelle Spectrograph"**, connected upward to the ICCD and to the right via a line labelled **"Collection lens"**.
- **Right:** the Nd:YAG laser beam is directed downward through focusing optics onto a **"Sample"** mounted on a **"Motorized XYZ transition stage"** (grey platform). A bright yellow/orange **"Plasma plume"** is drawn above the sample surface. An angled collection lens (with a small mirror icon) picks up the plasma light and routes it to the spectrograph.

### Figure 12 — A picture of the LOUD process [28] (p. 14)

A coloured 3-D schematic of the laser opto-ultrasonic dual detection bench, with an enlarged inset.

- **Main layout (left to right, top to bottom):** a **DDG** unit (blue LED display) at the top; a **PC** with a waveform on screen next to it; a black **"Nd:YAG Laser 532 nm"** head emitting a **green "Laser"** beam to the right; the beam hits a blue **"Reflector"**, is turned down toward a **"Pierced Mirror"**, passes **"Lens 1"** and focuses on the **Sample** mounted on a circular stage.
- **Collection branch:** the plasma light returning through the pierced mirror is drawn as a rainbow-coloured beam, passes **"Lens 2"** into a **"Collector"**, then through a **"Fiber"** into the **"Spectrometer"**, which carries a **"CCD"** detector module.
- **Ultrasound branch:** an **"Ultrasound Probe"** is coupled to the underside of the sample and cabled to a blue **"DAQ"** rack at the lower left.
- **Inset (right, circular magnification):** the focused **"Laser Beam"** (green cone) strikes the grey **"Sample"** surface; an orange/red **"Plasma"** burst with radiating arcs sits at the impact point, a rainbow cone labelled **"Optical emission"** leaves upward, and a blue cone labelled **"Ultrasound generated"** propagates downward into the sample.

### Figure 13 — A schematic of a proposed laser opto-ultrasonic setup for online monitoring by Ma et al. [28] (p. 15)

A coloured 3-D schematic of an inline WAAM monitoring cell.

- A large yellow cylindrical **"Robot Arm"** enters from the upper left and carries a blue **"Arc Torch"** angled down onto a blue **"Sample"** plate on a table.
- At the torch tip, an orange glow labelled **"Arc Plasma"** marks the melt pool.
- Two sensors point at the arc: an **"Optical Collector"** on the left and an **"Acoustic Collector"** (a conical probe) on the right of the torch.
- Cabling (brown and blue lines) runs from the collectors to a blue **"Spectrometer"** box (right) and a blue **"DAQ"** rack (lower right).
- A **"DDG"** unit (blue display) sits at the upper right, cabled to the spectrometer/DAQ and to a grey **"PC"** whose monitor displays acquired waveforms.

### Figure 14 — Thermography NDT techniques [105,106] (p. 16)

A four-level hierarchical block diagram (coloured boxes).

- **Level 1 (dark red, full width):** "Infrared Thermography".
- **Level 2 (grey):** a narrow box on the left, "Passive Thermography", and a wide box on the right, "Active Thermography".
- **Level 3 (teal, under Active Thermography only):** "Optical/ external excitation (laser, flash lamp, etc.)" on the left and "Mechanical/ external excitation" on the right.
- **Level 4 (dark purple):** under the optical branch — "Lock-in Thermography", "Pulsed Thermography", "Step Thermography"; under the mechanical branch — "Vibrothermography", "Eddy current Thermography".

### Figure 15 — Defect detection by means of the thermography technology performed by Broberg [108]. (a) displays the defect (the arrow shows its position). (b) shows the captured thermal image, in which the defect can be recognised (p. 16)

- **(a)** A greyscale photograph/micrograph of a machined or ground metal surface with strong curved grinding/machining striations sweeping from upper right to lower left. A white downward arrow in the lower-central part points to a small, dark, elongated horizontal **defect** (a flat, lens-shaped dark mark). A scale bar below the image is graduated **0, 1, 2, 3, 4 [mm]** — the defect is roughly 1 mm long.
- **(b)** A false-colour infrared thermal image, square, on a dark blue background. **y-axis in [mm], 0 to 12** (ticks 0, 2, 4, 6, 8, 10, 12); **x-axis in [mm], 0 to ~11** (ticks at 0, 5, 10). A roughly circular/oval hot region (cyan → green → yellow) is centred at about x ≈ 6 mm, y ≈ 5–7 mm, and within it sits a short, sharply defined **dark-red horizontal streak at about y ≈ 4.5 mm** — the defect indication, which is the hottest feature in the frame. A vertical white bracket labelled **"Weld"** on the right marks the vertical extent of the weld (about y = 3.5 to 9.5 mm). A horizontal **colour bar** below runs from dark blue through cyan, green, yellow, orange to dark red, calibrated **22, 24, 26, 28, 30, 32, 34 °C**.

### Figure 16 — A schematic of active thermography [106] (p. 17)

A line-art schematic on a grey background.

- Top left: an **"IR-camera"** (cylindrical lens body) aimed downward; two lines from the lens diverge to the specimen surface, indicating the imaged field of view.
- Top right: an **"Excitation source"** (a tilted box) with a large thick arrow pointing down toward the surface, labelled **"Energy for heat flow excitation"**.
- Bottom: a grey block labelled **"Specimen"**. Inside it, near the left, a small black elongated ellipse labelled **"Flaw"**. Concentric arc-shaped contour lines spread from the flaw region up to the surface, labelled **"Thermal answer"** — the disturbed heat flow that the IR camera sees as a surface temperature contrast.

### Figure 17 — Pulse thermography setup [105] (p. 17)

A line-art schematic of a reflection-mode PT bench.

- Centre top: an **"IR Camera"** on a tripod-like body, aimed downward at the sample.
- Left and right of the camera: two **"Flash Lamp"** units (trapezoidal reflectors) angled toward the sample.
- Bottom centre: the **"Sample"**, drawn as a long horizontal rectangle with two short dark dashes inside it representing subsurface defects.
- Between sample and camera: three dashed upward arrows representing emitted IR radiation.
- Right: a **"Control Unit"** box (with indicator LEDs) wired by lines running along the top of the figure to both flash lamps and to the camera; below it a **"PC"** (monitor plus tower) connected up to the control unit.

### Figure 18 — A picture of a vibrothermography setup [116] (p. 18)

A line-art schematic.

- Left: a tall vertical plate labelled **"Test sample"**. A **"Vibration source"** (a small cylindrical transducer with a horn tip) is coupled to its upper edge; an arrow from the control unit feeds it. Lower down inside the plate, concentric arcs radiate from a point, representing the ultrasonic energy converted to heat at a defect.
- Centre right: a rack box labelled **"Control unit"**, with arrows to the vibration source, from/to the infrared camera, and to the PC.
- Bottom centre: an **"Infrared camera"** (tilted box with lens) aimed at the test sample.
- Bottom right: a laptop labelled **"PC"**.

### Figure 19 — An illustration of eddy current thermography [118] (p. 18)

A schematic in grey/black line art.

- Left centre: a grey block labelled **"Part"**, containing a small dark defect and an arc labelled **"Thermal wave"** propagating toward the surface.
- Below the part: a coil icon (concentric arcs) labelled **"Eddy current"**, inductively coupled into the part.
- Right of the coil: a black rack unit labelled **"Generator"**, cabled to the coil and upward to the computer.
- Left: an **"IR-Camera"** (upright cylindrical body) aimed at the part surface.
- Top right: a grey **"Computer"** (monitor and tower), cabled to the IR camera and the generator, with a large white panel below it labelled **"Result image with detected defects"** showing an irregular black blob (the detected flaw) on a white field.

---

## Tables

### Table 1 (pp. 5–6) — A review of NDT methods and the smallest detected defect for WAAM and fusion welding. (✓ represents suitable method and X stands for unsuitable technique)

The "Suitable for Online/Offline Monitoring" column is written as **online / offline**.

| NDT Method | Summary of the Operation Procedure | Suitable for Online/Offline Monitoring | The Smallest Detected Defect (µm) |
|---|---|---|---|
| Visual inspection [17] | An expert evaluates the workpiece with a naked eye or various simple equipment such as magnifiers or endoscopes [17]. | X/✓ | No information available |
| Liquid penetrant testing [9] | The fluorescent penetrant is applied on the surface of the material. It penetrates the defects, then the additional fluorescent is cleaned, and a developer used, which causes the defects to be identified [9]. | X/✓ | >750 [26] |
| Magnetic particle testing [9] | In the first step, component magnetization occurs. Imperfections cause a magnetic current to penetrate the material. After that, the particles are spread on the surface of the component, leading to particle accumulation in the penetration zone and, finally, welding defects detection [9]. | X/✓ [17] | >1000 [27] |
| Eddy currents [9] | A magnetic field is created surrounding the examined workpiece by means of an emitted coil. The generated eddy currents inside the sample are alternated by the existing welding flaws. The welding defects can be detected via the variations in the impedance of the coil equivalent to the alternation of the eddy currents [9]. | ✓/✓ [17] | >350 [22] |
| Laser opto-ultrasonic dual detection [28,29] | It combines both laser ultrasonic and laser-induced breakdown spectroscopy technologies to detect defects and acquire elemental information of the tested material during the process [28,29]. | ✓/X | No information available |
| Conventional acoustic emission [9] | A piezoelectric transducer placed on the surface detects the generated acoustic waves during the manufacturing process [9]. | ✓/X [17] | No information available |
| Acoustic emission using optical microphone [30] | An airborne optical microphone with the ability to hear the frequencies up to 2 MHz is used to detect the soundwaves during the process [30]. | ✓/X [31] | No information available |
| Conventional ultrasonic testing [9] | Acoustic waves generated by a transducer, which has contact with the sample, are propagated into the specimen. These waves interact with the welding defects and then return to the surface of the specimen. These waves are detected and evaluated to recognize the defects [9]. | X/✓ [9] | >500 [32] |
| Phased array ultrasonic testing [9] | A PC is employed to control each multi-element probe instead of single element probe in conventional ultrasonic testing to create a concentrated ultrasonic beam, and a software to direct it [9]. | ✓/✓ [17] | >600 [24] |
| Immersion ultrasonic testing [9] | In comparison to conventional ultrasonic, the examined component is plunged into the liquid (usually water). Using this technology eases the transmission of the waves into the sample [9]. | X/✓ [17] | >500 [32] |
| Electro-magnetic acoustic transducer [9] | An electro-magnetic sensor is employed near to the surface of the sample to generate and capture the acoustic waves. This technology is contactless and does not require any couplant [9,33]. | ✓/✓ [17] | >500 [32] |
| Laser ultrasonic testing [9] | The excitation and reception of the soundwaves occurs by means of two different lasers [9]. | ✓/✓ [17] | >100 [34] |
| Radiographic inspection [9] | Although the sample uniformly receives the excited radiation energy, imperfections, density alternation and thickness areas captured the radiation energy ununiformly. Thereafter, film(s) or electronic devices are used to capture the absorption differences [9]. | X/✓ [17] | >45 Digital Radiographic [35] |
| Real-time radiography (RTR) [36] | Compared to conventional radiography, digital data are generated during X-ray penetration in the sample [36]. | ✓/✓ [11] | >250 conventional RTR [11]<br>>250 RTR with Image Processing [11]<br>>50 Microfocus RTR with Image Processing [11] |
| X-ray backscatter [9] | One of the main comparison between the X-ray backscatter and conventional X-ray technique is that the returned X-ray energy from a single side of the tested sample is recorded in the X-ray backscatter technique [9,37]. | ✓/✓ [17] | >20 [9] |
| Computed tomography [9] | A number of 2D X-ray images are captured surrounding a rotation axis. These are collected and used to create a 3D model of the sample by applying algorithms [9,38]. | X/✓ [17] | >600 [39]<br>>10 for micro-CT [40] |
| Infrared Thermography [9] | During the monitoring, an IR camera is used to measure the temperature difference on the surface of the sample caused by the presence of the defects [9]. | ✓/✓ [17] | >400 [41] |
| Eddy current thermography [9] | The heat is generated in the examined material generated by eddy current method and recorded by an IR camera [9]. | ✓/✓ [9] | >400 [41] |
| Vibrothermography [9] | The produced soundwaves by an UT transducer inside the material collide with the defects and cause a heat release as a consequence of friction. Then, the released heat is captured via an IR camera [9]. | X/✓ [9] | >400 [41] |
| Laser thermography [9] | The sample is heated up using a laser. The energy interacts with the defects. Assessing the heat distribution surrounding the laser spot on the surface of the material allows the defects to be identified [9]. | ✓/✓ [9] | >400 [41] |
| Voltage and current evaluation | During WAAM and fusion welding processes, voltage and current are captured in real time and/then analysed by means of statistical analysis tools or machine/deep learning techniques to detect defects [42]. | ✓/X | No information available |
| Optical emission spectroscopy [17] | The electronic temperature profile is determined during the process by means of assessing the generated light during welding process. This electronic temperature profile is then correlated with existing flaws in the component [17]. | ✓/X [17] | No information available |

### Table 2 (p. 7) — The most relevant propagation modes of ultrasonic waves in solids [49–51]

| Propagation Mode | Description |
|---|---|
| Longitudinal (compression) | The particle motion is parallel to the wave travel direction. |
| Transverse (shear) | The particle vibration is perpendicular to the wave travel direction. |
| Surface (Rayleigh) | The wave is generated at the surface of thick solids caused by an elliptical motion of particles. |
| Plate (Lamb including ZGV modes) | A complex particle motion happens throughout the thickness and parallel to the surface of the material. |

---

## Key numerical values and experimental conditions

### Detection limits (smallest detected defect, from Table 1)

| Technique | Limit | Source ref. |
|---|---|---|
| X-ray backscatter | >20 µm | [9] |
| Micro-CT | >10 µm | [40] |
| Digital radiography | >45 µm | [35] |
| Microfocus RTR with image processing | >50 µm | [11] |
| Laser ultrasonic testing | >100 µm | [34] |
| Real-time radiography (conventional; and with image processing) | >250 µm | [11] |
| Eddy currents | >350 µm | [22] |
| Infrared / eddy current / vibro- / laser thermography | >400 µm | [41] |
| Conventional UT, immersion UT, EMAT | >500 µm | [32] |
| Phased array ultrasonic testing | >600 µm | [24] |
| Computed tomography (standard) | >600 µm | [39] |
| Liquid penetrant testing | >750 µm | [26] |
| Magnetic particle testing | >1000 µm | [27] |

### Wave and sensor parameters

- Ultrasonic waves: frequencies **>20 kHz** (above human hearing).
- Laser ultrasonics: bandwidth **1 MHz to 100 MHz or even more**; standoff distance **more than 1 m**; operable at **any temperature**; no couplant; detects defects **larger than 100 µm and up to 700 µm deep**.
- Acoustic emission: typical frequency range **150 to 300 kHz**.
- Optical (membrane-free) microphone: variable frequency **10 kHz up to 2 MHz**.
- Pulsed thermography: thermal pulse(s) generated **within 2–10 ms**.
- LIBS: Q-switched Nd:YAG, pulse duration **5–100 ns**.
- LOUD: Nd:YAG laser at **532 nm**.

### Reported experiments — defects, materials and settings

| Study / ref. | Material & process | Conditions | Result |
|---|---|---|---|
| Bento et al. [22] | AA 6082-T6, WAAM, eddy current probe | during manufacturing; more coil turns → better detection | defects at depth **up to 5 mm**, **minimum thickness 0.350 mm** identified |
| Lopez et al. [23] | AA2319 WAAM, rough surface, PAUT | numerical simulation for parameter/transducer selection | defects **2–5 mm** |
| Chabot et al. [24] | Aluminium WAAM, PAUT | — | defects **0.6–1 mm** |
| Javadi et al. [12] | WAAM 20-layer wall, PAUT + TFM | tungsten carbide spheres, various diameters | most defects detected |
| Lukacs et al. [25] | Ti-6Al-4V, plasma arc WAAM, LIPA + FMC + TFM | full matrix capture takes **≈14 min** | defects **up to 10 mm depth**, offline only |
| Wang et al. [21] | Molybdenum WAAM, 3D CT | — | small spherical pores, inverted pear-shaped pores, cavities |
| Levesque et al. [59] | INCONEL718, Ti-6Al-4V (laser powder, laser wire, e-beam wire DED), LU + SAFT | measured from bottom side of coupon | porosity of **≈0.4 mm**, lack of fusion identified |
| Levesque et al. [60] | Thick butt welds, LU + SAFT with profile-camera geometry correction | machined surface | EDM slits **2–3 mm** resolved at **50 mm depth** |
| Klein et al. [61] | Titanium and steel, machined surfaces, SAW/LU + wavelet analysis | flat-bottom drilled holes | **1 mm diameter, 0.4 mm deep** clearly detected |
| Dixon et al. [62] | Laser SAW excitation + EMAT detection | artificial defects and real porosity | defects found; size/location characterization not possible — pre-screening only |
| Zeng et al. [63] | WAAM, no surface treatment, LU | crack **0.2 mm wide × 2 mm deep**; flat-bottom hole **⌀2 mm × 1 mm deep**; through hole **⌀2 mm × 2.5 mm deep** | all three identified |
| Fang et al. [64] | A 316 L stainless steel AM part, LU transmission mode | generator one side, detector other side; cross-correlation time delay | subsurface defects **as small as 1 mm diameter** |
| Guo et al. [65] | AW 2024 aluminium plate, LU + CNN + wavelet transform | wavelet images as CNN training data | very high detection accuracy for subsurface defect width |
| Nomura et al. [15] | Mild steel, GMAW, LU real-time | pulsed laser **9 ns pulse width**, **100 Hz**, **50 mm behind torch**, **4.5 mm behind melt pool**, ablation mode, SAFT | lack of penetration and solidification crack detected in real time; depth error **≈5%** |
| Karabutov et al. [69] | Titanium and nickel alloys, LU | — | subsurface stress distribution detected |
| Grad et al. [86] | GMAW, microphone + piezoelectric sensor | shielding gas type matters; **wire extension length >12 mm** | short circuiting and arc reignition are main AE sources |
| Zhang et al. [98] | Al alloy WAAM, OES | — | spectral intensity, electron density and layer width linearly related; steady state after **5 to 7 deposited layers** |
| Nassar et al. [100] | Ti-6Al-4V DED, OES + DAQ + control | — | correlation between **Ti I** and **V I** emissions and predefined defects |
| Ma et al. [28] | A6061 aluminium alloy WAAM, LOUD | in-process, simultaneous | residual stresses, elemental information and defects determined |
| Ma et al. [29] | Aluminium alloy WAAM, LOUD | validated against EBSD | grain size and elemental distribution measured simultaneously |
| Mireles et al. [39] | Powder bed fusion, IR thermography in situ | IR camera **640 × 480**, pixel length **260 µm** | defects **smaller than 600 µm not detected** |
| Runnemalm et al. [120] | Welded components; flash lamp / eddy current / continuous laser thermography | flash lamp at **120 mm**, **6 kJ within 0.05 s**; **FLIR SC5650**, spectral range **2.5–5.1 µm**, **27 mm lens**; induction coil at **>10 mm** | notch **760 µm long × 400 µm wide** detected; five holes **⌀1.0–2.5 mm** all recognized; all eight artificial defects detected with laser |
| Roemer et al. [112] | Aluminium bar, black-painted, laser thermography vs. vibrothermography | laser **100 W**, pulse **100 ms**, **5 K** rise, IR camera **256 × 320** at **60 Hz**; ultrasonic transducer **35 kHz**, **500 W**, pulse **500 ms**, IR camera at **150 Hz** | fatigue cracks identified easily in both |
| Sreedhar et al. [121] | AA 2219 TIG-welded tank, passive thermography | IR camera on welding arm at **60°**, **150 mm behind arc**, field **100 mm** | cluster pore **0.6 mm × 0.4 mm** detected |
| Elkihel et al. [122] | Weld joint, active thermography | inductive heating to **80 °C**; **FLIR T440**, **320 × 240**, bandwidth **7.5–13 µm** | heat loss on weld zone more significant than on defective region |
| Massaro et al. [123] | AISI 304/316 welded steel tank, IR thermography + image processing | heat gun excitation; **FLIR T 1020**, **1024 × 768 px**; line calculus, 2D K-Means, 2D morphology, LSTM ANN | real-time identification and classification of weld defects |
| Cerniglia et al. [125] | Two AM Inconel 600 specimens with micro-sized defects at different depths | laser ultrasonic vs. laser thermography | both able to inspect in-line; microbolometric IR cameras recommended; high-power laser needed for low-emissivity surfaces |
| Kumar et al. [129] | Two inverter + two generator power sources, two electrodes | DSO sample rate **40 kHz** | commercial DSO adequate for in-situ/online assessment |
| Kumar et al. [126] | SMAW | FFT low-pass filtering; **100 kHz** sample rate | FFT LPF gives highest SNR; 100 kHz sufficient |
| Mazlan et al. [131] | GMAW | DSO current as input to Short Time Energy (STE) in MATLAB/Simulink | smooth vs. disturbance current distinguished → defective vs. non-defective weld |

### Materials appearing in the review

AA 6082-T6, AA2319, AA2219, A6061, AW 2024 (aluminium alloys); Ti-6Al-4V; INCONEL 718 / Alloy 718; Inconel 600; A 316 L and AISI 304/316 stainless steels; 316L stainless steel; molybdenum; mild steel; carbon steel; titanium and nickel alloys.

---

## Conclusions (as stated by the authors)

This paper provides a comprehensive review of various NDT techniques, including laser-ultrasonic, acoustic emission with an airborne optical microphone, optical emission spectroscopy, laser-induced breakdown spectroscopy, laser opto-ultrasonic dual detection, thermography and also in-process defect detection via monitoring the process parameters in WAAM and fusion welding. In addition, novel research results, operating principles and the equipment required to perform these techniques have been presented. The minimum detectable welding defect size of most current NDT techniques was collected via previous research or experience of companies. According to this review paper, the following conclusions can be drawn:

- **LU** is a fast technique and capable of detecting internal defects as small as **100 µm** in WAAM and fusion welding. It requires no contact with the sample and can be implemented in harsh environments and also for automation processes. However, LU vaporizes a small amount of the component under inspection.
- **Acoustic emission** is able to measure the soundwaves ranges from **150 up to 300 kHz** during the manufacturing process. It is cost-effective and can be used for defect detection during WAAM and fusion welding. Since it is a passive technology, it cannot be used for offline monitoring. In addition, there is lack of knowledge on applying a membrane-free optical microphone for defect detection in WAAM and fusion welding.
- **Laser-induced breakdown spectroscopy** is capable of acquiring elemental information of the sample and detecting defects such as porosity by means of assessing the chemical elements of the sample. Detecting other types of the defects in WAAM and fusion welding has not been investigated yet.
- **Laser opto-ultrasonic dual detection** can rapidly detect defects and elemental information at the same time during the manufacturing process without having contact with the sample.
- **OES** is a contactless technique and able to detect defects in situ. However, it is not appropriate for offline monitoring.
- **Thermography** is able to detect surface and subsurface defects and recognize flaws as small as **600 µm** in WAAM and fusion welding. It requires no contact with the sample and can measure the thermophysical properties of the part online. It can be used as a signal for real-time closed-loop control systems; however, a heated sample and a proper machine learning algorithm for evaluation are required.
- **Monitoring process parameters**, such as voltage and current using DSOs or data acquisition systems, enables real-time defect detection. These signals are fast and sensitive and suitable for real-time closed-loop control systems.

As each method possesses its own merits and demerits, a **combination of different NDT methods** is required to monitor the WAAM and fusion welding processes in real time and to ensure production of high quality and defect-free final parts. **Future work should focus on the combination of the most suited NDT techniques at the laboratory scale to detect defects in real time during WAAM of light metal alloys.**
