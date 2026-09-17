# Methods of Electrophysical Diagnostics and Monitoring of Reactor Equipment

> **Source:** `Методы электрофизической диагностики и контроля реакторного оборудования.pdf` · 11 pp. · Global Nuclear Safety (Глобальная ядерная безопасность), 2016, No. 4(21), pp. 50–60 · V. I. Surin, Z. S. Volkova, R. A. Denisov, V. D. Motovilin, N. V. Rein (NRNU MEPhI)
> **Original language:** RU · **ID:** УДК 621.039.53: 620.179.118 (075)
> **Original title:** «Методы электрофизической диагностики и контроля реакторного оборудования»

## Bibliographic data

| Field | Value |
|---|---|
| Title (RU) | МЕТОДЫ ЭЛЕКТРОФИЗИЧЕСКОЙ ДИАГНОСТИКИ И КОНТРОЛЯ РЕАКТОРНОГО ОБОРУДОВАНИЯ |
| Title (EN, as printed in the journal's own English block) | The Electrophysical Diagnosis Methods and Reactor Equipment Control |
| Authors | V. I. Surin, Z. S. Volkova, R. A. Denisov, V. D. Motovilin, N. V. Rein (Рейн; transliterated "Rhine" in the journal's English block) |
| Affiliation | National Research Nuclear University «MEPhI», Kashirskoye Shosse 31, Moscow, Russia 115409 |
| Corresponding e-mails | VISurin@mephi.ru (Surin); volkovazs@rambler.ru (Volkova) |
| Journal | Глобальная ядерная безопасность / Global Nuclear Safety, 2016, No. 4(21), pp. 50–60 |
| Journal rubric | ЭКСПЛУАТАЦИЯ ОБЪЕКТОВ АТОМНОЙ ОТРАСЛИ (Operation of nuclear-industry facilities) |
| UDC | 621.039.53: 620.179.118 (075) |
| Received by the editors | 10.12.2016 |
| Copyright | © 2016 the authors; © National Research Nuclear University «MEPhI», 2016 |
| Laboratory referenced | ElphysLAB, NRNU MEPhI (electronic-library archive of diagnostic data) |

## Abstract

Diagnostics of reactor equipment that has been in service for a long time shows that the formation of dangerous macroscopic defects — such as circumferential or longitudinal cracks — proceeds in stages. The distribution of cracks by size or by depth of occurrence in load-bearing structural elements (brackets, frames, bases, supports and others) is determined by non-destructive testing (NDT) methods such as X-ray, ultrasonic and eddy current, which allow volumetric cracks to be reliably diagnosed with sizes from a few tenths of a millimetre at depths of occurrence of a few millimetres. At present the task of revealing corrosion cracks at an early stage of formation and of determining the causes of their appearance is a topical one. For example, in VVER-1000 type reactors corrosion cracking occurs in the assembly where the coolant collector (header) is welded to the steam-generator vessel (welded-joint zone No. 111). As is known, the cause of cracking is deposits of iron and copper compounds in the form of sludge, which accumulates over time in the pockets of the welding assembly.

The aim of the work is to demonstrate the achievements of electrophysical diagnostics and non-destructive testing and the prospects for applying the developed method under the operating conditions of reactor equipment.

*(The journal's own English-language abstract additionally states: "The theoretical aspects of the method of scanning contact potentiometry underlying functional electrophysical diagnostics are discussed, and a summary of the mathematical model to build the profile of the surface diagnosed is given. Using portable electrophysical complex functional diagnostics will allow us to carry out non-destructive testing on the process equipment of nuclear power plants. A software package included in the settlement and software module … provides processing of incoming information, creates the database and makes the necessary calculations, contains test and diagnostic programs, as well as visualization of the results.")*

## Keywords

Electrophysical diagnostics; non-destructive testing; scanning contact potentiometry; mathematical model for constructing the surface profile (in the English keyword block: "a mathematical model for the construction of the surface profile according to the electric potential difference function"); NPP (АЭС).

## 1. Introduction (unnumbered lead section)

Applying the above-listed NDT methods to operating reactor equipment is a difficult task. In particular, the difficulties of inspecting a weld by the ultrasonic method arise because the cracks that form are characterised by a high degree of branching and large extent, and also have very small opening — about **5–10 µm** [1].

Electrophysical non-destructive testing makes it possible to obtain information on the initial stages of crack nucleation and growth **under working conditions**. The authors have obtained results on the radiation resistance of nuclear fuel at an early stage of irradiation, where brittle fracture of the specimens occurred during low-cycle fatigue testing [2, 3].

One of the main advantages of electrophysical monitoring is that the sensors, which have small linear dimensions (**of the order of a few millimetres**), can be placed in practically any hard-to-reach location. They can also be placed directly on those sections of process equipment that have to be monitored or, for example, where a crack is expected to appear with high probability. The method of **scanning contact potentiometry (SCP)** lies at the basis of electrophysical diagnostics and monitoring [4–7]. Sensors may be installed uniformly over the surface with a prescribed linear density, or in an arbitrary manner, in numbers **from several units to several tens**. The high reliability of the measuring system allows continuous monitoring of a selected region of the object under inspection, including on the welds of butt joints, on equipment located in working rooms with elevated radiation background and in other special cases.

Instruments for electrophysical diagnostics and monitoring can find wide application at nuclear power stations. As implementation experience shows, high interest in them is also displayed in other branches of industry.

## 2. Fundamentals of scanning contact potentiometry

The electrical properties of the contact that is formed depend on the quality of machining and the cleanliness of the surfaces, on features of the electronic structure of the metals and on a number of other factors; this makes it possible to use the electrical contact as a **sensing element that converts an external action into electrical signals**.

The interaction of the electrophysical transducer with the surface is described by statistical laws. As is known, depending on the roughness of the surfaces and on the applied load, the size of the spots of real contact is **from 0.1 to 10–40 µm**. On these spots pressures arise that reach **10–20 % of the theoretical strength of the material**. As the load increases, the growth of the real contact area occurs mainly through an increase in the **number** of spots, with only an insignificant increase in their size. When the scanning contact potentiometry method is used, one of the principal questions is the question of the state of the contact surface.

The real contact area amounts to **from 10⁻⁴ to 10⁻¹ of the nominal contact area $S_0$**, and even at large loads it does not exceed **40 %**. For a pair of metals of different hardness, the actual contact area is determined by the properties of the softer metal and by the surface geometry of the harder one [8, 9].

The modern theory of the mechanics of solid-body contacts is valid provided the inequality $S \ll S_0$ holds, where $S$ is the area of the real contact surface. A large number of works on solid-body contact mechanics rest on the approximation of a "rough" surface with a random distribution of asperities in the form of spherical or elliptical protrusions, for which the Hertz contact theory is valid. In some cases the elastic contact interaction of the asperities in the contact zone can be neglected, if the mean distance between neighbouring contacting regions of the surfaces is sufficiently large.

In the measurement procedures developed by the authors, a **small value of the normal force** (the force pressing the transducer against the surface) is adopted, at which the real contact area is much smaller than the nominal contact area.

The real contact surface area $S$ can increase both with increasing pressing force $F$ and through the appearance of **elastic and plastic deformation waves** arising on the surface of the deformed metal. Deformation waves, acting on the sensing element of the transducer, cause a change in its readings.

Plastic deformation of materials is localised in the surface layers of the deformed article in the form of separate sites with differing degrees of manifestation. The initial stages are characterised by single slip lines, which develop into a dense set of parallel lines (slip packets). As deformation increases, slip bands form on the surface, characteristic of the bulk microstructure, together with surface deformation waves; taken as a whole this manifests itself as the **deformation activity of the material surface**. This leads to a change in surface properties: mechanical, optical and electrical. Deformation activity of the surface is connected with the flow process in the near-surface layers, even if the applied stress is significantly below the yield strength, owing to the presence on the surface of stress concentrators of technological origin [10]. Several mathematical models have been developed by the authors for studying the deformation activity of the surface.

### 2.1 Contact model of a rough surface (Hertz / Greenwood–Williamson)

Consider the interaction of a rough surface with a plane. Let the asperities formed on the surface be represented as a set of spheres of radius $R$. Assume that the asperity-height function obeys the normal distribution law. Assume also that the elastic interaction of the asperities in the contact region can be neglected. On the basis of the Hertz contact theory the following characteristics have been obtained [11, 12]:

— normalised contact area:

$$\frac{\Delta S}{S_0} = \pi n_0 R \int_{d_z}^{\infty} (h - d_z)\, p(h)\, dh \tag{1}$$

— number of contacting asperities per unit nominal area:

$$\frac{N}{S_0} = n_0 \int_{d_z}^{\infty} p(h)\, dh \tag{2}$$

— magnitude of the pressing (clamping) stress:

$$\sigma_{cl} = \frac{F}{S_0} = \frac{4E}{3\left(1-\nu^{2}\right)}\, n_0 \int_{d_z}^{\infty} (h - d_z)^{\frac{3}{2}} R^{\frac{1}{2}}\, p(h)\, dh \tag{3}$$

where $d_p = (h - d_z)$;

- $n_0$ — number of asperities per unit area, m⁻² (dimensionless per unit nominal area as used in (1)–(3));
- $h$ — height of the asperities, m (µm in practice);
- $d_z$ — magnitude of the gap between the interacting surfaces, m;
- $p(h)$ — probability density of the distribution of asperities on the surface, m⁻¹;
- $E$ — Young's modulus, Pa;
- $\nu$ — Poisson's ratio, dimensionless;
- $\Delta S$ — increment of real contact area, m²; $S_0$ — nominal contact area, m²;
- $N$ — number of contacting asperities, dimensionless;
- $F$ — pressing force, N; $\sigma_{cl}$ — clamping stress, Pa;
- $R$ — radius of the spheres representing the asperities, m.

In the one-dimensional case the amplitudes of the wave vectors of waviness and roughness vary within a narrow range of values near $q_m$, and the "lattice constant" is $\lambda_m = 2\pi/q_m$. In this case the Greenwood–Williamson theory gives the estimate of $n_0$ [12]:

$$n_0 \approx 0.029\, q_m^{2} \tag{4}$$

and of the radius of the asperity spheres:

$$R \approx \frac{1}{\sqrt{2}\, q_m^{2}\, \sigma} \tag{5}$$

where

- $q_m$ — characteristic wave-vector amplitude of the surface waviness/roughness, m⁻¹;
- $\lambda_m = 2\pi/q_m$ — corresponding "lattice constant" (characteristic surface wavelength), m;
- $\sigma$ — root-mean-square deviation of the roughness parameter, m (in (5); note that in equation (7) below the same symbol $\sigma$ denotes applied mechanical stress);
- $n_0$ — number of asperities per unit area, m⁻²;
- $R$ — radius of the asperity spheres, m.

### 2.2 Link between the diagnostic signal and surface roughness

For issuing diagnoses when diagnosing developing surface defects, and also nucleating near-surface cracks, the authors have developed dedicated software.

It is evident that the roughness distribution on the contact-spot area $h_i$ at each particular instant of time $t_i$ is different, since deformation processes run continuously in the material under load.

To determine the roughness with the help of the diagnostic signal, the empirical relation obtained by the authors is used, connecting the integral values of the diagnostic signal $\Delta\varphi_i$ (over the contact-spot area) and $h_i$ [13]:

$$\Delta\varphi_i = \frac{e\, h_i}{\varepsilon_r \varepsilon_0} \int_{0}^{L} \delta n(z)\, dz \tag{6}$$

where

- $e$ — electron charge, C (1.602 × 10⁻¹⁹ C);
- $\varepsilon_0$ — electric constant (vacuum permittivity), F/m;
- $\varepsilon_r$ — relative permittivity of the medium, dimensionless;
- $L$ — limit of integration, usually of the order of **~10⁻⁹ m** [14];
- $h_i$ — roughness on the contact spot at instant $t_i$, m;
- $\delta n(z)$ — the change of electron density as a function of the coordinate $z$ (the $z$ axis is perpendicular to the contact surface), m⁻³ per unit;
- $\Delta\varphi_i$ — integral value of the diagnostic signal (electric potential difference) over the contact spot, V.

Under the integral in (6) stands the function of the change of electron density $\delta n(z)$ with the coordinate, the $z$ axis being perpendicular to the contact surface. The function $\delta n(z)$ characterises the change of electron density (in the general case, of charge carriers) **in the gap**, which is the space between the interacting surfaces. To determine the number of contact spots, experimental methods and computational estimates are used.

According to (6), at any instant of time one can determine the value of roughness corresponding to the value of the diagnostic signal, and construct its time dependence for any chosen contact location on the surface under study. The diagnostic signal of the electric potential difference is an **integral value over the number of contact spots that form**. For metals and alloys the electrical contact that arises ensures the passage of electric current through the contact surface. In doing so, interacting surfaces are formed which are **effective barriers for conduction electrons**. Between the atoms of these surfaces forces arise that lead to correlated changes of their electron shells, and that depend on the magnitude of the gap between the surfaces. To obtain the dependence between the electrical characteristics and the roughness, it is necessary to solve the problem of electrons crossing the boundary at a high structural level [14].

Elastic and plastic deformation waves change the surface relief (dynamic waviness and roughness), which affects the **electrical double layer**, the local electron density and the distribution of electric potential on the surface. Because of the low energy of the mechanical waves that arise, the useful signal has a small amplitude and is screened by the noise component. In order to reduce the influence of this component, signal-processing programs are used (Figure 1). In a number of cases double filtering of the signal is applied, but part of the useful information may then be lost as well. Figure 1 shows the influence of the stages of successive loading of the specimen on the character of the change of the **diagnostic signal amplitude (DSA)**.

A **differential** electric potential difference arises in a closed electrical circuit containing two or more electrophysical transducers. When the SCP method is used, it becomes possible to investigate local surface phenomena and changes of the morphology of the surface layer by mechanically scanning the entire surface under study.

The informative parameters of the diagnostic signal are: amplitude, duration, the time of appearance of individual harmonics, the conditional power of the electrical signal and some other parameters. Electrical signals are characterised by spectral density, by amplitude, time and amplitude–time distributions, and also by mean value and variance. The stated parameters are connected with the physical processes that generate them and contain information about those processes or about the state of the object under inspection.

## 3. Determination of the waviness and roughness of the fuel kernel surface under irradiation

Consider the problem of determining the surface roughness and of estimating the local (point) deformation of the fuel kernel by an experimental–computational method. The estimate was performed in order to obtain the **critical value of the gap between the fuel and the cladding** under conditions of swelling and radiation creep. For this purpose the results of in-pile (in-reactor) tests of **carbonitride nuclear fuel on the IRT MEPhI reactor** [15, 16] were used. In those works the possibilities of applying the SCP method under in-pile conditions were demonstrated for the first time.

The measurement procedure and the requirements for choosing the electrophysical transducers depend on the test conditions and are described in detail in [17].

Modelling of the fuel-kernel surface was carried out on the basis of the results obtained on **radiation thermal–force treatment of uranium nitrides and carbonitrides**. The relative deformation of the kernel as a result of the thermal–force cycles had a high value (**up to 0.3 and more**), comparable with the value of the deformation at which fuel–cladding contact occurs.

The main problem of surface modelling using electrophysical diagnostics is that the roughness distribution function, at a chosen instant of time, depends on the **spatial coordinates**, whereas the function of the change of the diagnostic signal depends on **time**. The linking of the time function with the function of the spatial coordinates was performed on the basis of the approach developed by the authors. Expansion of the diagnostic signal into a **Fourier series** was carried out in order to determine the frequencies of the harmonics appearing at different stages of the experiment. If one assumes that the number of contact spots is preserved during the experiment, then the area of the contacts must change — growing or decreasing. It is possible that during the experiment some contact spots disappear, but because of the dynamics of the process new ones are formed. The **number of harmonics** obtained when the diagnostic signal was expanded into a Fourier series **correlated with the number of interacting asperities and valleys** on the contact-spot areas, which change dynamically in time.

In accordance with the measurement procedure, one of the contact areas was chosen to be **as far as possible from the site of deformation localisation**. In that case the contact potential difference (CPD) arising between the specimen and the transducer at that area changed only weakly with time, since the number of interacting asperities on it remained approximately constant with time.

In another contact region, where the process of deformation formation is active, the number of contact spots changed intensively with time. If only the contact spots of large area are taken into account (with linear dimensions **from tenths of a millimetre and larger**), then their number can be determined on the basis of the Greenwood–Williamson theory, and the time-varying roughness — from the diagnostic signal using expression (6).

### 3.1 Computational stages of the surface-profile reconstruction

The task consisted in constructing the roughness (waviness) distribution over the surface of the contact spot from the values of the diagnostic parameter, and was divided into several computational stages:

1. Construction of the roughness distribution on the specimen surface **before** testing (performed on the basis of profilometry results) and determination of the initial roughness value $h_0$;
2. Statistical processing of the diagnostic signals (determination of the mean, root-mean-square deviation, variance and others) and construction of the **amplitude distribution histogram**;
3. Calculation of the roughness parameters from the values of the diagnostic signal;
4. Modelling of the surface roughness by means of mathematical functions in such a way that the roughness value obtained from the model corresponds to the value calculated from the diagnostic signal.

Figure 2 presents the results obtained for the change of the fuel-kernel surface roughness under irradiation.

### 3.2 Calculated deformation

The calculated value of the deformation $\varepsilon_{calc}$ was determined by integrating the square of the diagnostic-signal function over a given time interval:

$$\varepsilon_{\text{calc}} = A \int_{t_1}^{t_2} \left(\Delta\varphi\right)^{2} dt, \qquad A = \frac{1}{\sigma \cdot V \cdot \rho} \tag{7}$$

where

- $\sigma$ — applied mechanical stress, Pa;
- $V$ — volume of the specimen, m³;
- $\rho$ — fitting function having the dimension of ohms, Ω;
- $\Delta\varphi$ — diagnostic signal (electric potential difference), V;
- $t_1, t_2$ — limits of the time interval of integration, s (hours in the experiment);
- $A$ — normalising coefficient, (Pa·m³·Ω)⁻¹;
- $\varepsilon_{\text{calc}}$ — calculated deformation, arbitrary units (plotted as such in Figure 3).

## 4. Results of electrophysical inspection of welded joints

For the quantitative assessment of the technical condition of articles — an **electrically welded, longitudinally seam-welded round pipe to GOST 10704-91, ⌀219 mm, wall thickness 6 mm, steel 20 (сталь 20)** — of the compressed-air pipeline of the engineering building of the Moscow Printing Factory, a branch of JSC Goznak, the SCP method was applied. During the work a **mobile information-and-measurement system (IMS)** was used, based on an **Asus X554L** laptop and the **certified instrument EDSS-1 (ЭДСС-1)** (Figure 4).

The software complex forming part of the computational-and-program module of the IMS makes it possible to process incoming information promptly, to build a database and to perform the necessary calculations in the **MathCAD** environment, and also contains test and diagnostic programs, programs for calculation and for visualisation of the obtained results.

Electrophysical inspection of the compressed-air pipeline was carried out during commissioning work with the aim of determining the quality of the welds and of revealing possible violations and defects. **Stationary electrophysical NDT sensors** were also used during the tests (Figure 5).

The pipe for supplying compressed air was welded from **six parts**, had **two bends** and **five welds**. All welds were made by **electric-arc welding**.

### 4.1 Transducers used

In the work, stationary sensors with **conical transducers** were used (cone angle close to **90 degrees**), having a **tip rounding radius of 0.3 mm**. The surface roughness ($R_a$) of the sensing element, measured with a **digital portable profilometer made by Vogel**, is given in Table 1. The **surface roughness determines the sensitivity threshold**. The transducers were manufactured from the alloys **D16T (Д16Т, GOST 21488-97)**, **Kh18N10T (Х18Н10Т, GOST 14955-77)**, **brass LS 59-1 (ЛС 59-1, GOST 15527-2004)** and **copper M1 (М1, GOST 859-2001)**.

### 4.2 Diagnostic results and interpretation

The results of diagnosing the compressed-air pipeline for three welds are presented in Table 2, which lists the obtained mean values of the diagnostic signal for each sample of measurements performed. The characteristics of the weld object are "**weld overlap / bead build-up**" (наплыв), "**contaminated area**" (загрязнённый участок) and "**cleaned area**" (очищенный участок).

Analysis of the results shows that for the weld overlap the electric potential difference grows noticeably **from the first weld to the fourth**, and then falls at the **fifth** weld. This is connected with the higher ambient temperature for the third and especially the fourth welds, which are located in the upper part of the room. The readings increase as a result of the appearance of an **additional thermo-EMF**. (Table 2 as printed tabulates welds 1, 2 and 3.)

On the basis of the criteria developed, a diagnosis was issued from the results of electrophysical diagnostics; in doing so, available data from the archive of the electronic library of the **ElphysLAB laboratory of NRNU MEPhI** were used. **Regulating threshold values of the diagnostic signal** and the corresponding indicators of the electric potential difference were determined for presenting the conclusion on the work performed.

The readings obtained in the work lie **within the permissible limits characteristic of steels of this class**. During diagnosis, **no critical values of the signal** affecting the conditions of normal operation of the pipeline were obtained.

## Figures

### Figure 1 — Processing of the detected signal (1), obtained under uniaxial tension of commercially pure aluminium, by means of a wavelet filter (the plot is shifted upwards along the ordinate axis by 1.7 units). The noise component of the signal (2) and the useful signal (3) are shifted downwards along the ordinate axis by one unit. In the lower part of the figure the mechanical loading diagram of the specimen (4) is shown (p. 5)

A four-trace time plot. Ordinate: **АДС, мкВ** — diagnostic signal amplitude (DSA) in microvolts, scaled from −3 to +2 with gridlines at every integer. Abscissa: **Время, ч** — time in hours, from 0 to about 4.6, with labelled ticks at 0, 1, 2, 3 and 4.

- **Curve 1 (blue, dense noisy band)** — the raw detected signal, offset upward by 1.7 units. From 0 to about 2.5 h its band is centred near +1.0 µV with excursions between roughly +0.3 and +1.9. At about 2.5–2.6 h the band drops abruptly by roughly one unit and thereafter (2.6–4.6 h) is centred near +0.3 with excursions down to about −0.6, i.e. the raw amplitude both shifts and broadens once the higher load steps are applied.
- **Curve 2 (grey, dense noisy band)** — the extracted noise component, offset downward by one unit; centred near −0.85 to −0.9 with roughly constant band width from 0 to 2.5 h, then visibly broadening (down to about −1.7) over the final, more heavily loaded part of the record.
- **Curve 3 (red, smooth line)** — the useful (filtered) signal, offset downward by one unit. It starts at about −2.05 at t = 0, rises to a local plateau near −1.7 during the unloaded stage, shows a sharp local maximum of about −1.55 at t ≈ 1.9 h, then falls in a step to about −2.1 at t ≈ 2.0 h, oscillates around −2.0 to −2.1 between 2.0 and 2.5 h, steps down again to about −2.35 at t ≈ 2.5 h, drifts slowly downwards to about −2.6 by t ≈ 4.4 h, and finally rises sharply to about −2.15 at the very end of the record (the unloading / fracture event).
- **Curve 4 (violet staircase)** — the mechanical loading diagram of the specimen, plotted in the lower part of the field and annotated with the stress level of each step: **0 MPa** from 0 to ≈1.45 h, **5 MPa** from ≈1.45 to ≈2.4 h, **9 MPa** from ≈2.4 to ≈3.4 h, **15 MPa** from ≈3.4 to ≈4.5 h, followed by a vertical drop back to the baseline at ≈4.5 h.

The key visual message is the correspondence between the steps of the loading staircase (curve 4) and the step changes in both the raw signal band (curve 1) and the filtered useful signal (curve 3).

### Figure 2 — Modelling of the waviness and roughness of the uranium carbonitride surface at different stages of the experiment: a — initial roughness before irradiation (Ra = 5–10 µm); the surface is constructed from the background value of the diagnostic signal; b — increase of the waviness parameter as a result of radiation thermal–force treatment; c — formation of the ring-shaped contour of contact between the transducer and the specimen surface (p. 6)

Three square greyscale shaded-relief renderings of the modelled surface, arranged with panel *a* at the upper left, panel *b* at the upper right and panel *c* at the lower right (the lower-left quadrant is empty). Each panel is a synthetic height map rendered with oblique illumination, so that grey level encodes local slope/height of the modelled relief.

- **Panel a** — a nearly smooth field with very fine, low-contrast granular texture, a diffuse bright spot slightly above the centre and a gradual darkening towards the upper-right corner. This corresponds to the initial state before irradiation, with $R_a = 5$–$10$ µm, built from the background level of the diagnostic signal.
- **Panel b** — the same field but with markedly stronger and coarser relief: elongated ridge-and-valley structures with clearly higher contrast run across the whole field, while the bright region near the upper centre is retained. This corresponds to the growth of the **waviness** parameter after radiation thermal–force treatment.
- **Panel c** — a dense, high-contrast, strongly grainy relief occupying the full panel, in which a ring-shaped (annular) contour is discernible. This corresponds to the formation of the ring contour of contact between the transducer and the specimen surface.

The figure shows the progression from an almost flat initial surface, through the development of long-wavelength waviness, to a fully developed short-wavelength rough relief bearing the imprint of the annular transducer contact.

### Figure 3 — Change of the deformation of uranium carbonitride during in-pile tests: curve (1) — experiment ($\varepsilon_{exp}$, in µm); curve (2) — calculation ($\varepsilon_{calc}$, in arbitrary units) [13] (p. 7)

A two-curve time plot on a light-grey field with a rectangular grid. Ordinate: dual label **ε_эксп, мкм** (experimental deformation, µm — curve 1) and **ε_расч, усл. ед.** (calculated deformation, arbitrary units — curve 2), with the origin marked **0** at the bottom and a single labelled gridline at **2·10³**; the horizontal gridlines are equally spaced, so they correspond to steps of 1·10³. Abscissa: **Время, ч** — time in hours, with labelled ticks at 0, 24 and 48 and the record running to roughly 60 h.

- **Curve 1 (bright magenta/pink)** — the experimental deformation. It remains essentially flat at the baseline (close to 0) from 0 to about 28 h, with only small jitter near 26–28 h; at about 28 h it steps up to a level of roughly 0.4·10³ µm and stays on that plateau until about 38 h; at about 38 h it rises almost vertically to a level of roughly 4·10³ µm, where it stays approximately constant to the end of the record, with a slight decrease and levelling after about 48 h.
- **Curve 2 (dark maroon)** — the calculated deformation obtained from equation (7). It rises smoothly and monotonically from near zero at t = 0, with an accelerating slope up to about 8–10 h, then an almost linear rise reaching roughly 1·10³ arbitrary units at 24 h; between about 30 and 36 h it rises more steeply, then flattens into a plateau slightly below 2·10³ from about 38 h to the end of the record, with a very small continuing rise after 48 h.

The two curves reproduce the same sequence of events in time (quiescent stage, intermediate stage, and a sharp transition at about 38 h), but the calculated curve resolves the gradual accumulation of deformation continuously, whereas the experimental curve registers it in discrete steps.

### Figure 4 — Portable complex for functional electrophysical diagnostics with the EDSS-1 instrument (at the bottom in the right part of the photograph) (p. 8)

A colour photograph of the measurement setup assembled on a light wooden bench in front of a wood-panelled wall.

- **Left** — a benchtop precision digital multimeter/nanovoltmeter (Agilent-type, rack-format grey case on a tilt stand), with a vacuum-fluorescent display reading "0.000005 mV DC" and a row of function pushbuttons; measurement leads are plugged into its front input terminals (red/black banana jacks) and run to the right.
- **Centre** — the **Asus X554L** laptop of the mobile information-and-measurement system, open, with the screen showing two stacked blue plotting windows containing the running waveform of the diagnostic signal on a fine rectangular grid (a wavelet-type transient is visible in each window). A cable runs from the multimeter to the laptop; a further white USB-type cable leaves the right-hand side of the laptop.
- **Bottom right** — the **EDSS-1 (ЭДСС-1)** instrument: a black moulded hand-held/portable unit resting on a grey metal plate, connected by a cable. A red laser line is visible across the bench surface in front of it.

The photograph documents the complete portable chain: probe/instrument → precision voltmeter → laptop with the computational-and-program module.

### Figure 5 — Installation of stationary electrophysical sensors on the object under inspection (p. 8)

A two-panel figure showing the same sensor arrangement as a rendering and as a photograph.

- **Left panel** — a 3D CAD rendering of a bent steel pipe with a textured (as-rolled) outer surface and a circumferential weld bead running around it. Two cylindrical stationary transducers with flat, disc-shaped bases are mounted on the pipe: one immediately on one side of the weld bead (with a slender pin-shaped body and a small terminal at the top) and one further along the pipe on the other side (a shorter cylindrical body with a terminal at its top). The two terminals are joined by a thin two-wire lead drawn as a loop, forming the closed measuring circuit that spans the weld — i.e. the differential potential difference is taken between the two transducers across the welded joint.
- **Right panel** — a colour photograph of the actual installation on the blue-painted compressed-air pipeline. The circumferential weld bead with its characteristic ripple pattern runs diagonally across the frame. Two metal cylindrical sensors with bright polished flat bases are seated on ground-bright (paint-removed) patches of pipe surface on either side of the bead: the lower-left one carries a black coaxial cable attached to a side connector, the upper-right one has a threaded terminal at the top with a brown lead. Additional fittings are visible at the right edge of the pipe.

Together the panels show the sensor layout used for continuous monitoring of a butt weld: two small-footprint contact transducers straddling the weld, connected into one measuring loop.

## Tables

### Table 1 — Surface roughness of the electrophysical transducers (p. 8)

| Transducer material | Roughness $R_a$, µm |
|---|---|
| D16T (Д16Т) | 0.08 |
| Kh18N10T (Х18Н10Т) | 0.15 |
| LS 59-1 (ЛС 59-1) | 0.23 |
| M1 (М1) | 0.10 |

### Table 2 — Characteristic of the weld object and mean values of the diagnostic signal for the transducers used (p. 9)

*(Units are not stated in the source table; the text describes the entries as the mean values of the diagnostic signal, i.e. of the electric potential difference, for each measurement sample. The dash in the Kh18N10T / contaminated-area cell of weld 2 is as printed.)*

| Transducer material | Weld overlap (наплыв) | Contaminated area (загрязнённый участок) | Cleaned area (очищенный участок) |
|---|---|---|---|
| **Weld 1** | | | |
| D16T (Д16Т) | 2.390·10⁻⁷ | 1.119·10⁻⁴ | 1.586·10⁻⁷ |
| Kh18N10T (Х18Н10Т) | 1.835·10⁻⁶ | 1.827·10⁻⁴ | 3.484·10⁻⁶ |
| LS59-1 (ЛС59-1) | 4.671·10⁻⁷ | 1.527·10⁻⁴ | 6.915·10⁻⁷ |
| M1 (М1) | 2.089·10⁻⁶ | 1.085·10⁻⁴ | 2.253·10⁻⁶ |
| **Weld 2** | | | |
| D16T (Д16Т) | 5.705·10⁻⁶ | 8.852·10⁻⁶ | 2.236·10⁻⁶ |
| Kh18N10T (Х18Н10Т) | 5.337·10⁻⁶ | – | 1.210·10⁻⁵ |
| LS59-1 (ЛС59-1) | 2.872·10⁻⁶ | 8.533·10⁻⁵ | 3.302·10⁻⁶ |
| M1 (М1) | 9.543·10⁻⁶ | 1.146·10⁻⁴ | 8.061·10⁻⁶ |
| **Weld 3** | | | |
| D16T (Д16Т) | 2.416·10⁻⁵ | 2.316·10⁻⁴ | 3.201·10⁻⁵ |
| Kh18N10T (Х18Н10Т) | 3.169·10⁻⁵ | 2.037·10⁻⁵ | 2.963·10⁻⁵ |
| LS59-1 (ЛС59-1) | 4.450·10⁻⁵ | 2.400·10⁻⁴ | 3.005·10⁻⁵ |
| M1 (М1) | 4.984·10⁻⁵ | 9.189·10⁻⁵ | 5.424·10⁻⁵ |

## Key numerical values and experimental conditions

**Defect detection limits and crack geometry**

| Quantity | Value | Context |
|---|---|---|
| Reliable detection limit of conventional NDT (X-ray, ultrasonic, eddy current) | volumetric cracks from a few tenths of a millimetre in size | at depths of occurrence of a few millimetres, in load-bearing structural elements |
| Crack opening of corrosion cracks in welds | about 5–10 µm [1] | reason why ultrasonic inspection of welds is difficult; cracks are also highly branched and of large extent |
| VVER-1000 cracking location | welded-joint zone No. 111 | coolant-collector-to-steam-generator-vessel welding assembly; cause: iron and copper compound deposits (sludge) accumulating in the pockets of the assembly |

**Contact physics**

| Quantity | Value |
|---|---|
| Size of real-contact spots | 0.1 to 10–40 µm (depending on surface roughness and applied load) |
| Pressure on the contact spots | 10–20 % of the theoretical strength of the material |
| Real contact area | 10⁻⁴ to 10⁻¹ of the nominal contact area $S_0$; not exceeding 40 % even at large loads |
| Validity condition of contact mechanics | $S \ll S_0$ |
| Integration limit $L$ in eq. (6) | ~10⁻⁹ m [14] |
| Greenwood–Williamson asperity density | $n_0 \approx 0.029\, q_m^2$ |
| Asperity sphere radius | $R \approx 1/(\sqrt{2}\, q_m^2 \sigma)$ |
| Contact-spot sizes accounted for in the Greenwood–Williamson estimate | from tenths of a millimetre and larger |

**Sensors and instrumentation**

| Quantity | Value |
|---|---|
| Sensor linear dimensions | of the order of a few millimetres |
| Number of sensors deployable on a surface | from several units to several tens (uniform prescribed linear density or arbitrary placement) |
| Transducer geometry | conical, cone angle close to 90°, tip rounding radius 0.3 mm |
| Transducer materials | D16T (GOST 21488-97); Kh18N10T (GOST 14955-77); brass LS 59-1 (GOST 15527-2004); copper M1 (GOST 859-2001) |
| Transducer sensing-element roughness $R_a$ | 0.08 µm (D16T); 0.15 µm (Kh18N10T); 0.23 µm (LS 59-1); 0.10 µm (M1) — measured with a Vogel digital portable profilometer; roughness determines the sensitivity threshold |
| Measuring instrument | certified instrument EDSS-1 (ЭДСС-1) |
| Computer of the mobile IMS | Asus X554L laptop; calculations in MathCAD |

**Fuel-kernel (in-pile) experiment**

| Quantity | Value |
|---|---|
| Fuel | carbonitride nuclear fuel (uranium nitrides and carbonitrides) |
| Reactor | IRT MEPhI research reactor [15, 16] |
| Purpose | obtaining the critical fuel–cladding gap under swelling and radiation creep |
| Relative deformation of the kernel after thermal–force cycles | up to 0.3 and more — comparable with the deformation at which fuel–cladding contact occurs |
| Initial surface roughness of the uranium carbonitride model surface | $R_a$ = 5–10 µm (before irradiation) |
| In-pile test duration (Figure 3) | about 60 h; transitions at ≈28 h and ≈38 h |
| Loading stages in the uniaxial tension test (Figure 1) | 0, 5, 9, 15 MPa; total record ≈4.6 h; signal amplitude scale in µV; raw trace offset +1.7 units, noise and useful traces offset −1 unit |
| Test material in Figure 1 | commercially pure aluminium, uniaxial tension |

**Compressed-air pipeline inspection**

| Quantity | Value |
|---|---|
| Object | compressed-air pipeline of the engineering building of the Moscow Printing Factory, a branch of JSC Goznak |
| Pipe | electrically welded, longitudinally seam-welded round pipe, GOST 10704-91 |
| Outer diameter | ⌀219 mm |
| Wall thickness | 6 mm |
| Steel grade | steel 20 (сталь 20) |
| Pipe construction | welded from six parts, two bends, five welds, all made by electric-arc welding |
| Inspection stage | commissioning (start-up and adjustment) work |
| Weld-object characteristics assessed | weld overlap; contaminated area; cleaned area |
| Result | all readings within the permissible limits characteristic of steels of this class; no critical signal values affecting normal operation |
| Reference data source for criteria | archive of the electronic library of the ElphysLAB laboratory, NRNU MEPhI |

## Conclusions (as stated by the authors)

1. The prospects of using functional electrophysical diagnostics methods in the nuclear industry have been demonstrated, on the examples of (a) the investigation of the radiation resistance of nuclear fuel and (b) the assessment of the technical condition of the compressed-air pipeline of the engineering building of the Moscow Printing Factory — a branch of JSC Goznak.
2. The theoretical aspects of the method of scanning contact potentiometry, which underlies functional electrophysical diagnostics, have been presented, together with the principal provisions of the mathematical model for constructing the profile of the diagnosed surface.
3. The use of the portable functional electrophysical diagnostics complex will make it possible to carry out non-destructive testing promptly on the process equipment of nuclear power stations.
4. A software complex has been developed, forming part of the computational-and-program module of the information-and-measurement system, which provides processing of incoming information, builds a database and performs the necessary calculations, contains test and diagnostic programs as well as programs for visualisation of the obtained results.

## Terminology notes

| Russian term | English term used in this summary |
|---|---|
| контактная разность потенциалов | contact potential difference (CPD) |
| работа выхода (электрона) | (electron) work function |
| сканирующая контактная потенциометрия (СКП) | scanning contact potentiometry (SCP) |
| электрофизическая диагностика | electrophysical diagnostics |
| функциональная электрофизическая диагностика | functional electrophysical diagnostics |
| неразрушающий контроль | non-destructive testing (NDT) |
| дефектоскопия | flaw detection / defectoscopy |
| вихретоковый (метод) | eddy current (method) |
| рентгеновский / ультразвуковой метод | X-ray / ultrasonic method |
| трещина | crack |
| круговая (кольцевая) трещина / продольная трещина | circumferential crack / longitudinal crack |
| коррозионное растрескивание | corrosion cracking |
| раскрытие трещины | crack opening |
| глубина залегания | depth of occurrence |
| несплошность | discontinuity |
| пора | pore |
| непровар | lack of fusion |
| датчик / преобразователь | sensor / transducer |
| стационарный датчик | stationary (permanently mounted) sensor |
| чувствительный элемент | sensing element |
| силовые элементы конструкций | load-bearing structural elements |
| выгородка | baffle |
| кронштейн | bracket |
| каркас | frame |
| основание | base |
| опора | support |
| ресурс | service life |
| старение | ageing |
| радиационное охрупчивание | radiation embrittlement |
| диагностический сигнал | diagnostic signal |
| амплитуда диагностического сигнала (АДС) | diagnostic signal amplitude (DSA) |
| разность электрических потенциалов | electric potential difference |
| дифференциальная разность электрических потенциалов | differential electric potential difference |
| двойной электрический слой | electrical double layer |
| электронная плотность | electron density |
| электроны проводимости | conduction electrons |
| шероховатость | roughness |
| волнистость | waviness |
| неровности / выступы / впадины | asperities / protrusions / valleys |
| пятно (реального) контакта | (real) contact spot |
| номинальная площадь касания | nominal contact area |
| площадь реального (фактического) контакта | real (actual) contact area |
| сила поджатия | pressing (clamping) force |
| прижимающее напряжение | pressing (clamping) stress |
| контактная теория Герца | Hertz contact theory |
| теория Гринвуда–Вильямсона | Greenwood–Williamson theory |
| профилометрия / профилометр | profilometry / profilometer |
| деформационная активность поверхности | deformation activity of the surface |
| линии скольжения / пачки скольжения / полосы скольжения | slip lines / slip packets / slip bands |
| волны упругой и пластической деформации | elastic and plastic deformation waves |
| предел текучести | yield strength |
| концентраторы напряжений | stress concentrators |
| малоцикловые усталостные испытания | low-cycle fatigue testing |
| хрупкое разрушение | brittle fracture |
| топливный сердечник | fuel kernel |
| оболочка (твэла) | (fuel-rod) cladding |
| зазор между топливом и оболочкой | fuel–cladding gap |
| распухание | swelling |
| радиационная ползучесть | radiation creep |
| радиационная температурно-силовая обработка | radiation thermal–force treatment |
| карбонитридное ядерное топливо | carbonitride nuclear fuel |
| внутриреакторные испытания | in-pile (in-reactor) tests |
| реактор ИРТ МИФИ | IRT MEPhI research reactor |
| узел приварки коллектора теплоносителя | coolant-collector welding assembly |
| корпус парогенератора | steam-generator vessel |
| сварное соединение / сварной шов | welded joint / weld (weld seam) |
| стыковое соединение | butt joint |
| электродуговая сварка | electric-arc welding |
| наплыв | weld overlap (bead build-up) |
| загрязнённый участок / очищенный участок | contaminated area / cleaned area |
| шлам | sludge |
| термо-эдс | thermo-EMF (thermoelectric power) |
| информационно-измерительная система (ИИС) | information-and-measurement system (IMS) |
| расчётно-программный модуль | computational-and-program module |
| пуско-наладочные работы | commissioning (start-up and adjustment) work |
| вейвлет-фильтр | wavelet filter |
| шумовая составляющая / полезный сигнал | noise component / useful signal |
| двойная фильтрация сигнала | double filtering of the signal |
| ряд Фурье / гармоники | Fourier series / harmonics |
| спектральная плотность | spectral density |
| среднеквадратическое отклонение / дисперсия | root-mean-square deviation / variance |
| гистограмма распределения амплитуды | amplitude distribution histogram |
| условная мощность электрического сигнала | conditional power of the electrical signal |
| пороговые значения диагностического сигнала | threshold values of the diagnostic signal |
| порог чувствительности | sensitivity threshold |
| объект контроля | object under inspection |
| повышенный радиационный фон | elevated radiation background |
| труба электросварная прямошовная круглая | electrically welded, longitudinally seam-welded round pipe |
| сталь 20 | steel 20 |
| Д16Т / Х18Н10Т / ЛС 59-1 / М1 | D16T / Kh18N10T / LS 59-1 / M1 |
| 12Х18Н10Т / 08Х18Н10Т | 12Kh18N10T / 08Kh18N10T |
