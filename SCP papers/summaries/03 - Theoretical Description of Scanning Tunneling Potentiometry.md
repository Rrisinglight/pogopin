# Theoretical Description of Scanning Tunneling Potentiometry

> **Source:** `Theoretical Description of Scanning Tunneling Potentiometry.pdf` · 14 pp. · arXiv:1007.1512v2 [cond-mat.mes-hall], 22 Mar 2011 · Weigang Wang, Malcolm R. Beasley (Stanford University)
> **Original language:** EN · **ID:** arXiv:1007.1512v2 · **PACS:** 07.79.-v, 72.10.Bg, 73.23.-b, 73.50.-h

## Bibliographic data

- **Title:** Theoretical Description of Scanning Tunneling Potentiometry
- **Authors:** Weigang Wang (王魏刚), Malcolm R. Beasley
- **Affiliation:** Geballe Laboratory for Advanced Materials, Stanford University, Stanford, CA 94305
- **Corresponding author:** weigwang@stanford.edu
- **Preprint:** arXiv:1007.1512v2 [cond-mat.mes-hall], posted 22 Mar 2011 (LaTeX date stamp on the compiled copy: May 29, 2022)
- **PACS:** 07.79.-v (scanning probe microscopes and components), 72.10.Bg (general theory of electronic transport in condensed matter), 73.23.-b (electronic transport in mesoscopic systems), 73.50.-h (electronic transport phenomena in thin films)
- **Sections:** I Introduction; II Scanning Tunneling Potentiometry (A STP setup, B A heuristic interpretation of STP); III General theory in terms of density matrix (A Simple model considered in the problem, B Quantum transport approach, C Total tunneling current, D Explicit expressions for measured potential — Subcase I, Subcase II); IV Local density matrix (A Outline of local density matrix, B Possible further developments); V Limiting cases (A Sample in equilibrium, B Homogeneous sample with no defect, C Landauer resistive dipole, D Chu and Sorbello model, E Atomic resolution in STP — 1 Sample with no defects, 2 Sample with defect(s)); VI Summary and discussion; Acknowledgments. **No appendices.**
- **Equations:** 35 numbered equations, (1)–(35), plus several displayed but unnumbered expressions.
- **Figures:** 7.
- **Funding:** Air Force Office of Scientific Research; W. Wang further acknowledges a Stanford Graduate Fellowship. The authors thank Supriyo Datta and Kirk H. Bevan for a critical reading of the original draft.

## Abstract

A theoretical description of scanning tunneling potentiometry (STP) measurement is presented to address the increasing need for a basis to interpret experiments on macroscopic samples. Based on a heuristic understanding of STP provided to facilitate theoretical understanding, the total tunneling current related to the density matrix of the sample is derived within the general framework of quantum transport. The measured potentiometric voltage is determined implicitly as the voltage necessary to null the tunneling current. Explicit expressions of measured voltages are presented under certain assumptions, and limiting cases are discussed to connect to previous results. The need to go forward and formulate the theory in terms of a local density matrix is also discussed.

## 1. Introduction

Scanning probes are widespread, but very few measure transport at very short length scales. The ultimate probe for such measurements is **scanning tunneling potentiometry (STP)** [1,2], in which an STM is used to measure the local potential due to the flow of an applied current. Only recently have the authors and others developed STP instruments that operate routinely over a wide range of conditions and essentially at the fundamental noise limit of STP [3–6].

The authors' focus is **local quantum transport in macroscopic materials**, as distinct from quantum transport *through* nanostructures (single molecules, nanotubes, lithographically produced nanostructures). Their work demonstrates that potential maps can be obtained in appropriate materials down to distances smaller than *all* the length scales relevant in transport — the inelastic scattering length, the elastic scattering length, and even the Fermi wavelength. Figure 1 shows such a measurement on epitaxial graphene: considerable local structure in the potential, relatively large in magnitude. The lack of a quantitative basis for interpreting such images motivates the paper.

**Two issues are identified.**
1. It is not clear exactly what potential is being measured. Macroscopically the measured potential would be the usual local electrochemical potential; but at the length scales STP probes, one cannot use thermodynamic concepts.
2. The situation is inherently quantum mechanical, so any calculation of the potential must include the underlying quantum mechanical processes.

These issues are not entirely new. They have been partly addressed by theories of transport through nanostructures, where the sample is small compared to the characteristic transport lengths. In those nanostructure cases, however, the measurement contacts are relatively macroscopic (compared with an STP tip), cannot be scanned, and the contact–sample interfaces play an important role in the overall transport. Several theories consider what an STP would measure inside a nanostructure [7–11], although no STP data yet exist that can be compared with them. In those treatments it was possible to write down explicit expressions for the STP voltage (for example, equation (37) of reference [7]); but those expressions are explicitly dependent on the voltages applied on the current leads. By contrast, when the sample is macroscopically large, the geometry and microscopic processes present in the leads obviously cannot matter. Hence a proper theoretical formulation is required, and precisely what STP measures remains unclear.

The paper takes first steps toward a theoretical description of an STP measurement of local quantum transport in a **macroscopic** sample. **The relevant quantum mechanical quantity is the density matrix**, and it is possible to develop an implicit (and, under some approximations, explicit) relation from which the measured potential can be determined in terms of the density matrix and the tunneling process into the sample. The tunneling process associated with the STM tip can be accounted for; how to *calculate* the density matrix under the relevant nonequilibrium conditions and short length scales in a macroscopic sample is a separate matter, and the authors do not address those computational challenges. Their goal is to make STP intelligible to experimentalists and to define the deeper theoretical questions needing attention; one example of the latter is the need for formulations in terms of **local density matrices** as opposed to global ones.

Some of these issues were addressed by **Chu and Sorbello** [12] in the context of their calculation of the residual resistivity dipole of a scattering center in the spirit of **Landauer** [13]. As noted in their paper, the potential measured in STP is *not* the same as the local electrostatic potential in the material generated by an electric current. The present work is a generalization of theirs and an articulation from the general point of view of a theory of STP measurement; the result is more general, and instead of a weighted sum the final result is a form built out of matrices that are either the density matrix of the sample or are defined with sample and tip wave functions.

**Organization:** (i) the STP setup, emphasizing that what is operationally measured is the potential necessary to achieve zero current through the potentiometric contact; (ii) a heuristic understanding of STP; (iii) a simple model with only two scattering centers separated by a mesoscopic distance, motivating a general theory and leading naturally to the density matrix of the sample in the expression for the tunneling current; (iv) the need for a *local* density matrix for macroscopic samples; (v) limiting cases.

## 2. Scanning tunneling potentiometry

### 2.A STP setup

As seen in Figure 2, **STP is effectively a four-point transport measurement using an STM tip**. A floating current source drives a current through the sample via electrodes 1 and 2. A voltage is applied between the third electrode and the STM tip, which serves as the fourth electrode. **The voltage is adjusted so that the tunneling current between the sample and the tip is zero — this is the definition of a potentiometric measurement.** This applied null-current voltage is the datum recorded in an STP measurement. The STM's ability to scan on nanometer scales makes STP a nanoscale transport measurement. The experimental output is a potential map of the scanned area accompanied by a topographic map (obtained by conventional STM operation) of the same area, taken point by point successively with the potential (see Ref. [3] for details).

### 2.B A heuristic interpretation of STP

Consider a macroscopic sample with the current contacts far removed — sample size and inter-contact distance large compared with the characteristic transport length scales. The question is what STP really measures under these conditions. In the thermodynamic limit (large distance between voltage measurements, large voltage-contact area, macroscopic sample) the measured value would correspond to the local electrochemical potential. In STP the situation is more subtle.

**Starting point.** In a conventional STM measurement, the total tunneling current is written [14]:

$$I=\frac{4\pi e}{\hbar}\sum_{\vec k,\vec k'}\bigl[f_s(\vec k)-f_t(\vec k')\bigr]\,\delta\!\left(E_{sc,\vec k}-eV_s,\;E'_{tc,\vec k'}-eV_t\right)|M|^2 \tag{1}$$

where $\delta(E_1,E_2)$ is the **Kronecker delta symbol**; $f_i$ ($i=s,t$) are Fermi–Dirac distribution functions of sample and tip; $|M|^2$ is the magnitude of the tunneling matrix elements, *assumed constant* in this equation; $E_{ic,\vec k}$ are eigen energies of specific states of sample and tip, measured with respect to the band ("chemical energy", see Figure 3); and $-eV_i$ are the energies associated with the electrostatic potential in sample and tip ("electrostatic energy", Figure 3). The sum of chemical and electrostatic energy is the **electrochemical energy**.

**Two modifications** are required to use the form of equation (1) for a potentiometric transport measurement:
1. The distribution function of the sample is **not an equilibrium** one, because of the applied current through the sample; hence it is not a Fermi–Dirac distribution.
2. The magnitude of the tunneling matrix elements $|M|^2$ should **not** be assumed constant for each tunneling channel; an equivalent **average value** must be used.

**Example non-equilibrium distribution.** In the linear-response region of a homogeneous, defect-free sample with only inelastic scattering of mean free path $l_{in}$, the set of electrons with a given direction of wave vector is described by an effective chemical potential that depends on that direction [12], i.e. $f_s(\vec k)\propto\bigl(e^{\beta(E-\mu_{\hat\theta})}+1\bigr)^{-1}$ with $\beta\equiv 1/(k_BT)$ (see also Section V). A distribution function $f_s(E_{s,ec})$ is defined as the average probability of occupancy for each energy $E_{s,ec}$, averaged over all degenerate states (different directions of wave vector). Plotted against $E_{s,ec}$, one expects $f_s\approx 1$ at low energy and $f_s\approx 0$ at high energy, but in the transition region it is **not** a Fermi–Dirac distribution. Ignoring thermal broadening, with a constant current and a cylindrical Fermi surface, one obtains (Figure 4):

$$f_s(E_{s,ec})=\begin{cases}
1 & E_{s,ec}<\mu-el_{in}E_0\\[2mm]
1-\dfrac{(el_{in}E_0-\mu+E_{s,ec})^{3/2}}{2(el_{in}E_0)^{3/2}} & \mu-el_{in}E_0<E_{s,ec}<\mu\\[3mm]
\dfrac{(el_{in}E_0+\mu-E_{s,ec})^{3/2}}{2(el_{in}E_0)^{3/2}} & \mu<E_{s,ec}<\mu+el_{in}E_0\\[3mm]
0 & E_{s,ec}>\mu+el_{in}E_0
\end{cases} \tag{2}$$

