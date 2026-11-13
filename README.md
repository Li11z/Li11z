<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:58A6FF,100:BC8CFF&height=200&section=header&text=Ali%20Afoud&fontSize=56&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Scientific%20ML%20%C2%B7%20Mathematics%20%C2%B7%20Computer%20Science&descAlignY=58&descSize=18" alt="header" />

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=20&pause=1200&color=58A6FF&center=true&vCenter=true&width=620&lines=Hi%2C+I%27m+Ali;CS+%2B+Math+graduate%2C+UBC;Learning+scientific+machine+learning;PINNs+%7C+Neural+ODEs+%7C+SINDy;Turning+differential+equations+into+code" alt="typing intro" />

[![arXiv](https://img.shields.io/badge/arXiv-Afoud%2C%20A-B31B1B?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/search/?searchtype=author&query=Afoud%2C+A)
[![Email](https://img.shields.io/badge/Email-Afoudali%40hotmail.com-0078D4?style=flat-square&logo=microsoftoutlook&logoColor=white)](mailto:Afoudali@hotmail.com)
![Location](https://img.shields.io/badge/Based%20in-Montreal%2C%20QC-2EA44F?style=flat-square)
![Profile views](https://komarev.com/ghpvc/?username=Li11z&color=58a6ff&style=flat-square&label=Profile+views)

</div>

## About me

<img align="right" width="300" src="assets/lorenz.svg" alt="Animated Lorenz attractor" />

- Computer Science + Mathematics graduate, University of British Columbia (2026)
- Interested in where machine learning meets mathematical modelling: physics-informed learning, neural differential equations and data-driven discovery of governing equations
- Drawn to ML for medicine and biology, PDE models of epidemics, and quantum computing
- Building things from scratch in the open: an ML library (Python/C++) and a linear algebra library (C)
- Languages: English, French, Arabic
- Fun fact: 

<br clear="right"/>

## What I work on

```mermaid
flowchart LR
    A(("Ali")) --> C["Scientific ML"]
    A --> D["ML for Health and Biology"]
    A --> I["Interpretable ML"]
    A --> Q["Quantum (exploring)"]
    C --> C1["PINNs and neural operators"]
    C --> C2["Neural ODEs / UDEs"]
    C --> C3["Equation discovery (SINDy)"]
    D --> D1["Epidemic and PDE models"]
    D --> D2["Medical imaging and signals"]
    I --> I1["Symbolic regression"]
    classDef root fill:#58A6FF,stroke:#58A6FF,color:#ffffff
    classDef area fill:#BC8CFF,stroke:#BC8CFF,color:#ffffff
    class A root
    class C,D,I,Q area
```

<details>
<summary><b>The equations behind it</b></summary>
<br>

**Physics-informed loss**: fit the data while penalising violations of the governing PDE

$$\mathcal{L}(\theta) = \mathcal{L}_{\text{data}}(\theta) + \lambda \, \big\| \mathcal{N}[u_\theta] \big\|^2$$

**Neural ODE**: let a network define the dynamics

$$\frac{dh}{dt} = f_\theta(h, t)$$

**SINDy**: find the few library terms that explain the data

$$\dot{X} = \Theta(X)\, \Xi, \qquad \Xi \text{ sparse}$$

</details>

## Selected projects

![public](https://img.shields.io/badge/-public-2EA44F?style=flat-square) ![soon](https://img.shields.io/badge/-going%20public%20soon-D29922?style=flat-square) ![private](https://img.shields.io/badge/-private%20(course%20or%20research)-555?style=flat-square)

| Project | What it does | Stack | Status |
|---|---|---|:-:|
| **Epidemic waves PDE model** | Age-structured, opinion-driven prophylaxis model of COVID-19 waves using contact matrices and age-specific fatality rates | Python, NumPy | ![](https://img.shields.io/badge/-private-555?style=flat-square) |
| **Jersey number recognition** | Broadcast soccer pipeline: image restoration, pose-based torso crops, OCR/VLM ensemble with calibrated voting | PyTorch, YOLOv8 | ![](https://img.shields.io/badge/-private-555?style=flat-square) |
| **ML from scratch** | Classical ML algorithms behind a shared fit/predict API, validated against scikit-learn | Python, C++ | ![](https://img.shields.io/badge/-soon-D29922?style=flat-square) |
| **Linear algebra in C** | Matrix library with manual memory management; naive vs cache-blocked multiplication | C | ![](https://img.shields.io/badge/-soon-D29922?style=flat-square) |

<details>
<summary><b>More projects</b></summary>
<br>

| Project | What it does | Stack | Status |
|---|---|---|:-:|
| **Live lecture Q&A** | Real-time question answering over lecture speech and board content with tiered retrieval memory | Python, pgvector | ![](https://img.shields.io/badge/-private-555?style=flat-square) |
| **Password analysis** | Character trigram grader and inverse generator built on 174.8M leaked passwords, tested with Hashcat | Python | ![](https://img.shields.io/badge/-private-555?style=flat-square) |
| **Toronto safety analysis** | Neighbourhood safety scores and LightGBM crime/collision forecasts, served through a web app | PostgreSQL, LightGBM, FastAPI, Next.js | ![](https://img.shields.io/badge/-private-555?style=flat-square) |
| **Brownian motion notes** | Expository report on Lévy's construction and path properties | LaTeX | ![](https://img.shields.io/badge/-private-555?style=flat-square) |

</details>

## Roadmap

- [ ] `ml-from-scratch`: classical ML library with C++ kernels
- [ ] `linalg-c`: matrix library and benchmarks
- [ ] `sindy-lorenz`: recover the Lorenz system with SINDy and PySR, then try noisy real data
- [ ] `pinn-vs-fno`: physics-informed network vs Fourier Neural Operator on a PDEBench problem
- [ ] `ude-epidemics`: universal differential equation for epidemic data, building on my PDE work
- [ ] Kaggle: late submission to LEAP ClimSim (hybrid physics-ML)
- [ ] Biomedical: PhysioNet Challenge entry
- [ ] Quantum: Qiskit notebooks

<details>
<summary><b>Publications</b></summary>
<br>

- J. Wu, A. P. Herlihy, A. S. Mirza, **A. Afoud**, F. Fard. *GrowthHacker.* ACM TOSEM, 2026. [DOI](https://doi.org/10.1145/3815588)
- **A. Afoud**, J. Wu. *VReAct.* JAWs @ IEEE/ACM ASE 2026. [arXiv](https://arxiv.org/abs/2609.31937)

</details>

## Tech stack

<p align="center">
  <img src="https://skillicons.dev/icons?i=py,cpp,c,java,r,js,postgres,pytorch,sklearn,fastapi,nextjs,azure,git&perline=7" alt="Tech stack" />
</p>

<p align="center"><b>Currently learning</b></p>

<p align="center">
  <img src="https://img.shields.io/badge/Julia-SciML-9558B2?style=flat-square&logo=julia&logoColor=white" />
  <img src="https://img.shields.io/badge/JAX-Diffrax-4285F4?style=flat-square" />
  <img src="https://img.shields.io/badge/PySINDy-PySR-2EA44F?style=flat-square" />
  <img src="https://img.shields.io/badge/Qiskit-Quantum-6929C4?style=flat-square&logo=qiskit&logoColor=white" />
</p>

## Activity

<p align="center">
  <img src="https://streak-stats.demolab.com?user=Li11z&theme=transparent&hide_border=true&ring=58A6FF&fire=BC8CFF&currStreakLabel=58A6FF" alt="Contribution streak" />
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Li11z/Li11z/output/github-snake-dark.svg" />
    <img alt="Contribution snake" src="https://raw.githubusercontent.com/Li11z/Li11z/output/github-snake.svg" />
  </picture>
</p>

<div align="center">
  <img src="https://github.com/user-attachments/assets/9487e424-740d-46ed-9abb-21a7fd8813c6" width="280" alt="kazumaup" />
  <br>
  <sub>Hello World!</sub>
  <img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:58A6FF,100:BC8CFF&height=120&section=footer" alt="footer" />
</div>