where $E_0$ is the electric field and $l_{in}$ the inelastic mean free path. The non-equilibrium distribution is thus smeared symmetrically about $\mu$ over a window $\pm el_{in}E_0$, with a characteristic $3/2$-power shape rather than the Fermi–Dirac shape.

**Consequence.** Comparing the sample distribution with the tip's (a Fermi–Dirac distribution), electrons with relatively low energies tend to flow from tip to sample and those with relatively high energies in the opposite direction. **The total tunneling current is therefore a weighted sum of the difference of the two distribution functions.** The weight for each energy is related to the density of states, but *also* to the tunneling matrix elements, which are determined by wave function values at a certain position (the tip's center of curvature) and must not be taken as in equation (1). One writes:

$$I=\frac{4\pi e}{\hbar}\int_{-\infty}^{\infty}\bigl[f_s(\epsilon)-f_t(\epsilon-eV_t)\bigr]N_s(\epsilon)\,N_t(\epsilon-eV_t)\,\overline{|M|^2}\,\mathrm d\epsilon \tag{3}$$

where $V_t$, the voltage on the tip, effectively translates the tip distribution function $f_t$ horizontally until the total tunneling current vanishes; $N_s$ and $N_t$ are the densities of states of sample and tip; $\overline{|M|^2}$ is the averaged squared tunneling matrix element. Here the densities of states are more or less semi-classical, while the average magnitude of the tunneling matrix **represents the quantum interference**, studied in detail in the next section. The structure "current proportional to a weighted sum of the difference of two distribution functions" is not unlike the thermoelectric effect, except that there the origin of the difference is a temperature difference, whereas here it is the **nonequilibrium nature of current flow**.

**Message of the heuristic.** From equation (3) it is clear that **STP does not measure a well-defined thermodynamic potential**; rather it measures the non-equilibrium distribution function of the sample, with the weight for each energy set by both densities of states and quantum interference effects in the tunneling matrix. To calculate this weight a density matrix is needed. It is also clear that **even with the same distribution function**, the STP voltage can change from one measurement point to another because of the relative change in the tunneling matrix element arising from quantum interference — this accounts for the STP fluctuation in Chu & Sorbello's paper [12]. The STP potential therefore reflects **both** changes in the distribution functions **and** changes in the tunneling matrix elements as a function of position.

## 3. General theory in terms of density matrix

### 3.A Simple model considered in the problem

The model of Figure 2 represents a macroscopic sample with defects closer to one another than the inelastic mean free path. The sample is macroscopic and macroscopically connected to the current-providing electrodes. The STM tip probes a small region containing **two scattering centers near each other**; the rest of the sample is defect-free and homogeneous, with inelastic mean free path $l_{in}$ and Fermi wavelength $\lambda_F$, both comparable to the distance between the two defects. The electrochemical potential on the sample is expected to be linear in position except at the defects (Figure 2, upper right). However, when comparing STP data taken at nearby points, such thermodynamic concepts are inadequate.

Two questions can be posed: **(a)** what is the STP measurement result *near* the two defects? **(b)** what is the cross section of the two defects if seen from far away, treating them as one single defect? The answer to (b) determines the STP result far from the defects, since there STP measures the **Landauer resistive dipole potential** [13]. A similar problem must be solved to answer both.

### 3.B Quantum transport approach

In the quantum transport approach [15] one uses a **density matrix** [16] to describe the sample, and treats all three macroscopic contacts as electron reservoirs having Fermi–Dirac distributions.

*Footnote [16]:* formally, to include all the information one needs **correlation functions**, which also give the phase difference between states at different *times*; but as shown below, the density matrix of the sample — which specifies only the phase difference between states at the *same* time — is sufficient to describe the situation.

**Why the density matrix is necessary** (plane waves as basis): start with an incident plane wave. It is scattered by either of the two defects; the scattered wave is coherent with the incident wave. As it propagates, the magnitude of the coherent part shrinks due to inelastic scattering, which generates waves having indefinite phase difference with the incident and scattered waves. The scattered coherent wave can be scattered again by the other defect, generating a coherent secondary scattered wave. The incident plane wave is thus scattered back and forth by both scattering centers, with a decaying coherent part. In addition, the incoherent waves generated by inelastic scattering are individually also scattered back and forth and generate coherent sets of their own. This combination of **coherence from elastic scattering** with **incoherence and probability from inelastic scattering** is formally described by a density matrix. The density matrices resulting from all the incident plane waves, which are mutually incoherent, are added to obtain the net density matrix.

**Stated assumptions.** The paper does *not* undertake the calculation of the density matrix; it is assumed to have been calculated. The macroscopic contacts are retained in the problem because they are needed to determine the density matrix of the sample in the **Non-Equilibrium Green Function–Landauer** approach [15]. **The objective is to calculate the total tunneling current given the density matrix of the sample and the properties of the STM tip; once that current is obtained with the tip voltage as a parameter, setting the current to zero implicitly determines the STP measurement result.**

### 3.C Total tunneling current

The sample is described by the abstract density matrix $\hat\varrho$; the STM tip is described by a Fermi–Dirac distribution function

$$f(E_{c,\vec p}-eV_t-\mu)=\frac{1}{e^{\beta(E_{c,\vec p}-eV_t-\mu)}+1}$$

with $\{|\chi_{\vec p}\rangle\}$ as its basis set. Here $V_t$ is the voltage applied on the STM tip, $E_{c,\vec p}$ is the chemical eigen energy of state $|\chi_{\vec p}\rangle$, and $\mu$ is the electrochemical potential of the tip.

**Step 1 — diagonalize the density matrix.** After diagonalization,

$$\hat\rho_\psi=\begin{pmatrix}\ddots&\cdots&&\cdots\\ &\rho_{\psi\vec k\vec k}&0&\\ \vdots&&\ddots&\vdots\\ &0&&\rho_{\psi\vec k'\vec k'}\\ \cdots&&\cdots&\ddots\end{pmatrix} \tag{4}$$

where $\rho_{\psi\vec k\vec k}=\langle\psi_{\vec k}|\hat\varrho|\psi_{\vec k}\rangle$. The symbol $\hat\varrho$ denotes the abstract density matrix and $\hat\rho_\psi$ its matrix form in the basis $\{|\psi_{\vec k}\rangle\}$, which in this case diagonalizes it.

The basis $\{|\psi_{\vec k}\rangle\}$ consists of wave functions that are **mutually incoherent**, so the diagonal elements have the physical meaning that the probability of finding an electron in state $|\psi_{\vec k}\rangle$ is $\rho_{\psi\vec k\vec k}$. Since **elastic scattering only scatters states of a given eigen electrochemical energy into states of the same eigen electrochemical energy**, one can choose $\{|\psi_{\vec k}\rangle\}$ to be energy eigenstates with $E_{ec,\vec k}$ as their eigen electrochemical energies. Because chemical energies are used for tip states and electrochemical energies for sample states, the subscripts "s" and "t" on energy levels are omitted.

**Step 2 — single-channel tunneling current** (Figure 5): the current between one sample state $|\psi_{\vec k}\rangle$ and one tip state $|\chi_{\vec p}\rangle$ is evaluated as a surface integral over a surface $\Sigma$ lying in vacuum between sample and tip [14]:

$$I_{\vec k,\vec p}=\frac{4\pi e}{\hbar}\Bigl[\rho_{\psi\vec k\vec k}-f(E_{c,\vec p}-eV_t-\mu)\Bigr]\,\delta\!\left(E_{ec,\vec k},\,E_{c,\vec p}-eV_t\right)\times\left(\frac{\hbar^2}{2m}\right)^{\!2}\left|\int_\Sigma\left(\psi_{\vec k}\vec\nabla\chi^*_{\vec p}-\chi^*_{\vec p}\nabla\psi_{\vec k}\right)\cdot\mathrm d\vec S\right|^2 \tag{5}$$

Here $m$ is the electron mass and $\mathrm d\vec S$ the oriented surface element on $\Sigma$. Note that the **diagonal density-matrix element $\rho_{\psi\vec k\vec k}$ has replaced the sample distribution function** of equation (1).

**Step 3 — sum over channels.** The tunneling currents from different channels are **additive**, because both the sample states and the tip states are mutually incoherent. Hence the total tunneling current is

$$I=\sum_{\vec k,\vec p}\left\{\frac{4\pi e}{\hbar}\Bigl[\rho_{\psi\vec k\vec k}-f(E_{c,\vec p}-eV_t-\mu)\Bigr]\delta\!\left(E_{ec,\vec k},E_{c,\vec p}-eV_t\right)\times\left(\frac{\hbar^2}{2m}\right)^{\!2}\left|\int_\Sigma\left(\psi_{\vec k}\vec\nabla\chi^*_{\vec p}-\chi^*_{\vec p}\nabla\psi_{\vec k}\right)\cdot\mathrm d\vec S\right|^2\right\} \tag{6}$$

with the tunneling matrix element defined as

$$M_{\vec k\vec p}\equiv\delta\!\left(E_{ec,\vec k},E_{c,\vec p}-eV_t\right)\frac{\hbar^2}{2m}\int_\Sigma\left(\psi_{\vec k}\vec\nabla\chi^*_{\vec p}-\chi^*_{\vec p}\nabla\psi_{\vec k}\right)\cdot\mathrm d\vec S \tag{7}$$

**Step 4 — Chen's derivative rule: eliminate the tip wave function.** Expanding the tip wave function in spherical harmonics (chapter 3.2 of reference [14]):

$$\chi_{\vec p}(\vec r)=\sum_{l,m}C_{lm,\vec p}\,k_l(\kappa\rho)\,Y_{lm}(\theta,\phi) \tag{8}$$

where $Y_{lm}$ are spherical harmonics, $k_l$ is the $l$-th spherical modified Bessel function of the second kind, $\kappa$ is the vacuum decay constant, $\rho$ the distance from the tip's center of curvature, and $C_{lm,\vec p}$ expansion coefficients. There exists a general **derivative rule** (chapter 3.4 of reference [14]) by which the matrix element (7) becomes a **linear operation on the sample state only, evaluated at the center of curvature $\vec r_0$ of the tip** (which is also the origin for the tip expansion):

$$M_{\vec k\vec p}=\left(\mathcal F_{(\vec p,V_t)}\psi_{\vec k}\right)\big|_{\vec r_0} \tag{9}$$

For example, for an $s$-wave tip state,

$$\mathcal F_{(\vec p,V_t)}=\frac{2\pi C_{\vec p}\hbar^2}{\kappa m}\,\delta\!\left(E_{ec,\vec k},E_{c,\vec p}-eV_t\right)$$

which is a **pure number**; and for a $p_z$-wave tip state,

$$\mathcal F_{(\vec p,V_t)}=\frac{2\pi C_{\vec p}\hbar^2}{\kappa m}\,\delta\!\left(E_{ec,\vec k},E_{c,\vec p}-eV_t\right)\frac{\partial}{\partial z}$$

When the pure state $\chi_{\vec p}$ is a combination of $s$, $p$, $d$, … waves, the corresponding operators are additive.

**Step 5 — total current in operator form.**

$$I=\sum_{\vec k,\vec p}\frac{4\pi e}{\hbar}\Bigl[\rho_{\psi\vec k\vec k}-f(E_{c,\vec p}-eV_t-\mu)\Bigr]\left|\left(\mathcal F_{(\vec p,V_t)}\psi_{\vec k}\right)\big|_{\vec r_0}\right|^2 \tag{10}$$

where the Kronecker delta has been absorbed into the operator $\mathcal F_{(\vec p,V_t)}$; these operators are **well defined only between energy eigenstates**. Compared with the heuristic Section II: $\rho_{\psi\vec k\vec k}$ plays the role of the **distribution function**, and $\bigl|(\mathcal F_{(\vec p,V_t)}\psi_{\vec k})|_{\vec r_0}\bigr|^2$ plays the role of the **squared tunneling matrix element**; the averaging of the tunneling matrix element in equation (3) is effectively *defined* by requiring equation (3) to equal equation (10). The densities of states of both sample and tip are reflected in the summations over all tip states and all sample states.

**Step 6 — basis-free matrix-product form.** Equation (10) requires diagonalization of the density matrix. To obtain an abstract expression one rewrites it as the product of a matrix with the density matrix of the sample. Using a basis $\{|\phi_{\vec k}\rangle\}$ of electrochemical-energy eigenstates (not necessarily diagonalizing $\hat\varrho$), the sample density matrix reads

$$\hat\rho_\phi=\begin{pmatrix}\ddots&\cdots&&\cdots\\ &\rho_{\phi\vec k\vec k}&\rho_{\phi\vec k\vec k'}&\\ \vdots&&\ddots&\vdots\\ &\rho_{\phi\vec k'\vec k}&\rho_{\phi\vec k'\vec k'}&\\ \cdots&&\cdots&\ddots\end{pmatrix} \tag{11}$$

now with **off-diagonal elements** present. The matrix-product form of the expression is

$$I=\sum_{\vec p}\frac{4\pi e}{\hbar}\,\mathrm{tr}\!\left[\vec\phi_0^{\,\dagger}\vec\phi_0\bigl[\hat\rho_\phi-f(E_{c,\vec p}-eV_t-\mu)\bigr]\right]=\frac{4\pi e}{\hbar}\,\mathrm{tr}\!\left[\left(\sum_{\vec p}\vec\phi_0^{\,\dagger}\vec\phi_0\right)\hat\rho_\phi-\left(\sum_{\vec p}f(E_{c,\vec p}-eV_t-\mu)\,\vec\phi_0^{\,\dagger}\vec\phi_0\right)\right] \tag{12}$$

where

$$\vec\phi_0=\Bigl(\mathcal F_{(\vec p,V_t)}\phi_{\vec k_1}(\vec r_0),\;\cdots,\;\mathcal F_{(\vec p,V_t)}\phi_{\vec k_i}(\vec r_0),\;\cdots,\;\mathcal F_{(\vec p,V_t)}\phi_{\vec k_n}(\vec r_0)\Bigr) \tag{13}$$

The order of stacking the $\phi_{\vec k}$'s in $\vec\phi_0^{\,\dagger}$ and $\vec\phi_0$ is the same as that adopted in writing $\hat\rho_\phi$. The basis functions $\{|\phi_{\vec k}\rangle\}$ are all electrochemical-energy eigenfunctions, which is what makes $\mathcal F_{(\vec p,V_t)}$ well defined. **However**, the matrices $\sum_{\vec p}\vec\phi_0^{\,\dagger}\vec\phi_0$ and $\sum_{\vec p}f(E_{c,\vec p}-eV_t-\mu)\vec\phi_0^{\,\dagger}\vec\phi_0$ obey the same transformation rules as any other operator (or density matrix) in the Hilbert space, so the *result* does not require energy eigenfunctions — under other basis sets, however, one generally does not have an explicit expression linking the matrix elements to the sample wave function value at a given point (except the special case of Section III D).

**Limitation.** In equation (12) the tip and sample properties are entangled by the $\delta$-symbols, and **no explicit expression for the measured STP potential $\mu$ could be found**, although $\mu$ is implicitly defined by setting equation (12) to zero.

### 3.D Explicit expressions for measured potential

**Assumptions (the "featureless tip"):**
- (a) the tip has a **uniform density of states $N_t$** over the energy range of interest (wide-band / flat-DOS approximation for the tip);
- (b) the operator of equation (9) reduces to

$$\mathcal F_{(\vec p,V_t)}=\delta\!\left(E_{ec,\vec k},E_{c,\vec p}-eV_t\right)\mathcal F_0 \tag{14}$$

i.e. the $\vec p$ dependence resides **only** in the $\delta$-symbol.

Under these simplifications the sum over $\vec p$ in equation (12) can be carried out explicitly:

$$\sum_{\vec p}\vec\phi_0^{\,\dagger}\vec\phi_0=N_t\,\vec\phi_{00}^{\,\dagger}\vec\phi_{00} \tag{15}$$

$$\sum_{\vec p}f(E_{c,\vec p}-eV_t-\mu)\,\vec\phi_0^{\,\dagger}\vec\phi_0=N_t\,\vec\phi_{00}^{\,\dagger}\vec\phi_{00}\,\hat\rho_{\phi,FD}(\mu) \tag{16}$$

where

$$\vec\phi_{00}=\Bigl(\mathcal F_0\phi_{\vec k_1}(\vec r_0),\;\cdots,\;\mathcal F_0\phi_{\vec k_i}(\vec r_0),\;\cdots,\;\mathcal F_0\phi_{\vec k_n}(\vec r_0)\Bigr) \tag{17}$$

$$\hat\varrho_{FD}(\mu)=\frac{1}{1+e^{\beta(\hat H_s-\mu)}} \tag{18}$$

and $\hat H_s$ is the Hamiltonian of the sample. These equations are **basis-transformation-independent**, so the basis wave functions need *not* be energy eigenfunctions for the expressions of this subsection. The matrix form of the total tunneling current is then

$$I=\frac{4\pi e}{\hbar}N_t\cdot\mathrm{tr}\!\left[\vec\phi_{00}^{\,\dagger}\vec\phi_{00}\left(\hat\rho_\phi-\hat\rho_{\phi,FD}(\mu)\right)\right] \tag{19}$$

**Comparison with equation (3).** The resemblance is immediate, except that the density of states of the sample is *implicitly* included in the summation of the trace operation. One also sees that **it is the difference of the density matrix (from a Fermi–Dirac reference) that STP measures, with a weight**; to express things in terms of effective distribution functions, a mean matrix element value must be used, and that value is expected to change over space — as seen in the definition of $\vec\phi_{00}$ in equation (17).

#### Subcase I — high temperature compared with the nonequilibrium deviation

Here the temperature is high compared with the deviations from thermal equilibrium caused by the applied current. For example, in the setting of Figure 4 one needs $k_BT\gg el_{in}E_0$, rather than a sharp transition in the distribution function implying $T\approx 0$. Assume the density matrix is very close to thermal equilibrium with electrochemical potential $\mu_0$, and that the measured STP potential is $\mu_0+\Delta\mu$. Setting equation (19) to zero gives

$$\mathrm{tr}\!\left[\vec\phi_{00}^{\,\dagger}\vec\phi_{00}\left(\hat\rho_\phi-\hat\rho_{\phi,FD}(\mu_0)\right)\right]=\mathrm{tr}\!\left[\vec\phi_{00}^{\,\dagger}\vec\phi_{00}\left(\hat\rho_{\phi,FD}(\mu_0+\Delta\mu)-\hat\rho_{\phi,FD}(\mu_0)\right)\right] \tag{20}$$

Linearizing the Fermi function in $\Delta\mu$:

$$\frac{1}{1+e^{\beta(E-\mu_0-\Delta\mu)}}-\frac{1}{1+e^{\beta(E-\mu_0)}}\;\approx\;\frac{\beta}{2+e^{-\beta(E-\mu_0)}+e^{\beta(E-\mu_0)}}\,\Delta\mu$$

one gets

$$\Delta\mu=\frac{1}{\beta}\,\frac{\mathrm{tr}\!\left[\vec\phi_{00}^{\,\dagger}\vec\phi_{00}\left(\hat\rho_\phi-\hat\rho_{\phi,FD}(\mu_0)\right)\right]}{\mathrm{tr}\!\left[\vec\phi_{00}^{\,\dagger}\vec\phi_{00}\,\hat\rho'_{\phi,FD}(\mu_0)\right]} \tag{21}$$

where

$$\hat\varrho'_{FD}(\mu_0)=\frac{1}{2+e^{-\beta(H_s-\mu_0)}+e^{\beta(H_s-\mu_0)}}$$

i.e. the (negative) derivative of the Fermi function promoted to an operator function of $H_s$.

#### Subcase II — sharp (delta-function) limit

Here it is assumed that **both** the thermal smoothing **and** the nonequilibrium modification of the distribution function correspond to a small reciprocal-vector change $\Delta\vec k$ compared with $\vec k_F$ and all other characteristic reciprocal vectors. A cruder approximation then reads

$$\frac{1}{1+e^{\beta(E-\mu_0-\Delta\mu)}}-\frac{1}{1+e^{\beta(E-\mu_0)}}\;\approx\;\delta(E-\mu_0)\,\Delta\mu$$

hence

$$\Delta\mu=\frac{\mathrm{tr}\!\left[\vec\phi_{00}^{\,\dagger}\vec\phi_{00}\left(\hat\rho_\phi-\hat\rho_{\phi,FD}(\mu_0)\right)\right]}{\mathrm{tr}\!\left[\vec\phi_{00}^{\,\dagger}\vec\phi_{00}\,\hat\rho''_{\phi,FD}(\mu_0)\right]} \tag{22}$$

where

$$\hat\varrho''_{FD}(\mu_0)=\delta(H_s-\mu_0)$$

**Status of the result.** These results constitute a general theory of STP **valid on all length scales**, putting coherent and incoherent processes on an equal footing through the use of the density matrix. The final results from which the measured potential is implicitly determined are **equations (6) or (12), which are equivalent**. The result is formal, however, and not as useful as desirable because it requires knowledge of the density matrix over the **entire** sample — a formidable problem. As argued on physical grounds in the next section, some form of local density matrix is desirable and appears possible (no rigorous proof is claimed). Put more strongly: **a formulation in terms of local properties will be necessary in order to make more quantitative interpretation of STP results practical.**

## 4. Local density matrix

The simple model as posed requires including both current contacts and large areas of the sample far from the measurement region, which is clearly unphysical. Moreover, the density matrix of the sample is very difficult to calculate numerically because of the large number of degrees of freedom. Equally important, one would ideally like a theory with which to uncover relevant transport physics *without a priori* knowledge of the sample density matrix. A proper theory should involve only wave functions in the vicinity of the probed area, and defects and material characteristics in roughly the same area; the measurement result should be determined by these parameters plus a proper boundary condition — for example the mean current flowing near that region of the sample. The authors therefore argue for **local density matrices defined for each point on the sample, with entries consisting of only local wave functions**.

### 4.A Outline of local density matrix

One needs electron wave functions that extend only locally. The energy eigenstates used above are extended throughout the sample (at least when there are no defects), so using that basis *all* states must be counted in expression (12), because the wave functions have non-zero magnitude at the tip's center of curvature $\vec r_0$. To isolate electrons far from the measurement area, the authors suggest going to basis sets involving only local wave functions. In principle the density matrix is the same object as before; but a new local basis leads to an **approximation that reduces the dimension of the density matrix**.

**Proposed basis (Figure 6):** a *different* basis set for each point on the sample,
$$\{|\xi_{\vec r+\Delta\vec r_i,\vec k}\rangle\}$$
consisting of electron **wave packets** centered around different positions $\vec r+\Delta\vec r_i$ with wave vector centered around $\vec k$. The set $\{\Delta\vec r_i\}$, the set $\{\vec k\}$, and the wave-function forms are the *same* for each point; only the vector $\vec r$ — the position probed by the STM tip — changes between measurement positions. Consequently the matrices transformed from $\sum_{\vec p}\vec\phi_0^{\,\dagger}\vec\phi_0$ and $\sum_{\vec p}f(E_{c,\vec p}-eV_t-\mu)\vec\phi_0^{\,\dagger}\vec\phi_0$ are the same for different positions **except for the lateral change in $\vec r$**. While incorrect in a strict quantum mechanical context, with this basis one can intuitively speak of electrons at certain positions with certain wave numbers.

Intuitively, $\{\Delta\vec r_i\}$ must cover the full range of the sample for completeness. The matrix form $\langle\xi_{\vec r+\Delta\vec r_i,\vec k}|\hat\varrho|\xi_{\vec r+\Delta\vec r_j,\vec k'}\rangle$ changes at different positions because the basis set changes.

**The simplification:** density matrix elements involving wave packets far away ($\Delta\vec r_i$ sufficiently large) should not affect the measurement result at position $\vec r$. The density matrix elements for these states will be finite, but because the region of finite amplitude of the wave function is far from $\vec r$, one expects both matrices $\sum_{\vec p}\vec\phi_0^{\,\dagger}\vec\phi_0$ and $\sum_{\vec p}f(E_{c,\vec p}-eV_t-\mu)\vec\phi_0^{\,\dagger}\vec\phi_0$ in equation (12) to have **zero elements involving these states** [17]. One then discards all states with sufficiently large $\Delta\vec r_i$, reducing the problem to one involving only electron wave packets near the STM tip position $\vec r$. **This reduced, position-dependent matrix is what is defined as the local density matrix.**

*Footnote [17]:* this is obtained from physical intuition and needs to be verified once the basis set is chosen; the intuition that zero wave function value implies zero tunneling current comes from energy eigenstates, whereas the new basis does not consist of energy eigenstates in the strict sense. In the special case of subsection III D, with a featureless tip, this physical intuition is **formally proven**.

**Interpretation:** what STP probes under the relevant non-equilibrium conditions is the **local density matrix** at certain positions on the sample.

**Tip sharpness requirement:** if the total tunneling current is to relate to the local density matrix at only one point, the STM tip must be sharp, with radius of curvature smaller than the length scale of variation of the local density matrix. Only then can one choose a surface $\Sigma$ in equation (5) that is localized in space.

**Relation to prior practice:** basis sets with localized wave functions are not new — e.g. codes based on the **linear combination of atomic orbitals (LCAO)** are common in electron transport calculations [18,19]. These naturally lead to local density matrices in the authors' sense, but existing usages are mostly on small or even molecular samples; the calculational strategy for large samples has not been worked out. Hence the concept of local density matrix is not only a theoretical convenience but **poses a new problem in mesoscopic transport**.

### 4.B Possible further developments

The local density matrix is defined on a basis $\{|\xi_{\vec r+\Delta\vec r_i,\vec k}\rangle\}$ of wave packets near the STM tip position $\vec r$. The matrices transformed from $\sum_{\vec p}\vec\phi_0^{\,\dagger}\vec\phi_0$ and $\sum_{\vec p}f(E_{c,\vec p}-eV_t-\mu)\vec\phi_0^{\,\dagger}\vec\phi_0$ in equation (12) are determined by Hilbert-space transformation rules and, once computed, are fixed except for the position $\vec r$. In the special case of subsection III D, the two matrices are given explicitly by equation (17) no matter what basis set is used.

**Proposed calculational route:** the approach to calculating the local density matrix should differ from the path of its definition. Since the local density matrix is spatially variant, **there should be a controlling differential equation governing its variation over space**. One can then pose a problem with **proper boundary conditions reflecting the mean current around the probed area**, without needing to treat the current-providing contacts or the sample far from the probed area. Although the derivation of the controlling equations is based on the sample density matrix, in the actual calculation only the local density matrix is relevant, and one does not even need to know the density matrix of the sample. The detailed form of the differential equations and boundary conditions depends on the basis set chosen and the further approximations made. These computational challenges are not addressed ("they require proper theorists").

**Choice of wave-packet size — two competing limits.** The size of the wave packets in space must be **small compared with macroscopic lengths** to make the local-density-matrix simplification feasible, yet **large compared with $\lambda_F$**, because of the uncertainty principle and the need to keep the energy uncertainty small. Two limits follow: (i) relatively **large** wave packets — more states included in the local density matrix, small energy uncertainty; (ii) relatively **small** wave packets — few states in the local density matrix, at the expense of large energy uncertainty for each basis state.

The two transformed matrices depend on how the new basis is chosen at each point. One can compute them according to the transformation rules, or — if large wave packets are adopted — assume each wave packet is an approximate energy eigenstate and use the two matrices in the explicit form.

**Recommended simplification:** assume all operators $\mathcal F_{(\vec p,V_t)}$ are the same for the tip states, as in the special case of subsection III D, viewing the tip as part of the instrument controlled by the experimentalist. For example, since only nanometer-scale signals are being probed, one can assume an **$s$-wave tip with the same constant in the matrix element calculation** — the approximation adopted in Chu & Sorbello's paper [12]. Under this approximation the local density matrix approach is also better solidified.

## 5. Limiting cases

### 5.A Sample in equilibrium

When the sample carries no current, after diagonalization the sample density matrix becomes a Fermi–Dirac distribution; supposing $\{|\psi_{\vec k}\rangle\}$ diagonalizes $\hat\varrho$, equation (6) gives

$$I=\sum_{\vec k,\vec p}\left\{\frac{4\pi e}{\hbar}\Bigl[f(E_{ec,\vec k}-\mu_s)-f(E_{c,\vec p}-eV_t-\mu_t)\Bigr]\delta\!\left(E_{ec,\vec k},E_{c,\vec p}-eV_t\right)\left|\left(\mathcal F_{(\vec p,V_t)}\psi_{\vec k}\right)\big|_{\vec r_0}\right|^2\right\} \tag{23}$$

The Kronecker delta requires the electrochemical energies of the sample state and the tip state to be equal. Under this condition, and when tip and sample are at the **same temperature**: if $\mu_s>\mu_t$ all terms are positive, so the total tunneling current is positive; if $\mu_s<\mu_t$ it is negative. **The only possibility for zero total tunneling current is $\mu_s=\mu_t$, regardless of where the tip is** — as expected physically. When the temperatures differ, this conclusion no longer holds, but that is expected as a thermoelectric effect.

### 5.B Homogeneous sample with no defect

Suppose the sample has no defects — only inelastic scattering, no elastic scattering — and the current is uniform. In a **jellium model**, translational symmetry (neglecting effects from the macroscopic contacts) implies the local density matrix is the same throughout the probed area, except for the effect of a **linear electrostatic potential distribution** reflecting the constant current and inelastic scattering. The local density matrix is then described by a distribution function (**no off-diagonal elements**), because electrons in different eigenstates are mutually incoherent. In the linear response limit:

$$f(\vec k,\vec r)\propto\frac{1}{e^{\beta(E_{\vec k}-\mu_{\hat\theta,\vec r})}+1}$$

$$\mu_{\hat\theta,\vec r}=e\vec E\cdot\vec r+\mu-el_{in}\vec E\cdot\hat\theta \tag{24}$$

**For each direction of momentum $\hat\theta$ there is an effective chemical potential $\mu_{\hat\theta}$.** This distribution function leads to the distribution function with electrochemical energy as variable in equation (2). In this case, in an STP measurement **the difference of data at different points comes from the $-\vec E\cdot\vec r$ term** (i.e. from the linear electrostatic ramp).

### 5.C Landauer resistive dipole

Suppose there is only one defect on an otherwise homogeneous sample, or that the defects are far apart compared with $l_{in}$. Far from the defect(s), electrons are mutually incoherent because of inelastic scattering events occurring after they are reflected by the defect(s). At such positions the local density matrix is again described by a distribution function. In the linear response limit it is very similar to equation (24):

$$f(\vec k,\vec r)\propto\frac{1}{e^{\beta(E_{\vec k}-\mu_{\hat\theta,\vec r})}+1}$$

$$\mu_{\hat\theta,\vec r}=-e\phi(\vec r)+\mu+el_{in}\nabla\phi\cdot\hat\theta \tag{25}$$

where $\phi(\vec r)$ is the **Landauer resistive dipole potential** [13]. **This demonstrates that STP can measure the Landauer resistive dipole potential**, as expected physically; resistive dipoles have been observed experimentally [2]. Equations (24) and (25) are similar because, in the regions where Landauer derived the resistive dipole, the only practical difference is that the electrostatic potential differs from the previous limiting case owing to the scattering center: here $\phi(\vec r)$ is the dipole field **plus** the homogeneous electric field.

### 5.D Chu and Sorbello model

Chu and Sorbello [12] calculated the STP result *much nearer* to a defect than $l_{in}$. They assume electrons have a specific distribution function in $\vec k$ space before encountering the scattering center, and that after being deflected by the scatterer the electrons are not deflected again by the same scatterer. Interpreted in the present context, they view most of the sample as the current-providing electrodes that inject incoming electrons with the specific distribution into the "sample", whose size is effectively much smaller than $l_{in}$ and centered on the defect. Once the electrons enter the sample they remain coherent in the presence of elastic scattering. Their reservoir case, background-scatterers case and semiclassical-barrier case all describe the distribution of injected electrons. In the present context the density matrix of this very small region near the defect is completely known:

$$\varrho=\sum_{\vec k}f(\vec k)\left|\psi^{(+)}_{\vec k}\right\rangle\left\langle\psi^{(+)}_{\vec k}\right| \tag{26}$$

where $\bigl|\psi^{(+)}_{\vec k}\bigr\rangle$ is the **purely coherent** scattering state resulting from one channel of injected electron from the contacts.

If one also measures the part of the sample not close to the defect, equation (26) no longer describes all the electrons in the system. However, it is conceivable that with a **local** density matrix description, the local density matrix very near the defect does look like equation (26).

Using equation (22) and noting $f(E_{\vec k}-\mu_{\vec k})-f(E_{\vec k}-\mu)\approx\delta(E_{\vec k}-\mu)(\mu_{\vec k}-\mu)$, one obtains

$$\delta V_{STP}(\vec r_0)=\frac{(1/e)\sum_{\vec k}\bigl|\psi^{(+)}_{\vec k}(\vec r_0)\bigr|^2\,\delta(E_{\vec k}-\mu)\,(\mu_{\vec k}-\mu)}{\sum_{\vec k}\bigl|\psi^{(+)}_{\vec k}(\vec r_0)\bigr|^2\,\delta(E_{\vec k}-\mu)} \tag{27}$$

**which is equation (14) of Chu and Sorbello's paper.** This illustrates why tunneling matrix elements must not be assumed to have the same magnitude when writing down the total tunneling current: the variation of this magnitude *is* the interference term. It also shows that **the density matrix of the sample determines how and where this variation occurs.**

### 5.E Atomic resolution in STP

The tunneling matrix elements depend on electron wave function values, which change over space, producing the quantum interference effects in the STP result. In normal STM mode it is also the change of tunneling matrix elements *within a unit cell* that produces atomic resolution (in practice, for atomic corrugations to be measurable the tip should usually be sharper than an $s$-wave tip, i.e. the operators $\mathcal F$ acting on the wave functions should not be as simple as a pure number; see chapter 7 of reference [14]). Hence the question: **does atomic resolution exist in STP measurements?**

Part of the answer is simple: as shown in limiting case V A, **without a current (sample in equilibrium) there is atomic resolution in STM, but no atomic corrugation in the STP measurement**, because the STP result is a constant throughout the sample. So if atomic resolution exists in STP, it must be different in origin from STM's. With a current on the sample the answer becomes complicated. To demonstrate, a **one-dimensional tight-binding toy model with only one atomic orbital** is analyzed (basic setup: chapter 10 of reference [20]).

The sample is one-dimensional, well described by a tight-binding model with a single atomic orbital of wave function $\phi(x)$ centered at $x=0$; the lattice constant is $a$. The band wave functions are

$$\psi_k(x)=\sum_n e^{ikna}\phi(x-na) \tag{28}$$

with $k\in(-\pi/a,\pi/a)$, the first Brillouin zone. Assuming $\phi(x)$ is an $s$-level and using the nearest-neighbour approximation:

$$E(k)=E_0-\gamma\cos(ka) \tag{29}$$

where $E_0$ and $\gamma$ are numbers related to the $s$-level energy and to $\Delta U(x)$, the correction to the atomic Hamiltonian. All operators $\mathcal F$ are taken to be the same for all states (i.e. approximation (14) holds and the total current is given by equation (19)).

#### 5.E.1 Sample with no defects

With no defects, the density matrix is diagonal in the basis $\{\psi_k\}$, so a distribution function $f(k)$ suffices, and $f(E)$ can be computed from $f(k)$. Ignoring thermal broadening, both are sketched in Figure 7. The total tunneling current reads

$$I=\frac{4\pi e}{\hbar}N_t\cdot\sum_k\left|\mathcal F_0\psi_k(x_0)\right|^2\left(f(k)-f_{FD}(k,\mu)\right) \tag{30}$$

where $f_{FD}(k,\mu)$ is the Fermi–Dirac distribution with chemical potential $\mu$ (free to move horizontally according to $\mu$). **The question becomes: does the value of $\mu$ that makes equation (30) vanish depend on $x_0$ within the unit cell?**

**(a) $x_0$ close to the origin.** Only the $n=0$ component of equation (28) is relevant, so

$$I\propto\sum_k\left|\mathcal F_0\phi(x_0)\right|^2\left(f(k)-f_{FD}(k,\mu)\right)=\left|\mathcal F_0\phi(x_0)\right|^2\sum_k\left(f(k)-f_{FD}(k,\mu)\right) \tag{31}$$

Hence **there is no spatial dependence in $\mu$** — in contrast to atomically resolved corrugations in STM mode, where the change in $|\mathcal F_0\phi(x_0)|^2$ indicates a spatial change in the measured sample height.

**(b) $x_0$ close to $a/2$.** Now at least two components ($n=0$ and $n=1$ in the nearest-neighbour approximation) matter:

$$I\propto\sum_k\left|\mathcal F_0\phi(x_0)+e^{ika}\mathcal F_0\phi(x_0-a)\right|^2\left(f(k)-f_{FD}(k,\mu)\right)=\left(\left|\mathcal F_0\phi(x_0)\right|^2+\left|\mathcal F_0\phi(x_0-a)\right|^2\right)\sum_k\left(f(k)-f_{FD}(k,\mu)\right)$$
$$+\sum_k\left[\left(\mathcal F_0\phi(x_0)\right)^*\mathcal F_0\phi(x_0-a)e^{ika}+\mathcal F_0\phi(x_0)\left(\mathcal F_0\phi(x_0-a)\right)^*e^{-ika}\right]\left(f(k)-f_{FD}(k,\mu)\right) \tag{32}$$

Assuming $\left(\mathcal F_0\phi(x_0)\right)^*\mathcal F_0\phi(x_0-a)$ is real, the second line of equation (32) equals

$$2\left(\mathcal F_0\phi(x_0)\right)^*\mathcal F_0\phi(x_0-a)\sum_k\cos(ka)\left(f(k)-f_{FD}(k,\mu)\right) \tag{33}$$

**When the current is small (linear response)** and $\mu$ is the value that nulls the first line of equation (32), the range of $k$ with nonzero $[f(k)-f_{FD}(k,\mu)]$ consists of two very narrow regions centered on $-k_F$ and $+k_F$; since $\cos(k_Fa)=\cos(-k_Fa)$, expression (33) also vanishes. **To this order there is still no spatial dependence in the measured STP potential.** If the current is large enough that $\Delta k$ in Figure 7 is significant, this argument breaks down and there *will* be a small corrugation in the measured STP potential at atomic resolution.

#### 5.E.2 Sample with defect(s)

With defects, the density matrix has **off-diagonal elements** in the $\{\psi_k\}$ basis. Considering only one off-diagonal element between the degenerate states $k_0$ and $-k_0$ (with $k_0$ close to $k_F$), with value $\delta$ in the $(k_0,-k_0)$ entry and $\delta^*$ in the $(-k_0,k_0)$ entry, one additional term is needed in equation (31) or (32):

$$\Delta I=\mathcal F_0\psi_{k_0}(x_0)\left(\mathcal F_0\psi_{-k_0}(x_0)\right)^*\delta^*+\text{complex conjugate} \tag{34}$$

With the same reality assumption as in the defect-free case, that $\mathcal F_0\psi_{k_0}(x_0)\left(\mathcal F_0\psi_{-k_0}(x_0)\right)^*$ is real:

$$\Delta I=2\,\mathcal F_0\psi_{k_0}(x_0)\left(\mathcal F_0\psi_{-k_0}(x_0)\right)^*\mathrm{Re}(\delta) \tag{35}$$

**(a) $x_0$ close to the origin.** Equation (31) becomes
$$\sum_k\left(f(k)-f_{FD}(k,\mu)\right)+2\mathrm{Re}(\delta)=0$$
hence **no spatial dependence in $\mu$**.

**(b) $x_0$ close to $a/2$.** The correction to equation (32) includes the term
$$2\mathrm{Re}(\delta)\left(\mathcal F_0\phi(x_0)\right)^*\mathcal F_0\phi(x_0-a)\cos(k_0a)\times\left(f(k_0)-f_{FD}(k_0,\mu)\right)$$
which **does** lead to a spatial dependence in $\mu$, proportional to $\delta$.

**Summary of 5.E:** with static defects in the sample, in the transition region between two adjacent atomic sites there will be atomically resolved corrugations due to changes in wave function values, but this corrugation is a **second-order effect**, as opposed to the **first-order effect** in STM mode. If the sample has no defects — hence no interference between states — the atomic corrugation is an **even higher-order effect**. Although obtained in a simplified toy model, the authors believe this conclusion has some universality. It demonstrates the nature of the STP potential problem: to first order the results are often trivial; to manifest effects from either wave function value changes or quantum interference, one often needs to go to higher order. This is part of why the authors cannot provide estimates of the size of these effects without calculating the actual density matrices.

## 6. Summary and discussion

The paper develops a viewpoint of STP measurement in the framework of quantum transport. **Equation (12) gives the total tunneling current in terms of the distribution function of the STM tip and the density matrix of the sample; setting this current to zero implicitly determines the STP measurement result.** The expression is in matrix-product form so that a **basis-set-free definition** can be made. With some approximations (featureless tip), explicit expressions for the measured STP potential were obtained — equations (21) and (22).

To remove the unphysical requirement of knowing material characteristics far from the STP probing area, the authors propose **local density matrices** (Section IV) as a parameter varying over space, controlled by a differential equation and a set of boundary conditions. This allows relating STP to sample properties near the probed region.

Section V provides limiting-case calculations demonstrating the use of the description, mostly with given or assumed sample density matrices. In particular, with the one-dimensional tight-binding toy model, **atomic resolution in STP measurement is a high-order effect**. The null results are partly due to assumed **symmetry in the Fermi surface** (e.g. equation (33) vanishing under the adopted assumptions) or in the operators $\mathcal F$ acting on the sample wave functions. The authors **speculate that asymmetry in the Fermi surface with respect to $\vec k$, or in the tip wave function (hence operator $\mathcal F$) with respect to energy, could lead to lower-order effects in STP measurement.**

**Analogy to scattering theory.** Comparing equation (12) with, for example, equation (8.6.6) of reference [15] (Datta), the analogy is immediate: the matrices $\sum_{\vec p}\vec\phi_0^{\,\dagger}\vec\phi_0$ and $\sum_{\vec p}f(E_{c,\vec p}-eV_t-\mu)\vec\phi_0^{\,\dagger}\vec\phi_0$ sit **where the scattering matrices are**. Keeping in mind the subtle difference between correlation function and density matrix, these two matrices can be viewed as a special kind of **scattering matrix**.

**The tip as an electron source.** As a special contact the STM tip provides scattering described by a scattering matrix related to those matrices. This implies it also acts as an **electron source**, whose strength depends on the strength of the scattering. This source effect will change the density matrix of the sample, or the local density matrix, as the tip moves. However, in the limiting case of **weak coupling** (small scattering strength, probe weakly interacting with the sample) the STP result is not expected to change much. STP therefore has the advantage of **perturbing the sample minimally**, compared with other contact-based probes such as using conducting cantilevers as the fourth electrode with an AFM. Conceptually, a good criterion for minimal source effect is that the tip should be far enough from the sample to sit in the **far tail of the exponential decay of the electron wave function** for sample states — though this corresponds to a large tunneling resistance and therefore low STP resolution due to large **Johnson noise**. It is nevertheless a valid starting point. When the sample is small compared with its characteristic transport lengths, the effect of the tip is generally large, and such effects are already explicitly included in the formalism of works on that case [7,8].

## Figures

### Figure 1 — STP data taken on epitaxial graphene as an example of transport measurement at length scales smaller than all the length scales relevant in the transport. As seen in the figure, on top of the average gradient, STP shows variations on the nanometer length scale. (p. 2)

A three-dimensional rendered surface plot titled "STP". Horizontal axes: X (nm), ticked 5, 10, 15, 20; Y (nm), ticked 5, 10, 15, 20 — i.e. a roughly 20 × 20 nm scan area. Vertical axis: $\phi$ ($\mu$V), ticked $-10$, $-5$, $0$, $5$. A colour bar to the right, also labelled $\phi$ ($\mu$V), runs from about $-13$ (dark blue) through $-10$, $-5$, $0$, $5$ to about $+7$ (dark red). The surface falls monotonically on average from the far-left/back corner (dark red, $\approx +5$ to $+7\ \mu$V) to the near-right corner (dark blue, $\approx -13\ \mu$V), i.e. an average potential gradient of order 1 $\mu$V/nm set by the applied current. Superimposed on that ramp the surface is visibly rough on the few-nanometre scale, with local bumps and dips of order a few $\mu$V. Two black scale bars drawn on the surface label $l_{in}=11$ nm (inelastic mean free path) and $\lambda_F=12$ nm (Fermi wavelength), both comparable to the whole scan size — the figure's physical point is that the observed potential structure occurs on length scales **shorter than every relevant transport length**, so that conventional thermodynamic/local-electrochemical-potential interpretation cannot apply.

### Figure 2 — Schematic setup of scanning tunneling potentiometry, and model problem to be considered in this paper. Electrodes 1, 2 and 3 are macroscopic contacts, while the STM tip, microscopically connected to the sample, functions as the fourth electrode. The sample is macroscopic in size and STP probes a small region which is enlarged to the upper left. The region has two scattering centers, and the rest of the sample is assumed to be homogeneous and defect-free, with no defects (scatterers) present. The distance between the two defects, the Fermi wavelength and the inelastic mean free path of the sample are all comparable. To the upper right presents an expected STP result on a large length scale, including the electrodes. (p. 2)

A three-panel composite. **Main drawing (bottom):** a perspective view of a brown rectangular sample slab carrying three gold pad electrodes, labelled **1** (left end), **3** (middle) and **2** (right end). Electrodes 1 and 2 are wired into an external loop containing a **floating current source** (green/grey cylinder) with the current $I$ and blue arrows marking the current direction through the sample from 1 to 2. An orange cylindrical **STM tip** hovers over the sample between electrodes 1 and 3; a grey analog meter marked **V** is connected between the tip and electrode 3 — the potentiometric (fourth-electrode) circuit. **Upper-left inset (boxed, connected by a leader line to the tip position):** the enlarged probed region, showing two scatterers drawn as asterisks separated by a vertical distance $d$, together with two horizontal calibration bars labelled $l_{in}$ and $\lambda_F$; the bars and $d$ are drawn comparable in length, encoding the model assumption $d\sim\lambda_F\sim l_{in}$. **Upper-right panel:** the expected large-scale STP result, $\mu_{\mathrm{STP}}$ (vertical axis) versus $x$ (horizontal axis), drawn as a red piecewise-linear curve: a flat plateau at the "1st electrode", then a downward ramp through the sample, a steeper drop labelled "defects", a short flatter segment near the "3rd electrode", a further ramp, and a final plateau at the "2nd electrode". The figure defines both the measurement circuit and the model problem.

### Figure 3 — Definitions of different energies in the problem. Chemical energies ($E_c$) are defined with respect to the band, e.g., the band bottom; electrostatic energies ($E_e$) are energy differences associated with the band bending due to existence of an electrostatic field; and the sum of these two energies are the electrochemical energies ($E_{ec}$). Electrons at different positions of the sample with the same chemical energy and wave vector have the same wave function, while they do not necessarily have the same electrochemical energy due to band bending. Although electrochemical energy is the appropriate energy one needs to use when comparing energies at different positions, it is easier to keep track of quantum states with chemical energies. (p. 3)

An energy-versus-position sketch. Two parabolic band minima are drawn side by side against a common absolute-energy baseline; the right-hand parabola's minimum sits **lower** than the left-hand one, representing band bending in an electrostatic field (an arrow labelled "band" points to the parabolas). At each of the two positions, three bracketed energy intervals are marked: a blue bracket $E_c$ running from the local band bottom up to the state energy (chemical energy); a dark-red bracket $E_e$ running from the common baseline up to the local band bottom (electrostatic energy, which is larger on the left than on the right); and a red bracket $E_{ec}$ spanning the whole interval from the baseline to the state energy — the electrochemical energy, $E_{ec}=E_c+E_e$. The figure makes concrete the bookkeeping convention used throughout: **chemical energies for tip states, electrochemical energies for sample states.**

### Figure 4 — Comparison of distribution functions with and without current. (a) When there is a current, the equilibrium Fermi surface (dashed line and shaded) is shifted to the right (solid line). (b) When viewed in the $E-\vec k$ diagram, in equilibrium, the Fermi surface is a horizontal circle, (c) while when current exists, the Fermi surface is tilted. (d) The occupation rate for each energy, i.e., the distribution function (solid red curve), is different than Fermi-Dirac distribution (blue curve). The distribution function in more complicated situations, for example, when elastic scattering exists, is expected to be different and more interesting than illustrated here. (p. 4)

Four panels. **(a)** A $k_x$–$k_y$ plane with both axes ticked $-k_F$, $0$, $k_F$. A dashed, hatched circle of radius $k_F$ marks the equilibrium Fermi surface; a solid circle of the same radius is displaced to the right (positive $k_x$) by a small amount indicated by a blue double arrow labelled $el_{in}E_0$ — the drift shift caused by the current. **(b)** A three-dimensional coloured paraboloid $E_{\vec k}$ over the $(k_x,k_y)$ plane with a **horizontal** circular cut (dashed, hatched) at the top, representing the equilibrium Fermi surface. **(c)** The same paraboloid with a **tilted** planar cut, representing the current-carrying Fermi surface. **(d)** Occupation $f$ (vertical axis, ticked 0 and 1) versus electrochemical energy $E_{ec}$ (horizontal axis, tick at $\mu$). The blue curve is a sharp Fermi–Dirac step at $\mu$; the solid red curve is the non-equilibrium distribution of equation (2), which falls off more gradually over the window $\mu\pm el_{in}E_0$, with the width indicated by blue arrows labelled $el_{in}E_0$. The figure supplies the physical picture behind equations (2) and (3): the current tilts/shifts the Fermi surface and smears the energy-resolved occupancy into a non-Fermi-Dirac shape.

### Figure 5 — Calculation of the tunneling current. The tunneling matrix element between one state of the sample and one state of the tip is evaluated by a surface integration over the surface $\Sigma$ between the sample and the tip (see equation (5)). Refer to reference 14 for details. This figure is redrawn in complete analogy to Figure 3.1 in this reference. Here the circles represent atoms of the sample (left) or the tip (right), and the surface $\Sigma$ is an imaginary surface in vacuum over which the integration in equation (5) is performed. (p. 7)

A simple line drawing: on the left, an irregular close-packed array of open circles labelled "sample"; on the right, a smaller cluster of open circles tapering to a point, labelled "tip". Between them a single smooth curved line labelled $\Sigma$ separates the two, curving around the tip apex. Nothing is plotted quantitatively; the figure establishes the geometry of the Bardeen-type surface integral of equation (5) — $\Sigma$ lies entirely in vacuum, so the integrand involves only the exponentially decaying tails of the sample and tip wave functions.

### Figure 6 — Schematic of the new basis set that we propose to use in order to construct local density matrix of the sample. In this figure, only the $\Delta\vec r$ degree of freedom is shown. The new basis set is defined with reference to the position of the STM tip $\vec r$, with the states centered around $\vec r+\Delta\vec r_i$. The states have finite wave function values at position $\vec r$ when $\Delta\vec r_i$ is small, and states far away with $\Delta\vec r_i$ large have negligible wave function values. When the position of the STM tip changes, the set $\{\Delta\vec r_i\}$ remains the same, hence the central locations $\{\vec r+\Delta\vec r_i\}$ changes, and the basis set changes. (p. 8)

A perspective rendering: an orange cylindrical STM tip at top centre, with a vertical dashed line dropping onto a central bell-shaped (Gaussian) wave packet drawn as a magenta-to-cyan shaded surface, labelled $\Delta\vec r=\Delta\vec r_0$. Four further identical wave packets are arranged around it at the four diagonal positions, labelled $\Delta\vec r=\Delta\vec r_1$, $\Delta\vec r_2$, $\Delta\vec r_3$, $\Delta\vec r_4$. Only the spatial ($\Delta\vec r$) degree of freedom is shown; the $\vec k$ label of each packet is suppressed. The point of the figure: the tip sits directly above the $\Delta\vec r_0$ packet, so only packets with small $|\Delta\vec r_i|$ have appreciable amplitude at the tip — justifying truncation of the density matrix to a **local** one.

### Figure 7 — Sketch of distribution function with respect to $k$ (upper panel) and $E$ (lower panel), both without current (dashed lines) and with a current (solid lines), in the tight-binding model without defects under consideration. (p. 12)

**Upper panel:** $f(k)$ (vertical axis, ticked 0 and 1) versus $k$ (horizontal axis), spanning the first Brillouin zone from $-\pi/a$ to $+\pi/a$, with the two Fermi points labelled $k_F$ (the left one at $-k_F$). The dashed trace is the equilibrium box distribution, equal to 1 for $|k|<k_F$ and 0 outside. The solid trace is the same box **rigidly shifted to the right** by an amount $\Delta k$, indicated by a pair of opposing arrows labelled $\Delta k$ at the right-hand edge — the current-carrying distribution.

**Lower panel:** $f(E)$ (vertical axis, ticked 0 and 1) versus $E$ (horizontal axis), with ticks at the band bottom $E_0-\gamma$, at $E_F$, and at the band top $E_0+\gamma$, i.e. the full tight-binding bandwidth $2\gamma$ of equation (29). The dashed trace is a single sharp step from 1 to 0 at $E_F$ (equilibrium, $T=0$). The solid trace, obtained by projecting the shifted box of the upper panel onto energy, is a **two-step staircase**: it drops from 1 to roughly $1/2$ at the energy corresponding to $-(k_F+\Delta k)$ and then from $1/2$ to 0 at the energy corresponding to $+(k_F-\Delta k)$ — that is, over a narrow window straddling $E_F$, half the states at a given energy (one direction of $k$) are occupied and half are not. This asymmetric occupancy window is exactly the region in which $[f(k)-f_{FD}(k,\mu)]$ is non-zero in equations (30)–(33), and its narrowness (two thin regions at $\pm k_F$) is what makes expression (33) vanish in linear response.

## Symbol glossary

| Symbol | Meaning | Units |
|---|---|---|
| $I$ | total tunneling current between tip and sample | A |
| $I_{\vec k,\vec p}$ | tunneling current in the single channel $(\vec k,\vec p)$ | A |
| $\Delta I$ | correction to the tunneling current from one off-diagonal density-matrix element | A |
| $e$ | elementary charge | C |
| $\hbar$ | reduced Planck constant | J·s |
| $m$ | electron mass | kg |
| $\beta\equiv 1/(k_BT)$ | inverse temperature | J$^{-1}$ (or eV$^{-1}$) |
| $k_B$ | Boltzmann constant | J/K |
| $T$ | temperature | K |
| $f_s(\vec k)$, $f_s(E_{s,ec})$ | sample distribution function (in $\vec k$, or averaged over degenerate states at energy $E_{s,ec}$) | dimensionless |
| $f_t(\vec k')$ | tip distribution function (Fermi–Dirac) | dimensionless |
| $f(E_{c,\vec p}-eV_t-\mu)$ | Fermi–Dirac occupancy of tip state $\vec p$ | dimensionless |
| $f_{FD}(k,\mu)$ | Fermi–Dirac distribution with chemical potential $\mu$ (tight-binding section) | dimensionless |
| $f(\vec k,\vec r)$ | position- and direction-resolved local distribution function | dimensionless |
| $\delta(E_1,E_2)$ | **Kronecker** delta symbol (energy conservation between discrete levels) | dimensionless |
| $\delta(E-\mu_0)$, $\delta(H_s-\mu_0)$ | Dirac delta function / operator-valued delta function | energy$^{-1}$ |
| $M$, $|M|^2$, $\overline{|M|^2}$ | tunneling matrix element, its square, and its channel-average | J (for $M$) |
| $M_{\vec k\vec p}$ | tunneling matrix element between sample state $\vec k$ and tip state $\vec p$ | J |
| $E_{sc,\vec k}$, $E'_{tc,\vec k'}$ | chemical eigen energies of sample and tip states | J (eV) |
| $E_{ic,\vec k}$ | chemical eigen energy of state $\vec k$ of subsystem $i=s,t$ | J (eV) |
| $E_c$ | chemical energy, measured from the band bottom | J (eV) |
| $E_e$ | electrostatic energy (band-bending energy difference) | J (eV) |
| $E_{ec}$, $E_{ec,\vec k}$, $E_{s,ec}$ | electrochemical energy $=E_c+E_e$; eigen electrochemical energy of sample state $\vec k$ | J (eV) |
| $E_{c,\vec p}$ | chemical eigen energy of tip state $|\chi_{\vec p}\rangle$ | J (eV) |
| $E_{\vec k}$, $E(k)$ | band energy of state $\vec k$ | J (eV) |
| $E_0$ (Section II) | applied electric field magnitude | V/m |
| $E_0$ (Section V E) | $s$-level band-centre energy in the tight-binding model | J (eV) |
| $\gamma$ | tight-binding nearest-neighbour hopping parameter (half-bandwidth) | J (eV) |
| $V_s$, $V_t$ | electrostatic potentials (voltages) applied on sample and tip | V |
| $-eV_i$ | electrostatic energy associated with potential $V_i$ | J (eV) |
| $\delta V_{STP}(\vec r_0)$ | local STP voltage deviation at tip position $\vec r_0$ (Chu–Sorbello form) | V |
| $\mu$ | electrochemical potential of the tip / the measured STP potential | J (eV) |
| $\mu_s$, $\mu_t$ | electrochemical potentials of sample and tip in equilibrium | J (eV) |
| $\mu_0$ | reference (equilibrium) electrochemical potential | J (eV) |
| $\Delta\mu$ | deviation of the measured STP potential from $\mu_0$ | J (eV) |
| $\mu_{\hat\theta}$, $\mu_{\hat\theta,\vec r}$ | direction-dependent (and position-dependent) effective chemical potential | J (eV) |
| $\mu_{\vec k}$ | effective chemical potential of channel $\vec k$ (Chu–Sorbello) | J (eV) |
| $\mu_{\mathrm{STP}}$ | STP-measured potential plotted in Figure 2 | V (or eV) |
| $l_{in}$ | inelastic mean free path | m (nm) |
| $\lambda_F$ | Fermi wavelength | m (nm) |
| $d$ | distance between the two scattering centers | m (nm) |
| $a$ | lattice constant of the 1D tight-binding sample | m |
| $\hat\theta$ | unit vector giving the direction of the wave vector | dimensionless |
| $\vec E$ | electric field vector | V/m |
| $\phi(\vec r)$ | Landauer resistive dipole potential plus the homogeneous field potential | V |
| $\phi(x)$ | atomic orbital wave function in the tight-binding model | m$^{-1/2}$ |
| $N_s(\epsilon)$, $N_t(\epsilon)$ | densities of states of sample and tip | states/J |
| $N_t$ | uniform (energy-independent) tip density of states | states/J |
| $\epsilon$ | integration variable (energy) in equation (3) | J (eV) |
| $\hat\varrho$ | abstract density matrix of the sample | dimensionless |
| $\hat\rho_\psi$, $\hat\rho_\phi$ | matrix form of the density matrix in basis $\{|\psi_{\vec k}\rangle\}$ / $\{|\phi_{\vec k}\rangle\}$ | dimensionless |
| $\rho_{\psi\vec k\vec k}$ | diagonal density-matrix element $=\langle\psi_{\vec k}|\hat\varrho|\psi_{\vec k}\rangle$; occupation probability of $|\psi_{\vec k}\rangle$ | dimensionless |
| $\rho_{\phi\vec k\vec k'}$ | general (possibly off-diagonal) density-matrix element in basis $\{|\phi_{\vec k}\rangle\}$ | dimensionless |
| $\delta$ (Section V E 2) | off-diagonal density-matrix element in the $(k_0,-k_0)$ entry | dimensionless |
| $\hat\varrho_{FD}(\mu)$, $\hat\rho_{\phi,FD}(\mu)$ | Fermi–Dirac density matrix / its matrix form, eq. (18) | dimensionless |
| $\hat\varrho'_{FD}(\mu_0)$ | $\bigl[2+e^{-\beta(H_s-\mu_0)}+e^{\beta(H_s-\mu_0)}\bigr]^{-1}$, Subcase I kernel | dimensionless |
| $\hat\varrho''_{FD}(\mu_0)$ | $\delta(H_s-\mu_0)$, Subcase II kernel | energy$^{-1}$ |
| $\hat H_s$, $H_s$ | Hamiltonian of the sample | J (eV) |
| $|\psi_{\vec k}\rangle$, $\psi_{\vec k}$ | sample eigenstates that diagonalize the density matrix | — |
| $|\psi^{(+)}_{\vec k}\rangle$ | purely coherent scattering state from one injected channel (Chu–Sorbello) | — |
| $\psi_k(x)$ | tight-binding Bloch wave function, eq. (28) | m$^{-1/2}$ |
| $|\phi_{\vec k}\rangle$, $\phi_{\vec k}$ | sample electrochemical-energy eigenstates used as a general basis | — |
| $|\chi_{\vec p}\rangle$, $\chi_{\vec p}(\vec r)$ | tip eigenstates | — |
| $|\xi_{\vec r+\Delta\vec r_i,\vec k}\rangle$ | local wave-packet basis state centered at $\vec r+\Delta\vec r_i$ with mean wave vector $\vec k$ | — |
| $\vec r$ | position of the STM tip (scanning coordinate) | m |
| $\vec r_0$ | center of curvature of the tip; evaluation point for sample wave functions | m |
| $x_0$ | tip position within the unit cell (1D toy model) | m |
| $\Delta\vec r_i$ | offset of the $i$-th wave packet from the tip position | m |
| $\Sigma$ | imaginary surface in vacuum between sample and tip | — |
| $\mathrm d\vec S$ | oriented surface element on $\Sigma$ | m$^2$ |
| $\mathcal F_{(\vec p,V_t)}$ | linear operator acting on the sample wave function, replacing the surface integral (eq. 9) | varies |
| $\mathcal F_0$ | the featureless-tip, $\vec p$-independent version of $\mathcal F$ (eq. 14) | varies |
| $\vec\phi_0$ | row vector of $\mathcal F_{(\vec p,V_t)}\phi_{\vec k_i}(\vec r_0)$ over the basis index $i$ (eq. 13) | varies |
| $\vec\phi_{00}$ | row vector of $\mathcal F_0\phi_{\vec k_i}(\vec r_0)$ (eq. 17) | varies |
| $C_{lm,\vec p}$, $C_{\vec p}$ | spherical-harmonic expansion coefficients of the tip wave function | varies |
| $k_l(\kappa\rho)$ | $l$-th spherical modified Bessel function of the second kind | dimensionless |
| $Y_{lm}(\theta,\phi)$ | spherical harmonic | dimensionless |
| $\kappa$ | vacuum wave-function decay constant | m$^{-1}$ |
| $\rho$ (in eq. 8) | radial distance from the tip's center of curvature | m |
| $k_F$, $\vec k_F$ | Fermi wave vector | m$^{-1}$ |
| $\Delta k$, $\Delta\vec k$ | current-induced shift of the distribution in reciprocal space | m$^{-1}$ |
| $k_0$ | wave vector of the degenerate pair $(k_0,-k_0)$ carrying the off-diagonal element | m$^{-1}$ |
| $n$ | lattice site index in eq. (28) | dimensionless |
| $\Delta U(x)$ | correction to the atomic Hamiltonian in the tight-binding model | J (eV) |
| $\mathrm{tr}[\cdot]$ | trace operation | — |
| $\mathrm{Re}(\delta)$ | real part of the off-diagonal element $\delta$ | dimensionless |

## Key results and limiting cases

1. **STP is defined operationally by a null condition.** The measured datum is the tip voltage $V_t$ (equivalently the potential $\mu$) at which the total tunneling current vanishes. Every result of the paper follows from setting one of the current expressions to zero.
2. **The central general result is equation (12)** (equivalently equation (6)): the total tunneling current is the trace of a product of (i) matrices built from the tip states and the sample wave functions evaluated at the tip's center of curvature, and (ii) the **sample density matrix**. Setting $I=0$ determines the STP potential implicitly. This result is valid on all length scales and treats coherent (elastic) and incoherent (inelastic) processes on the same footing.
3. **Replacement of distribution function by density matrix.** In the heuristic form (3), the sample enters through a distribution function $f_s(\epsilon)$ weighted by $N_s N_t\overline{|M|^2}$. In the general form (10), $f_s$ is replaced by the diagonal element $\rho_{\psi\vec k\vec k}$ and $\overline{|M|^2}$ by $\bigl|(\mathcal F_{(\vec p,V_t)}\psi_{\vec k})|_{\vec r_0}\bigr|^2$; the *definition* of the average matrix element is that (3) equals (10). The off-diagonal elements enter through the basis-free matrix-product form (12).
4. **Explicit expressions require a featureless tip** — flat tip DOS $N_t$ and $\vec p$-independent operator $\mathcal F_0$ (eq. 14). Then eq. (19) holds, and the measured potential shift is
   - **Subcase I** (high temperature, $k_BT\gg el_{in}E_0$): eq. (21), with the smeared kernel $\hat\varrho'_{FD}$;
   - **Subcase II** (sharp limit, $\Delta\vec k\ll k_F$): eq. (22), with the delta-function kernel $\hat\varrho''_{FD}=\delta(H_s-\mu_0)$.
   In both cases $\Delta\mu$ is a **ratio of two traces**, weighted identically by $\vec\phi_{00}^{\,\dagger}\vec\phi_{00}$.
5. **Limiting case A — sample in equilibrium:** $I=0$ requires $\mu_s=\mu_t$ regardless of tip position (equal tip and sample temperatures). Hence **no atomic corrugation appears in STP in equilibrium**, even though STM shows atomic resolution. With unequal temperatures the statement fails, as expected for thermoelectric effects.
6. **Limiting case B — homogeneous defect-free sample:** the local density matrix is diagonal and is described by a direction-dependent effective chemical potential, eq. (24), $\mu_{\hat\theta,\vec r}=e\vec E\cdot\vec r+\mu-el_{in}\vec E\cdot\hat\theta$; the spatial variation of STP data comes entirely from the $-\vec E\cdot\vec r$ (linear ramp) term. This distribution reproduces eq. (2).
7. **Limiting case C — Landauer resistive dipole:** far from an isolated defect, eq. (25), $\mu_{\hat\theta,\vec r}=-e\phi(\vec r)+\mu+el_{in}\nabla\phi\cdot\hat\theta$, where $\phi$ is the Landauer resistive dipole potential plus the homogeneous field. **STP measures the Landauer resistive dipole potential** — consistent with the experimental observation of resistive dipoles [2].
8. **Limiting case D — Chu and Sorbello [12]:** with the fully coherent density matrix (26) inserted into the Subcase-II formula (22), the theory reproduces **equation (14) of Chu & Sorbello**, namely eq. (27). This is the paper's explicit connection to the earlier literature and shows why the tunneling matrix element magnitude may not be taken as constant: its spatial variation *is* the interference term.
9. **Limiting case E — atomic resolution in STP:** in the 1D single-orbital tight-binding toy model with $\mathcal F=\mathcal F_0$ constant,
   - defect-free sample, tip over an atom: the matrix element factorizes out entirely (eq. 31) — **no spatial dependence of $\mu$**;
   - defect-free sample, tip midway between atoms: the interference term (33) vanishes in linear response because $\cos(k_Fa)=\cos(-k_Fa)$ — **still no spatial dependence**; a corrugation appears only when the current is large enough that $\Delta k$ is significant;
   - sample with one off-diagonal element $\delta$ between $k_0$ and $-k_0$, tip over an atom: again **no spatial dependence**;
   - sample with defects, tip midway between atoms: a term $\propto 2\mathrm{Re}(\delta)(\mathcal F_0\phi(x_0))^*\mathcal F_0\phi(x_0-a)\cos(k_0a)\,[f(k_0)-f_{FD}(k_0,\mu)]$ **does** produce spatial dependence proportional to $\delta$.
   **Conclusion:** atomic corrugation in STP is a **second-order** effect with defects, an even higher-order effect without them, versus a **first-order** effect in STM mode.
10. **Need for a local density matrix.** The global formulation is unphysical (it requires the contacts and distant sample regions), numerically intractable, and does not permit extracting transport physics without prior knowledge of $\hat\varrho$. The proposed remedy is a position-dependent wave-packet basis $\{|\xi_{\vec r+\Delta\vec r_i,\vec k}\rangle\}$, truncated by discarding packets with large $|\Delta\vec r_i|$, giving a **local density matrix** governed by a spatial differential equation with boundary conditions set by the mean local current — a new problem posed for mesoscopic transport theory. Wave-packet size must satisfy $\lambda_F\ll(\text{packet size})\ll(\text{macroscopic lengths})$.
11. **Analogy to scattering theory and the tip as a source.** The matrices $\sum_{\vec p}\vec\phi_0^{\,\dagger}\vec\phi_0$ and $\sum_{\vec p}f(E_{c,\vec p}-eV_t-\mu)\vec\phi_0^{\,\dagger}\vec\phi_0$ occupy the position of scattering matrices in Datta's equation (8.6.6) [15], and can be viewed as a special kind of scattering matrix. The tip therefore also acts as an electron source; in the **weak-coupling limit** this perturbation is negligible, which is STP's advantage over contact-based probes — at the cost of large tunneling resistance and Johnson-noise-limited resolution.

## Conclusions (as stated by the authors)

- A viewpoint of STP measurement was developed within the framework of quantum transport. **Equation (12) gives the total tunneling current in terms of the distribution function of the STM tip and the density matrix of the sample; setting this current to zero implicitly determines the STP measurement result.** The expression is in matrix-product form, so a basis-set-free definition can be made. With some approximations, explicit expressions for the measured STP potential were also obtained in the featureless-tip case.
- To get rid of the unphysical requirement of knowing material characteristics far away from the STP probing area when writing down the density matrix of the sample, the authors proposed to use **local density matrices** (Section IV) as a parameter varying over space, controlled by a certain differential equation and a set of boundary conditions. This allows relating STP to sample properties near the region where STP is performed.
- Section V provided limiting-case calculations demonstrating the use of the theoretical description, mostly with given or assumed density matrices of the sample. In particular, in the toy model of a one-dimensional tight-binding metal, **atomic resolution in STP measurement is a high-order effect**. The null results are partly due to assumed symmetry in the Fermi surface (e.g. equation (33) vanishing under the adopted assumptions) or in the operators $\mathcal F$ acting on the sample wave functions. The authors **speculate that asymmetry in the Fermi surface with respect to $\vec k$, or in the tip wave function (hence in operator $\mathcal F$) with respect to energy, could lead to lower-order effects in STP measurement.**
- Comparing equation (12) with equation (8.6.6) of reference [15], the analogy is immediate: the two matrices built from tip states and sample wave functions occupy the place of scattering matrices, and — keeping in mind the subtle difference between correlation function and density matrix — can be viewed as a special kind of scattering matrix.
- The STM tip, as a special contact providing scattering, also acts as an **electron source** whose strength depends on the scattering strength, changing the (local) density matrix as the tip moves. In the limit of weak probe–sample interaction the STP result is not expected to change much; **STP thus perturbs the sample minimally** compared with other contact-based probes such as conducting AFM cantilevers. A good criterion for minimal source effect is that the tip be in the far tail of the exponential decay of the sample wave functions — at the cost of large tunneling resistance and low resolution due to Johnson noise. When the sample is small compared with its characteristic transport lengths, the tip effect is generally large and is already explicitly included in the formalism of references [7,8].
